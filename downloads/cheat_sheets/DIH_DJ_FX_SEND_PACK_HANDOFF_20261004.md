# DIHWorld Audio — DJ FX Send Pack Handoff

**Release:** 2026-10-04  
**Audience:** DJs, club engineers, mobile DJs, and producers preparing DJ-ready returns  
**Status:** Current send/return workflow; category/preset delivery blueprint; DIH Live is future scope

## Executive summary

This pack defines the current DJ workflow for DIHWorld Audio. DJs use the effect-send and effect-return paths already exposed by their DJ mixer, controller, interface, or host. A dry deck path stays in the mixer while a DIHWorld plugin processes a dedicated return. The result is hands-on, tempo-aware DJ control without claiming direct Serato, Rekordbox, Traktor, or DIH Live integration.

The pack contains a public routing guide, a starter preset list, a machine-readable category catalog, and this implementation handoff. The category names and single-return entries are the delivery contract; they are not advertised as factory-installed presets until each plugin passes the verification checklist.

## Product boundary

- **Available now:** DJ mixer effect sends, plugin returns, return-level automation, and pre-rendered stem preparation.
- **Not available yet:** DIH Live, direct DJ-software integration, automatic deck discovery, or a proprietary controller protocol.
- **Safe language:** “Use DIHWorld Audio through your DJ system’s effect send/return path.”
- **Avoid:** Promising a one-click Serato, Rekordbox, Traktor, or standalone DJ integration before that product exists.

## What the DJ needs

- A DJ mixer/controller with an FX send/return or external effects loop.
- A Mac and a host that can load AU or VST3 effects on live input (Logic Pro or Ableton Live are suitable examples).
- An audio interface with at least two inputs and two outputs, plus the correct Core Audio driver.
- Two stereo cable pairs, unless the mixer exposes the send/return over multichannel USB.

## Reference routing

`Deck A/B → DJ mixer FX Send → DIHWorld plugin return → DJ mixer FX Return → master`

The mixer remains the source of the dry signal. The return is an effects-only lane. If a host inserts the plugin directly on a deck, use the plugin’s mix control conservatively and compare against the dry deck; a send-return setup is the preferred live workflow.

### Logic Pro setup

1. Connect the mixer FX Send to interface inputs 1–2 and interface outputs 1–2 to the mixer FX Return.
2. Start with a 128-sample buffer (64 if the computer remains stable).
3. Create a stereo audio track, choose inputs 1–2, enable input monitoring, and route its output to the return pair.
4. Insert one DIH plugin, load a DJ RETURN category entry when its verification is complete, or set Mix to 100% wet.
5. Set the mixer return to unity, then raise the channel FX send.

Ableton Live uses the same topology: a monitored audio track with the send pair as input and the return pair as output. Never assign the FX Return back into the FX Send; that creates a feedback loop.

### Level, latency, and tempo

- Aim for interface input peaks around **–12 to –6 dBFS**; never hit 0 dBFS.
- At 48 kHz, 64 samples is about 2.7 ms round trip before converter time; 128 is about 5.3 ms. Reverb and movement returns tolerate this well.
- The Mac does not automatically know the deck BPM. Use free-time millisecond settings, a plugin tap tempo when available, or set the host tempo manually.

## Send-friendly return roles

| Return job | Recommended plugin | Starting point | Guardrail |
| --- | --- | --- |
| Vocal throw / transition tail | SACREDVERB | 100% wet, short-to-medium decay, conservative return | Keep the dry vocal in the deck path |
| Wide break / stereo lift | PARALLAX | Moderate width and depth, wet return | Check mono and front-to-back focus |
| Spatial movement | NSR or NTRSTLLR | Moderate motion, return-only | Avoid extreme width on a crowded club system |
| Source-position / vocal movement | EchoLocate | Wet return, automate the send | Keep the source intelligible before the throw |
| Spectral movement | TEHUTI | Use only when a separate key/sidechain is available | Detector information must not replace the dry path |

Start with one processor per return. A two-plugin return is the upper limit for a first live pass; keep the chain short enough that a DJ can troubleshoot it during a transition.

## Preset category architecture

The DJ delivery should not force a user to browse all 42 plugins. It uses two layers:

1. **Plugin-specific DJ categories** keep the controls and language honest for the plugin’s real job.
2. **DJ FX RETURN / SINGLE PLUGIN** is a host-facing bank of six safe first-return choices. Each entry loads one plugin, so the DJ can work from one return lane without learning a multi-plugin chain.

| Category | Plugins | Delivery |
| --- | --- | --- |
| DJ RETURN / SPACE | SACREDVERB, PARALLAX | One wet return per plugin |
| DJ RETURN / MOTION | NSR, NTRSTLLR, EchoLocate | One wet return per plugin |
| DJ RETURN / KEYED SPECTRAL | TEHUTI | One return; external key optional |
| DJ PREP / INSERT OR STEM | OTIS, ANUBIS, MARIANA, MONOLITH, DrumKrushGlue, MAAT, SPHYNX, PLATINUM, IMHOTEP | Insert, family bus, or prepared stem |

The machine-readable catalog shipped with this pack is `DIH_DJ_FX_SEND_PRESET_CATALOG_20261004.json`. It is the implementation contract for the preset browser, installer, and future host templates: category, eligible plugin, wet default, send-control behavior, and safety checks live in one place.

### Single-return bank

- `DJ VOCAL THROW` → SACREDVERB
- `TRANSITION SPACE` → EchoLocate
- `WIDE BREAK` → PARALLAX
- `DEEP RETURN` → NSR
- `CLUB SAFE FX` → SACREDVERB
- `DRY/WET CUT` → NTRSTLLR

The single-return bank is intentionally a delivery layer, not a new audio processor. It tells the host or installer which existing plugin preset belongs on the return and prevents unsupported multi-plugin assumptions.

## Verification gate

Before a category entry is promoted to a factory preset, test that plugin individually with a dry source and a mixer-style return:

- input and output pairs pass signal without a feedback loop;
- the effect is truly wet-only at the return default;
- return at unity and send level changes produce the intended intensity change;
- no unexpected low-end widening or mono collapse occurs;
- latency is acceptable for a transition;
- preset recall restores the routing-safe values without a click or level jump.

Until those checks pass, the entry remains a catalog/host-template definition rather than a shipped factory program.

## Insert and stem roles

These are better suited to an insert, family bus, or pre-rendered stem than to an always-on DJ return:

- **OTIS** — dynamics guard and gain-match discipline.
- **ANUBIS** — controlled dynamics or character processing.
- **MARIANA** — bass-field/sub-pressure shaping.
- **MONOLITH** — foundation and weight preparation.
- **DrumKrushGlue** — drum-bus cohesion.
- **MAAT** — corrective balance and mastering-core verification.
- **SPHYNX** — density and field shaping.
- **PLATINUM** — finishing and ceiling control.
- **IMHOTEP** — final architecture and master-building decisions.

Prepare these in advance when possible. Live DJ returns should remain obvious, reversible, and low-risk.

## DJ starter workflows

### Transition throw

1. Put SACREDVERB on a dedicated return and set it 100% wet.
2. Keep the dry deck audible in the mixer.
3. Raise the send for the last vocal, stab, or phrase.
4. Pull the send back before the next downbeat; leave the return at unity.

### Vocal lift and space

Use EchoLocate or SACREDVERB on a return. Automate the send rather than riding the plugin output. Keep the source centered and intelligible before increasing the effect.

### Width break

Use PARALLAX on a return for a controlled break or intro. Check mono, use moderate width, and avoid widening the low end. Return-level control should be the DJ’s main performance control.

### Club-safe FX

Use SACREDVERB or PARALLAX with a conservative output ceiling and matched return level. Compare the effect engaged and bypassed at similar loudness. If the return changes the perceived punch more than the intended space, reduce the send.

### Stem preparation

Use OTIS, MARIANA, MONOLITH, MAAT, or PLATINUM before exporting a DJ stem. Print a clean dry reference and a processed reference so the DJ can choose the right version in the moment.

## Technical rules

- Return plugins are **100% wet** unless a specific guide says otherwise.
- The dry deck remains authoritative; never hide it behind a wet-only return.
- Keep the return fader at unity during setup. Use the mixer send for performance intensity.
- Use one processor per return initially; two maximum for a live first pass.
- Use sidechain only when the host exposes a separate key input. A detector path is control information, not a replacement for the source.
- Match perceived level before judging “better.” A louder return is not automatically a better return.
- Check mono compatibility and correlation before a club set, especially with PARALLAX, NSR, and NTRSTLLR.
- Keep output trim conservative and leave headroom for the mixer and PA.
- Treat latency as part of the return design. Prefer low-latency settings for rhythmic throws and transitions.
- Save the session and plugin state so a closed DJ session can be reopened without rebuilding the return routing.

## Starter preset taxonomy

- `DJ VOCAL THROW` — SACREDVERB, 100% wet, short/medium decay.
- `TRANSITION SPACE` — SACREDVERB or EchoLocate, wet return, send automation.
- `WIDE BREAK` — PARALLAX, moderate width/depth, mono check required.
- `DEEP RETURN` — SACREDVERB or NSR, low-risk return, conservative ceiling.
- `CLUB SAFE FX` — SACREDVERB/PARALLAX, matched level and restrained spread.
- `DRY/WET CUT` — any send-friendly return, host automation on the send only.

## Implementation checklist

- [x] Publish a DJ-facing routing guide in the website Cheat Sheets section.
- [x] Publish this detailed handoff PDF.
- [x] Publish starter preset definitions for the first DJ return bank.
- [x] Publish a machine-readable category catalog for plugin-specific and single-return delivery.
- [ ] Add the category metadata to each relevant plugin's factory preset browser without renaming existing non-DJ presets.
- [ ] Add a host template that creates one return lane and loads the selected single-return entry.
- [ ] Verify each send-friendly plugin individually against the return checklist before promoting its category to factory content.
- [ ] Build and audition the six starter presets inside the current DIHWorld plugin builds.
- [ ] Test one return at a time in Logic and one external DJ mixer/interface path.
- [ ] Measure return latency, mono behavior, and matched-loudness behavior for each preset.
- [ ] Add screenshots or short demos after the live return tests are approved.
- [ ] Keep DIH Live and direct DJ-software integration in a separate future roadmap.

## Acceptance criteria

The pack is ready for public use when a DJ can load one return, hear the dry deck unchanged, raise the send for a transition, and return to dry without a level jump, unexpected low-end spread, or confusing plugin state. The guide must make the current boundary clear: this is a DJ-system send/return workflow, not DIH Live.

## Out of scope

- DIH Live development or release claims.
- Direct Serato, Rekordbox, Traktor, or controller integration.
- Automatic routing of every plugin into every DJ system.
- Unbounded multi-plugin live returns.
