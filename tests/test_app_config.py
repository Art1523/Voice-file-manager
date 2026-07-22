from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.app_config import AppConfig


class AppConfigTests(unittest.TestCase):
    def test_reload_persists_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config = AppConfig(path=config_path)
            config.set("speech_speed", 210)
            config.set("microphone", 2)
            config.set("search_roots", ["C:/Temp"])

            reloaded = AppConfig(path=config_path)
            self.assertEqual(reloaded.get("speech_speed"), 210)
            self.assertEqual(reloaded.get("microphone"), 2)
            self.assertEqual(reloaded.get("search_roots"), ["C:/Temp"])


if __name__ == "__main__":
    unittest.main()
