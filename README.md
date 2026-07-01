# DIHWorld Audio Storefront Package

This folder is the local build package for DIHWorldAudio.com.

## Files

- `index.html` - static storefront preview for the current 42-plugin suite and bundle strategy.
- `assets/images/` - storefront-ready preview images, including the Core Bundle product art.
- `assets/source/_image_cache.zip` - full source image cache archive copied from the launch package.
- `assets/css/styles.css` - responsive storefront styling.
- `assets/js/storefront.js` - product filtering.
- `data/woocommerce-core-system-draft.csv` - primary WooCommerce draft import for SacredVerb, Cathedral, DEBO, DrumKrushGlue, Mariana, and the DIH Core Bundle.
- `data/woocommerce-products-draft.csv` - companion bundle and future catalog draft import.
- `data/plugin-catalog-42-current-canon.csv` - current 42-plugin catalog reference for future imports.
- `data/image-cache-manifest.csv` - image-cache inventory with dimensions and upload status.
- `data/wordpress-media-upload-plan.csv` - first-pass media upload plan for WordPress.
- `docs/GODADDY_LAUNCH_CHECKLIST.md` - GoDaddy + WordPress launch sequence.
- `docs/WORDPRESS_CONTENT_GUIDE.md` - page copy and product copy for WordPress.
- `docs/CORE_SYSTEM_STOREFRONT_COPY.md` - paste-ready Core Bundle storefront copy.
- `docs/SOURCE_PRIORITY.md` - source-of-truth notes for current catalog categories.
- `docs/FULL_CATALOG_ROADMAP.md` - full 42-plugin expansion plan.
- `docs/BETTER_BUSES_TUTORIAL_PAGE.md` - tutorial/download page draft from the Better Buses archive.
- `docs/RELEASE_GATES.md` - current storefront release gate and publication safety rules.
- `docs/IMAGE_ASSET_GUIDE.md` - image upload guidance for the full source asset pack.

## Preview

Open `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/index.html` in a browser.

## Publish Path

The clean path is:

1. Provision GoDaddy Managed WordPress or Managed Hosting for WooCommerce.
2. Install or confirm WooCommerce.
3. Import `data/woocommerce-core-system-draft.csv` as the first draft product CSV.
4. Upload only the first-pass media assets from `data/wordpress-media-upload-plan.csv`.
5. Add prices, product images, final download URLs, manuals, audio demos, video, and FAQ.
6. Connect Stripe, PayPal, analytics, and customer account flows.
7. Publish only after final installer packages are signed, notarized, stapled, and Gatekeeper verified.
