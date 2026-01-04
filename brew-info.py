#!/usr/bin/env python3
"""
brew-info.py
Fast Homebrew package information generator with JSON export
Usage: ./brew-info.py [--json] [--output FILE]
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ANSI color codes
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


def run_command(cmd: List[str], capture_output=True) -> Tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, timeout=10
        )
        return result.returncode == 0, result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False, ""


def get_installed_packages() -> Tuple[List[str], List[str]]:
    """Get lists of installed formulas and casks."""
    success, formulas_output = run_command(["brew", "list", "--formula"])
    formulas = formulas_output.split("\n") if success and formulas_output else []

    success, casks_output = run_command(["brew", "list", "--cask"])
    casks = casks_output.split("\n") if success and casks_output else []

    return formulas, casks


def get_formula_info(package: str) -> Dict:
    """Get information for a formula package."""
    info = {
        "name": package,
        "type": "formula",
        "description": "",
        "dependencies": [],
        "required_by": [],
        "homepage": "",
        "version": "",
        "status": "success",
    }

    # Get basic info using brew info --json
    success, json_output = run_command(["brew", "info", "--json=v2", package])
    if success and json_output:
        try:
            data = json.loads(json_output)
            if data.get("formulae") and len(data["formulae"]) > 0:
                formula = data["formulae"][0]
                info["description"] = formula.get("desc", "")
                info["homepage"] = formula.get("homepage", "")
                info["version"] = formula.get("versions", {}).get("stable", "")
                info["dependencies"] = formula.get("dependencies", [])
        except json.JSONDecodeError:
            pass

    # Get reverse dependencies (what requires this package)
    success, rdeps = run_command(["brew", "uses", "--installed", package])
    if success and rdeps:
        info["required_by"] = [dep.strip() for dep in rdeps.split("\n") if dep.strip()]

    return info


def get_cask_info(package: str) -> Dict:
    """Get information for a cask package."""
    info = {
        "name": package,
        "type": "cask",
        "description": "",
        "homepage": "",
        "version": "",
        "status": "success",
    }

    # Get cask info using brew info --json
    success, json_output = run_command(["brew", "info", "--cask", "--json=v2", package])
    if success and json_output:
        try:
            data = json.loads(json_output)
            if data.get("casks") and len(data["casks"]) > 0:
                cask = data["casks"][0]
                info["description"] = cask.get("desc", "")
                info["homepage"] = cask.get("homepage", "")
                info["version"] = cask.get("version", "")
        except json.JSONDecodeError:
            pass

    return info


def process_package(package: str, is_cask: bool) -> Dict:
    """Process a single package and return its info."""
    try:
        if is_cask:
            return get_cask_info(package)
        else:
            return get_formula_info(package)
    except Exception as e:
        return {
            "name": package,
            "type": "cask" if is_cask else "formula",
            "status": "error",
            "error": str(e),
        }


def print_package_info(info: Dict, use_colors: bool = True):
    """Print package information in a formatted way."""
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    print(f"\n{c.BOLD}{c.BLUE}{'=' * 64}{c.NC}")
    print(f"{c.BOLD}{c.GREEN}📦 {info['name']}{c.NC}")
    print(f"{c.BLUE}{'=' * 64}{c.NC}")

    type_label = (
        "Cask (GUI Application)" if info["type"] == "cask" else "Formula (CLI/Library)"
    )
    print(f"{c.YELLOW}Type:{c.NC} {type_label}")

    if info.get("description"):
        print(f"{c.YELLOW}Description:{c.NC} {info['description']}")

    if info.get("version"):
        print(f"{c.YELLOW}Version:{c.NC} {info['version']}")

    if info.get("homepage"):
        print(f"{c.YELLOW}Homepage:{c.NC} {info['homepage']}")

    if info["type"] == "formula":
        deps = info.get("dependencies", [])
        if deps:
            print(f"{c.YELLOW}Dependencies:{c.NC} {', '.join(deps)}")
        else:
            print(f"{c.YELLOW}Dependencies:{c.NC} None")

        rdeps = info.get("required_by", [])
        if rdeps:
            print(f"{c.YELLOW}Required by:{c.NC} {', '.join(rdeps)}")

    if info.get("status") == "error":
        print(f"{c.RED}⚠ Error: {info.get('error', 'Unknown error')}{c.NC}")


def print_header(use_colors: bool = True):
    """Print the report header."""
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    print(f"{c.BOLD}{c.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║           HOMEBREW PACKAGE INFORMATION REPORT                    ║")
    print(
        f"║                   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                           ║"
    )
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{c.NC}")


def print_summary(formulas_count: int, casks_count: int, use_colors: bool = True):
    """Print the summary section."""
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    total = formulas_count + casks_count
    print(f"\n{c.BOLD}{c.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                         SUMMARY                                  ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print(f"║  Total Formulas: {formulas_count:<48}║")
    print(f"║  Total Casks:    {casks_count:<48}║")
    print(f"║  Total Packages: {total:<48}║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{c.NC}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Homebrew package information report"
    )
    parser.add_argument("--json", action="store_true", help="Generate JSON output")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
        help="Maximum parallel workers (default: 10)",
    )

    args = parser.parse_args()

    # Get installed packages
    print("Fetching installed packages...", file=sys.stderr)
    formulas, casks = get_installed_packages()

    if not formulas and not casks:
        print("No Homebrew packages found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(formulas)} formulas and {len(casks)} casks", file=sys.stderr)

    # Collect package information in parallel
    print("Gathering package information (this may take a moment)...", file=sys.stderr)

    formula_infos = []
    cask_infos = []

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # Submit all tasks
        future_to_package = {}

        for formula in formulas:
            future = executor.submit(process_package, formula, False)
            future_to_package[future] = ("formula", formula)

        for cask in casks:
            future = executor.submit(process_package, cask, True)
            future_to_package[future] = ("cask", cask)

        # Collect results as they complete
        total_tasks = len(formulas) + len(casks)
        completed = 0

        for future in as_completed(future_to_package):
            pkg_type, pkg_name = future_to_package[future]
            completed += 1
            print(f"\rProcessing: {completed}/{total_tasks}", end="", file=sys.stderr)

            try:
                info = future.result()
                if pkg_type == "formula":
                    formula_infos.append(info)
                else:
                    cask_infos.append(info)
            except Exception as e:
                print(f"\nError processing {pkg_name}: {e}", file=sys.stderr)

        print("\n", file=sys.stderr)

    # Sort results by name
    formula_infos.sort(key=lambda x: x["name"])
    cask_infos.sort(key=lambda x: x["name"])

    # Generate output
    if args.json:
        # JSON output
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_formulas": len(formula_infos),
                "total_casks": len(cask_infos),
                "total_packages": len(formula_infos) + len(cask_infos),
            },
            "formulas": formula_infos,
            "casks": cask_infos,
        }

        json_output = json.dumps(output_data, indent=2)

        if args.output:
            with open(args.output, "w") as f:
                f.write(json_output)
            print(f"JSON report saved to: {args.output}", file=sys.stderr)
        else:
            print(json_output)
    else:
        # Text output
        use_colors = not args.no_color and (not args.output or sys.stdout.isatty())

        if args.output:
            sys.stdout = open(args.output, "w")

        print_header(use_colors)

        # Print formulas
        c = (
            Colors
            if use_colors
            else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
        )
        print(f"\n{c.BOLD}{c.CYAN}{'━' * 64}{c.NC}")
        print(
            f"{c.BOLD}{c.CYAN}                    FORMULAS ({len(formula_infos)} packages){c.NC}"
        )
        print(f"{c.CYAN}{'━' * 64}{c.NC}")

        for info in formula_infos:
            print_package_info(info, use_colors)

        # Print casks
        print(f"\n{c.BOLD}{c.CYAN}{'━' * 64}{c.NC}")
        print(
            f"{c.BOLD}{c.CYAN}                    CASKS ({len(cask_infos)} packages){c.NC}"
        )
        print(f"{c.CYAN}{'━' * 64}{c.NC}")

        for info in cask_infos:
            print_package_info(info, use_colors)

        # Print summary
        print_summary(len(formula_infos), len(cask_infos), use_colors)

        if args.output:
            sys.stdout.close()
            print(f"Report saved to: {args.output}", file=sys.__stdout__)


if __name__ == "__main__":
    main()
