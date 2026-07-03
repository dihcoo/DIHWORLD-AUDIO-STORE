#!/usr/bin/env python3
"""Build the DIHWorld Audio storefront fulfillment map.

The output CSV connects sellable storefront offers to current release artifacts,
checksums, prices, and publication blockers.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_CSV = ROOT / "data" / "plugin-catalog-42-current-canon.csv"
PRICE_CSV = ROOT / "data" / "dihworld-price-list-20260703.csv"
OUTPUT_CSV = ROOT / "data" / "fulfillment-map-20260703.csv"

RELEASE_INDEX = Path("/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/CURRENT_RELEASE_INDEX.md")
MANUAL_PATH = Path("/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/DIHWorld_Audio_User_Manual_CURRENT.pdf")
WINDOWS_INSTALLER = Path(
    "/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FINISHED/WINDOWS_RELEASE_20260702/"
    "DIHWorld_Audio_42_Plugin_Installer_Windows_x64.exe"
)
WINDOWS_SHA256 = "7f237bf3e5a41642d459ea66c76dacc7c8293300faccd7194f581160f6e5974e"

FIELDNAMES = [
    "SKU",
    "Product",
    "Offer Type",
    "Storefront Status",
    "Primary Family",
    "Included Products",
    "Count",
    "Launch Price",
    "Regular Price",
    "Mac DMG Path",
    "Mac DMG SHA256",
    "Mac PKG Path",
    "Mac PKG SHA256",
    "Windows Installer Path",
    "Windows SHA256",
    "SHA256 Source",
    "Manual Path",
    "Download 1 Name",
    "Download 1 URL",
    "WooCommerce Product URL",
    "Demo Asset URL",
    "Release Gate Status",
    "Next Action",
    "Notes",
]

FAMILY_SKUS = {
    "VOCAL_MIC_SOURCE": "DIH-FAM-VOCAL-MIC-SOURCE",
    "DYNAMICS_GUARD": "DIH-FAM-DYNAMICS-GUARD",
    "BASS_LOW_END": "DIH-FAM-BASS-LOW-END",
    "DRUM_INSTRUMENT": "DIH-FAM-DRUM-INSTRUMENT",
    "COLOR_AMP_TAPE": "DIH-FAM-COLOR-AMP-TAPE",
    "FIELD_TONE_BALANCE": "DIH-FAM-FIELD-TONE-BALANCE",
    "DIMENSIONAL_IMPACT_MOVE": "DIH-FAM-DIMENSIONAL-IMPACT-MOVE",
    "FX_SPATIAL": "DIH-FAM-FX-SPATIAL",
    "HARMONICS_PITCH": "DIH-FAM-HARMONICS-PITCH",
    "CREATIVE_TRANSFORM": "DIH-FAM-CREATIVE-TRANSFORM",
    "MASTERING_CORE": "DIH-FAM-MASTERING-CORE",
    "MASTER_FIELD": "DIH-FAM-MASTER-FIELD",
    "UTILITY_OBSERVATION": "DIH-FAM-UTILITY-OBSERVATION",
}

ARTIFACT_ALIASES = {
    "AEGIS NOVA": "AEGIS_NOVA",
    "DEPTH IMPACT HYBRID X": "Depth_Impact_Hybrid_X",
    "DEPTH BOOST PRO": "DEPTH_BOOST_PRO",
    "HORIZON X": "Horizon_X",
    "DIH DRUM MORPHER": "Drum_Morpher",
    "ARCHAEOLOGIST X": "ARCHAEOLOGIST_X",
    "PTAHTUBE": "PtahTube",
    "KHEPRI": "Khepri_Sacred_Tape_Machine",
    "MAAT": "Maat",
    "PLATINUM": "PLATINUM",
    "LOOKOUT": "LookOut",
    "DEBO": "DeBo",
    "DRUMKRUSHGLUE": "DrumKrushGlue",
    "BALLPARK": "Ballpark",
    "SLOTMACHINE": "SlotMachine",
    "THOTH": "Thoth",
}

WORKFLOW_TO_FAMILY = {
    "DIH-BUNDLE-VOCAL-CAPTURE": "VOCAL_MIC_SOURCE",
    "DIH-BUNDLE-BASS-FOUNDATION": "BASS_LOW_END",
    "DIH-BUNDLE-COLOR-AMP-TAPE": "COLOR_AMP_TAPE",
}


def norm(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", value.upper())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_release_dirs() -> tuple[Path, dict[str, Path]]:
    text = RELEASE_INDEX.read_text(encoding="utf-8")
    root_match = re.search(r"## Release Root\s+`([^`]+)`", text)
    bulk_match = re.search(r"## Bulk Release\s+`([^`]+)`", text)
    if not root_match or not bulk_match:
        raise RuntimeError(f"Could not parse release root/bulk release from {RELEASE_INDEX}")

    release_root = Path(root_match.group(1))
    family_dirs: dict[str, Path] = {}
    for family, folder in re.findall(r"\| ([A-Z0-9_]+) \| `([^`]+)` \|", text):
        family_dirs[family] = release_root / folder
    return Path(bulk_match.group(1)), family_dirs


def sha_map(release_dir: Path) -> dict[str, str]:
    source = release_dir / "SHA256SUMS.txt"
    hashes: dict[str, str] = {}
    if not source.exists():
        return hashes
    for line in source.read_text(encoding="utf-8").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, path = parts
        hashes[str(Path(path.strip()))] = digest
    return hashes


def choose_file(files: list[Path], target: str, required_part: str | None = None) -> Path | None:
    if required_part:
        files = [path for path in files if required_part in path.parts]
    target_norm = norm(target)
    for path in files:
        if target_norm in norm(path.stem):
            return path
    return None


def artifact_target(product_name: str) -> str:
    return ARTIFACT_ALIASES.get(product_name, product_name.replace(" ", "_"))


def money(value: str) -> str:
    return f"${int(value):,}" if value and value.isdigit() else value


def price_by_sku(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["SKU"]: row for row in rows}


def base_row() -> dict[str, str]:
    return {field: "" for field in FIELDNAMES}


def output_row(**kwargs: str) -> dict[str, str]:
    row = base_row()
    row.update(kwargs)
    return row


def artifact_details(release_dir: Path, target: str, scope: str) -> dict[str, str]:
    files = sorted(path for path in release_dir.rglob("*") if path.suffix.lower() in {".dmg", ".pkg"})
    hashes = sha_map(release_dir)
    dmg = choose_file([path for path in files if path.suffix == ".dmg"], target, scope)
    pkg = choose_file([path for path in files if path.suffix == ".pkg"], target, scope)
    source = release_dir / "SHA256SUMS.txt"
    return {
        "Mac DMG Path": str(dmg) if dmg else "",
        "Mac DMG SHA256": hashes.get(str(dmg), "") if dmg else "",
        "Mac PKG Path": str(pkg) if pkg else "",
        "Mac PKG SHA256": hashes.get(str(pkg), "") if pkg else "",
        "SHA256 Source": str(source) if source.exists() else "",
    }


def build() -> list[dict[str, str]]:
    catalog = read_csv(CATALOG_CSV)
    price_rows = price_by_sku(read_csv(PRICE_CSV))
    bulk_dir, family_dirs = read_release_dirs()
    rows: list[dict[str, str]] = []

    family_products: dict[str, list[str]] = {}
    for item in catalog:
        family_products.setdefault(item["Primary family"], []).append(item["Name"])

    # Individual plugin products.
    individual_price = price_rows["DIH-INDIVIDUAL-STANDARD"]
    for item in catalog:
        family = item["Primary family"]
        release_dir = family_dirs[family]
        details = artifact_details(release_dir, artifact_target(item["Name"]), "Individual")
        gate = "READY_FOR_UPLOAD_URL" if details["Mac DMG Path"] and details["Mac PKG Path"] else "ARTIFACT_MATCH_NEEDED"
        rows.append(
            output_row(
                SKU=item["SKU"],
                Product=item["Name"],
                **{
                    "Offer Type": "Individual",
                    "Storefront Status": item["Storefront role"],
                    "Primary Family": family,
                    "Included Products": item["Name"],
                    "Count": "1",
                    "Launch Price": money(individual_price["Launch Price"]),
                    "Regular Price": money(individual_price["Regular Price"]),
                    "Manual Path": str(MANUAL_PATH),
                    "Download 1 Name": f"{item['Name']} Mac Installer",
                    "Release Gate Status": gate,
                    "Next Action": "Upload DMG/PKG to protected GoDaddy/WooCommerce storage and paste final download URL.",
                    "Notes": "Current release index artifact. Keep unpublished until download URL and product page are connected.",
                    **details,
                },
            )
        )

    # Primary family products.
    for family, products in family_products.items():
        sku = FAMILY_SKUS[family]
        price = price_rows[sku]
        release_dir = family_dirs[family]
        details = artifact_details(release_dir, family, "Families")
        gate = "READY_FOR_UPLOAD_URL" if details["Mac DMG Path"] and details["Mac PKG Path"] else "ARTIFACT_MATCH_NEEDED"
        rows.append(
            output_row(
                SKU=sku,
                Product=f"{family} Family",
                **{
                    "Offer Type": "Primary Family",
                    "Storefront Status": "Current primary family",
                    "Primary Family": family,
                    "Included Products": ", ".join(products),
                    "Count": str(len(products)),
                    "Launch Price": money(price["Launch Price"]),
                    "Regular Price": money(price["Regular Price"]),
                    "Manual Path": str(MANUAL_PATH),
                    "Download 1 Name": f"{family} Mac Family Installer",
                    "Release Gate Status": gate,
                    "Next Action": "Upload family DMG/PKG to protected GoDaddy/WooCommerce storage and paste final download URL.",
                    "Notes": "Family package matches the current release index.",
                    **details,
                },
            )
        )

    # Workflow bundles, complete collection, download, and membership offers.
    for sku, price in price_rows.items():
        offer_type = price["Product Type"]
        if offer_type in {"Individual", "Primary Family"}:
            continue

        included = price["Includes"]
        product = price["Offer"]
        details = {}
        windows_path = ""
        windows_sha = ""
        gate = "PACKAGE_ASSEMBLY_NEEDED"
        next_action = "Create exact protected download package, then paste final WooCommerce download URL."
        notes = "Workflow bundle does not yet have a dedicated bundle installer in the current release index."

        if sku in WORKFLOW_TO_FAMILY:
            family = WORKFLOW_TO_FAMILY[sku]
            details = artifact_details(family_dirs[family], family, "Families")
            gate = "READY_FOR_UPLOAD_URL"
            next_action = "Use matching family installer as fulfillment, then paste final WooCommerce download URL."
            notes = "Workflow bundle is identical to a current primary family package."
        elif sku == "DIH-COMPLETE-COLLECTION":
            details = artifact_details(bulk_dir, "ALL_FAMILIES_Complete", "Bulk")
            windows_path = str(WINDOWS_INSTALLER)
            windows_sha = WINDOWS_SHA256
            gate = "READY_FOR_UPLOAD_URL"
            next_action = "Upload Mac bulk installer and Windows installer to protected storage; attach both customer downloads."
            notes = "Mac all-family bulk package plus Windows x64 VST3 bulk installer are current release artifacts."
        elif sku == "DIH-BETTER-BUSES":
            gate = "DOWNLOAD_PACKAGE_NEEDED"
            next_action = "Export final Better Buses ZIP and choose free, gated, or paid delivery rules."
            notes = "Lead magnet/tutorial package, not an audio plugin installer."
        elif offer_type == "Membership":
            details = artifact_details(bulk_dir, "ALL_FAMILIES_Complete", "Bulk")
            windows_path = str(WINDOWS_INSTALLER)
            windows_sha = WINDOWS_SHA256
            gate = "TERMS_NEEDED"
            next_action = "Approve lifetime terms, update license/customer-account rules, then attach Complete Collection downloads."
            notes = "Use Complete Collection artifacts as the first entitlement; future-release terms still need approval."

        rows.append(
            output_row(
                SKU=sku,
                Product=product,
                **{
                    "Offer Type": offer_type,
                    "Storefront Status": price["Notes"],
                    "Primary Family": WORKFLOW_TO_FAMILY.get(sku, "MULTI_FAMILY" if offer_type != "Download" else ""),
                    "Included Products": included,
                    "Count": price["Count"],
                    "Launch Price": money(price["Launch Price"]),
                    "Regular Price": money(price["Regular Price"]),
                    "Manual Path": str(MANUAL_PATH) if offer_type != "Download" else "",
                    "Download 1 Name": f"{product} Installer" if offer_type != "Download" else "DIHWorld Better Buses ZIP",
                    "Windows Installer Path": windows_path,
                    "Windows SHA256": windows_sha,
                    "Release Gate Status": gate,
                    "Next Action": next_action,
                    "Notes": notes,
                    **details,
                },
            )
        )

    return rows


def main() -> None:
    rows = build()
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
