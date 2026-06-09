[README](README.md) | [Introduction](Introduction.md) | Setup ⮕ [Datasets](Datasets.md) | [Tasks](Tasks.md) | [Notebook](notebook.ipynb)

# Setup your local environment

This module uses [uv](https://docs.astral.sh/uv/), a Python package and project manager that handles Python installation and dependencies for you.

## Step 1: Install uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal (or run `source ~/.bashrc` / `source ~/.zshrc`) so the `uv` command is available.

### Windows

Open **PowerShell** and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart PowerShell so the `uv` command is available.

## Step 2: Install dependencies

Run this once from the project directory to install all required packages (including Jupyter):

```bash
uv sync
```

## Step 3: Launch the notebook

```bash
uv run jupyter notebook notebook.ipynb
```

This will open Jupyter in your browser. If the browser does not open automatically, copy the URL printed in the terminal (it looks like `http://127.0.0.1:8888/...`) and paste it into your browser.
