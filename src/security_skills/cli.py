"""Read-only command-line interface. No project-supplied commands are executed."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .correlate import correlate
from .evaluate import score_document
from .inventory import inventory
from .models import ValidationError, validate_report
from .report import render_json, render_markdown
from .sarif import normalize_sarif
from .validate_skills import validate_library


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="security-skills")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("normalize", "correlate", "report", "validate", "inventory", "evaluate"):
        item = sub.add_parser(command)
        item.add_argument("source", type=Path)
        if command in {"normalize", "correlate", "report"}:
            item.add_argument("--output", type=Path, help="Output file (default stdout)")
        if command == "report":
            item.add_argument("--format", choices=("json", "markdown"), default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "inventory":
            output = json.dumps(inventory(args.source), indent=2) + "\n"
        elif args.command == "validate":
            problems = validate_library(args.source)
            for problem in problems:
                print(problem, file=sys.stderr)
            if problems:
                return 1
            print("All skills passed local structural checks")
            return 0
        else:
            content = json.loads(args.source.read_text(encoding="utf-8"))
            if args.command == "normalize":
                output = render_json(normalize_sarif(content))
            elif args.command == "correlate":
                validate_report(content)
                content["findings"] = correlate(content["findings"])
                output = render_json(content)
            elif args.command == "report":
                output = render_json(content) if args.format == "json" else render_markdown(content)
            else:
                output = json.dumps(score_document(content), indent=2) + "\n"
        if hasattr(args, "output") and args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0
    except (ValidationError, ValueError, OSError) as exc:
        print(f"security-skills: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
