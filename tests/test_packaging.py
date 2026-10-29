import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://api.voygr.tech/places/mcp"


class TestPluginPackaging(unittest.TestCase):
    def test_claude_and_codex_connect_to_places_mcp(self):
        for manifest in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            with self.subTest(manifest=manifest):
                data = json.loads((ROOT / manifest).read_text())
                self.assertEqual(data["mcpServers"],
                                 {"places": {"type": "http", "url": MCP_URL}})

    def test_package_versions_match(self):
        manifests = (
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
        )
        versions = []
        for manifest in manifests:
            data = json.loads((ROOT / manifest).read_text())
            versions.append(data["plugins"][0]["version"] if "plugins" in data else data["version"])
        self.assertEqual(len(set(versions)), 1)

    def test_install_instructions_include_plugin_and_browser_login(self):
        readme = (ROOT / "README.md").read_text()
        for command in (
            "/plugin marketplace add voygr-tech/prospecting",
            "/plugin install prospecting@prospecting",
            "codex plugin marketplace add voygr-tech/prospecting",
            "codex plugin add prospecting@prospecting",
            "select `plugin:prospecting:places`",
            "codex mcp login places",
        ):
            with self.subTest(command=command):
                self.assertIn(command, readme)

    def test_skill_describes_mcp_path_and_confirmation(self):
        skill = (ROOT / "skills/prospecting/SKILL.md").read_text()
        for item in ("places_count", "places_find", "places_fill", "places_rows",
                     "places_export", "confirm_token", "needs_confirmation"):
            with self.subTest(item=item):
                self.assertIn(item, skill)
        self.assertIn(MCP_URL, skill)


if __name__ == "__main__":
    unittest.main()
