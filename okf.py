from __future__ import annotations

import re
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n?", re.DOTALL)
# Matches [text](path) but skips images ![alt](path) and non-local links (http...)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


@dataclass
class OKFConcept:
    concept_id: str  # e.g. "tables/users" (file path minus .md)
    path: Path  # absolute path on disk
    frontmatter: dict = field(default_factory=dict)
    body: str = ""
    links: list[str] = field(default_factory=list)  # resolved concept_ids

    @property
    def type(self) -> str:
        return self.frontmatter.get("type", "unknown")

    @property
    def title(self) -> str:
        return self.frontmatter.get("title", self.concept_id)

    @property
    def tags(self) -> list[str]:
        return self.frontmatter.get("tags", []) or []

    def as_text(self) -> str:
        """What you'd hand an LLM: frontmatter as a readable header + body."""
        meta_lines = "\n".join(f"{k}: {v}" for k, v in self.frontmatter.items())
        return f"# {self.title}\n\n{meta_lines}\n\n{self.body}".strip()


class OKFBundle:
    """Loads a directory of .md files into a navigable concept graph."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.concepts: dict[str, OKFConcept] = {}
        self._load()

    def _load(self) -> None:
        for md_path in self.root.rglob("*.md"):
            concept_id = md_path.relative_to(self.root).with_suffix("").as_posix()
            raw = md_path.read_text(encoding="utf-8")

            fm_match = FRONTMATTER_RE.match(raw)
            if fm_match:
                frontmatter = yaml.safe_load(fm_match.group(1)) or {}
                body = raw[fm_match.end() :]
            else:
                frontmatter = {}
                body = raw

            links = self._resolve_links(body, md_path)

            self.concepts[concept_id] = OKFConcept(
                concept_id=concept_id,
                path=md_path,
                frontmatter=frontmatter,
                body=body.strip(),
                links=links,
            )

    def _resolve_links(self, body: str, source_path: Path) -> list[str]:
        resolved = []
        for raw_target in LINK_RE.findall(body):
            target = raw_target.split()[0]  # strip any "title" suffix
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = (source_path.parent / target).resolve()
            if target_path.suffix == ".md":
                try:
                    cid = target_path.relative_to(self.root).with_suffix("").as_posix()
                    resolved.append(cid)
                except ValueError:
                    pass  # link escapes the bundle root; ignore
        return resolved

    # -- graph primitives ---------------------------------------------------

    def get(self, concept_id: str) -> Optional[OKFConcept]:
        return self.concepts.get(concept_id)

    def neighbors(self, concept_id: str) -> list[OKFConcept]:
        c = self.get(concept_id)
        if not c:
            return []
        return [self.concepts[cid] for cid in c.links if cid in self.concepts]

    def by_tag(self, tag: str) -> list[OKFConcept]:
        return [c for c in self.concepts.values() if tag in c.tags]

    def by_type(self, type_: str) -> list[OKFConcept]:
        return [c for c in self.concepts.values() if c.type == type_]

    def list_ids(self) -> list[str]:
        return sorted(self.concepts.keys())


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python okf_agent.py /path/to/okf_bundle")
        sys.exit(1)

    bundle = OKFBundle(sys.argv[1])
    print(f"Loaded {len(bundle.concepts)} concepts:")
    for cid in bundle.list_ids():
        c = bundle.get(cid)
        print(f"  {cid} [{c.type}] -> links: {c.links}")
