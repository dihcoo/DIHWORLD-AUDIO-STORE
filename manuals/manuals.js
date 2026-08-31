const familyNames = {
  VOCAL_MIC_SOURCE: "Vocal / Mic / Source",
  DYNAMICS_GUARD: "Dynamics / Guard",
  BASS_LOW_END: "Bass / Low End",
  DRUM_INSTRUMENT: "Drum / Instrument",
  COLOR_AMP_TAPE: "Color / Amp / Tape",
  HARMONICS_PITCH: "Harmonics / Pitch",
  FIELD_TONE_BALANCE: "Field / Tone / Balance",
  FX_SPATIAL: "FX / Spatial",
  MASTERING_CORE: "Mastering Core",
  MASTER_FIELD: "Master Field",
  CREATIVE_TRANSFORM: "Creative Transform",
  UTILITY_OBSERVATION: "Utility / Observation",
  DIMENSIONAL_IMPACT_MOVE: "Dimensional / Impact / Move",
};

const chapters = [
  ["overview", "Overview"], ["flow", "Signal Flow"], ["controls", "Controls"],
  ["meters", "Meters"], ["presets", "Presets"], ["workflows", "Workflows"],
  ["daw", "DAW Setup"], ["documents", "Documents"], ["troubleshooting", "Troubleshooting"],
];

const sidechainIllustrations = {
  ANUBIS: "illustrations/ANUBIS_SIDECHAIN_ROUTING.png",
  TEHUTI: "illustrations/TEHUTI_SIDECHAIN_ROUTING.png",
  MARIANA: "illustrations/MARIANA_SIDECHAIN_ROUTING.png",
  MONOLITH: "illustrations/MONOLITH_SIDECHAIN_ROUTING.png",
  NTRPL: "illustrations/NTRPL_SIDECHAIN_ROUTING.png",
  DRUMKRUSHGLUE: "illustrations/DRUMKRUSHGLUE_SIDECHAIN_ROUTING.png",
};

const specialFlows = {
  DIH_DRUM_MORPHER: ["MIDI / PAD TRIGGER", "SAMPLE · HYBRID · SYNTH ENGINE", "PAD ENVELOPE & MORPH", "SEQUENCER / PERFORMANCE", "DIH FIELD & GOVERNOR", "STEREO OUTPUT"],
  TEHUTI: ["MAIN INPUT", "SIDECHAIN DETECTOR", "3-BAND SPLITTER", "ENVELOPE FOLLOWERS", "GAIN REDUCTION", "FLOWER ENGINE", "MIX", "OUTPUT"],
  ANUBIS: ["MAIN / KEY INPUT", "THRESHOLD", "ATTACK", "HOLD", "RELEASE", "EXPANSION CURVE", "DYNAMICS GUARD", "TRANSPARENT PASS", "OUTPUT"],
};

const specialWorkflows = {
  DIH_DRUM_MORPHER: [
    "Start from PHI CALI MOOG BASS for a tight bass-led pocket, or PHI DREAM SYNTH for a spacious synthetic drum field.",
    "Use the calibrated note shown in the upper-left of the target pad when programming or playing MIDI.",
    "SOLO sits directly under each note: when any pad is soloed, all non-soloed pads are muted.",
    "Sample plays loaded audio only; Hybrid blends loaded audio and the model; Synth is model-forward and plays without a loaded sample.",
    "After choosing the engine, refine Pitch, Morph, Decay and Release in the complete groove.",
  ],
  TEHUTI: [
    "Kick → bass: insert on bass, route kick to Side Chain, begin with Low Duck and moderate Depth.",
    "Vocal → music: insert on the music bus, route the lead vocal, favor Mid Duck for intelligibility.",
    "Guitar → pads: use Mid and High Duck with slower Speed for transparent harmonic space.",
    "EDM pumping: raise Depth and Speed, then blend with Mix; Flower adds coordinated harmonic motion.",
    "Mastering: use shallow band values, low Depth, Gain Match, and verify that the tonal center remains stable.",
  ],
  ANUBIS: [
    "Drum cleanup: shorten Attack enough to preserve the transient, use Hold to prevent chatter, then set Range.",
    "Vocal noise control: use gentle Ratio and Range before lowering Threshold.",
    "Guitar tightness: use fast Attack, moderate Hold, and a Release that follows the performance.",
    "Room microphone gating: preserve ambience with a longer Hold and Release; avoid a full hard-gate Range.",
    "Sidechain ducking: route the key signal, enable Duck, and leave Key optional when the key should not open the gate.",
  ],
};

const specialTroubleshooting = {
  DIH_DRUM_MORPHER: [
    "A pad is silent: clear any active SOLO buttons to restore the full kit.",
    "Sample mode needs audio loaded on that pad; select Hybrid or Synth for model-generated sound without a sample.",
    "If MIDI triggers the wrong pad, use the calibrated note printed in the target pad’s upper-left corner.",
    "For synth voice length, adjust the pad Decay and Release rather than stretching a sample.",
  ],
  TEHUTI: [
    "No sidechain activity: select the sending track in the host Side Chain menu and confirm SIDECHAIN SEND moves.",
    "No reduction: enable Power, raise a band Duck control and Depth, and verify nonzero sidechain energy.",
    "Pumping: reduce Depth, slow Speed, or reduce the most active band.",
    "Level mismatch: enable Gain Match and compare at equal loudness.",
  ],
  ANUBIS: [
    "Gate chatters: increase Hold or Release, or lower Ratio.",
    "Transients disappear: slow Attack slightly and reduce Range.",
    "Key meter is idle: route the external sidechain and enable Key when it should drive the detector.",
    "Unexpected ducking: Key and Duck are independent—disable Duck if the sidechain should only open the gate.",
  ],
};

let plugins = [];
let selected = null;
let activeChapter = "overview";

const list = document.querySelector("#plugin-list");
const search = document.querySelector("#manual-search");
const familyFilter = document.querySelector("#family-filter");
const resultCount = document.querySelector("#result-count");
const chapterContent = document.querySelector("#chapter-content");

const escapeHtml = (value = "") => String(value).replace(/[&<>'"]/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
}[char]));
const familyLabel = (family) => familyNames[family] || family.replaceAll("_", " ");
const visualPath = (plugin) => `plugins/${encodeURIComponent(plugin.id)}.jpg`;
const manualPath = (family, kind) => `docs/families/${family}/${family}_${kind}_MANUAL.pdf`;

function controlGuidance(parameter) {
  const id = parameter.id.toLowerCase();
  if (id.includes("gainmatch")) return "Maintains a level-fair comparison between processed and bypassed signal.";
  if (id.includes("mix")) return "Blends the processed path with the unprocessed source.";
  if (id.includes("output")) return "Sets final level after processing; use it for matching, not effect intensity.";
  if (id.includes("input")) return "Sets or reports the signal entering the processor.";
  if (parameter.type === "Bool") return "Touch control: toggle the function on or off.";
  if (parameter.type === "Choice") return "Selects a discrete operating mode stored with the session.";
  return "Adjust from reset in small moves, then verify in context and at matched loudness.";
}

function filteredPlugins() {
  const needle = search.value.trim().toLowerCase();
  return plugins.filter((plugin) =>
    (familyFilter.value === "ALL" || plugin.family === familyFilter.value) &&
    (!needle || plugin.name.toLowerCase().includes(needle) || plugin.description.toLowerCase().includes(needle) ||
      plugin.parameters.some((parameter) => parameter.name.toLowerCase().includes(needle)))
  );
}

function renderList() {
  const filtered = filteredPlugins();
  resultCount.textContent = `${filtered.length} of ${plugins.length} plugins`;
  list.innerHTML = filtered.length ? filtered.map((plugin) => {
    const canonicalIndex = plugins.findIndex((item) => item.id === plugin.id) + 1;
    return `<button class="plugin${selected?.id === plugin.id ? " active" : ""}" data-plugin="${escapeHtml(plugin.id)}">
      <span>${String(canonicalIndex).padStart(2, "0")}</span><div><strong>${escapeHtml(plugin.name)}</strong><small>${escapeHtml(familyLabel(plugin.family))}</small></div>
    </button>`;
  }).join("") : `<p class="empty">No plugin or control matches that search.</p>`;
}

function setPlugin(id, scroll = true) {
  selected = plugins.find((plugin) => plugin.id === id) || plugins[0];
  activeChapter = "overview";
  const url = new URL(window.location.href);
  url.searchParams.set("plugin", selected.id);
  history.replaceState({}, "", url);
  renderList();
  renderManual();
  if (scroll) document.querySelector(".manual-title").scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderManual() {
  document.querySelector("#plugin-family").textContent = familyLabel(selected.family);
  document.querySelector("#plugin-name").textContent = selected.name;
  document.querySelector("#plugin-description").textContent = selected.description;
  document.querySelector("#plugin-badges").innerHTML = [`v${selected.version}`, ...selected.formats, selected.placement]
    .map((badge) => `<span>${escapeHtml(badge)}</span>`).join("");
  document.querySelector("#chapter-nav").innerHTML = chapters.map(([id, label]) =>
    `<button data-chapter="${id}" class="${activeChapter === id ? "active" : ""}">${label}</button>`).join("");
  renderChapter();
}

function chapterFrame(number, eyebrow, title, body) {
  return `<section class="chapter"><div class="chapter-number">${number}</div><div><p class="eyebrow">${eyebrow}</p><h3>${title}</h3>${body}</div></section>`;
}

function renderChapter() {
  const name = escapeHtml(selected.name);
  if (activeChapter === "overview") {
    chapterContent.innerHTML = chapterFrame("01", "INTRODUCTION", `What ${name} does`, `
      <p>${escapeHtml(selected.description)}</p>
      <figure class="plugin-hero"><img src="${visualPath(selected)}" alt="${name} plugin interface"><figcaption><strong>${name}</strong><span>${escapeHtml(familyLabel(selected.family))} · interface reference</span></figcaption></figure>
      <div class="fact-grid">
        <div><span>Preferred placement</span><strong>${escapeHtml(selected.placement)}</strong></div>
        <div><span>Parameters</span><strong>${selected.parameters.length}</strong></div>
        <div><span>Factory presets</span><strong>${selected.presets.length}</strong></div>
        <div><span>Gain Match</span><strong>${selected.gainMatch ? "Included" : "Not exposed"}</strong></div>
        <div><span>Sidechain</span><strong>${selected.sidechain ? "Supported" : "Main input"}</strong></div>
        <div><span>Channel modes</span><strong>${selected.channelMode ? "Selectable" : "Host managed"}</strong></div>
      </div>
      <div class="canon-note"><strong>DIH operating law</strong><p>Begin from Canon Reset or a purpose-matched preset. Compare at equal loudness, adjust one system at a time, and judge the result in the full arrangement—not in solo alone.</p></div>`);
  } else if (activeChapter === "flow") {
    const flow = specialFlows[selected.id] || ["INPUT", "CORE ENGINE", "HARMONIC CONTROL", "MIX", "OUTPUT"];
    const illustration = sidechainIllustrations[selected.id] ? `<figure class="routing"><img src="${sidechainIllustrations[selected.id]}" alt="${name} sidechain routing diagram"><figcaption>Cyan marks the host detector/key path. It controls the target processor and is not mixed into the audible output.</figcaption></figure>` : "";
    chapterContent.innerHTML = chapterFrame("02", "SIGNAL FLOW", "From source to output", `<div class="flow">${flow.map((stage, index) => `<div><span>${String(index + 1).padStart(2, "0")}</span><strong>${escapeHtml(stage)}</strong></div>`).join("")}</div>${illustration}<p class="fineprint">${selected.sidechain ? "The external sidechain is a detector/control path and is not mixed into the audible output." : "The host provides the main program signal; internal stages remain bounded by the plugin’s protected output behavior."}</p>`);
  } else if (activeChapter === "controls") {
    chapterContent.innerHTML = chapterFrame("03", "INTERFACE TOUR", "Every exposed control", `<figure class="reference-shot"><img src="${visualPath(selected)}" alt="${name} plugin interface"><figcaption>${name} · current visual reference</figcaption></figure><div class="control-grid">${selected.parameters.map((parameter, index) => `<div class="control-card"><span>${String(index + 1).padStart(2, "0")}</span><div><h4>${escapeHtml(parameter.name)}</h4><code>${escapeHtml(parameter.id)}</code><p>${escapeHtml(controlGuidance(parameter))}</p></div><b>${escapeHtml(parameter.type)}</b></div>`).join("")}</div>`);
  } else if (activeChapter === "meters") {
    const body = selected.meters.length ? `<div class="meter-table">${selected.meters.map((meter) => `<div><strong>${escapeHtml(meter.display)}</strong><span>${escapeHtml(meter.measures)}</span><p>${escapeHtml(meter.reading)}</p></div>`).join("")}</div>` : `<div class="canon-note">No nonstandard reactive display requires a separate interpretation guide. Standard host and input/output meters retain their conventional meaning.</div>`;
    chapterContent.innerHTML = chapterFrame("04", "ANALYZER & METERING", "Read the interface correctly", `${body}<p class="fineprint">Meters observe; they do not improve audio by themselves. Bypass-match, check mono where relevant, and investigate sustained warnings before changing controls.</p>`);
  } else if (activeChapter === "presets") {
    const body = selected.presets.length ? `<ol class="preset-list">${selected.presets.map((preset, index) => `<li><span>${String(index).padStart(2, "0")}</span><strong>${escapeHtml(preset)}</strong><p>Load, level-match, then refine the primary controls for the source and arrangement.</p></li>`).join("")}</ol>` : `<div class="canon-note">No named factory preset list is currently published for this processor. Use Reset and the parameter map as your starting point.</div>`;
    chapterContent.innerHTML = chapterFrame("05", "FACTORY PRESETS", "Purpose-built starting points", body);
  } else if (activeChapter === "workflows") {
    const fallback = [`Insert ${selected.name} at its recommended ${selected.placement.toLowerCase()} position.`, "Load Canon Reset or the closest factory preset and establish level-matched bypass.", `Use ${selected.parameters.slice(0, 3).map((p) => p.name).join(", ")} to shape the result.`, "Automate only after the static sound works in the full arrangement."];
    const items = specialWorkflows[selected.id] || fallback;
    chapterContent.innerHTML = chapterFrame("06", "PROFESSIONAL WORKFLOWS", "Put it to work", `<div class="workflow-list">${items.map((item, index) => `<div><span>${index + 1}</span><p>${escapeHtml(item)}</p></div>`).join("")}</div>`);
  } else if (activeChapter === "daw") {
    const daws = [["Logic Pro", "Insert Audio Units → DIHWorld Audio. Select the key source from the plug-in header Side Chain menu when required."], ["Pro Tools", "Insert using the supported host format, then assign the key input from the plug-in key menu."], ["Cubase", "Insert the VST3, activate Side-Chain, then add a send from the key track."], ["Studio One", "Insert the VST3 and choose the source from the Sidechain selector."], ["Ableton Live", "Insert the VST3, unfold routing, enable Sidechain, and choose the source."], ["Reaper", "Insert the VST3, route key audio to channels 3/4, and expose the auxiliary input pins."], ["FL Studio", "Load the VST3, assign a mixer sidechain route, and select the input in the wrapper Processing tab."]];
    chapterContent.innerHTML = chapterFrame("07", "DAW SETUP", "Routing in major hosts", `<div class="daw-grid">${daws.map(([daw, instruction]) => `<div><strong>${daw}</strong><p>${instruction}</p></div>`).join("")}</div>`);
  } else if (activeChapter === "documents") {
    const label = escapeHtml(familyLabel(selected.family));
    chapterContent.innerHTML = chapterFrame("08", "FAMILY DOCUMENTS", `${label} downloads`, `<p>The customer manual is the primary companion for ${name}. The technical manual preserves advanced implementation and support detail.</p><div class="document-cards"><a class="primary" href="${manualPath(selected.family, "USER")}" target="_blank" rel="noopener"><span>PDF · CUSTOMER MANUAL</span><strong>${label}</strong><p>Use cases, controls, signal flow, presets, and practical operation.</p><b>Open user manual in new tab ↗</b></a><a href="${manualPath(selected.family, "TECHNICAL")}" target="_blank" rel="noopener"><span>PDF · ADVANCED / SUPPORT</span><strong>Technical Manual</strong><p>Engineering-facing behavior, implementation notes, and deeper reference.</p><b>Open technical manual in new tab ↗</b></a></div><div class="related-docs"><a href="docs/templates/42_PLUGIN_PLACEMENT_SCHEMATIC.pdf" target="_blank" rel="noopener">PDF · 42-plugin placement schematic ↗</a><a href="docs/guides/PLUGIN_CATEGORY_CHEAT_SHEET.pdf" target="_blank" rel="noopener">PDF · Plugin category cheat sheet ↗</a><a href="docs/guides/BETTER_BUS_MAP.pdf" target="_blank" rel="noopener">PDF · Better Bus map ↗</a></div>`);
  } else {
    const generic = ["No sound: confirm the plug-in is enabled, the source reaches the insert, and Output is not fully reduced.", "No audible change: reset, raise one primary control deliberately, and compare using matched loudness.", "Unexpected image or phase change: return width, channel mode, and dual-mono controls to reset, then check mono.", "Session mismatch: confirm the current plug-in version and reload a current preset before rebuilding the setting."];
    const items = specialTroubleshooting[selected.id] || generic;
    chapterContent.innerHTML = chapterFrame("09", "TROUBLESHOOTING", "Fast checks before support", `<div class="workflow-list troubleshooting">${items.map((item, index) => `<div><span>${index + 1}</span><p>${escapeHtml(item)}</p></div>`).join("")}</div><div class="canon-note"><strong>Still need help?</strong><p>Record the host, operating system, plug-in format, version, track type, preset, and exact result before contacting support.</p><a href="../#support">Open DIHWorld Audio support</a></div>`);
  }
}

list.addEventListener("click", (event) => {
  const button = event.target.closest("[data-plugin]");
  if (button) setPlugin(button.dataset.plugin);
});
document.querySelector("#chapter-nav").addEventListener("click", (event) => {
  const button = event.target.closest("[data-chapter]");
  if (!button) return;
  activeChapter = button.dataset.chapter;
  renderManual();
  document.querySelector(".chapter").scrollIntoView({ behavior: "smooth", block: "start" });
});
search.addEventListener("input", renderList);
familyFilter.addEventListener("change", renderList);

fetch("plugin-data.json")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((data) => {
    plugins = data;
    [...new Set(plugins.map((plugin) => plugin.family))].forEach((family) => {
      familyFilter.insertAdjacentHTML("beforeend", `<option value="${family}">${escapeHtml(familyLabel(family))}</option>`);
    });
    const requested = new URLSearchParams(window.location.search).get("plugin");
    setPlugin(requested || "DEPTH_IMPACT_HYBRID_X", false);
  })
  .catch(() => {
    resultCount.textContent = "The manual data could not be loaded.";
    document.querySelector("#plugin-name").textContent = "Manual unavailable";
  });
