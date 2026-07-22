from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.history import HistoryManager


class HistoryManagerTests(unittest.TestCase):
    def test_record_and_reload_history(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "history.json"
            history = HistoryManager(path=history_path)
            history.record("open chrome", "open_app", "Launched chrome.", True, "text")

            reloaded = HistoryManager(path=history_path)
            entries = reloaded.latest(1)

            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].command, "open chrome")
            self.assertTrue(entries[0].success)


if __name__ == "__main__":
    unittest.main()
