"""YAML load/dump helpers (PyYAML if available, else minimal fallback for simple docs)."""

from __future__ import annotations

from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


def load(text: str) -> Any:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for Midlayer runtime (python3-yaml).")
    # Multi-doc (YAML frontmatter + body): merge mappings, last keys win
    text = text.lstrip("\ufeff")
    docs = list(yaml.safe_load_all(text))
    merged: dict = {}
    last_non_dict = None
    for doc in docs:
        if doc is None:
            continue
        if isinstance(doc, dict):
            merged.update(doc)
        else:
            last_non_dict = doc
    if merged:
        return merged
    return last_non_dict if last_non_dict is not None else {}


def load_file(path) -> Any:
    return load(path.read_text(encoding="utf-8"))


def dump(data: Any) -> str:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for Midlayer runtime (python3-yaml).")
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )


def dump_file(path, data: Any) -> None:
    path.write_text(dump(data), encoding="utf-8")
