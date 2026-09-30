"""Enkripsi data teks menggunakan AES-256-GCM."""

import base64
import binascii
import os
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_KEY_SIZE = 32
_NONCE_SIZE = 12
_ROOT = Path(__file__).resolve().parents[1]


def _read_secret_key() -> str:
    """Ambil SECRET_KEY dari environment, atau fallback dari file .env."""
    secret_key = os.getenv("SECRET_KEY", "").strip()
    if secret_key:
        return secret_key

    env_file = _ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "SECRET_KEY":
                return value.strip().strip("\"'")

    raise ValueError("SECRET_KEY belum diatur di environment atau file .env.")


def _get_aes_key() -> bytes:
    """Decode dan validasi SECRET_KEY untuk AES-256."""
    encoded_key = _read_secret_key()
    try:
        aes_key = base64.urlsafe_b64decode(encoded_key + "=" * (-len(encoded_key) % 4))
    except (ValueError, binascii.Error) as exc:
        raise ValueError("SECRET_KEY harus berupa Base64 URL-safe yang valid.") from exc

    if len(aes_key) != _KEY_SIZE:
        raise ValueError(
            "SECRET_KEY harus merepresentasikan key AES-256 sepanjang 32 byte."
        )
    return aes_key


def encrypt(plaintext: str) -> str:
    """Enkripsi string dan kembalikan token Base64 URL-safe."""
    if not isinstance(plaintext, str):
        raise TypeError("plaintext harus berupa string.")

    nonce = os.urandom(_NONCE_SIZE)
    ciphertext = AESGCM(_get_aes_key()).encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")


def decrypt(token: str) -> str:
    """Dekripsi token hasil encrypt dan kembalikan plaintext."""
    if not isinstance(token, str):
        raise TypeError("token harus berupa string.")

    try:
        encrypted_data = base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Token enkripsi tidak valid.") from exc

    if len(encrypted_data) <= _NONCE_SIZE:
        raise ValueError("Token enkripsi tidak valid.")

    nonce, ciphertext = encrypted_data[:_NONCE_SIZE], encrypted_data[_NONCE_SIZE:]
    try:
        return AESGCM(_get_aes_key()).decrypt(nonce, ciphertext, None).decode("utf-8")
    except (InvalidTag, UnicodeDecodeError) as exc:
        raise ValueError("Token enkripsi tidak valid atau telah dimodifikasi.") from exc
