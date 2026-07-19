"""Character card frontmatter parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import yaml_util
from .paths import CHARACTERS, SKIP_CARD_NAMES


@dataclass
class CharacterCard:
    slug: str
    path: Path
    meta: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def name(self) -> str:
        return str(self.meta.get("name") or self.slug)

    @property
    def call_name(self) -> str:
        return str(self.meta.get("call_name") or self.name)

    @property
    def cognitive_bias(self) -> str:
        return str(self.meta.get("cognitive_bias") or "")

    @property
    def active_focus(self) -> str:
        return str(self.meta.get("active_focus") or "")

    @property
    def default_somatic(self) -> str:
        return str(self.meta.get("default_somatic_alignment") or "")

    @property
    def hard_bans(self) -> list[str]:
        voice = self.meta.get("voice") or {}
        bans = voice.get("hard_bans") if isinstance(voice, dict) else None
        if isinstance(bans, list):
            return [str(b) for b in bans]
        return []

    @property
    def latent_anchors(self) -> list[str]:
        raw = self.meta.get("latent_anchors") or []
        if isinstance(raw, list):
            return [str(x) for x in raw]
        return []

    def realm_keys(self) -> list[str]:
        """Extract Roman/Arabic realm tokens from focus + latents."""
        keys: list[str] = []
        blob = " ".join([self.active_focus, *self.latent_anchors])
        for m in re.finditer(
            r"\bRealm\s+(I{1,3}|IV|V?I{0,3}|IX|X|\d+)\b|\b(I{1,3}|IV|V?I{0,3}|IX|X)\s*[—-]",
            blob,
            re.I,
        ):
            tok = (m.group(1) or m.group(2) or "").upper()
            # normalize arabic
            arabic = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V",
                      "6": "VI", "7": "VII", "8": "VIII", "9": "IX", "10": "X"}
            tok = arabic.get(tok, tok)
            if tok and tok not in keys:
                keys.append(tok)
        # Also bare "VIII — Integration" style from logs
        for m in re.finditer(
            r"\b(I|II|III|IV|V|VI|VII|VIII|IX|X)\b",
            blob,
        ):
            tok = m.group(1)
            if tok not in keys:
                keys.append(tok)
        return keys


def parse_card(path: Path) -> CharacterCard:
    text = path.read_text(encoding="utf-8")
    slug = path.stem
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml_util.load(parts[1]) or {}
            body = parts[2].lstrip("\n")
            if not isinstance(meta, dict):
                meta = {}
            return CharacterCard(slug=slug, path=path, meta=meta, body=body)
    return CharacterCard(slug=slug, path=path, meta={}, body=text)


def list_cards() -> list[CharacterCard]:
    if not CHARACTERS.is_dir():
        return []
    cards: list[CharacterCard] = []
    for path in sorted(CHARACTERS.glob("*.md")):
        if path.name in SKIP_CARD_NAMES:
            continue
        if path.name.startswith("_"):
            continue
        cards.append(parse_card(path))
    return cards


def load_cards(slugs: list[str] | None = None) -> list[CharacterCard]:
    cards = list_cards()
    if slugs is None:
        return cards
    want = {s.lower() for s in slugs}
    found = [c for c in cards if c.slug.lower() in want]
    missing = want - {c.slug.lower() for c in found}
    if missing:
        raise FileNotFoundError(f"Unknown character slug(s): {', '.join(sorted(missing))}")
    # preserve requested order
    by = {c.slug.lower(): c for c in found}
    return [by[s.lower()] for s in slugs]
