#!/usr/bin/env python3
"""Install the complete Founder skill pack for Codex. Python 3.8+, no dependencies."""

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent


def install(destination):
    """Copy all skills together, refusing collisions before changing anything."""
    source = (ROOT / "skills").resolve()
    skills = sorted(path for path in source.iterdir()
                    if path.is_dir() and (path / "SKILL.md").is_file())
    if not skills:
        raise ValueError("no skills found beside the installer")
    destination = Path(destination).expanduser().resolve()
    for skill in skills:
        target = destination / skill.name
        if target.exists() or target.is_symlink():
            raise ValueError("already exists: %s; move the existing folder before installing" % target)
    # Do not install inside a source skill and recursively copy its own output.
    if destination == source or source in destination.parents:
        raise ValueError("destination must be outside the source skills directory")
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    try:
        for skill in skills:
            target = destination / skill.name
            # Reserve the target so a competing install cannot be overwritten.
            target.mkdir()
            installed.append(target)
            shutil.copytree(skill, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    except OSError:
        for target in reversed(installed):
            shutil.rmtree(target)
        raise
    return installed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills",
                        help="skill directory (default: ~/.agents/skills); use <project>/.agents/skills for repo scope")
    args = parser.parse_args(argv)
    try:
        installed = install(args.dest)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("Installed %d skills into %s" % (len(installed), installed[0].parent))
    print("In Codex, try: $founder-board <your business idea>")
    print("If the skills do not appear, restart Codex.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
