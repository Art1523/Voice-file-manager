from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.conversation_memory import ConversationMemory


class ConversationMemoryTests(unittest.TestCase):
    def test_remember_persists_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_path = Path(temp_dir) / "conversation_memory.json"
            memory = ConversationMemory(path=memory_path)
            memory.remember("user", "open chrome", "text")
            memory.remember("assistant", "Launched chrome.", "text")

            reloaded = ConversationMemory(path=memory_path)
            recent = reloaded.recent(2)

            self.assertEqual(len(recent), 2)
            self.assertEqual(recent[0].role, "user")
            self.assertEqual(recent[1].role, "assistant")


if __name__ == "__main__":
    unittest.main()
