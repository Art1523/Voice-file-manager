from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.tool_registry import ToolRegistry


class ToolRegistryTests(unittest.TestCase):
    def test_execute_registered_tool(self) -> None:
        registry = ToolRegistry()
        registry.register("echo", lambda payload: payload["message"])

        result = registry.execute("echo", {"message": "hello"})

        self.assertTrue(result.success)
        self.assertEqual(result.output, "hello")

    def test_execute_unknown_tool(self) -> None:
        registry = ToolRegistry()

        result = registry.execute("missing", {})

        self.assertFalse(result.success)
        self.assertEqual(result.output, "Unknown command.")


if __name__ == "__main__":
    unittest.main()
