import sys
import re
from pathlib import Path
import nbformat as nbf

CENTER_OPEN_RE = re.compile(
    r'<div[^>]*?\balign=["\']?center["\']?[^>]*>|'
    r'<div[^>]*?\bstyle=["\'][^"\']*text-align\s*:\s*center[^"\']*["\'][^>]*>|'
    r'<center\s*>',
    flags=re.IGNORECASE
)
DIV_OPEN_RE = re.compile(r'<div\b[^>]*>', flags=re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r'</div\s*>', flags=re.IGNORECASE)
CENTER_CLOSE_RE = re.compile(r'</center\s*>', flags=re.IGNORECASE)
STYLE_BLOCK_RE = re.compile(r'<style\b[^>]*>.*?</style\s*>', flags=re.IGNORECASE | re.DOTALL)
SPAN_OPEN_RE = re.compile(r'<span\b[^>]*>', flags=re.IGNORECASE)
SPAN_CLOSE_RE = re.compile(r'</span\s*>', flags=re.IGNORECASE)

def fix_cell_text(text: str) -> str:
    if not isinstance(text, str) or "<" not in text:
        return text

    t = text

    # Remove style blocks entirely (GitHub strips them anyway)
    t = STYLE_BLOCK_RE.sub('', t)

    # Normalize various "center" wrappers to <p align="center">
    t = CENTER_OPEN_RE.sub('<p align="center">', t)
    t = CENTER_CLOSE_RE.sub('</p>', t)

    # Convert any remaining <div>…</div> to paragraphs
    t = DIV_OPEN_RE.sub('<p>', t)
    t = DIV_CLOSE_RE.sub('</p>', t)

    # Remove spans (keep their contents)
    t = SPAN_OPEN_RE.sub('', t)
    t = SPAN_CLOSE_RE.sub('', t)

    # Ensure a newline after opening centered paragraphs to prevent odd wrapping
    t = t.replace('<p align="center">', '<p align="center">\n')

    # Balance <p>…</p>
    opens = len(re.findall(r'<p(?:\s+[^>]*)?>', t))
    closes = len(re.findall(r'</p>', t))
    if opens > closes:
        t += '\n' + ('</p>' * (opens - closes))

    return t

def fix_notebook(path: Path) -> bool:
    nb = nbf.read(path, as_version=4)
    changed = False
    for cell in nb.cells:
        if cell.get("cell_type") == "markdown":
            new_src = fix_cell_text(cell.get("source", ""))
            if new_src != cell.get("source", ""):
                cell["source"] = new_src
                changed = True
    if changed:
        nbf.write(nb, path)
        print(f"Fixed: {path}")
    else:
        print(f"No changes: {path}")
    return changed

def main():
    targets = [Path(p) for p in sys.argv[1:]] or list(Path(".").rglob("*.ipynb"))
    for p in targets:
        fix_notebook(p)

if __name__ == "__main__":
    main()
