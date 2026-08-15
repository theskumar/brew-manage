# Brewfile — declarative Homebrew package list
#
# Source of truth for `brew bundle`. Migrated from dotfiles setup/setup_mac.sh.
# Install everything:   brew bundle --file=Brewfile
# Check for drift:      brew bundle check --file=Brewfile
# Remove strays:        brew bundle cleanup --file=Brewfile
#
# Non-brew installs (bun, npm -g, gh extensions) stay in dotfiles setup_mac.sh.

# ---------------------------------------------------------------------------
# Taps
# ---------------------------------------------------------------------------
tap "ivandokov/contrib"   # phockup
tap "rjyo/moshi"          # moshi-hook (iPhone clipboard/notification sync)
tap "theskumar/tap"       # personal casks (recordly, usagepal)

# ---------------------------------------------------------------------------
# GNU replacements for outdated macOS built-ins
# ---------------------------------------------------------------------------
brew "coreutils"          # GNU file, shell, text utilities
brew "findutils"          # GNU find, xargs, locate
brew "gnu-sed"            # GNU stream editor
brew "grep"               # GNU grep with PCRE support
brew "bash"               # modern Bash 5.x
brew "curl"               # URL transfer tool
brew "wget"               # file downloader
brew "watch"              # run command periodically
brew "wdiff"              # word-level diff

# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
brew "zsh"                # Z shell
brew "zplug"             # zsh plugin manager
brew "fzf"                # fuzzy finder
brew "zoxide"            # smarter cd with frecency
brew "eza"                # modern ls replacement
brew "tree"              # directory tree listing
brew "bat"                # cat with syntax highlighting
brew "fd"                 # fast find alternative
brew "ripgrep"          # fast recursive grep
brew "starship"          # cross-shell prompt
brew "zsh-history-substring-search"  # history search as you type
brew "spacer"            # visual separator in command output
brew "yazi"              # TUI file manager
brew "superfile"        # TUI file manager
brew "ffmpegthumbnailer"  # video thumbnails (yazi preview)
brew "poppler"          # PDF rendering (yazi preview)
brew "sevenzip"         # 7z/archive handling (yazi)
brew "helix"            # modal editor (hx)

# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------
brew "git"                # version control
brew "git-extras"        # extra git commands (info, effort, etc.)
brew "git-filter-repo"   # rewrite git history
brew "git-town"          # branch workflow automation
brew "git-delta"         # better diff pager
brew "git-trim"          # prune merged branches
brew "gitleaks"          # secret scanner
brew "lazygit"           # TUI git client
brew "jj"                 # Jujutsu VCS — Git-compatible, change-first model
brew "jjui"              # TUI for jj (like lazygit but for jj)
brew "gh"                 # GitHub CLI

# ---------------------------------------------------------------------------
# Search and HTTP
# ---------------------------------------------------------------------------
brew "ack"                # grep for source code
brew "httpie"            # human-friendly HTTP client
brew "jq"                 # JSON processor
brew "xsv"                # CSV toolkit

# ---------------------------------------------------------------------------
# Network diagnostics
# ---------------------------------------------------------------------------
brew "mtr"                # traceroute + ping combined
brew "ngrep"            # network packet grep
brew "nmap"            # network scanner and auditor
brew "mosh"            # mobile shell, survives roaming

# ---------------------------------------------------------------------------
# Network / Cloud services
# ---------------------------------------------------------------------------
brew "caddy"             # web server with automatic HTTPS
brew "cloudflared"       # Cloudflare tunnel
brew "flyctl"            # Fly.io CLI
brew "heroku/brew/heroku"  # Heroku CLI
brew "snowflake-cli"     # Snowflake developer CLI
brew "mailpit"           # local email testing
brew "mkcert"            # local HTTPS certs
brew "ttyd"              # terminal over web

# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------
brew "ffmpeg"           # video/audio converter
brew "webp"             # WebP image tools
brew "graphviz"         # DOT graph rendering
brew "imagemagick"      # image manipulation toolkit
brew "sox"              # audio processing
brew "tesseract"        # OCR engine
brew "gdal"             # geospatial data toolkit

# ---------------------------------------------------------------------------
# Docs and writing
# ---------------------------------------------------------------------------
brew "pandoc"           # universal document converter
brew "glow"             # markdown renderer in terminal
brew "marksman"         # markdown LSP (helix, zed)
brew "hugo"             # static site generator
brew "typst"            # modern typesetting
brew "monolith"         # save web pages as single HTML
brew "weasyprint"       # HTML to PDF

# ---------------------------------------------------------------------------
# Dev tools
# ---------------------------------------------------------------------------
brew "redis"            # in-memory data store
brew "stow"             # symlink farm manager
brew "ossp-uuid"       # UUID generation library
brew "moor"            # human-friendly terminal pager
brew "htop"            # interactive process viewer
brew "mactop"         # macOS system monitor
brew "ncdu"           # disk usage analyzer
brew "television"     # fuzzy file finder TUI
brew "phockup"        # organizes photos by EXIF date
brew "just"           # command runner (Makefile alternative)
brew "rust"           # Rust toolchain
brew "cmake"          # build system generator
brew "php"            # PHP interpreter
brew "virtualenv"    # Python virtual environments
brew "typos-cli"     # spell checker for source code
brew "fsouza/prettierd/prettierd"  # Prettier as a daemon
brew "avencera/tap/rustywind"      # Tailwind class sorter
brew "dotenvx/brew/dotenvx"        # dotenv with encryption support
brew "difftastic"    # structural diffs (AST-aware)
brew "diffr"         # LCS-based diff highlighting
brew "adr-tools"     # architecture decision records
brew "hf"            # Hugging Face CLI
brew "hl"            # log viewer

# ---------------------------------------------------------------------------
# Dotfiles companions (have stow packages in this repo)
# ---------------------------------------------------------------------------
brew "joshmedeski/sesh/sesh"  # smart tmux session manager
brew "tmuxinator"    # tmux session manager
brew "worktrunk"     # git worktree CLI for parallel work

# ---------------------------------------------------------------------------
# JS / Node
# ---------------------------------------------------------------------------
brew "fnm"           # Node version manager
brew "pnpm"          # fast Node package manager
brew "yarn"          # Node package manager

# ---------------------------------------------------------------------------
# Databases
# ---------------------------------------------------------------------------
brew "postgresql@16"  # PostgreSQL 16
brew "postgresql@14"  # PostgreSQL 14
brew "duckdb"        # embedded analytical database
brew "litecli"       # SQLite client with autocomplete
brew "valkey"        # Redis fork (open source)
brew "pgsync"        # Postgres data sync

# ---------------------------------------------------------------------------
# Linters and security
# ---------------------------------------------------------------------------
brew "semgrep"       # static analysis tool
brew "zizmor"        # GitHub Actions linter

# ---------------------------------------------------------------------------
# Benchmarking
# ---------------------------------------------------------------------------
brew "siege"         # HTTP load testing
brew "sloccount"     # source line counter
brew "multitail"     # tail multiple files simultaneously
brew "bombardier"    # HTTP benchmarking

# ---------------------------------------------------------------------------
# Desktop notifications
# ---------------------------------------------------------------------------
brew "terminal-notifier"  # macOS banners with click actions

# ---------------------------------------------------------------------------
# iPhone integration
# ---------------------------------------------------------------------------
brew "rjyo/moshi/moshi-hook"  # Moshi host daemon (pair once: `moshi-hook host setup`)

# ---------------------------------------------------------------------------
# RSS
# ---------------------------------------------------------------------------
brew "newsboat"      # terminal RSS/Atom feed reader

# ---------------------------------------------------------------------------
# Fun
# ---------------------------------------------------------------------------
brew "fortune"       # random quotes
brew "cowsay"        # ASCII cow messages
brew "cmatrix"       # Matrix rain animation

# ---------------------------------------------------------------------------
# Niche / Hobby
# ---------------------------------------------------------------------------
brew "scarvalhojr/tap/aoc-cli"  # Advent of Code CLI
brew "tw93/tap/mole"            # macOS app uninstaller
brew "iwe-org/iwe/iwe"          # markdown knowledge management

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
cask "font-fira-code-nerd-font"     # Fira Code with Nerd Font icons
cask "font-hack-nerd-font"          # Hack with Nerd Font icons
cask "font-source-code-pro"         # Adobe Source Code Pro
cask "font-symbols-only-nerd-font"  # Nerd Font icons only
cask "sf-symbols"                   # Apple SF Symbols

# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
cask "ghostty"           # GPU-accelerated terminal
cask "orbstack"          # Docker and Linux on macOS
cask "obsidian"          # markdown knowledge base
cask "bruno"             # API client
cask "1password-cli"     # 1Password CLI
cask "stats"             # menu bar system monitor
cask "monitorcontrol"    # external display brightness
cask "finicky"           # default browser router
cask "omniwm"            # tiling window manager
cask "basictex"          # minimal TeX distribution
cask "iterm2"            # terminal emulator
cask "karabiner-elements"  # keyboard customizer
cask "thaw"              # macOS menu bar manager

# ---------------------------------------------------------------------------
# Personal tap casks (theskumar/tap — apps not in homebrew-cask)
# ---------------------------------------------------------------------------
cask "theskumar/tap/recordly"  # screen recording app
cask "theskumar/tap/usagepal"  # menubar AI coding usage tracker

# ---------------------------------------------------------------------------
# Quick Look plugins (run `qlmanage -r` after install)
# ---------------------------------------------------------------------------
cask "qlcolorcode"       # syntax-highlighted source preview
cask "qlstephen"         # preview extensionless plain-text files
cask "qlmarkdown"        # markdown preview
cask "quicklook-json"    # JSON preview
cask "qlprettypatch"     # .patch/.diff preview
cask "quicklook-csv"     # CSV preview
cask "betterzipql"       # archive preview
cask "webp-quicklook"    # WebP preview
cask "suspicious-package"  # inspect .pkg installers
