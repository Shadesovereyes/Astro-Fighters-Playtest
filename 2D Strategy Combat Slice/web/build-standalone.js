"use strict";
// Regenerates web/astro-fighters-standalone.html: a single self-contained copy of the
// V3.5 entry point with the seven runtime modules inlined, so it can be loaded directly
// on another device (remote play/testing) with no sibling files. Run: node build-standalone.js
const fs = require("fs");
const path = require("path");
const dir = __dirname + path.sep;
const ENTRY = "astro-fighters-2d-v3.4.html";
const MODULES = ["af-core.js", "af-dc-model-v3.js", "af-core-v3-patch.js", "af-ui-v3.js", "af-anim-map-v3.js", "af-sprites-v3.js", "af-page-v3.js", "af-map-v3.js", "af-progression-v3.js"];

let html = fs.readFileSync(dir + ENTRY, "utf8");
const inlined = MODULES.map(m => `<script>\n/* ${m} */\n` + fs.readFileSync(dir + m, "utf8") + `\n</script>`).join("\n");
// Replace the run of six external <script src="…"> tags with the inlined bundle.
let replaced = html.replace(/<script src="af-core\.js"><\/script>[\s\S]*?<script src="af-progression-v3\.js"><\/script>/, inlined);
if (replaced === html) { console.error("ERROR: could not find the module <script src> block to inline."); process.exit(1); }
if (/<script src="af-[^"]+\.js">/.test(replaced)) { console.error("ERROR: external module script tags remain after inlining."); process.exit(1); }

// --rig: inline the imported character rig (web/characters/male.json and its sheets, as data URIs) so the
// single file draws the sprite replay too; without it the arena keeps its glyph tokens.
let rigNote = "";
if (process.argv.includes("--rig")) {
  const def = JSON.parse(fs.readFileSync(dir + "characters/male.json", "utf8"));
  const files = {};
  const walk = v => { if (typeof v === "string" && /^characters\/.+\.png$/.test(v)) files[v] = "data:image/png;base64," + fs.readFileSync(dir + v).toString("base64");
    else if (v && typeof v === "object") Object.values(v).forEach(walk); };
  walk(def);
  const rig = `<script>\n/* character rig (playtest ${def.source && def.source.commit || "?"}) */\nwindow.AF_RIG=${JSON.stringify({ def, files })};\n</script>\n`;
  replaced = replaced.replace("<script>\n/* af-core.js */", rig + "<script>\n/* af-core.js */");
  if (!replaced.includes("window.AF_RIG=")) { console.error("ERROR: could not inline the rig."); process.exit(1); }
  rigNote = `, rig inlined (${Object.keys(files).length} sheets)`;
}

const out = dir + "astro-fighters-standalone.html";
fs.writeFileSync(out, replaced);
console.log(`wrote ${path.basename(out)} (${(replaced.length / 1024).toFixed(1)} KB, ${MODULES.length} modules inlined${rigNote})`);

// Optional: emit the same page as an Artifact-ready fragment. The Artifact host supplies its
// own <!doctype>/<html>/<head>/<body> skeleton, so the fragment is the <head> contents (minus
// the meta tags the host provides) followed by the <body> contents. Run: node build-standalone.js --artifact
if (process.argv.includes("--artifact")) {
  const head = replaced.slice(replaced.indexOf("<head>") + 6, replaced.indexOf("</head>")).replace(/<meta[^>]*\/?>/g, "");
  const body = replaced.slice(replaced.indexOf("<body>") + 6, replaced.lastIndexOf("</body>"));
  const fragment = head.trim() + "\n" + body.trim() + "\n";
  for (const tag of ["<!DOCTYPE", "<html", "</html>", "<head>", "</head>", "<body>", "</body>"]) {
    if (fragment.includes(tag)) { console.error(`ERROR: wrapper tag ${tag} survived the artifact transform.`); process.exit(1); }
  }
  const artifactOut = dir + "astro-fighters-artifact.html";
  fs.writeFileSync(artifactOut, fragment);
  console.log(`wrote ${path.basename(artifactOut)} (${(fragment.length / 1024).toFixed(1)} KB, Artifact-ready fragment)`);
}
