#!/usr/bin/env python3
"""
Smoke-run curated DwC-A fixture zips and write per-fixture FAIRy reports.

Assumptions (Phase 0):
- Fixtures are occurrence-core archives and include occurrence.txt (or occurrence.csv)
- We do a minimal structure check (meta.xml present)
- We run existing dwc_starter rulepack on the extracted core file

Outputs:
reports/dwca_fixtures/<fixture_name>/{structure.summary.txt, report.json, report.md}
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def run(cmd: list[str]) -> int:
    """Run a command, stream stdout/stderr, return exit code."""
    print("  $", " ".join(cmd))
    return subprocess.call(cmd)

def parse_dwca_core_from_meta(meta_path: Path) -> tuple[str | None, int | None]:
    """
    Parse DwC-A meta.xml and return (core_location, core_id_index).
    Returns (None, None) if not found.
    """
    tree = ET.parse(meta_path)
    root = tree.getroot()

    # DwC-A meta.xml often uses a namespace; handle both namespaced and non-namespaced.
    def find_first(elem, tag: str):
        # Try without namespace
        x = elem.find(tag)
        if x is not None:
            return x
        # Try with any namespace
        for child in elem.iter():
            if child.tag.endswith(tag):
                return child
        return None

    core = find_first(root, "core")
    if core is None:
        return None, None

    files = find_first(core, "files")
    location = find_first(files, "location") if files is not None else None
    core_location = location.text.strip() if (location is not None and location.text) else None

    id_el = find_first(core, "id")
    core_id_index = None
    if id_el is not None:
        idx = id_el.attrib.get("index")
        if idx is not None:
            try:
                core_id_index = int(idx)
            except ValueError:
                core_id_index = None

    return core_location, core_id_index

def get_core_location_from_meta(meta_path: Path) -> str | None:
    """
    Return the DwC-A core <location> from meta.xml, or None if not found.
    Handles namespaces by matching tag suffixes.
    """
    tree = ET.parse(meta_path)
    root = tree.getroot()

    def find_first_by_suffix(elem, suffix: str):
        for e in elem.iter():
            if e.tag.endswith(suffix):
                return e
        return None

    core = find_first_by_suffix(root, "core")
    if core is None:
        return None

    # Find the first <location> under <core>/<files>
    files = None
    for e in core.iter():
        if e.tag.endswith("files"):
            files = e
            break
    if files is None:
        return None

    location = find_first_by_suffix(files, "location")
    if location is None or not location.text:
        return None

    return location.text.strip() or None


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fixtures_dir = repo_root / "datasets" / "fixtures" / "dwca" / "zips"
    rulepack = repo_root / "rulepacks" / "dwc_starter" / "rulepack.yaml"
    out_base = repo_root / "reports" / "dwca_fixtures"

    if not fixtures_dir.exists():
        print(f"ERROR: fixtures dir not found: {fixtures_dir}", file=sys.stderr)
        return 2
    if not rulepack.exists():
        print(f"ERROR: rulepack not found: {rulepack}", file=sys.stderr)
        return 2

    out_base.mkdir(parents=True, exist_ok=True)

    zips = sorted(fixtures_dir.glob("*.zip"))
    if not zips:
        print(f"No .zip fixtures found in {fixtures_dir}")
        return 0

    print("Running DwC-A fixture smoke tests...")
    print(f"Fixtures: {fixtures_dir}")
    print(f"Rulepack:  {rulepack}")
    print(f"Outputs:   {out_base}")
    print()

    for zip_path in zips:
        name = zip_path.stem
        outdir = out_base / name

        # Clean output dir
        if outdir.exists():
            shutil.rmtree(outdir)
        outdir.mkdir(parents=True, exist_ok=True)

        print(f"=== {name} ===")
        print(f"zip: {zip_path}")
        print(f"out: {outdir}")

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)

            # Unzip
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(tmpdir)
            except zipfile.BadZipFile:
                (outdir / "structure.summary.txt").write_text("zip_readable=false\n")
                print("FAIL: bad zip file")
                print()
                continue

            # Minimal structure check
            meta = tmpdir / "meta.xml"
            lines = []
            if not meta.exists():
                lines.append("meta_xml_present=false\n")
                (outdir / "structure.summary.txt").write_text("".join(lines))
                print("FAIL: meta.xml missing")
                print()
                continue
            lines.append("meta_xml_present=true\n")

            # Locate core via meta.xml
            try:
                core_location, core_id_index = parse_dwca_core_from_meta(meta)
            except ET.ParseError:
                lines.append("meta_xml_parseable=false\n")
                (outdir / "structure.summary.txt").write_text("".join(lines))
                print("FAIL: meta.xml not parseable XML")
                print()
                continue

            lines.append("meta_xml_parseable=true\n")

            if not core_location:
                lines.append("core_found=false\n")
                lines.append("core_reason=meta_xml_missing_core_location\n")
                (outdir / "structure.summary.txt").write_text("".join(lines))
                print("FAIL: meta.xml missing core/files/location")
                print()
                continue

            lines.append(f"core_location={core_location}\n")
            if core_id_index is not None:
                lines.append(f"core_id_index={core_id_index}\n")

            core = tmpdir / core_location
            if not core.exists():
                lines.append("core_found=false\n")
                lines.append("core_reason=core_location_missing\n")
                lines.append(f"core_expected_path={core}\n")
                
                # Helpful debug: list files actually present
                found = sorted(p.name for p in tmpdir.iterdir() if p.is_file())
                lines.append(f"files_present={','.join(found)}\n")

                (outdir / "structure.summary.txt").write_text("".join(lines))
                print(f"FAIL: meta.xml core file not found at {core_location}")
                print()
                continue

            # If core is occurrence.txt (DwC-A standard), copy to .tsv so FAIRy treats it as tabular.
            if core.suffix.lower() == ".txt":
                core_tsv = core.with_suffix(".tsv")
                shutil.copyfile(core, core_tsv)
                core = core_tsv

            lines.append("core_found=true\n")
            lines.append(f"core_path={core}\n")
            (outdir / "structure.summary.txt").write_text("".join(lines))


            # Run FAIRy validate. We don't hard-fail the smoke run if a fixture fails validation,
            # because broken fixtures are *expected* to fail. We still want the report artifacts.
            cmd = [
                "fairy",
                "validate",
                "--rulepack",
                str(rulepack),
                "--inputs",
                f"default={core}",
                "--report-json",
                str(outdir / "report.json"),
                "--report-md",
                str(outdir / "report.md"),
            ]
            exit_code = run(cmd)
            print(f"fairy validate exit code: {exit_code}")
            print()

    print("Complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
