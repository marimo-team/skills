---
name: wasm-compatibility
description: Check if a marimo notebook is compatible with WebAssembly (WASM) and report any issues.
---

# WASM Compatibility Checker for marimo Notebooks

Check whether a marimo notebook can run in a WebAssembly (WASM) environment — the marimo playground, community cloud, or exported WASM HTML.

## Instructions

### 1. Read the notebook

Read the target notebook file. If the user doesn't specify one, ask which notebook to check.

### 2. Run marimo's WASM lint rules

marimo ships three lint rules that catch most WASM incompatibilities automatically. Run them first, and build the report from their output instead of re-deriving these checks by hand:

```bash
marimo check <notebook> --select MW --format json
```

- **MW001** `incompatible-import` — stdlib modules missing or non-functional in Pyodide (`subprocess`, `pdb`, `dbm`, `resource`, `fcntl`, `termios`, `readline`, `curses`, `tkinter`, `pydecimal`, `test`), plus multiprocessing exports and submodules that need native synchronization, shared memory, pipes, or process forking (`Lock`, `Condition`, `Semaphore`, `Barrier`, `Manager`, `Pipe`, `RLock`, `shared_memory`, `ForkContext`/`ForkProcess`, `ThreadPool`, and others). `Process`, `Queue`, `SimpleQueue`, `Pool`, and `ProcessPoolExecutor` stay allowed — they run on WASM-compatible cooperative adapters (see step 3).
- **MW002** `unsafe-system-call` — calls such as `os.system()`, `os.fork()`, `signal.signal()`, `breakpoint()` that fail in Pyodide even when the import itself succeeds.
- **MW003** `incompatible-package` — resolves the notebook's PEP 723 dependency tree (skipping anything excluded by a `sys_platform != 'emscripten'` marker) and checks PyPI for a WASM-compatible wheel, catching cases like `jaxlib` pulled in transitively through `jax`.

**Caveat:** MW001 flags import statements (`from multiprocessing import Lock`, `import multiprocessing.synchronize`), not later attribute access. A bare `import multiprocessing` followed by `multiprocessing.Lock()` deeper in the code can slip through. For notebooks with concurrency code, skim for this by hand too.

**Caveat:** a clean MW003 result does not by itself mean a package is safe to use in the browser. If a notebook marks a package `sys_platform != 'emscripten'`, MW003 skips it entirely — that only tells you the package will not be *installed* in WASM, not that the notebook is free to use it. Check whether the notebook also has `cache_cells = true` and was exported with `--execute` (see step 4). If so, the excluded package can still be used, through caching. If not, any code path that imports or touches the excluded package will fail in the browser, and MW003 will not have warned about it.

### 3. Check what the linter does not cover

These stay manual, agent-driven checks:

- **PEP 723 metadata.** If the notebook has no `# /// script` block, or imports a package that is not listed in `dependencies`, WARN. Without that metadata, packages do not auto-install when the notebook starts in WASM. Version pins and lower bounds are fine — marimo strips version constraints when running in WASM.
- **Runtime-only patterns.** Static lint does not catch these: reading environment variables (`os.environ`, `os.getenv`), hard-coded absolute file paths or `Path.home()`/`Path.cwd()` expecting a real filesystem, and large in-memory datasets (WASM notebooks are capped at 2GB). Flag these where you see them.
- **Concurrency semantics.** WASM notebooks run cooperative adapters for `threading.Thread`, `Event`, `local`, `ThreadPoolExecutor`, `wait`, `as_completed`, and process-shaped `multiprocessing.Process`, `Queue`, `SimpleQueue`, `Pool`, `ProcessPoolExecutor`. The API shape is real, but there are no OS threads, no shared memory, and no true parallelism. Everything runs one task at a time in the single Pyodide interpreter. If the notebook relies on actual concurrent speedup rather than the API shape alone, warn that it runs correctly but sequentially.
- **Cached execution already in place.** Check the notebook's `pyproject.toml` (or inline `# /// script` block) for `[tool.marimo.runtime] cache_cells = true`. If it is set, an incompatible package marked `sys_platform != 'emscripten'` is not automatically a FAIL — see the escape hatches in step 4.

### 4. Produce the report

Output a clear, actionable report:

**Compatibility: PASS / FAIL / WARN**

- **PASS** — the lint check and step 3 both found nothing.
- **WARN** — nothing failed, but step 3 turned up something worth a second look (missing PEP 723 metadata, a runtime-only pattern, or concurrency that will run but not in parallel).
- **FAIL** — the lint check reported a diagnostic, or step 3 found something that will not run at all.

**Lint findings** — paste the diagnostics from step 2 verbatim (file, line, code, message).

**Manual findings** — list anything from step 3, with the cell or line and a suggested fix.

**Recommendations** — for FAIL/WARN notebooks, suggest concrete fixes:
- Replace an incompatible package with a WASM-friendly alternative
- Rewrite an incompatible code pattern

For a package with no WASM build, there is no drop-in replacement. Two escape hatches exist, and they solve different problems — check which one the notebook actually needs:

1. **Precompute every reachable result and cache it.** Exclude the package from WASM with a `sys_platform != 'emscripten'` marker. marimo then runs the real computation once, server-side, and bundles the result into the export:

   ```toml
   # /// script
   # dependencies = [
   #     "marimo",
   #     "torch; sys_platform != 'emscripten'",
   # ]
   #
   # [tool.marimo.runtime]
   # cache_cells = true
   # ///
   ```

   ```bash
   marimo export html-wasm notebook.py -o output_dir --execute
   ```

   This covers a single static result (a plot, a one-off computation) directly. For a small, enumerable set of results — a dropdown or slider over a fixed list of options — decorate the computation with `@mo.persistent_cache(method="lazy")` instead. Add a cell that calls it once for every option before export. See [caching precomputed values](https://docs.marimo.io/guides/exporting/webassembly_html/#precomputed-values). Either way, the excluded package never runs in the browser — the notebook only reads its cached result.
2. **Use a compatibility layer that runs the real computation in the browser.** Precomputing does not cover an input space that cannot be enumerated ahead of time — a slider driving live inference over a continuous range, for example. The notebook needs an actual WASM-native implementation of the computation here. [`moutils.onnx.OnnxRuntime`](https://github.com/marimo-team/moutils/commit/a3a6651bd400429ddb416351aaec54b97535a069) is one example of this pattern: it converts a PyTorch or JAX model to ONNX, and the object it returns runs inference with `onnxruntime-web` in the browser instead of the original framework.

## Additional context

- WASM notebooks run via [Pyodide](https://pyodide.org) in the browser
- Memory is capped at 2GB
- Network requests work but may need CORS-compatible endpoints
- Chrome has the best WASM performance; Firefox, Edge, Safari also supported
- `micropip` can install any pure-Python wheel from PyPI at runtime
- For the full list of marimo's WASM lint rules, see the [lint rules reference](https://docs.marimo.io/guides/lint_rules/#-wasm-rules)
- For a hand-maintained snapshot of Pyodide's built-in packages, see [pyodide-packages.md](references/pyodide-packages.md). It is a quick human-readable reference, but `marimo check --select MW003` queries PyPI directly and stays current automatically
