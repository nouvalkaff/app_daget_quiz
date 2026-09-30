import os
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

ROOT = Path(__file__).resolve().parent
JUMLAH_SOAL = 5
DIR_PATH_IDN = ROOT / "question_bank" / "ind" / "bank_soal_secured.txt"


def ambil_link_daget() -> str | None:
    link = os.getenv("DAGET_LINK", "").strip()
    if not link:
        try:

            link = str(st.secrets.get("DAGET_LINK", "")).strip()
        except (FileNotFoundError, ImportError, AttributeError):
            pass

    if not link:
        env_file = ROOT / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8-sig").splitlines():
                key, separator, value = line.partition("=")
                if separator and key.strip() == "DAGET_LINK":
                    link = value.strip().strip("\"'")
                    break

    parsed = urlparse(link)
    return link if parsed.scheme in ("http", "https") and parsed.netloc else None
