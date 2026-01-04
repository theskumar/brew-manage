#!/usr/bin/env python3
"""
brew-deps-graph.py
Visualize Homebrew package dependency graph from JSON file
Usage: ./brew-deps-graph.py [brew-packages.json] [OPTIONS]
"""

import argparse
import json
import sys
from collections import defaultdict
from typing import Dict, List, Set


class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[0;36m"
    MAGENTA = "\033[0;35m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    NC = "\033[0m"


def load_packages(json_file: str) -> Dict:
    """Load package data from JSON file."""
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}", file=sys.stderr)
        sys.exit(1)


def build_dependency_graph(formulas: List[Dict]) -> Dict[str, Dict]:
    """Build a dependency graph from formula list."""
    graph = {}

    for formula in formulas:
        name = formula.get("name")
        if not name:
            continue

        graph[name] = {
            "dependencies": formula.get("dependencies", []),
            "required_by": formula.get("required_by", []),
            "description": formula.get("description", ""),
            "version": formula.get("version", ""),
        }

    return graph


def print_tree(
    package: str,
    graph: Dict[str, Dict],
    prefix: str = "",
    is_last: bool = True,
    visited: Set[str] = None,
    max_depth: int = -1,
    current_depth: int = 0,
    show_versions: bool = False,
    use_colors: bool = True,
):
    """Print dependency tree recursively."""
    if visited is None:
        visited = set()

    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    # Check if we've reached max depth
    if max_depth >= 0 and current_depth >= max_depth:
        return

    # Check if package exists in graph
    if package not in graph:
        connector = "└── " if is_last else "├── "
        version_str = ""
        print(
            f"{prefix}{c.DIM}{connector}{c.RED}{package}{version_str} {c.DIM}(not found){c.NC}"
        )
        return

    # Prepare display strings
    connector = "└── " if is_last else "├── "
    pkg_data = graph[package]
    version_str = (
        f" {c.DIM}({pkg_data['version']}){c.NC}"
        if show_versions and pkg_data["version"]
        else ""
    )

    # Check for circular dependencies
    if package in visited:
        print(
            f"{prefix}{connector}{c.YELLOW}{package}{version_str} {c.DIM}(circular){c.NC}"
        )
        return

    # Print current package
    dep_count = len(pkg_data["dependencies"])
    dep_info = f" {c.DIM}[{dep_count} deps]{c.NC}" if dep_count > 0 else ""
    print(f"{prefix}{connector}{c.GREEN}{package}{c.NC}{version_str}{dep_info}")

    # Mark as visited
    visited.add(package)

    # Print dependencies
    dependencies = pkg_data["dependencies"]
    if dependencies and (max_depth < 0 or current_depth < max_depth - 1):
        extension = "    " if is_last else "│   "
        for i, dep in enumerate(dependencies):
            is_last_dep = i == len(dependencies) - 1
            print_tree(
                dep,
                graph,
                prefix + extension,
                is_last_dep,
                visited.copy(),
                max_depth,
                current_depth + 1,
                show_versions,
                use_colors,
            )


def print_reverse_tree(
    package: str,
    graph: Dict[str, Dict],
    prefix: str = "",
    is_last: bool = True,
    visited: Set[str] = None,
    max_depth: int = -1,
    current_depth: int = 0,
    show_versions: bool = False,
    use_colors: bool = True,
):
    """Print reverse dependency tree (what depends on this package)."""
    if visited is None:
        visited = set()

    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    if max_depth >= 0 and current_depth >= max_depth:
        return

    if package not in graph:
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{c.DIM}{connector}{c.RED}{package} {c.DIM}(not found){c.NC}")
        return

    connector = "└── " if is_last else "├── "
    pkg_data = graph[package]
    version_str = (
        f" {c.DIM}({pkg_data['version']}){c.NC}"
        if show_versions and pkg_data["version"]
        else ""
    )

    if package in visited:
        print(
            f"{prefix}{connector}{c.YELLOW}{package}{version_str} {c.DIM}(circular){c.NC}"
        )
        return

    required_by_count = len(pkg_data["required_by"])
    req_info = (
        f" {c.DIM}[required by {required_by_count}]{c.NC}"
        if required_by_count > 0
        else ""
    )
    print(f"{prefix}{connector}{c.CYAN}{package}{c.NC}{version_str}{req_info}")

    visited.add(package)

    required_by = pkg_data["required_by"]
    if required_by and (max_depth < 0 or current_depth < max_depth - 1):
        extension = "    " if is_last else "│   "
        for i, dep in enumerate(required_by):
            is_last_dep = i == len(required_by) - 1
            print_reverse_tree(
                dep,
                graph,
                prefix + extension,
                is_last_dep,
                visited.copy(),
                max_depth,
                current_depth + 1,
                show_versions,
                use_colors,
            )


def find_root_packages(graph: Dict[str, Dict]) -> List[str]:
    """Find packages that are not dependencies of any other package."""
    all_deps = set()
    for pkg_data in graph.values():
        all_deps.update(pkg_data["dependencies"])

    roots = [pkg for pkg in graph.keys() if pkg not in all_deps]
    return sorted(roots)


def find_leaf_packages(graph: Dict[str, Dict]) -> List[str]:
    """Find packages that have no dependencies."""
    leaves = [pkg for pkg, data in graph.items() if not data["dependencies"]]
    return sorted(leaves)


def find_most_depended_on(graph: Dict[str, Dict], top_n: int = 10) -> List[tuple]:
    """Find packages that are depended on by the most other packages."""
    dep_count = defaultdict(int)

    for pkg_data in graph.values():
        for dep in pkg_data["dependencies"]:
            dep_count[dep] += 1

    sorted_deps = sorted(dep_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_deps[:top_n]


def find_most_dependencies(graph: Dict[str, Dict], top_n: int = 10) -> List[tuple]:
    """Find packages that depend on the most other packages."""
    pkg_deps = [(pkg, len(data["dependencies"])) for pkg, data in graph.items()]
    sorted_pkgs = sorted(pkg_deps, key=lambda x: x[1], reverse=True)
    return sorted_pkgs[:top_n]


def print_statistics(graph: Dict[str, Dict], use_colors: bool = True):
    """Print statistics about the dependency graph."""
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    total_packages = len(graph)
    total_dependencies = sum(len(data["dependencies"]) for data in graph.values())
    avg_deps = total_dependencies / total_packages if total_packages > 0 else 0

    roots = find_root_packages(graph)
    leaves = find_leaf_packages(graph)

    print(f"\n{c.BOLD}{c.CYAN}{'=' * 70}{c.NC}")
    print(f"{c.BOLD}{c.CYAN}DEPENDENCY STATISTICS{c.NC}")
    print(f"{c.CYAN}{'=' * 70}{c.NC}\n")

    print(f"{c.YELLOW}Total Packages:{c.NC} {total_packages}")
    print(f"{c.YELLOW}Total Dependencies:{c.NC} {total_dependencies}")
    print(f"{c.YELLOW}Average Dependencies per Package:{c.NC} {avg_deps:.2f}")
    print(f"{c.YELLOW}Root Packages (not depended on):{c.NC} {len(roots)}")
    print(f"{c.YELLOW}Leaf Packages (no dependencies):{c.NC} {len(leaves)}")

    # Most depended on packages
    print(f"\n{c.BOLD}{c.GREEN}Top 10 Most Depended On Packages:{c.NC}")
    most_depended = find_most_depended_on(graph, 10)
    for i, (pkg, count) in enumerate(most_depended, 1):
        print(
            f"  {c.DIM}{i:2d}.{c.NC} {c.GREEN}{pkg:<30}{c.NC} {c.DIM}({count} packages){c.NC}"
        )

    # Packages with most dependencies
    print(f"\n{c.BOLD}{c.MAGENTA}Top 10 Packages with Most Dependencies:{c.NC}")
    most_deps = find_most_dependencies(graph, 10)
    for i, (pkg, count) in enumerate(most_deps, 1):
        print(
            f"  {c.DIM}{i:2d}.{c.NC} {c.MAGENTA}{pkg:<30}{c.NC} {c.DIM}({count} dependencies){c.NC}"
        )

    print(f"\n{c.CYAN}{'=' * 70}{c.NC}\n")


def list_packages(graph: Dict[str, Dict], use_colors: bool = True):
    """List all packages with basic info."""
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    packages = sorted(graph.keys())

    print(f"\n{c.BOLD}{c.CYAN}ALL PACKAGES ({len(packages)} total){c.NC}\n")

    for pkg in packages:
        data = graph[pkg]
        dep_count = len(data["dependencies"])
        req_count = len(data["required_by"])
        version = data["version"]

        print(
            f"{c.GREEN}{pkg:<30}{c.NC} {c.DIM}v{version:<15}{c.NC} "
            f"{c.YELLOW}deps:{dep_count:<3}{c.NC} {c.CYAN}required_by:{req_count:<3}{c.NC}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Visualize Homebrew package dependency graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show dependency tree for a specific package
  ./brew-deps-graph.py brew-packages.json -p python@3.12

  # Show reverse dependencies (what depends on this)
  ./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse

  # Show statistics
  ./brew-deps-graph.py brew-packages.json --stats

  # Show all root packages (not depended on by others)
  ./brew-deps-graph.py brew-packages.json --roots

  # Limit tree depth
  ./brew-deps-graph.py brew-packages.json -p node --depth 2
        """,
    )

    parser.add_argument(
        "json_file",
        nargs="?",
        default="brew-packages.json",
        help="Path to brew-packages.json file (default: brew-packages.json)",
    )
    parser.add_argument(
        "-p",
        "--package",
        help="Show dependency tree for specific package",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Show reverse dependencies (what depends on this package)",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=-1,
        help="Maximum depth to display (default: unlimited)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show dependency statistics",
    )
    parser.add_argument(
        "--roots",
        action="store_true",
        help="Show root packages (not depended on by others)",
    )
    parser.add_argument(
        "--leaves",
        action="store_true",
        help="Show leaf packages (no dependencies)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all packages with basic info",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show package versions in tree",
    )

    args = parser.parse_args()
    use_colors = not args.no_color and sys.stdout.isatty()
    c = (
        Colors
        if use_colors
        else type("C", (), {k: "" for k in dir(Colors) if not k.startswith("_")})()
    )

    # Load package data
    data = load_packages(args.json_file)
    formulas = data.get("formulas", [])

    if not formulas:
        print("No formulas found in JSON file.", file=sys.stderr)
        sys.exit(1)

    # Build dependency graph
    graph = build_dependency_graph(formulas)

    # Handle different modes
    if args.stats:
        print_statistics(graph, use_colors)
    elif args.list:
        list_packages(graph, use_colors)
    elif args.roots:
        roots = find_root_packages(graph)
        print(f"\n{c.BOLD}{c.GREEN}Root Packages ({len(roots)}):{c.NC}")
        print(f"{c.DIM}(Packages not depended on by any other package){c.NC}\n")
        for pkg in roots:
            dep_count = len(graph[pkg]["dependencies"])
            print(f"  {c.GREEN}{pkg:<30}{c.NC} {c.DIM}({dep_count} dependencies){c.NC}")
    elif args.leaves:
        leaves = find_leaf_packages(graph)
        print(f"\n{c.BOLD}{c.CYAN}Leaf Packages ({len(leaves)}):{c.NC}")
        print(f"{c.DIM}(Packages with no dependencies){c.NC}\n")
        for pkg in leaves:
            req_count = len(graph[pkg]["required_by"])
            print(f"  {c.CYAN}{pkg:<30}{c.NC} {c.DIM}(required by {req_count}){c.NC}")
    elif args.package:
        if args.package not in graph:
            print(
                f"Error: Package '{args.package}' not found in graph.", file=sys.stderr
            )
            sys.exit(1)

        pkg_data = graph[args.package]

        # Print package header
        print(f"\n{c.BOLD}{c.BLUE}{'=' * 70}{c.NC}")
        print(f"{c.BOLD}Package: {c.GREEN}{args.package}{c.NC}")
        if pkg_data["version"]:
            print(f"{c.YELLOW}Version:{c.NC} {pkg_data['version']}")
        if pkg_data["description"]:
            print(f"{c.YELLOW}Description:{c.NC} {pkg_data['description']}")
        print(f"{c.BLUE}{'=' * 70}{c.NC}\n")

        if args.reverse:
            print(
                f"{c.BOLD}{c.CYAN}Reverse Dependencies (what depends on {args.package}):{c.NC}\n"
            )
            print_reverse_tree(
                args.package,
                graph,
                max_depth=args.depth,
                show_versions=args.version,
                use_colors=use_colors,
            )
        else:
            print(f"{c.BOLD}{c.GREEN}Dependencies for {args.package}:{c.NC}\n")
            print_tree(
                args.package,
                graph,
                max_depth=args.depth,
                show_versions=args.version,
                use_colors=use_colors,
            )
    else:
        # Default: show statistics
        print_statistics(graph, use_colors)


if __name__ == "__main__":
    main()
