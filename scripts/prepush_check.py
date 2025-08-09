# scripts/prepush_check.py
import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

# Simple patterns for common secrets
SECRET_PATTERNS = [
    r"password\s*[:=]\s*.+",
    r"passwd\s*[:=]\s*.+",
    r"api[_-]?key\s*[:=]\s*.+",
    r"secret\s*[:=]\s*.+",
    r"token\s*[:=]\s*.+",
    r"AKIA[0-9A-Z]{16}",             # AWS Access Key
    r"AIza[0-9A-Za-z\-_]{35}",       # Google API key
    r"sk-[A-Za-z0-9]{20,}",          # Generic secret key pattern (e.g., API tokens)
]

TEXT_EXTENSIONS = {
    ".py", ".ipynb", ".md", ".txt", ".json", ".yml", ".yaml",
    ".ini", ".cfg", ".toml", ".csv", ".tsv", ".env"
}

LARGE_FILE_BYTES = 10 * 1024 * 1024  # 10 MB


def sh(args: List[str]) -> str:
    return subprocess.check_output(args, cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL)


def git_tracked_files() -> List[Path]:
    out = sh(["git", "ls-files"])
    return [REPO_ROOT / line for line in out.splitlines() if line.strip()]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def scan_file_for_secrets(path: Path) -> List[Tuple[int, str]]:
    findings = []
    try:
        if path.suffix.lower() == ".ipynb":
            with path.open("r", encoding="utf-8") as f:
                nb = json.load(f)
            def walk(obj):
                if isinstance(obj, dict):
                    for v in obj.values():
                        yield from walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        yield from walk(v)
                elif isinstance(obj, str):
                    yield obj
            for text in walk(nb):
                for pat in SECRET_PATTERNS:
                    m = re.search(pat, text, flags=re.IGNORECASE)
                    if m:
                        findings.append((-1, m.group(0)[:120]))
        else:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, start=1):
                    for pat in SECRET_PATTERNS:
                        if re.search(pat, line, flags=re.IGNORECASE):
                            findings.append((i, line.strip()[:200]))
    except Exception:
        # Skip unreadable/binary files
        pass
    return findings


def clear_ipynb_outputs(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as f:
            nb = json.load(f)
        changed = False
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "code":
                if cell.get("outputs"):
                    cell["outputs"] = []
                    changed = True
                if "execution_count" in cell and cell["execution_count"] is not None:
                    cell["execution_count"] = None
                    changed = True
        if changed:
            with path.open("w", encoding="utf-8") as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
                f.write("\n")
        return changed
    except Exception:
        return False


def main() -> int:
    fix = "--fix" in sys.argv
    files = git_tracked_files()

    # Large file check
    large = [p for p in files if p.exists() and p.is_file() and p.stat().st_size >= LARGE_FILE_BYTES]

    # Secret scan
    secret_hits = {}
    for p in files:
        if not p.exists() or not p.is_file():
            continue
        if not is_text_file(p):
            continue
        hits = scan_file_for_secrets(p)
        if hits:
            secret_hits[p] = hits

    # Notebook outputs
    ipynbs = [p for p in files if p.suffix.lower() == ".ipynb"]
    cleared = []
    if fix:
        for nb in ipynbs:
            if clear_ipynb_outputs(nb):
                cleared.append(nb)

    # Report
    print("Pre-push check")
    print("==============")
    print(f"Tracked files: {len(files)}")
    print(f"Notebooks: {len(ipynbs)}")
    if fix:
        print(f"Cleared notebook outputs: {len(cleared)}")
        for nb in cleared:
            print(f"  - {nb.relative_to(REPO_ROOT)}")

    if large:
        print("\nLarge files (>= 10MB):")
        for p in large:
            size_mb = p.stat().st_size / (1024 * 1024)
            print(f"  - {p.relative_to(REPO_ROOT)} ({size_mb:.1f} MB)")

    if secret_hits:
        print("\nPotential secrets found:")
        for p, hits in secret_hits.items():
            rel = p.relative_to(REPO_ROOT)
            for line_no, excerpt in hits:
                loc = f"line {line_no}" if line_no != -1 else "embedded"
                print(f"  - {rel} ({loc}): {excerpt}")

    # Exit code
    if large or secret_hits:
        print("\nResult: issues detected. Review before pushing.")
        if fix and cleared:
            print("Note: notebook outputs were cleared; remember to add/commit those changes.")
        return 1

    print("\nResult: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())