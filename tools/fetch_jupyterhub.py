"""
Fetch new weekly folders (uke36, Uke 37, ...) from jupyterhub.uio.no into this repo.

Runs automatically every day on GitHub Actions (.github/workflows/fetch-jupyterhub.yml),
but can also be run by hand from the repo folder:

    python tools/fetch_jupyterhub.py           # fetch any new weekly folders
    python tools/fetch_jupyterhub.py --list    # only show what's on the hub, download nothing

It needs a JupyterHub API token in the environment variable JUPYTERHUB_TOKEN.
Get one at https://jupyterhub.uio.no/hub/token. Never paste the token into this file.

Rules:
  - Only folders whose name looks like a week ("uke42", "Uke 42", "uke_42") are fetched.
  - A folder is skipped if the repo already has it (case and spaces ignored,
    so "Uke 36" on the hub matches "uke36" here).
  - Files that already exist locally are never overwritten.
  - Hidden files, .ipynb_checkpoints and files over 95 MB (GitHub's limit is 100 MB) are skipped.
"""

import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

try:
    # Use the operating system's certificate store instead of Python's own list.
    # Fixes "CERTIFICATE_VERIFY_FAILED" on Windows (e.g. when antivirus inspects HTTPS).
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

# ---- settings -------------------------------------------------------------
HUB_URL = "https://jupyterhub.uio.no"
REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_DIR = REPO_ROOT / "JupyterHub Download - BIOS1101"
SEARCH_DEPTH = 2          # how many folder levels down from the hub home to look for week folders
WEEK_PATTERN = re.compile(r"^uke[\s_-]*\d{1,2}$", re.IGNORECASE)
MAX_FILE_MB = 95
# ---------------------------------------------------------------------------

session = requests.Session()


def fail(msg):
    # GitHub Actions shows lines starting with ::error:: as a red error.
    print(f"::error::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"ERROR: {msg}")
    sys.exit(1)


TOKEN = os.environ.get("JUPYTERHUB_TOKEN")
if not TOKEN:
    fail("JUPYTERHUB_TOKEN is not set. Locally: see the top of this file. "
         "On GitHub: add it under Settings -> Secrets and variables -> Actions.")
session.headers["Authorization"] = f"token {TOKEN}"


def hub_user():
    r = session.get(f"{HUB_URL}/hub/api/user", timeout=30)
    if r.status_code in (401, 403):
        fail("JupyterHub rejected the token. It may have expired: make a new one at "
             f"{HUB_URL}/hub/token and update the JUPYTERHUB_TOKEN secret.")
    r.raise_for_status()
    return r.json()


def server_url(timeout=180):
    """Return the base URL of the personal server, starting it if needed."""
    user = hub_user()
    name = user["name"]
    server = user.get("servers", {}).get("")
    if server and server.get("ready"):
        return HUB_URL + server["url"]

    print(f"Starting the JupyterHub server for {name} ...")
    r = session.post(f"{HUB_URL}/hub/api/users/{quote(name)}/server", timeout=30)
    if r.status_code not in (201, 202, 400):   # 400 = already starting
        fail(f"Could not start the server (HTTP {r.status_code}): {r.text[:300]}")

    deadline = time.time() + timeout
    while time.time() < deadline:
        server = hub_user().get("servers", {}).get("")
        if server and server.get("ready"):
            return HUB_URL + server["url"]
        time.sleep(5)
    fail("The server did not start in time. Log in once in the browser and run the job again.")


def list_dir(base, path):
    r = session.get(f"{base}api/contents/{quote(path)}", params={"content": 1}, timeout=60)
    r.raise_for_status()
    return [i for i in r.json()["content"] if not i["name"].startswith(".")]


def find_week_folders(base, path="", depth=0):
    found = []
    for item in list_dir(base, path):
        if item["type"] != "directory":
            continue
        if WEEK_PATTERN.match(item["name"]):
            found.append(item)
        elif depth + 1 < SEARCH_DEPTH:
            found.extend(find_week_folders(base, item["path"], depth + 1))
    return found


def norm(name):
    return re.sub(r"[\s_-]", "", name).lower()


def download(base, item, dest, counts):
    if item["type"] == "directory":
        dest.mkdir(parents=True, exist_ok=True)
        for child in list_dir(base, item["path"]):
            download(base, child, dest / child["name"], counts)
        return
    if dest.exists():
        return
    size = item.get("size") or 0
    if size > MAX_FILE_MB * 1024 * 1024:
        print(f"  ! skipped (too big for GitHub, {size // 2**20} MB): {item['path']}")
        counts["too_big"] += 1
        return
    r = session.get(f"{base}files/{quote(item['path'])}", stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
    counts["files"] += 1


def main():
    base = server_url()
    weeks = find_week_folders(base)
    if not weeks:
        print("No week folders found on the hub.")
        return

    LOCAL_DIR.mkdir(exist_ok=True)
    have = {norm(p.name) for p in LOCAL_DIR.iterdir() if p.is_dir()}
    new = [w for w in weeks if norm(w["name"]) not in have]

    print("Week folders on the hub:")
    for w in sorted(weeks, key=lambda w: w["path"]):
        print(f"  {'NEW ' if w in new else '    '}{w['path']}")

    if "--list" in sys.argv:
        return
    if not new:
        print("Nothing new.")
        return

    for w in new:
        counts = {"files": 0, "too_big": 0}
        print(f"Fetching {w['path']} ...")
        download(base, w, LOCAL_DIR / w["name"], counts)
        print(f"  {counts['files']} file(s) downloaded"
              + (f", {counts['too_big']} skipped as too big" if counts["too_big"] else ""))


if __name__ == "__main__":
    main()
