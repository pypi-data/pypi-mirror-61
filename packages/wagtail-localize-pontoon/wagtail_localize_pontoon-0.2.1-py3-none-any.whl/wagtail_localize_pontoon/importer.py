import json

from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
import polib

from wagtail.core.models import Page
from wagtail_localize.models import (
    Locale,
    Region,
    ParentNotTranslatedError,
    TranslatablePageMixin,
)
from wagtail_localize.translation.segments import SegmentValue, TemplateValue
from wagtail_localize.translation.segments.ingest import ingest_segments
from wagtail_localize.translation.models import (
    Segment,
    SegmentLocation,
    TemplateLocation,
    SegmentTranslationContext,
)

from .models import (
    PontoonResource,
    PontoonSyncLog,
    PontoonSyncLogResource,
)


class Importer:
    def __init__(self, source_locale, logger):
        self.source_locale = source_locale
        self.logger = logger
        self.log = None

    def changed_entries(self, old_po, new_po):
        """
        Iterator of all entries that exists in new_po but not
        old_po.
        This retrieves any strings that have been added or changed.
        """
        old_entry_keys = set(str(entry) for entry in old_po)
        new_entry_keys = set(str(entry) for entry in new_po)
        new_entries = {str(entry): entry for entry in new_po}

        for changed_key in new_entry_keys - old_entry_keys:
            yield new_entries[changed_key]

    def import_resource(self, resource, locale, old_po, new_po):
        for changed_entry in self.changed_entries(old_po, new_po):
            # Don't import black strings
            if not changed_entry.msgstr:
                continue

            try:
                segment = Segment.objects.get(
                    language=self.source_locale.language, text=changed_entry.msgid
                )
                translation, created = segment.translations.get_or_create(
                    language=locale.language,
                    context=SegmentTranslationContext.objects.get(
                        object_id=resource.object_id, path=changed_entry.msgctxt,
                    )
                    if changed_entry.msgctxt
                    else None,
                    defaults={
                        "text": changed_entry.msgstr,
                        "updated_at": timezone.now(),
                    },
                )

                if not created:
                    # Update the translation only if the text has changed
                    if translation.text != changed_entry.msgstr:
                        translation.text = changed_entry.msgstr
                        translation.updated_at = timezone.now()
                        translation.save()

            except Segment.DoesNotExist:
                self.logger.warning(f"Unrecognised segment '{changed_entry.msgid}'")

    def try_update_resource_translation(self, resource, locale):
        # Check if there is a submission ready to be translated
        translatable_submission = resource.find_translatable_submission(locale)

        if translatable_submission:
            for dependency in translatable_submission.get_dependencies():
                if not dependency.object.has_translation(locale):
                    self.logger.info(
                        f"Can't translate '{resource.path}' into {locale.language.get_display_name()} because its dependency '{dependency.path}' hasn't been translated yet"
                    )
                    return

            self.logger.info(
                f"Saving translation for '{resource.path}' in {locale.language.get_display_name()}"
            )

            try:
                (
                    translation,
                    created,
                ) = translatable_submission.revision.create_or_update_translation(
                    locale
                )
            except ParentNotTranslatedError:
                # These pages will be handled when the parent is created in the code below
                self.logger.info(
                    f"Cannot save translation for '{resource.path}' in {locale.language.get_display_name()} yet as its parent must be translated first"
                )
                return

            if created:
                # The translation was created.

                # The logic in this part checks to find any other submissions that were waiting
                # for this object to be translated first and triggers them to be translated as
                # well.

                # Look for any submissions that were waiting for this object to be translated.
                # For example, any linked snippets, images, etc must be translated before
                # the page. So if a page (the dependee) is ready to be translated and its last
                # linked item has just been translated, we can translate that page now.
                for dependee in resource.get_dependees():
                    # Check that the next translatable submission of the dependee resource is
                    # the dependee submission that's linked to this resource.
                    # This prevents us from translating an old submission that's been replaced.
                    if (
                        dependee.resource.find_translatable_submission(locale)
                        != dependee
                    ):
                        continue

                    # FIXME: Could we pass in the translatable submission instead?
                    self.try_update_resource_translation(dependee.resource, locale)

                # If a page was created, check to see if it has any children that are
                # now ready to translate.
                if translatable_submission.revision.page_revision is not None:
                    source_page = translatable_submission.revision.page_revision.page

                    child_page_resources = PontoonResource.objects.filter(
                        object__translation_key__in=[
                            child.translation_key
                            for child in source_page.get_children().specific()
                            if isinstance(child, TranslatablePageMixin)
                        ]
                    )

                    for resource in child_page_resources:
                        self.try_update_resource_translation(resource, locale)

    def start_import(self, commit_id):
        self.log = PontoonSyncLog.objects.create(
            action=PontoonSyncLog.ACTION_PULL, commit_id=commit_id
        )

    def import_file(self, filename, old_content, new_content):
        self.logger.info(f"Pull: Importing changes in file '{filename}'")
        resource, locale = PontoonResource.get_by_po_filename(filename)

        # Log that this resource was updated
        PontoonSyncLogResource.objects.create(
            log=self.log, resource=resource, locale=locale
        )

        old_po = polib.pofile(old_content.decode("utf-8"))
        new_po = polib.pofile(new_content.decode("utf-8"))

        self.import_resource(resource, locale, old_po, new_po)

        # Check if the translated page is ready to be created/updated
        self.try_update_resource_translation(resource, locale)
