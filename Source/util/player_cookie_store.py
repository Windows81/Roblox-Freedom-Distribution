from __future__ import annotations

import base64
import binascii
import dataclasses
import json
import os
from pathlib import Path

import util.resource

try:
    import win32crypt
except ImportError:  # pragma: no cover - optional dependency
    win32crypt = None


COOKIE_NAME = ".ROBLOSECURITY"
COOKIE_VERSION = "1"


@dataclasses.dataclass
class cookie_entry:
    domain: str
    include_subdomains: bool
    path: str
    secure: bool
    expiry: str
    name: str
    value: str
    http_only: bool = True

    def serialise(self) -> str:
        domain = (
            f"#HttpOnly_{self.domain}"
            if self.http_only else
            self.domain
        )
        return "\t".join([
            domain,
            "TRUE" if self.include_subdomains else "FALSE",
            self.path,
            "TRUE" if self.secure else "FALSE",
            self.expiry,
            self.name,
            self.value,
        ])


def get_roblox_dir_type():
    for name in dir(util.resource.dir_type):
        if name.endswith("BLOX"):
            return getattr(util.resource.dir_type, name)
    raise AttributeError("Roblox dir type not found")


def get_roblox_root_path() -> Path:
    candidate = Path(util.resource.retr_full_path(
        get_roblox_dir_type(),
    ))
    if candidate.exists():
        return candidate
    return Path(__file__).resolve().parents[2] / "Roblox"


def get_cookie_store_path() -> Path:
    return Path(os.path.normpath(str(
        get_roblox_root_path().parent / "LocalStorage" / "RobloxCookies.dat"
    )))


def get_fallback_cookie_store_path() -> Path:
    return Path(
        os.getenv("USERPROFILE", ""),
        "AppData",
        "Local",
        "Roblox",
        "LocalStorage",
        "RobloxCookies.dat",
    )


def normalise_hosts(hosts: set[str] | None) -> set[str]:
    if not hosts:
        return set()
    return {
        host.strip("[]").lower()
        for host in hosts
        if host
    }


def _parse_segment(segment: str) -> cookie_entry | None:
    if not segment:
        return None

    fields = segment.split("\t")
    if len(fields) != 7:
        return None

    raw_domain = fields[0]
    http_only = raw_domain.startswith("#HttpOnly_")
    domain = raw_domain.removeprefix("#HttpOnly_")
    return cookie_entry(
        domain=domain,
        include_subdomains=fields[1] == "TRUE",
        path=fields[2],
        secure=fields[3] == "TRUE",
        expiry=fields[4],
        name=fields[5],
        value=fields[6],
        http_only=http_only,
    )


def read_cookie_entries(path: Path | None = None) -> list[cookie_entry]:
    if win32crypt is None:
        return []

    path = path or get_cookie_store_path()
    if not path.exists():
        fallback_path = get_fallback_cookie_store_path()
        if fallback_path.exists():
            path = fallback_path
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            file_content = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    encoded_cookies = file_content.get("CookiesData")
    if not isinstance(encoded_cookies, str):
        return []

    try:
        decoded_cookies = base64.b64decode(encoded_cookies)
        decrypted_cookies = win32crypt.CryptUnprotectData(
            decoded_cookies,
            None,
            None,
            None,
            0,
        )[1].decode("utf-8", errors="ignore")
    except (binascii.Error, OSError, ValueError):
        return []
    return [
        entry
        for entry in (
            _parse_segment(segment)
            for segment in decrypted_cookies.split("; ")
        )
        if entry is not None
    ]


def get_cookie_value(
    *,
    name: str = COOKIE_NAME,
    preferred_hosts: set[str] | None = None,
    path: Path | None = None,
) -> str | None:
    entries = [
        entry
        for entry in read_cookie_entries(path)
        if entry.name == name
    ]
    if not entries:
        return None

    preferred_hosts = normalise_hosts(preferred_hosts)
    if preferred_hosts:
        for entry in entries:
            if entry.domain.lower() in preferred_hosts:
                return entry.value

    return entries[0].value


def write_cookie_entries(
    entries: list[cookie_entry],
    path: Path | None = None,
) -> None:
    if win32crypt is None:
        return

    path = path or get_cookie_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    serialised = "; ".join(
        entry.serialise()
        for entry in entries
    ).encode("utf-8")
    encrypted = win32crypt.CryptProtectData(
        serialised,
        None,
        None,
        None,
        None,
        0,
    )
    with path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "CookiesVersion": COOKIE_VERSION,
                "CookiesData": base64.b64encode(encrypted).decode("ascii"),
            },
            file,
            ensure_ascii=False,
        )


def sync_auth_cookie(
    hosts: set[str],
    value: str | None,
    path: Path | None = None,
) -> None:
    if win32crypt is None:
        return

    normalised_hosts = normalise_hosts(hosts)
    if not normalised_hosts:
        return

    entries = read_cookie_entries(path)
    entries = [
        entry
        for entry in entries
        if not (
            entry.name == COOKIE_NAME and
            entry.domain.lower() in normalised_hosts
        )
    ]

    if value is not None:
        for host in sorted(normalised_hosts):
            entries.append(cookie_entry(
                domain=host,
                include_subdomains=False,
                path="/",
                secure=True,
                expiry="0",
                name=COOKIE_NAME,
                value=value,
                http_only=True,
            ))

    write_cookie_entries(entries, path)
