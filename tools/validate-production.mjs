import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const read = (p) => fs.readFileSync(path.join(root, p), 'utf8');
const readJson = (p) => JSON.parse(read(p));

const manifest = readJson('production/asset-manifest.json');
const rubric = readJson('docs/data/art-review-rubric.json');
const docs = {
  readme: read('README.md'),
  agents: read('AGENTS.md'),
  master: read('ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md'),
  epe: read('IMPERIAL_CITY_EARLY_PLAYER_EXPERIENCE_V0.md'),
  status: read('DEVELOPMENT_STATUS.md'),
  rubricMd: read('Astro Fighters — Art Preview Review Rubric.md'),
  worldChecklist: read('Astro Fighters — Imperial City Zone-by-Zone Asset Checklist.md'),
  characterChecklist: read('ASTRO_FIGHTERS_CHARACTER_CLOTHING_ACCESSORY_CHECKLIST.md'),
  sliceBrief: read('production/SLICE_0_SOURCE_ART_BRIEF.md')
};

const errors = [];
const fail = (message) => errors.push(message);
const assert = (condition, message) => { if (!condition) fail(message); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const nonEmpty = (value) => typeof value === 'string' && value.trim().length > 0;
const positivePair = (value) => Array.isArray(value) && value.length === 2 && value.every((n) => Number.isInteger(n) && n > 0);

function unique(values, label) {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) fail(`${label} contains duplicate value: ${value}`);
    seen.add(value);
  }
}

function thresholdFor(code) {
  return rubric.thresholds.find((item) => item.code === code);
}

function section(markdown, startHeading, endHeading) {
  const start = markdown.indexOf(startHeading);
  if (start < 0) return '';
  const bodyStart = start + startHeading.length;
  const end = endHeading ? markdown.indexOf(endHeading, bodyStart) : -1;
  return markdown.slice(bodyStart, end >= 0 ? end : undefined);
}

function bulletLines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.slice(2).trim());
}

function validateRubric() {
  assert(rubric.version === 1, 'Rubric version must remain 1 until the review payload schema changes.');
  assert(rubric.maxScore === 50, 'Rubric maxScore must be 50.');
  assert(Array.isArray(rubric.categories) && rubric.categories.length === 10, 'Rubric must define exactly 10 scored categories.');
  assert(Array.isArray(rubric.automaticFailures) && rubric.automaticFailures.length > 0, 'Rubric must define automatic failures.');
  unique(rubric.categories.map((c) => c.id), 'Rubric category ids');
  unique(rubric.automaticFailures, 'Rubric automatic failures');

  const requiredCritical = new Map([
    ['homogeneity', 4],
    ['characterCompletion', 4],
    ['environmentQuality', 4],
    ['worldIdentity', 4],
    ['architecture', 4],
    ['projection', 4]
  ]);
  const critical = new Map(rubric.categories.filter((c) => c.critical).map((c) => [c.id, c.min]));
  for (const [id, minimum] of requiredCritical) {
    assert(critical.get(id) === minimum, `Critical rubric category ${id} must remain at minimum ${minimum}.`);
  }

  const screenshot = rubric.categories.find((c) => c.id === 'screenshot');
  assert(screenshot?.publicMinimum === 4, 'Gameplay Screenshot Readiness public minimum must be 4.');

  for (let total = 0; total <= rubric.maxScore; total += 1) {
    const matches = rubric.thresholds.filter((t) => total >= t.min && total <= t.max);
    assert(matches.length === 1, `Rubric thresholds must classify score ${total} exactly once.`);
  }

  assert(thresholdFor('rework-required')?.min === 30 && thresholdFor('rework-required')?.max === 36, 'Rework range must be 30–36.');
  assert(thresholdFor('conditional')?.min === 37 && thresholdFor('conditional')?.max === 41, 'Conditional range must be 37–41.');
  assert(thresholdFor('production-approved')?.min === 42, 'Production approval must begin at 42.');
  assert(thresholdFor('lock-quality')?.min === 46, 'Lock quality must begin at 46.');

  for (const phrase of [
    'Anatomical weapon or equipment routing',
    'Clothing layers incorrectly cover anatomy',
    'Modular isolates contain neighboring-item contamination',
    'Automatically reduced or segmented assets',
    'non-Phaser preview',
    'Fixed grid-step exploration'
  ]) {
    assert(rubric.automaticFailures.some((item) => item.includes(phrase)), `Machine rubric missing required blocker: ${phrase}`);
  }

  const humanFailures = bulletLines(section(docs.rubricMd, '## Automatic Failure Conditions', '---\n\n# Scored Review'));
  assert(same(humanFailures, rubric.automaticFailures), 'Human rubric automatic-failure bullets must exactly match docs/data/art-review-rubric.json.');
  assert(docs.rubricMd.includes('**30–36** | **REWORK REQUIRED**'), 'Human rubric must state 30–36 as REWORK REQUIRED.');
  assert(docs.rubricMd.includes('**37–41** | **CONDITIONAL**'), 'Human rubric must state 37–41 as CONDITIONAL.');
}

function validateAuthorityDocs() {
  assert(docs.readme.includes('**`main` is authoritative**'), 'README must identify main as authoritative.');
  assert(!docs.readme.includes('Until PR #11 is merged'), 'README contains stale pre-merge PR #11 wording.');
  assert(docs.status.includes('**Authoritative branch:** `main`'), 'Development Status must identify main as authoritative.');
  assert(!docs.status.includes('**Draft PR:** #11'), 'Development Status contains stale Draft PR #11 metadata.');
  assert(!docs.status.includes('**Working branch:** `development/art-review-workflow-v1`'), 'Development Status still points to the merged workflow branch.');

  const oldRangeDocs = [
    ['README', docs.readme],
    ['AGENTS', docs.agents],
    ['Master Art Direction', docs.master],
    ['EPE', docs.epe],
    ['Development Status', docs.status],
    ['Human Rubric', docs.rubricMd],
    ['World Checklist', docs.worldChecklist],
    ['Character Checklist', docs.characterChecklist]
  ];
  for (const [label, text] of oldRangeDocs) {
    assert(!text.includes('36–41'), `${label} contains obsolete 36–41 threshold language.`);
  }

  assert(!docs.epe.includes('- [ ]'), 'EPE must not duplicate completion state with checkboxes.');
  assert(docs.epe.includes('This document owns **route scope, production priority, composition requirements, and execution order**'), 'EPE must declare its scope/order role.');
  assert(docs.worldChecklist.includes('This file owns **world completion state**'), 'World checklist must declare completion-state ownership.');
  assert(docs.agents.includes('# Generation vocabulary discipline'), 'AGENTS must include generation-vocabulary discipline.');
  assert(docs.master.includes('# 2. Generation vocabulary discipline'), 'Master Art Direction must include generation-vocabulary discipline.');
  assert(docs.sliceBrief.includes('14 shared-foundation world dependencies'), 'Slice 0 brief must acknowledge the 14-asset package contract.');
  assert(docs.sliceBrief.includes('8-asset core subset'), 'Slice 0 brief must distinguish the 8-asset assembly subset.');
}

function validateCanonical() {
  const c = manifest.canonical || {};
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const layers = ['ground', 'decals', 'architecture', 'architecture-dressing', 'props-back', 'collision', 'interactives', 'actors', 'props-front-occluders', 'local-shadows', 'atmosphere-fx'];

  assert(manifest.schema === 'astro-fighters-production-manifest/v2', 'Production manifest schema must be v2.');
  assert(manifest.masterDirection === 'ASTRO_FIGHTERS_LOCKED_MASTER_ART_DIRECTION_PROMPT.md', 'Manifest must point to the locked Master Art Direction.');
  assert(manifest.approvalAuthority === 'Astro Fighters — Art Preview Review Rubric.md', 'Manifest must point to the Art Review Rubric.');
  assert(c.gridPixels === 32, 'Hidden grid must remain 32×32.');
  assert(c.projection === 'flat-faced 3/4 cabinet', 'Projection must remain flat-faced 3/4 cabinet.');
  assert(c.lightingDirection === 'upper-left / northwest', 'Lighting must remain upper-left / northwest.');
  assert(same(c.directions, directions), 'Canonical direction order drifted.');
  assert(same(c.characterSourceCanvas, [480, 640]), 'Character source canvas must remain 480×640.');
  assert(same(c.characterSourceBodyCenter, [240, 600]), 'Character source body center must remain [240,600].');
  assert(c.characterSourceFootContactY === 600, 'Character source foot-contact line must remain y=600.');
  assert(same(c.characterRuntimeFrame, [48, 64]), 'Runtime frame must remain 48×64.');
  assert(same(c.characterRuntimePivot, [24, 60]), 'Runtime pivot must remain [24,60].');
  assert(same(c.characterAnimationFramesPerDirection, { idle: 4, walk: 6, ready: 2 }), 'Animation counts drifted.');
  assert(c.worldSourceScale === 10, 'Shared-foundation source scale must remain 10×.');
  assert(same(c.worldLayerOrder, layers), 'World layer order drifted.');

  for (const item of ['body/skin', 'hair/face', 'base shorts']) assert(c.baseUnderlayer?.male?.includes(item), `Male base missing ${item}.`);
  for (const item of ['body/skin', 'hair/face', 'base shorts', 'sports bra']) assert(c.baseUnderlayer?.female?.includes(item), `Female base missing ${item}.`);
}

function validateReviewEvidence(evidence, label) {
  assert(evidence && typeof evidence === 'object', `${label} is approved without reviewEvidence.`);
  if (!evidence) return;
  assert(evidence.integratedPhaser === true, `${label} approval requires integratedPhaser=true.`);
  assert(Number.isInteger(evidence.total) && evidence.total >= 42 && evidence.total <= 50, `${label} approval requires a 42–50 total.`);
  assert(Array.isArray(evidence.automaticFailures) && evidence.automaticFailures.length === 0, `${label} approval requires zero automatic failures.`);
  assert(evidence.criticalMinimumsPass === true, `${label} approval requires all critical minimums.`);
  assert(nonEmpty(evidence.sceneId), `${label} reviewEvidence needs sceneId.`);
  assert(nonEmpty(evidence.reviewDate), `${label} reviewEvidence needs reviewDate.`);
}

function validateWorldDependency(dep, index, assetStatuses) {
  const label = `worldDependencies[${index}]`;
  assert(nonEmpty(dep.id), `${label} needs id.`);
  assert(nonEmpty(dep.name), `${label} needs name.`);
  assert(assetStatuses.includes(dep.status), `${label} has invalid status ${dep.status}.`);
  assert(positivePair(dep.sourceCanvas), `${label} needs sourceCanvas.`);
  assert(positivePair(dep.runtimeCanvas), `${label} needs runtimeCanvas.`);
  if (positivePair(dep.sourceCanvas) && positivePair(dep.runtimeCanvas)) {
    assert(dep.sourceCanvas[0] === dep.runtimeCanvas[0] * 10 && dep.sourceCanvas[1] === dep.runtimeCanvas[1] * 10, `${label} must preserve 10× source/runtime scale.`);
  }
  assert(manifest.canonical.worldLayerOrder.includes(dep.layer), `${label} has noncanonical layer ${dep.layer}.`);
  assert(Array.isArray(dep.palette) && dep.palette.length > 0 && dep.palette.every(nonEmpty), `${label} needs palette families.`);
  assert(nonEmpty(dep.anchor), `${label} needs anchor.`);
  assert(nonEmpty(dep.collision), `${label} needs collision role.`);
  assert(nonEmpty(dep.occlusion), `${label} needs occlusion role.`);
  assert(nonEmpty(dep.runtimePath) && dep.runtimePath.startsWith('docs/assets/'), `${label} needs docs/assets runtimePath.`);
  if (dep.status === 'approved') validateReviewEvidence(dep.reviewEvidence, label);
}

function validatePattern(value, label, tokens = []) {
  assert(nonEmpty(value), `${label} must be non-empty.`);
  if (!nonEmpty(value)) return;
  for (const token of tokens) assert(value.includes(`{${token}}`), `${label} must include {${token}}.`);
  assert(value.endsWith('.png'), `${label} must resolve to PNG.`);
}

function validateActivePackage() {
  const pkg = manifest.activePackage || {};
  const packageStatuses = manifest.statusVocabulary?.package || [];
  const assetStatuses = manifest.statusVocabulary?.asset || [];

  assert(nonEmpty(pkg.id), 'activePackage needs id.');
  assert(packageStatuses.includes(pkg.status), `activePackage has invalid status ${pkg.status}.`);
  assert(nonEmpty(pkg.goal), 'activePackage needs goal.');

  const wc = pkg.worldContract || {};
  assert(wc.sourceScale === 10, 'worldContract sourceScale must be 10.');
  assert(nonEmpty(wc.alpha), 'worldContract needs alpha rule.');
  assert(nonEmpty(wc.projection), 'worldContract needs projection.');
  assert(nonEmpty(wc.lighting), 'worldContract needs lighting.');
  assert(nonEmpty(wc.gridRule), 'worldContract needs grid rule.');
  assert(nonEmpty(wc.sourceRoot), 'worldContract needs sourceRoot.');
  assert(nonEmpty(wc.runtimeRoot) && wc.runtimeRoot.startsWith('docs/assets/'), 'worldContract needs docs/assets runtimeRoot.');

  assert(Array.isArray(pkg.worldDependencies) && pkg.worldDependencies.length === 14, 'Shared-foundation package must contain exactly 14 world dependencies.');
  unique(pkg.worldDependencies.map((d) => d.id), 'World dependency ids');
  unique(pkg.worldDependencies.map((d) => d.runtimePath), 'World dependency runtime paths');
  pkg.worldDependencies.forEach((dep, index) => validateWorldDependency(dep, index, assetStatuses));

  const ch = pkg.characterDependencies || {};
  assert(assetStatuses.includes(ch.status), `characterDependencies has invalid status ${ch.status}.`);
  assert(nonEmpty(ch.benchmarkId), 'Character benchmark needs benchmarkId.');
  assert(nonEmpty(ch.role), 'Character benchmark needs role.');
  assert(same(ch.sourceCanvas, manifest.canonical.characterSourceCanvas), 'Character sourceCanvas must match canonical.');
  assert(same(ch.bodyCenter, manifest.canonical.characterSourceBodyCenter), 'Character bodyCenter must match canonical.');
  assert(ch.footContactY === manifest.canonical.characterSourceFootContactY, 'Character footContactY must match canonical.');
  assert(same(ch.runtimeFrame, manifest.canonical.characterRuntimeFrame), 'Character runtimeFrame must match canonical.');
  assert(same(ch.runtimePivot, manifest.canonical.characterRuntimePivot), 'Character runtimePivot must match canonical.');
  assert(same(ch.directions, manifest.canonical.directions), 'Character directions must match canonical.');
  assert(ch.weaponRequired === false, 'First shared-foundation benchmark must remain unarmed unless re-contracted.');
  assert(Array.isArray(ch.sourceAuthoritiesRequired) && ch.sourceAuthoritiesRequired.length === 3, 'Character benchmark must require three source authorities.');

  validatePattern(ch.sourcePaths?.baseUnderlayerPattern, 'baseUnderlayerPattern', ['direction']);
  validatePattern(ch.sourcePaths?.dressedBenchmarkPattern, 'dressedBenchmarkPattern', ['direction']);
  validatePattern(ch.sourcePaths?.modularLayerPattern, 'modularLayerPattern', ['layer', 'direction']);
  validatePattern(ch.runtimePaths?.benchmarkPattern, 'benchmarkPattern', ['direction']);
  validatePattern(ch.runtimePaths?.animationPattern, 'animationPattern', ['state', 'direction']);

  assert(Array.isArray(ch.underlayer) && ch.underlayer.includes('base shorts'), 'Character underlayer must retain base shorts.');
  assert(Array.isArray(ch.benchmarkOutfit) && ch.benchmarkOutfit.length >= 7, 'Character benchmark outfit is incomplete.');
  assert(Array.isArray(ch.paletteFamilies) && ch.paletteFamilies.length > 0, 'Character benchmark needs palette families.');
  assert(Array.isArray(ch.layerFamilies) && ch.layerFamilies.length > 0, 'Character benchmark needs layer families.');
  assert(nonEmpty(ch.drawOrderRule), 'Character benchmark needs draw-order rule.');
  assert(Array.isArray(ch.validation) && ch.validation.length >= 6, 'Character validation contract is incomplete.');

  const acceptance = pkg.acceptance || {};
  assert(acceptance.integrationRequired === true, 'Package must require integration.');
  assert(acceptance.phaserRequired === true, 'Package must require Phaser.');
  assert(acceptance.automaticFailuresAllowed === 0, 'Package must allow zero automatic failures.');
  assert(acceptance.criticalMinimumsMustPass === true, 'Package must require all critical minimums.');
  assert(acceptance.checklistCompletionMinimum === 42, 'Checklist completion threshold must be 42.');
  assert(acceptance.lockQualityMinimum === 46, 'Lock-quality threshold must be 46.');
  assert((pkg.sourceGate?.requiredBeforeRuntimeDerivation || []).length >= 6, 'Source gate must block runtime derivation until source authorities/QA pass.');

  if (ch.status === 'approved') validateReviewEvidence(ch.reviewEvidence, 'characterDependencies');
  if (['production-approved', 'lock-quality'].includes(pkg.status)) validateReviewEvidence(pkg.reviewEvidence, 'activePackage');
}

function validateApprovedPackages() {
  assert(Array.isArray(manifest.approvedPackages), 'approvedPackages must be an array.');
  for (const [index, pkg] of manifest.approvedPackages.entries()) {
    assert(['production-approved', 'lock-quality'].includes(pkg.status), `approvedPackages[${index}] has non-approved status ${pkg.status}.`);
    validateReviewEvidence(pkg.reviewEvidence, `approvedPackages[${index}]`);
  }
}

validateRubric();
validateAuthorityDocs();
validateCanonical();
validateActivePackage();
validateApprovedPackages();

if (errors.length) {
  console.error(`Production validation FAILED (${errors.length}):`);
  errors.forEach((message) => console.error(`  - ${message}`));
  process.exit(1);
}

console.log('Production validation passed.');
console.log('  branch authority: main');
console.log(`  package: ${manifest.activePackage.id} (${manifest.activePackage.status})`);
console.log(`  world dependencies: ${manifest.activePackage.worldDependencies.length}`);
console.log(`  rubric automatic failures: ${rubric.automaticFailures.length}`);
console.log(`  conditional range: ${thresholdFor('conditional').min}–${thresholdFor('conditional').max}`);
console.log(`  checklist completion threshold: ${manifest.activePackage.acceptance.checklistCompletionMinimum}/50`);
