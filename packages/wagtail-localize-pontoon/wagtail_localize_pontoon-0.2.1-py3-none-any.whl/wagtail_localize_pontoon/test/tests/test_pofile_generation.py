import logging

import polib
from django.db.models import F
from django.test import TestCase

from wagtail.core.models import Page
from wagtail_localize.models import Language, Locale
from wagtail_localize.test.models import TestPage
from wagtail_localize.translation.models import (
    Segment,
    SegmentTranslationContext,
    SegmentTranslation,
    SegmentLocation,
)

from wagtail_localize_pontoon.models import PontoonResource
from wagtail_localize_pontoon.pofile import (
    generate_source_pofile,
    generate_locale_pofile,
)


def create_test_page(**kwargs):
    root_page = Page.objects.get(id=1)
    page = root_page.add_child(instance=TestPage(**kwargs))
    revision = page.save_revision()
    revision.publish()
    return page


class TestGenerateSourcePOFile(TestCase):
    def setUp(self):
        self.page = create_test_page(
            title="Test page",
            slug="test-page",
            test_charfield="The test translatable field",
            test_synchronized_charfield="The test synchronized field",
        )
        self.resource = PontoonResource.objects.get(
            object__translation_key=self.page.translation_key
        )

    def test_generate_source_pofile(self):
        pofile = generate_source_pofile(self.resource)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr) for m in parsed_po],
            [("The test translatable field", "")],
        )

    def test_generate_source_pofile_with_multiple_revisions(self):
        # Create another revision with the same segment text, but in a different otder
        # We check this to make sure that the segment is not duplicated in the PO file
        # See issue: https://github.com/mozilla/donate-wagtail/issues/559

        new_revision = self.page.save_revision()
        new_revision.publish()
        SegmentLocation.objects.filter(revision__page_revision=new_revision).update(
            order=F("order") + 1
        )

        pofile = generate_source_pofile(self.resource)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr) for m in parsed_po],
            [("The test translatable field", "")],
        )


class TestGenerateLanguagePOFile(TestCase):
    def setUp(self):
        self.page = create_test_page(
            title="Test page",
            slug="test-page",
            test_charfield="The test translatable field",
            test_synchronized_charfield="The test synchronized field",
        )
        self.resource = PontoonResource.objects.get(
            object__translation_key=self.page.translation_key
        )
        Language.objects.create(code="fr")
        self.locale = Locale.objects.get(language__code="fr")

    def test_generate_locale_pofile(self):
        pofile = generate_locale_pofile(self.resource, self.locale)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr) for m in parsed_po],
            [("The test translatable field", "")],
        )

    def test_generate_locale_pofile_with_existing_translation(self):
        segment = Segment.objects.get(text="The test translatable field")
        context = SegmentTranslationContext.objects.get(
            object_id=self.page.translation_key, path="test_charfield"
        )
        SegmentTranslation.objects.create(
            translation_of=segment,
            language_id=self.locale.language_id,
            context=context,
            text="Le champ traduisible de test",
        )

        pofile = generate_locale_pofile(self.resource, self.locale)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr) for m in parsed_po],
            [("The test translatable field", "Le champ traduisible de test")],
        )

    def test_generate_locale_pofile_with_existing_obsolete_translation(self):
        # Update the existing segment. The save_revision bit below will generate a new segment with the current text
        segment = Segment.objects.get()
        segment.text = "Some obsolete text"
        segment.text_id = Segment.get_text_id(segment.text)
        segment.save()

        context = SegmentTranslationContext.objects.get(
            object_id=self.page.translation_key, path="test_charfield"
        )
        SegmentTranslation.objects.create(
            translation_of=segment,
            context=context,
            language_id=self.locale.language_id,
            text="Du texte obsolète",
        )

        # Create a new revision. This will create a new segment like how the current segment was before I changed it
        # It will also update the revision field on the resource so we need to refresh that
        self.page.save_revision().publish()
        self.resource.refresh_from_db()

        pofile = generate_locale_pofile(self.resource, self.locale)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr, m.obsolete) for m in parsed_po],
            [
                ("The test translatable field", "", 0),
                ("Some obsolete text", "Du texte obsolète", 1),
            ],
        )

    def test_generate_locale_pofile_with_multiple_revisions(self):
        # Create another revision with the same segment text, but in a different otder
        # We check this to make sure that the segment is not duplicated in the PO file
        # See issue: https://github.com/mozilla/donate-wagtail/issues/559

        new_revision = self.page.save_revision()
        new_revision.publish()
        SegmentLocation.objects.filter(revision__page_revision=new_revision).update(
            order=F("order") + 1
        )

        pofile = generate_locale_pofile(self.resource, self.locale)
        parsed_po = polib.pofile(pofile)
        self.assertEqual(
            [(m.msgid, m.msgstr) for m in parsed_po],
            [("The test translatable field", "")],
        )
