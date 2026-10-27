"""Package the small CLI exercise without local outputs or credentials."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


root = Path(__file__).resolve().parents[1]
source = root / "practicals" / "cli-assistant"
members = ("README.md", "score.py", "check_score.py", "digital-chemistry.config.toml")
target = root / "downloads" / "cli-assistant.zip"
target.parent.mkdir(parents=True, exist_ok=True)

with ZipFile(target, "w") as archive:
    for name in members:
        info = ZipInfo(f"cli-assistant/{name}", date_time=(2026, 10, 27, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, (source / name).read_bytes())

print(f"Built {target.name} with {len(members)} files.")
