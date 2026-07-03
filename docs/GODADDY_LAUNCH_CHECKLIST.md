# DIHWorld Audio GoDaddy Launch Checklist

## Hosting Direction

The handoff names GoDaddy Managed WordPress, WooCommerce, Stripe, PayPal, and analytics as the target stack. Build this storefront on WordPress + WooCommerce rather than GoDaddy Website Builder so the product catalog, customer accounts, digital downloads, manuals, and future licensing flow can grow cleanly.

## GoDaddy Account Setup

1. In GoDaddy, confirm DIHWorldAudio.com is attached to Managed WordPress or Managed Hosting for WooCommerce.
2. Open the WordPress admin dashboard from the GoDaddy product card.
3. Install or confirm WooCommerce is active.
4. Set the store address, currency, checkout pages, customer account pages, and email sender identity.
5. Connect Stripe and PayPal only after the product pages, refunds policy, terms, privacy policy, and support mailbox are ready.
6. Add analytics after the first draft pages exist, so page and checkout events have real destinations.

## WooCommerce Product Import

Use `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/woocommerce-core-system-draft.csv` as the first import for SacredVerb, Cathedral, DEBO, DrumKrushGlue, Mariana, and the DIH Core Bundle.

Keep `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/woocommerce-products-draft.csv` as the companion bundle and future-catalog planning CSV.

Import path in WordPress:

1. Go to `Products > All Products`.
2. Select `Import`.
3. Choose the CSV file.
4. Continue to column mapping.
5. Confirm `SKU`, `Name`, `Published`, `Short description`, `Description`, `Categories`, `Tags`, `Download limit`, and `Download expiry days` map correctly.
6. Run the importer.

The CSV intentionally sets products to draft using `Published = -1`. Prices are drafted in `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/dihworld-price-list-20260703.csv`; fulfillment status is drafted in `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/fulfillment-map-20260703.csv`.

Before publishing, add product images, protected installer download URLs, manual links, demos, and FAQs. Use the fulfillment map to verify release paths, SHA-256 values, manual attachment, and remaining publish blockers.

## Media Upload

Use `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/wordpress-media-upload-plan.csv` for the first WordPress media upload pass.

First-pass Core Bundle images:

- `DIHWorld_Audio_Logo.jpg`
- `DIH_World_Audio Disk Image.PNG`
- `SacredVerb_SacredVerb.png`
- `Cathedral_Cathedral.png`
- `DEBO_debo.png`
- `DRUMKRUSHGLUE_DrumKrushGlue.png`
- `MARIANA_Mariana.png`

The full image archive is staged at `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/assets/source/_image_cache.zip`, and its manifest is at `/Users/hakeemsalaam/Development/DIHWorldAudio_Storefront/data/image-cache-manifest.csv`.

## Product Page Content Blocks

Each Core Bundle plugin page should include:

- Hero image
- Overview
- Features
- Screenshots
- Audio demos
- Walkthrough video
- PDF manual
- Buy button
- Demo download
- FAQ

## Digital Delivery Gate

Do not connect final downloads until each installer is:

- Developer ID signed
- Apple notarized
- Stapled
- Gatekeeper verified
- Matched to the current release notes
- Matched to current family and product naming

## Customer Portal

The customer account area should eventually contain:

- Downloads
- Licenses
- Activations
- Manuals
- Updates
- Order history

## First Publish Order

1. Home page
2. Plugins catalog
3. SacredVerb
4. Cathedral
5. DEBO
6. DrumKrushGlue
7. Mariana
8. DIH Core Bundle
9. Demo Downloads
10. Support
11. Account
12. Tutorials
13. Better Buses tutorial/download page
14. Companion bundle draft pages
15. Future catalog drafts
