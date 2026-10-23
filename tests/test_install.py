import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from _load import ROOT

spec = importlib.util.spec_from_file_location("founder_install", Path(ROOT) / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class Install(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.destination = self.base / "installed skills"
        self.project = self.base / "business project"
        self.project.mkdir()

    def run_tool(self, skill, script, *args):
        return subprocess.run([sys.executable, str(self.destination / skill / script)] + list(args),
                              cwd=str(self.project), capture_output=True, text=True)

    def test_complete_pack_runs_outside_checkout(self):
        installed = installer.install(self.destination)
        self.assertEqual(len(installed), 11)
        for folder in installed:
            self.assertTrue((folder / "SKILL.md").is_file())
            self.assertTrue((folder / "agents" / "openai.yaml").is_file())

        cfo = self.destination / "founder-cfo"
        result = self.run_tool("founder-cfo", "unit_economics.py", str(cfo / "example.json"),
                               "--out", "cfo.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / "cfo.md").is_file())

        consumer = self.destination / "founder-consumer"
        result = self.run_tool("founder-consumer", "panel.py", "init", "--customer",
                               str(consumer / "customer.example.json"), "--pitch",
                               str(consumer / "pitch.example.md"), "--n", "20", "--seed", "7")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_tool("founder-consumer", "panel.py", "prompts", "--wave", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        panel_dir = self.project / "founder" / "panel"
        self.assertEqual(len(list((panel_dir / "briefs").glob("*.md"))), 20)
        # Fixture answers test the tools; these are not simulated research results.
        for i in range(1, 21):
            pid = "P%03d" % i
            answer = {"id": pid, "buys": True, "reason_code": "quality", "reason": "test fixture",
                      "purchases_first_month": 2, "would_change_my_mind": "",
                      "price_too_cheap": 2.0, "price_cheap": 4.0,
                      "price_expensive": 7.0, "price_too_expensive": 9.0}
            (panel_dir / "answers" / (pid + ".json")).write_text(json.dumps(answer))
        for command in ("check", "tally"):
            result = self.run_tool("founder-consumer", "panel.py", command)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_tool("founder-pricing", "van_westendorp.py", "founder/panel/answers",
                               "--price", "6.50", "--out", "founder/pricing.md")
        self.assertEqual(result.returncode, 0, result.stderr)

        (self.project / "founder" / "numbers.json").write_bytes((cfo / "example.json").read_bytes())
        result = self.run_tool("founder-plan", "compile.py", "--dir", "founder")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = self.project / "founder" / "business-plan.md"
        self.assertIn("Verdict: Profitable", plan.read_text())
        self.assertIn("$founder-board", plan.read_text())

    def test_collision_does_not_partially_install_or_overwrite(self):
        existing = self.destination / "founder-pricing"
        existing.mkdir(parents=True)
        sentinel = existing / "SKILL.md"
        sentinel.write_text("user customization")
        with self.assertRaises(ValueError):
            installer.install(self.destination)
        self.assertEqual(sentinel.read_text(), "user customization")
        self.assertEqual(list(self.destination.iterdir()), [existing])

    def test_unrelated_skills_are_preserved(self):
        unrelated = self.destination / "other-skill"
        unrelated.mkdir(parents=True)
        installer.install(self.destination)
        self.assertTrue(unrelated.is_dir())
        self.assertEqual(len(list(self.destination.iterdir())), 12)

    def test_broken_symlink_collision_is_refused(self):
        self.destination.mkdir()
        target = self.destination / "founder-board"
        target.symlink_to(self.base / "missing")
        with self.assertRaises(ValueError):
            installer.install(self.destination)
        self.assertTrue(target.is_symlink())

    def test_copy_failure_rolls_back_new_skills(self):
        copytree = installer.shutil.copytree

        def fail_second(src, dst, *args, **kwargs):
            if Path(src).name == "founder-brand":
                raise OSError("simulated disk error")
            return copytree(src, dst, *args, **kwargs)

        with patch.object(installer.shutil, "copytree", side_effect=fail_second):
            with self.assertRaises(OSError):
                installer.install(self.destination)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_cli_custom_destination_and_collision_exit_code(self):
        command = [sys.executable, str(Path(ROOT) / "install.py"), "--dest", str(self.destination)]
        first = subprocess.run(command, cwd=str(self.project), capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        second = subprocess.run(command, cwd=str(self.project), capture_output=True, text=True)
        self.assertEqual(second.returncode, 1)
        self.assertIn("already exists", second.stderr)

    def test_destination_inside_source_is_refused(self):
        fake_root = self.base / "pack"
        skill = fake_root / "skills" / "founder-test"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("test skill")
        destination = skill / "nested-output"
        with patch.object(installer, "ROOT", fake_root):
            with self.assertRaises(ValueError):
                installer.install(destination)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
