#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "_pages"
INCLUDES_DOCS = ROOT / "_includes/docs"

EXCLUDE_DIRS = {".git", ".github", "_pages", "_site", ".jekyll-cache", "vendor", ".bundle"}

TOP_LEVEL_SLUGS = {
    "1 - Introduction to Escape-to-Host Flaws": "introduction",
    "2 - Kiosk Playbook": "kiosk-playbook",
    "3 - Presented App Playbook": "presented-app-playbook",
    "4 - Specific Escape Scenarios": "escape-scenarios",
    "5 - Defensive Recommendations": "defensive-recommendations",
}

_NUM_PREFIX_RE = re.compile(r"^\s*\d+\s*-\s*(.*)$")

def strip_numeric_prefix(s: str) -> str:
    m = _NUM_PREFIX_RE.match(s)
    return m.group(1) if m else s

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = strip_numeric_prefix(s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "page"

def title_from_path(md_rel: Path) -> str:
    if md_rel.name.lower() == "readme.md":
        if md_rel.parent == Path("."): return "About"
        return strip_numeric_prefix(md_rel.parent.name).strip()
    return strip_numeric_prefix(md_rel.stem).strip()

def permalink_for(md_rel: Path) -> str:
    parts = list(md_rel.parts)
    if parts and parts[0] in TOP_LEVEL_SLUGS:
        parts[0] = TOP_LEVEL_SLUGS[parts[0]]
    elif parts:
        parts[0] = slugify(parts[0])
    if md_rel.name.lower() == "readme.md": parts = parts[:-1]
    else: parts[-1] = slugify(md_rel.stem)
    parts = [parts[0]] + [slugify(p) for p in parts[1:]]
    return "/" + "/".join(parts) + "/"

def iter_markdown_files():
    out = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts): continue
        if rel in {Path("README.md"), Path("index.md")}: continue
        if "_includes" in rel.parts: continue
        out.append(rel)
    return sorted(out)

def sync_includes_docs():
    if INCLUDES_DOCS.exists(): shutil.rmtree(INCLUDES_DOCS)
    INCLUDES_DOCS.mkdir(parents=True)
    for md_rel in iter_markdown_files():
        parts = [slugify(p) if i < len(md_rel.parts)-1 else slugify(md_rel.stem) + ".md" for i, p in enumerate(md_rel.parts)]
        dest = INCLUDES_DOCS / Path(*parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / md_rel, dest)
    shutil.copy2(ROOT / "README.md", INCLUDES_DOCS / "readme.md")
    for src, slug in TOP_LEVEL_SLUGS.items():
        src_path = ROOT / src / "README.md"
        if src_path.exists():
            dest = INCLUDES_DOCS / slug / "readme.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest)

def main():
    if PAGES_DIR.exists(): shutil.rmtree(PAGES_DIR)
    PAGES_DIR.mkdir(exist_ok=True)
    sync_includes_docs()
    
    # About page
    about_dir = PAGES_DIR / "about"
    about_dir.mkdir()
    (about_dir / "index.md").write_text("---\nlayout: page\ntitle: \"About\"\npermalink: /about/\n---\n\n{% include docs/readme.md %}\n")

    for md_rel in iter_markdown_files():
        permalink = permalink_for(md_rel)
        title = title_from_path(md_rel)
        out_dir = PAGES_DIR / permalink.strip("/")
        out_dir.mkdir(parents=True, exist_ok=True)
        parts = [slugify(p) if i < len(md_rel.parts)-1 else slugify(md_rel.stem) + ".md" for i, p in enumerate(md_rel.parts)]
        include_path = "docs/" + "/".join(parts)
        (out_dir / "index.md").write_text(f"---\nlayout: page\ntitle: \"{title}\"\npermalink: {permalink}\n---\n\n{{% include {include_path} %}}\n")

    for slug in TOP_LEVEL_SLUGS.values():
        out_dir = PAGES_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.md").write_text(f"---\nlayout: page\ntitle: \"{slug.replace('-', ' ').title()}\"\npermalink: /{slug}/\n---\n\n{{% include docs/{slug}/readme.md %}}\n")

if __name__ == "__main__": main()
