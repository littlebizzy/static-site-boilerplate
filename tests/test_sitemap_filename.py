"""Tests for the optional XML sitemap output filename."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build


class SitemapFilenameTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

        root_patch = patch.object(build, "ROOT", self.root)
        output_patch = patch.object(build, "OUTPUT", self.root / "public")
        root_patch.start()
        output_patch.start()
        self.addCleanup(output_patch.stop)
        self.addCleanup(root_patch.stop)

    def write_site(self, **overrides):
        site = {
            "name": "Example",
            "url": "https://example.com/",
            "description": "Example site",
        }
        site.update(overrides)
        (self.root / "site.json").write_text(json.dumps(site), encoding="utf-8")
        return build.load_site()

    def test_default_filename_when_omitted(self):
        site = self.write_site()
        self.assertEqual(site["sitemap_filename"], "sitemap.xml")

    def test_explicit_default_filename(self):
        site = self.write_site(sitemap_filename="sitemap.xml")
        self.assertEqual(site["sitemap_filename"], "sitemap.xml")

    def test_custom_filename_is_used_for_output(self):
        filename = "a7k2m9q4v6r8.xml"
        site = self.write_site(sitemap_filename=filename)
        build.OUTPUT.mkdir()
        build.write_sitemap(site, [], {}, {})
        self.assertTrue((build.OUTPUT / filename).is_file())
        self.assertFalse((build.OUTPUT / "sitemap.xml").exists())

    def test_invalid_filenames_are_rejected(self):
        invalid = (
            "", "abc.xml", "abcdefghijklmnop.xml", "A7k2m9q4v6r8.xml",
            "a7k2m9q4v6r8.XML", "../a7k2m9q4v6r8.xml",
            "nested/a7k2m9q4v6r8.xml", "a7k2m9q4v6r8-x.xml",
            None, 12,
        )
        for filename in invalid:
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError):
                    self.write_site(sitemap_filename=filename)

    def test_root_static_file_collision_is_rejected(self):
        filename = "a7k2m9q4v6r8.xml"
        (self.root / filename).write_text("<existing/>", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "conflicts with root file"):
            self.write_site(sitemap_filename=filename)

    def test_filename_is_validated_without_production_url(self):
        with self.assertRaises(ValueError):
            self.write_site(url="", sitemap_filename="../a7k2m9q4v6r8.xml")


if __name__ == "__main__":
    unittest.main()
