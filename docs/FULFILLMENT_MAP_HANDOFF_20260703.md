# DIHWorld Audio Fulfillment Map Handoff

Date: 2026-07-03

Primary file: `data/fulfillment-map-20260703.csv`

Generator: `tools/build_fulfillment_map.py`

## Purpose

This handoff connects every storefront offer to its operational fulfillment state: product SKU, price, included products, release artifact paths, SHA-256 checksums, customer manual, and the next action required before publishing in WooCommerce or GoDaddy.

## Source Authority

- Product catalog: `data/plugin-catalog-42-current-canon.csv`
- Price list: `data/dihworld-price-list-20260703.csv`
- Release index: `/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/CURRENT_RELEASE_INDEX.md`
- Current manual: `/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FAMILIES/DIHWorld_Audio_User_Manual_CURRENT.pdf`
- Windows bulk installer: `/Users/hakeemsalaam/Development/DIH_BUILDS/DIH_FINISHED/WINDOWS_RELEASE_20260702/DIHWorld_Audio_42_Plugin_Installer_Windows_x64.exe`

The map follows the current release index instead of selecting the newest folder by date. That protects the storefront while NTRSTLLR, DIHMOTION-related work, Mariana notes, or other repairs are still being handled.

## Row Counts

| Offer type | Rows | Fulfillment meaning |
|---|---:|---|
| Individual | 42 | Each individual plugin has current Mac DMG/PKG paths and checksums. |
| Primary Family | 13 | Each primary family has current Mac family DMG/PKG paths and checksums. |
| Workflow Bundle | 8 | Family-identical bundles can use existing family installers; composite bundles need exact package assembly. |
| Bulk | 1 | Complete Collection has Mac all-family installer paths plus the Windows x64 VST3 installer. |
| Download | 1 | Better Buses needs a final ZIP/export decision. |
| Membership | 3 | Lifetime offers can use Complete Collection artifacts, but terms and account rules still need approval. |

Total rows: 68

## Status Codes

| Status | Meaning | Action |
|---|---|---|
| `READY_FOR_UPLOAD_URL` | Release artifacts and checksums are available. | Upload to protected GoDaddy/WooCommerce storage and paste the final customer download URL. |
| `PACKAGE_ASSEMBLY_NEEDED` | The offer is a composite workflow bundle with no exact dedicated installer yet. | Decide whether to create a bundle archive/installer or deliver included single/family installers. |
| `DOWNLOAD_PACKAGE_NEEDED` | A non-plugin download needs its final ZIP or package. | Export the final Better Buses package and set free/gated/paid rules. |
| `TERMS_NEEDED` | The product is technically deliverable, but legal/customer entitlement language is not final. | Approve lifetime terms, license rules, and customer-account handling before publishing. |

## Publish Use

1. In WooCommerce, keep products unpublished until their row has a protected `Download 1 URL`.
2. Use `Mac DMG SHA256`, `Mac PKG SHA256`, and `Windows SHA256` as team verification values after upload.
3. Do not publish composite workflow bundles until the `PACKAGE_ASSEMBLY_NEEDED` decision is resolved.
4. Do not publish lifetime/legacy memberships until `TERMS_NEEDED` is resolved.
5. Rebuild the CSV after any release-index update:

```bash
python3 tools/build_fulfillment_map.py
```
