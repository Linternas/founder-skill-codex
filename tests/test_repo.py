import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["founder-board", "founder-marketing", "founder-cfo", "founder-consumer", "founder-launch",
          "founder-pricing", "founder-offer", "founder-competitors", "founder-brand", "founder-ops", "founder-plan"]


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


EM = chr(0x2014)  # built in code so this file does not trip its own check


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_eleven_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            description = re.search(r"^description: (.+)$", fm, re.M)
            self.assertIsNotNone(description, s)
            self.assertTrue(json.loads(description.group(1)).strip(), s)
            self.assertEqual(set(re.findall(r"^(\w[\w-]*):", fm, re.M)), {"name", "description"})

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"\$\{SKILL_DIR\}/([\w.\-/]+\.(?:py|md))", text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS_DIR, s, tool))), "%s: %s" % (s, tool))

    def test_plugin_manifests(self):
        with open(os.path.join(ROOT, ".codex-plugin", "plugin.json")) as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "founder-skill-codex")
        self.assertTrue(plugin["description"].strip())
        self.assertEqual(plugin["license"], "MIT")
        self.assertEqual(os.path.realpath(os.path.join(ROOT, plugin["skills"])), os.path.realpath(SKILLS_DIR))
        with open(os.path.join(ROOT, ".agents", "plugins", "marketplace.json")) as fh:
            market = json.load(fh)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], plugin["name"])
        source = entry["source"]
        self.assertEqual(source["source"], "local")
        plugin_root = os.path.realpath(os.path.join(ROOT, source["path"]))
        self.assertTrue(os.path.isfile(os.path.join(plugin_root, ".codex-plugin", "plugin.json")))
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")

    def test_skill_references_resolve(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for reference in re.findall(r"\$founder-[a-z-]+", text):
                self.assertIn(reference[1:], SKILLS, s)

    def test_no_claude_runtime_dependencies(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for legacy in ("CLAUDE_SKILL_DIR", "$ARGUMENTS", "subagent_type", "Claude Code", "`/founder-"):
                self.assertNotIn(legacy, text, s)

    def test_ui_metadata(self):
        for s in SKILLS:
            with open(os.path.join(SKILLS_DIR, s, "agents", "openai.yaml"), encoding="utf-8") as fh:
                text = fh.read()
            for field in ("display_name", "short_description"):
                value = re.search(r"^  %s: (.+)$" % field, text, re.M)
                self.assertIsNotNone(value, s)
                self.assertTrue(json.loads(value.group(1)).strip(), s)

    def test_readme_lists_installable_skills(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)
            self.assertIn("`$%s`" % s, readme)

    def test_examples_parse(self):
        for rel in ("founder-cfo/example.json", "founder-consumer/customer.example.json"):
            with open(os.path.join(SKILLS_DIR, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_no_em_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                self.assertNotIn(EM, fh.read(), os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
