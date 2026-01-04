# Brew Package Manager Tools

A collection of fast, Python-based tools for managing and visualizing Homebrew packages.

## Tools

### 1. `brew-info.py` - Fast Package Information Generator

Generates detailed information about all installed Homebrew packages with JSON export support.

#### Features

- ⚡ **Fast**: Uses parallel processing to gather package info quickly
- 📊 **JSON Export**: Generate machine-readable JSON output
- 🎨 **Colored Output**: Beautiful terminal output with colors
- 📝 **Comprehensive Info**: Dependencies, reverse dependencies, versions, and descriptions

#### Usage

```bash
# Display to terminal with colors
./brew-info.py

# Save text report to file
./brew-info.py --output report.txt

# Generate JSON output
./brew-info.py --json

# Save JSON to file (recommended for use with other tools)
./brew-info.py --json --output brew-packages.json

# Disable colors (useful for piping)
./brew-info.py --no-color

# Adjust parallel workers (default: 10)
./brew-info.py --max-workers 5
```

#### JSON Output Structure

```json
{
  "generated_at": "2025-01-15T10:30:00",
  "summary": {
    "total_formulas": 337,
    "total_casks": 15,
    "total_packages": 352
  },
  "formulas": [...],
  "casks": [...]
}
```

---

### 2. `brew-deps-graph.py` - Dependency Graph Visualizer

Visualizes package dependencies in a beautiful tree structure in your terminal.

#### Features

- 🌳 **Tree Visualization**: ASCII tree with proper connectors
- 🔄 **Reverse Dependencies**: See what depends on a package
- 📊 **Statistics**: Analyze dependency patterns
- 🎯 **Filtering**: Show roots, leaves, or specific packages
- 🎨 **Colored Output**: Easy-to-read color-coded trees

#### Usage

##### Basic Statistics

```bash
# Show dependency statistics (default)
./brew-deps-graph.py brew-packages.json --stats
```

Output:

```
======================================================================
DEPENDENCY STATISTICS
======================================================================

Total Packages: 337
Total Dependencies: 733
Average Dependencies per Package: 2.18
Root Packages (not depended on): 101
Leaf Packages (no dependencies): 151

Top 10 Most Depended On Packages:
   1. openssl@3                      (42 packages)
   2. zstd                           (21 packages)
   3. gettext                        (21 packages)
   ...
```

##### View Package Dependencies

```bash
# Show full dependency tree for a package
./brew-deps-graph.py brew-packages.json -p python@3.14

# Limit tree depth
./brew-deps-graph.py brew-packages.json -p node --depth 2

# Show package versions
./brew-deps-graph.py brew-packages.json -p ffmpeg --version
```

Output example:

```
Dependencies for python@3.14:

└── python@3.14 [5 deps]
    ├── mpdecimal
    ├── openssl@3 [1 deps]
    │   └── ca-certificates
    ├── sqlite [1 deps]
    │   └── readline
    ├── xz
    └── zstd [2 deps]
        ├── lz4
        └── xz
```

##### View Reverse Dependencies

```bash
# Show what depends on a package
./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse

# Limit depth to avoid overwhelming output
./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse --depth 2
```

Output example:

```
Reverse Dependencies (what depends on openssl@3):

└── openssl@3 [required by 67]
    ├── apache-arrow [required by 1]
    ├── curl [required by 1]
    ├── python@3.14 [required by 13]
    ├── node [required by 1]
    └── ruby [required by 1]
```

##### List Packages

```bash
# List all packages with basic info
./brew-deps-graph.py brew-packages.json --list

# Filter with grep
./brew-deps-graph.py brew-packages.json --list | grep python
```

##### Find Root and Leaf Packages

```bash
# Show root packages (not depended on by others)
./brew-deps-graph.py brew-packages.json --roots

# Show leaf packages (have no dependencies)
./brew-deps-graph.py brew-packages.json --leaves
```

#### Command-Line Options

```
positional arguments:
  json_file             Path to brew-packages.json file (default: brew-packages.json)

options:
  -h, --help            Show help message and exit
  -p, --package PKG     Show dependency tree for specific package
  -r, --reverse         Show reverse dependencies
  -d, --depth N         Maximum depth to display (default: unlimited)
  --stats               Show dependency statistics
  --roots               Show root packages (not depended on by others)
  --leaves              Show leaf packages (no dependencies)
  --list                List all packages with basic info
  --no-color            Disable colored output
  --version             Show package versions in tree
```

## Installation

1. Make scripts executable:

```bash
chmod +x brew-info.py brew-deps-graph.py
```

2. Ensure Python 3 is installed (comes with macOS by default)

## Workflow

### Complete Workflow Example

```bash
# Step 1: Generate package information and save as JSON
./brew-info.py --json --output brew-packages.json

# Step 2: View statistics
./brew-deps-graph.py brew-packages.json --stats

# Step 3: Investigate specific packages
./brew-deps-graph.py brew-packages.json -p python@3.14

# Step 4: Find what depends on a critical package
./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse --depth 2

# Step 5: Find packages you can safely remove (no reverse dependencies)
./brew-deps-graph.py brew-packages.json --roots
```

## Use Cases

### 1. Understanding Your System

- See what packages you have installed
- Understand package relationships
- Find unused packages

### 2. Before Removing Packages

```bash
# Check what depends on a package before removing it
./brew-deps-graph.py brew-packages.json -p <package-name> --reverse
```

### 3. Debugging Dependency Issues

```bash
# Find why a package was installed
./brew-deps-graph.py brew-packages.json -p <package-name> --reverse

# Find all dependencies of a problematic package
./brew-deps-graph.py brew-packages.json -p <package-name>
```

### 4. Finding Heavy Dependencies

```bash
# See which packages have the most dependencies
./brew-deps-graph.py brew-packages.json --stats
```

### 5. Identifying Critical Packages

```bash
# Find packages that many others depend on
./brew-deps-graph.py brew-packages.json --stats

# Then investigate further
./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse --depth 1
```

## Performance

- **brew-info.py**: Gathers info for 300+ packages in ~30-60 seconds (vs 5+ minutes for bash script)
- **brew-deps-graph.py**: Instant visualization from JSON file

## Tips

1. **Save JSON output** for repeated analysis without re-querying brew
2. **Use depth limiting** (`--depth 2`) for large dependency trees
3. **Pipe to `less`** for large outputs: `./brew-deps-graph.py ... | less -R`
4. **Use `--no-color`** when redirecting to files or piping to other tools
5. **Combine with grep** for filtering: `./brew-deps-graph.py --list | grep python`

## Requirements

- Python 3.6+
- Homebrew installed
- macOS or Linux

## License

MIT

## Contributing

Feel free to submit issues or pull requests!

## Future Enhancements

- [ ] Export dependency graph to DOT format for Graphviz
- [ ] Interactive TUI mode
- [ ] Diff between two JSON snapshots
- [ ] Suggest packages to remove
- [ ] Generate Brewfile from JSON
- [ ] HTML report generation
