# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Generate Package Data

First, generate a JSON file with all your Homebrew package information:

```bash
./brew-info.py --json --output brew-packages.json
```

This will take about 30-60 seconds and create a `brew-packages.json` file.

### Step 2: Explore Your Packages

Now you can instantly analyze your packages!

#### See Overall Statistics

```bash
./brew-deps-graph.py brew-packages.json --stats
```

#### View a Specific Package's Dependencies

```bash
./brew-deps-graph.py brew-packages.json -p python@3.14
```

#### Find What Depends on a Package

```bash
./brew-deps-graph.py brew-packages.json -p openssl@3 --reverse --depth 2
```

## 📖 Common Tasks

### Before Removing a Package

**Want to remove a package? Check what depends on it first:**

```bash
./brew-deps-graph.py brew-packages.json -p <package-name> --reverse
```

If nothing depends on it, it's safe to remove!

### Find Packages You Can Remove

**Find "root" packages (nothing depends on them):**

```bash
./brew-deps-graph.py brew-packages.json --roots
```

These are packages you explicitly installed. Remove any you don't need.

### Understand Why a Package Was Installed

**Did Homebrew install something you didn't ask for?**

```bash
./brew-deps-graph.py brew-packages.json -p <mystery-package> --reverse
```

This shows what depends on it and why it's there.

### Find Your Most Critical Packages

**Which packages are most depended upon:**

```bash
./brew-deps-graph.py brew-packages.json --stats
```

Look at the "Top 10 Most Depended On Packages" section.

### List All Packages

```bash
./brew-deps-graph.py brew-packages.json --list
```

Or search for specific ones:

```bash
./brew-deps-graph.py brew-packages.json --list | grep python
```

## 💡 Pro Tips

1. **Save the JSON file** - Run `brew-info.py` once, then use `brew-deps-graph.py` many times
2. **Use `--depth 2`** - Large trees are easier to read with limited depth
3. **Pipe to less** - For long output: `./brew-deps-graph.py ... | less -R`
4. **Update regularly** - Regenerate JSON after installing/removing packages

## 🎯 Real-World Examples

### Example 1: Cleaning Up Your System

```bash
# Generate current state
./brew-info.py --json --output brew-packages.json

# Find packages nothing depends on
./brew-deps-graph.py brew-packages.json --roots

# Check if you need any of them - if not, remove:
brew uninstall <package-name>
```

### Example 2: Understanding Python Dependencies

```bash
# What does Python depend on?
./brew-deps-graph.py brew-packages.json -p python@3.14

# What depends on Python?
./brew-deps-graph.py brew-packages.json -p python@3.14 --reverse
```

### Example 3: Investigating Heavy Packages

```bash
# Show packages with most dependencies
./brew-deps-graph.py brew-packages.json --stats

# Then examine them:
./brew-deps-graph.py brew-packages.json -p ffmpeg --depth 2
```

## 🔧 Troubleshooting

### Script won't run?
```bash
chmod +x brew-info.py brew-deps-graph.py
```

### Package not found?
List all packages to find the exact name:
```bash
./brew-deps-graph.py brew-packages.json --list | grep <search-term>
```

### Output too long?
- Use `--depth 2` to limit tree depth
- Pipe to `less -R` for scrolling
- Use `| head -50` to see first 50 lines

## 📚 Learn More

See [README.md](README.md) for complete documentation and all available options.

## ⏱️ How Long Does It Take?

- **brew-info.py**: ~30-60 seconds (one-time, save JSON)
- **brew-deps-graph.py**: Instant (reads from JSON)

vs. old bash script which took 5+ minutes every time!
