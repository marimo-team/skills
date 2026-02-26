---
name: wasm-compatibility
description: Check if a marimo notebook is compatible with WebAssembly (WASM) and report any issues.
---

# WASM Compatibility Checker for marimo Notebooks

Check whether a marimo notebook can run in a WebAssembly (WASM) environment — the marimo playground, community cloud, or exported WASM HTML.

## Instructions

### 1. Read the notebook

Read the target notebook file. If the user doesn't specify one, ask which notebook to check.

### 2. Extract dependencies

Collect every package the notebook depends on from **both** sources:

- **PEP 723 metadata** — the `# /// script` block at the top:
  ```python
  # /// script
  # dependencies = [
  #     "marimo",
  #     "torch>=2.0.0",
  # ]
  # ///
  ```
- **Import statements** — scan all cells for `import foo` and `from foo import bar`. Map submodules to their top-level distribution name (e.g. `from sklearn.cluster import KMeans` → `scikit-learn`; `import cv2` → `opencv-python`).

### 3. Check each package against Pyodide

For each dependency, determine if it can run in WASM:

1. **Is it in the Python standard library?** Most stdlib modules work, but these do **not**:
   - `multiprocessing` — browser sandbox has no process spawning
   - `subprocess` — same reason
   - `threading` — limited; no real threads (may improve in future)
   - `sqlite3` — use `apsw` instead (available in Pyodide)
   - `pdb` — not supported
   - `tkinter` — no GUI toolkit in browser
   - `readline` — no terminal in browser

2. **Is it a Pyodide built-in package?** See [pyodide-packages.md](references/pyodide-packages.md) for the full list. These work out of the box.

3. **Is it a pure-Python package?** Packages with only `.py` files (no compiled C/Rust extensions) can be installed at runtime via `micropip` and will work.

4. **Does it have C/native extensions not built for Pyodide?** These will **not** work. Common culprits:
   - `torch` / `pytorch`
   - `tensorflow`
   - `jax` / `jaxlib`
   - `psycopg2` (suggest `psycopg` with pure-Python mode)
   - `mysqlclient` (suggest `pymysql`)
   - `uvloop`
   - `grpcio`
   - `psutil`

### 4. Check for WASM-incompatible patterns

Scan the notebook code for patterns that won't work in WASM:

| Pattern | Why it fails | Suggestion |
|---|---|---|
| `subprocess.run(...)`, `os.system(...)`, `os.popen(...)` | No process spawning in browser | Remove or gate behind a non-WASM check |
| `multiprocessing.Pool(...)`, `ProcessPoolExecutor` | No process forking | Use single-threaded approach |
| `threading.Thread(...)`, `ThreadPoolExecutor` | Limited thread support | Use `asyncio` or single-threaded approach |
| `open("/some/local/path")` | No real filesystem; only in-memory fs | Fetch data via URL or embed in notebook |
| `sqlite3.connect(...)` | stdlib sqlite3 unavailable | Use `apsw` or `duckdb` |
| `pdb.set_trace()`, `breakpoint()` | No debugger in WASM | Remove breakpoints |
| Reading env vars (`os.environ[...]`, `os.getenv(...)`) | Environment variables not available in browser | Use `mo.ui.text` for user input or hardcode defaults |
| `Path.home()`, `Path.cwd()` with real file expectations | Virtual filesystem only | Use URLs or embedded data |
| Large dataset loads (>100 MB) | 2 GB total memory cap | Use smaller samples or remote APIs |

### 5. Produce the report

Output a clear, actionable report with these sections:

**Compatibility: PASS / FAIL / WARN**

Use these verdicts:
- **PASS** — all packages and patterns are WASM-compatible
- **WARN** — likely compatible, but some packages could not be verified as pure-Python (list them so the user can check)
- **FAIL** — one or more packages or patterns are definitely incompatible

**Package Report** — table with columns: Package, Status (OK / WARN / FAIL), Notes

Example:
| Package | Status | Notes |
|---|---|---|
| marimo | OK | Available in WASM runtime |
| numpy | OK | Pyodide built-in |
| pandas | OK | Pyodide built-in |
| torch | FAIL | No WASM build — requires native C++/CUDA extensions |
| my-niche-lib | WARN | Not in Pyodide; verify it is pure-Python |

**Code Issues** — list each problematic code pattern found, with the cell or line and a suggested fix.

**Recommendations** — if the notebook fails, suggest concrete fixes:
- Replace incompatible packages with WASM-friendly alternatives
- Rewrite incompatible code patterns
- Suggest moving heavy computation to a hosted API and fetching results

## Additional context

- WASM notebooks run via [Pyodide](https://pyodide.org) in the browser
- Memory is capped at 2 GB
- Network requests work but may need CORS-compatible endpoints
- Chrome has the best WASM performance; Firefox, Edge, Safari also supported
- `micropip` can install any pure-Python wheel from PyPI at runtime
- For the full Pyodide built-in package list, see [pyodide-packages.md](references/pyodide-packages.md)
