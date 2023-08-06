import logging

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.utils.module_loading import import_string
import polib

from wagtail_localize.models import Locale, ParentNotTranslatedError
from wagtail_localize.translation.models import Segment

from .git import Repository
from .models import (
    PontoonResourceSubmission,
    PontoonResource,
    PontoonSyncLog,
    PontoonSyncLogResource,
)
from .pofile import generate_source_pofile, generate_locale_pofile
from .importer import Importer


@transaction.atomic
def _pull(repo, logger):
    # Get the last commit ID that we either pulled or pushed
    last_log = PontoonSyncLog.objects.order_by("-time").exclude(commit_id="").first()
    last_commit_id = None
    if last_log is not None:
        last_commit_id = last_log.commit_id

    current_commit_id = repo.get_head_commit_id()

    if last_commit_id == current_commit_id:
        logger.info("Pull: No changes since last sync")
        return

    importer = Importer(Locale.objects.default(), logger)
    importer.start_import(current_commit_id)
    for filename, old_content, new_content in repo.get_changed_files(
        last_commit_id, repo.get_head_commit_id()
    ):
        importer.import_file(filename, old_content, new_content)


@transaction.atomic
def _push(repo, logger):
    reader = repo.reader()
    writer = repo.writer()
    writer.copy_unmanaged_files(reader)

    def update_po(filename, new_po_string):
        try:
            current_po_string = reader.read_file(filename).decode("utf-8")
            current_po = polib.pofile(current_po_string, wrapwidth=200)

            # Take metadata from existing PO file
            new_po = polib.pofile(new_po_string, wrapwidth=200)
            new_po.metadata = current_po.metadata
            new_po_string = str(new_po)

        except KeyError:
            pass

        writer.write_file(filename, new_po_string)

    locales = Locale.objects.filter(is_active=True).exclude(
        id=Locale.objects.default_id()
    )

    paths = []
    pushed_submission_ids = []
    for submission in (
        PontoonResourceSubmission.objects.filter(
            revision_id=F("resource__current_revision_id")
        )
        .select_related("resource")
        .order_by("resource__path")
    ):
        source_po = generate_source_pofile(submission.resource)
        update_po(str(submission.resource.get_po_filename()), source_po)

        for locale in locales:
            locale_po = generate_locale_pofile(submission.resource, locale)
            update_po(
                str(submission.resource.get_po_filename(locale=locale)), locale_po
            )

        paths.append(
            (
                submission.resource.get_po_filename(),
                submission.resource.get_locale_po_filename_template(),
            )
        )

        pushed_submission_ids.append(submission.id)

    writer.write_config(
        [locale.language.as_rfc5646_language_tag() for locale in locales], paths
    )

    # A queryset of submissions we've just written that haven't been pushed before
    pushed_submissions = PontoonResourceSubmission.objects.filter(
        id__in=pushed_submission_ids, push_log__isnull=True
    )

    if writer.has_changes() or pushed_submissions.exists():
        # Create a new log for this push
        log = PontoonSyncLog.objects.create(
            action=PontoonSyncLog.ACTION_PUSH, commit_id=""
        )

        # Add an entry for each resource we just pushed
        for resource_id in pushed_submissions.values_list("resource_id", flat=True):
            PontoonSyncLogResource.objects.create(log=log, resource_id=resource_id)

        pushed_submissions.update(pushed_at=timezone.now(), push_log=log)

        if writer.has_changes():
            logger.info("Push: Committing changes")
            writer.commit("Updates to source content")

            log.commit_id = repo.get_head_commit_id()
            log.save(update_fields=["commit_id"])

            repo.push()
        else:
            logger.info(
                "Push: Not committing anything as recent changes haven't affected any translatable content"
            )

    else:
        logger.info("Push: No changes since last sync")


class SyncManager:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def sync(self):
        self.logger.info("Pulling repository")
        repo = Repository.open()
        repo.pull()

        _pull(repo, self.logger)
        _push(repo, self.logger)

        self.logger.info("Finished")

    def trigger(self):
        """
        Called when user presses the "Sync" button in the admin

        This should enqueue a background task to run the sync() function
        """
        self.sync()

    def is_queued(self):
        """
        Returns True if the background task is queued
        """
        return False

    def is_running(self):
        """
        Returns True if the background task is currently running
        """
        return False


def get_sync_manager():
    sync_manager_class_path = getattr(
        settings,
        "WAGTAILLOCALIZE_PONTOON_SYNC_MANAGER_CLASS",
        "wagtail_localize_pontoon.sync.SyncManager",
    )
    sync_manager = import_string(sync_manager_class_path)
    return sync_manager()
