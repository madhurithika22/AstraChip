#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from backend.agents.generation_agent import GenerationAgent
from backend.agents.refactor_agent import RefactorAgent
from backend.services.analysis_service import AnalysisService


def main() -> None:
    parser = argparse.ArgumentParser(prog="astra", description="AstraChip AI CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate design artifacts")
    gen.add_argument("prompt", nargs="*", default=["Design an 8-bit RISC-V ALU optimized for low power"])

    sub.add_parser("analyze", help="Run analysis pipeline")

    fix = sub.add_parser("fix", help="Fix design issues")
    fix.add_argument("issue", choices=["thermal", "congestion"])

    args = parser.parse_args()

    generator = GenerationAgent()
    analyzer = AnalysisService()
    refactor = RefactorAgent()

    if args.command == "generate":
        prompt = " ".join(args.prompt)
        print(json.dumps(generator.generate_project_artifacts(prompt), indent=2))
        return

    if args.command == "analyze":
        print(json.dumps(analyzer.run_analysis(), indent=2))
        return

    if args.command == "fix":
        result = analyzer.run_analysis()
        print(json.dumps(refactor.apply_fix(args.issue, result), indent=2))


if __name__ == "__main__":
    main()
