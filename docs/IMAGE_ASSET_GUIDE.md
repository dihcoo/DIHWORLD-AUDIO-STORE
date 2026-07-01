# DIHWorld Audio Image Asset Guide

Source asset pack:

`/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/assets/source/_image_cache.zip`

Generated manifest:

`/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/image-cache-manifest.csv`

## Manifest Summary

The source zip contains the full launch image cache. The storefront should upload assets in controlled batches, starting with the Core Bundle and brand images.

| Status | Meaning |
| --- | --- |
| launch-ready | Use in the first storefront draft upload. |
| future-catalog | Valid current-canon asset, but not part of the first media pass. |
| review-before-upload | Legacy, alternate, reference, or non-current names. Review before using publicly. |

## Launch-Ready Uploads

Use these for the first WordPress media upload pass:

| File | Use |
| --- | --- |
| `DIHWorld_Audio_Logo.jpg` | Site logo, favicon, brand card. |
| `DIH_World_Audio Disk Image.PNG` | Homepage hero and brand background. |
| `SacredVerb_SacredVerb.png` | SacredVerb product hero/gallery image. |
| `Cathedral_Cathedral.png` | Cathedral product hero/gallery image. |
| `DEBO_debo.png` | DEBO product hero/gallery image. |
| `DRUMKRUSHGLUE_DrumKrushGlue.png` | DrumKrushGlue product hero/gallery image. |
| `MARIANA_Mariana.png` | Mariana product hero/gallery image. |

## Future-Catalog Assets

These are valid current-canon assets for later product or bundle pages:

| File | Use |
| --- | --- |
| `APIS_background_stripped.png` | APIS product image. |
| `NTRPL_ntrpl.png` | NTRPL product image. |
| `PLATINUM_platinum_bg.png` | Platinum mastering product image. |
| `NTRSTLLR_NTRSTLLR.png` | NTRSTLLR spatial product image. |

## Retired / Review Assets

Use NSR naming in current public copy and only upload a current NSR visual asset when one is available for the storefront media library.

Review-before-upload assets include:

- `ACCHORD_ACRD_Background.png`
- `AEGIS_aegis.png`
- `DIHV2_Dih.png`
- `EXCAVATOR_Excavator.png`
- `HEKA_Heka2.png`
- `IMPACTFX_impactfx.jpg`
- `IMPACTFX_train.png`
- `INVERSEIMPACT_InverseImpact.png`
- `NEBULA_Nebula_BG_Direction_01.png`
- `OBELISK_Obelisk_BG_Direction_01.png`
- `OSIRIS_Osiris_BG_Direction_01.png`
- `PARALUXE_PARALUXE.png`
- `RA_ra_touch_bg.png`
- `URA_URA_ice_Friz_reference.png`
- `WORMHOLE_Wormhole_BG_Direction_01.png`

## WordPress Upload Order

1. Upload only the launch-ready brand and Core Bundle assets first.
2. Attach SacredVerb, Cathedral, DEBO, DrumKrushGlue, and Mariana images to their WooCommerce draft products.
3. Keep NSR artwork pending until the storefront has a current NSR asset.
4. Keep APIS, NTRPL, Platinum, and NTRSTLLR images for future catalog or companion bundle drafts.
5. Use `image-cache-manifest.csv` when expanding the full catalog, so future upload batches stay aligned to current family names.
6. Avoid uploading `__MACOSX` files, `.DS_Store`, duplicate alternates, or legacy/reference assets.
