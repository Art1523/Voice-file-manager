from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.commands import detect_intent


class CommandDetectionTests(unittest.TestCase):
    def test_detects_application_launch(self) -> None:
        intent = detect_intent("open chrome")
        self.assertEqual(intent["intent"], "open_app")
        self.assertEqual(intent["target"], "chrome")

    def test_detects_search_command(self) -> None:
        intent = detect_intent("search downloads invoice")
        self.assertEqual(intent["intent"], "search")
        self.assertEqual(intent["target"], "downloads invoice")

    def test_detects_existing_file_command(self) -> None:
        intent = detect_intent("open report.pdf")
        self.assertEqual(intent["intent"], "open")
        self.assertEqual(intent["target"], "report.pdf")


if __name__ == "__main__":
    unittest.main()
