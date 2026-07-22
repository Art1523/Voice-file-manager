from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.search_index import FileSearchIndex


class SearchIndexTests(unittest.TestCase):
    def test_search_finds_partial_matches_in_configured_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "Downloads").mkdir()
            target_file = root / "Downloads" / "Invoice_August.pdf"
            target_file.write_text("sample", encoding="utf-8")

            cache_path = root / "search_index.json"
            index = FileSearchIndex(cache_path=cache_path)

            with patch.object(index, "_default_roots", return_value=[root / "Downloads"]):
                matches = index.search("invoice")

            self.assertTrue(matches)
            self.assertEqual(matches[0].name, "Invoice_August.pdf")
            self.assertEqual(matches[0].path, str(target_file))


if __name__ == "__main__":
    unittest.main()
