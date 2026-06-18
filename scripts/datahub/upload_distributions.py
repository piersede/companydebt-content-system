"""Upload the data-hub CSV distributions to the public theme-assets path.

Serves them at:
  /wp-content/themes/company-debt-webpigment/assets/data-hub/downloads/<file>.csv

Run AFTER export_distributions.py. Reuses the SFTP creds in .env.
  PYTHONIOENCODING=utf-8 python scripts/datahub/upload_distributions.py
"""
from __future__ import annotations

import os
import pathlib

import paramiko
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
SRC = ROOT / "data" / "distributions"
REMOTE_DIR = "wp-content/themes/company-debt-webpigment/assets/data-hub/downloads"
FILES = [
    "uk-company-insolvency-statistics.csv",
    "uk-winding-up-petition-notices.csv",
    "uk-company-dissolutions-vs-insolvencies.csv",
    "uk-payment-practices-by-sector.csv",
]


def main() -> int:
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    s = paramiko.SFTPClient.from_transport(t)
    try:
        try:
            s.mkdir(REMOTE_DIR)
            print(f"created {REMOTE_DIR}")
        except IOError:
            print(f"dir exists: {REMOTE_DIR}")
        for f in FILES:
            local = SRC / f
            remote = f"{REMOTE_DIR}/{f}"
            s.put(str(local), remote)
            size = s.stat(remote).st_size
            print(f"PUT {f}  ({size} bytes)")
    finally:
        s.close(); t.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
