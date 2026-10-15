#!/usr/bin/env python3
# coding: utf-8
"""Generate web/af-abilities-generated.js from the canonical Astro Fighters XLSX.

No third-party packages are required. The workbook remains the authored source of truth
for the live Sign + Universal + Medical + Martial + Weapon ability values.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL_NS = {"pr": "http://schemas.openxmlformats.org/package/2006/relationships"}

def col_index(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1

def read_shared_strings(zf):
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    out = []
    for si in root.findall("m:si", NS):
        out.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))
    return out

def sheet_paths(zf):
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    relmap = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall("pr:Relationship", REL_NS)}
    out = {}
    for s in wb.findall("m:sheets/m:sheet", NS):
        name = s.attrib["name"]
        rid = s.attrib["{%s}id" % NS["r"]]
        target = relmap[rid].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        out[name] = target
    return out

def read_sheet(zf, path, shared):
    root = ET.fromstring(zf.read(path))
    rows = []
    for row in root.findall(".//m:sheetData/m:row", NS):
        vals = {}
        for c in row.findall("m:c", NS):
            idx = col_index(c.attrib["r"])
            typ = c.attrib.get("t")
            if typ == "inlineStr":
                val = "".join(t.text or "" for t in c.findall(".//m:t", NS))
            else:
                v = c.find("m:v", NS)
                if v is None:
                    val = None
                else:
                    raw = v.text or ""
                    if typ == "s":
                        val = shared[int(raw)]
                    elif typ in ("str", "e"):
                        val = raw
                    elif typ == "b":
                        val = raw == "1"
                    else:
                        try:
                            num = float(raw)
                            val = int(num) if num.is_integer() else num
                        except ValueError:
                            val = raw
            vals[idx] = val
        if vals:
            width = max(vals) + 1
            rows.append([vals.get(i) for i in range(width)])
    return rows

def load_canonical(path: Path):
    data = path.read_bytes()
    source_sha = hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(path) as zf:
        shared = read_shared_strings(zf)
        paths = sheet_paths(zf)
        roster = read_sheet(zf, paths["Live Canonical Roster"], shared)
        notes = read_sheet(zf, paths["Live Sync Notes"], shared)

    headers = roster[1]
    records = []
    for row in roster[2:]:
        row = row + [None] * (len(headers) - len(row))
        d = dict(zip(headers, row))
        if not d.get("Ability"):
            continue
        records.append({
            "section": d.get("Section") or "",
            "source": d.get("Source / Kit") or "",
            "discipline": d.get("Discipline") or "",
            "name": d.get("Ability") or "",
            "dmg": d.get("Dmg Type") or "None",
            "power": d.get("Base Power"),
            "slots": int(d.get("Slots") or 0),
            "stam": int(d.get("Base Stamina") or 0),
            "chakra": int(d.get("Base Chakra") or 0),
            "tier": d.get("Tier") or "",
            "access": d.get("Access") or "",
            "range": str(d.get("Range / Delivery") or "").strip(),
            "notes": d.get("Notes") or "",
        })

    note_map = {}
    for row in notes[2:]:
        if row and row[0]:
            note_map[str(row[0])] = str(row[1] if len(row) > 1 and row[1] is not None else "")
    palm_note = note_map.get("Palm Healing", "")
    m = re.search(r"(?:×|x)\s*(\d+(?:\.\d+)?)\s*%", palm_note, re.I)
    palm_mult = float(m.group(1)) / 100.0 if m else 1.0
    return records, source_sha, palm_mult

def js_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def render_module(records, source_sha, palm_mult):
    meta = {
        "canonicalName": "AstroFighters_Abilities_LIVE_CANONICAL_2026-08-13.xlsx",
        "repoWorkbook": "AstroFighters_Abilities.xlsx",
        "driveFileId": "1sAwyTQYUuPEP5NDkm3eGAjifl_kBQbYQ",
        "sourceSha256": source_sha,
        "recordCount": len(records),
        "palmHealingOutputMult": palm_mult,
    }
    template = r'''/* AUTO-GENERATED FILE — DO NOT HAND EDIT.
   Source: __CANONICAL__ (Drive file __DRIVE_ID__)
   SHA-256: __SHA__
   Regenerate: python3 web/generate-abilities-from-xlsx.py AstroFighters_Abilities.xlsx
*/
(function(root){
"use strict";
const META=__META__;
const ROWS=__ROWS__;
const SOURCE_ALIASES={MuayThai:"Muay Thai",JiuJitsu:"Jiu-Jitsu",Kenjutsu:"Kenjutsu (Weapon)",Kyudo:"Kyudo (Weapon)",Kobudo:"Kobudo (Weapon)"};
const MEDICAL_NAMES=ROWS.filter(r=>r.section==="Medical Kit").map(r=>r.name);
const MEDICAL_SET=new Set(MEDICAL_NAMES);
const KEY=(section,source,name)=>section+"\u0000"+source+"\u0000"+name;
const INDEX=new Map(ROWS.map(r=>[KEY(r.section,r.source,r.name),r]));
const SHARED=new Map(ROWS.filter(r=>r.section==="Martial & Weapon Styles"&&r.source==="Shared").map(r=>[r.name,r]));

function record(section,source,name){return INDEX.get(KEY(section,source,name))||null;}
function cloneEffects(a){if(a&&Array.isArray(a.effects))a.effects=a.effects.map(e=>({...e}));return a;}
function setPower(a,power){
  if(power==null||!a||!Array.isArray(a.effects))return;
  let e=a.effects.find(x=>x.k==="Damage");
  if(!e)e=a.effects.find(x=>x.k==="Heal");
  if(!e)e=a.effects.find(x=>x.k==="GrappleTech");
  if(e)e.power=Number(power);
}
function setExplicitRange(a,rec){
  if(!a||!rec)return;
  const txt=String(rec.range||"");
  let m=txt.match(/within\s+(\d+)\s+tiles?/i)||txt.match(/\((\d+)\s*tiles?\)/i);
  if(m)a.maxR=Number(m[1]);
  if(/^Adjacent ally/i.test(txt))a.maxR=1;
  if(/^Melee\b/i.test(txt))a.maxR=1;
  m=txt.match(/Reach\s*\+(\d+)m/i)||txt.match(/\+(\d+)m\s+Reach/i);
  if(m){const metersPerTile=(root.AF&&root.AF.BAL&&root.AF.BAL.metersPerTile)||2;a.reach=Math.max(1,Math.round(Number(m[1])/metersPerTile));}
}
function applyRecord(a,rec){
  if(!a||!rec)return a;
  cloneEffects(a);
  a.slots=Number(rec.slots)||1;
  a.stam=Number(rec.stam)||0;
  a.chakra=Number(rec.chakra)||0;
  if(rec.tier)a.balanceTier=rec.tier;
  setPower(a,rec.power);
  if(rec.section==="Medical Kit"){
    a.group="Medical";a.disc="Medical";setExplicitRange(a,rec);
    if(rec.name==="Palm Healing")a.healOutputMult=META.palmHealingOutputMult;
  }
  a.canonicalAuthoring={section:rec.section,source:rec.source,name:rec.name,workbookSha256:META.sourceSha256};
  return a;
}
function canonicalForAbility(a,sourceHint){
  if(!a)return null;
  if(a.canonicalAuthoring){const c=a.canonicalAuthoring,r=record(c.section,c.source,c.name||a.name);if(r)return r;}
  if(a.group==="Medical"||a.disc==="Medical")return record("Medical Kit","Medical",a.name);
  if(a.kitSign)return record("Sign Kits",a.kitSign,a.name);
  if(a.sourceKind==="Martial"){const src=SOURCE_ALIASES[a.sourceKey]||a.sourceKey;return record("Martial & Weapon Styles",src,a.name)||SHARED.get(a.name)||null;}
  if(a.sourceKind==="Weapon"){const src=SOURCE_ALIASES[a.sourceKey]||a.sourceKey;return record("Martial & Weapon Styles",src,a.name)||null;}
  if(sourceHint){
    const src=SOURCE_ALIASES[sourceHint]||sourceHint;
    const sec=src.endsWith("(Weapon)")||["Boxing","Muay Thai","Judo","Jiu-Jitsu","Karate","Wrestling","Shared"].includes(src)?"Martial & Weapon Styles":"Sign Kits";
    return record(sec,src,a.name)||SHARED.get(a.name)||null;
  }
  if(["General","Trap","Summon","Genjutsu"].includes(a.group))return record("Universal Arts",a.group,a.name);
  return null;
}
function applyArray(rows,sourceHint){return (rows||[]).map(a=>applyRecord(a,canonicalForAbility(a,sourceHint)));}
function patchStaticCollections(AF){
  for(const sign of AF.SIGNS||[]){
    const k=AF.KITS&&AF.KITS[sign];if(!k)continue;
    const allowed=new Set(ROWS.filter(r=>r.section==="Sign Kits"&&r.source===sign).map(r=>r.name));
    for(const lane of ["tai","nin","gen"])if(Array.isArray(k[lane]))k[lane]=k[lane].filter(a=>allowed.has(a.name)).map(a=>applyRecord(a,record("Sign Kits",sign,a.name)));
  }
  for(const [key,style] of Object.entries(AF.MARTIAL||{})){
    const src=SOURCE_ALIASES[key]||key;
    const allowed=new Set(ROWS.filter(r=>r.section==="Martial & Weapon Styles"&&r.source===src).map(r=>r.name));
    const allow=a=>allowed.has(a.name)||SHARED.has(a.name);
    if(style.stance)applyRecord(style.stance,record("Martial & Weapon Styles",src,style.stance.name)||SHARED.get(style.stance.name));
    if(Array.isArray(style.moves))style.moves=style.moves.filter(allow).map(a=>applyRecord(a,record("Martial & Weapon Styles",src,a.name)||SHARED.get(a.name)));
  }
  for(const [key,kit] of Object.entries(AF.WEAPONS||{})){
    const src=SOURCE_ALIASES[key]||key;
    const allowed=new Set(ROWS.filter(r=>r.section==="Martial & Weapon Styles"&&r.source===src).map(r=>r.name));
    if(kit.stance)applyRecord(kit.stance,record("Martial & Weapon Styles",src,kit.stance.name));
    if(Array.isArray(kit.moves))kit.moves=kit.moves.filter(a=>allowed.has(a.name)).map(a=>applyRecord(a,record("Martial & Weapon Styles",src,a.name)));
  }
}
function applyGeneralRows(rows){
  const allowed=new Set(ROWS.filter(r=>r.section==="Universal Arts"||r.section==="Medical Kit").map(r=>r.name));
  return (rows||[]).filter(a=>allowed.has(a.name)).map(a=>{
    const rec=(a.group==="Medical"||a.disc==="Medical")?record("Medical Kit","Medical",a.name):record("Universal Arts",a.group,a.name);
    return applyRecord(a,rec);
  });
}
function enforceMedicalAccess(rows,learned,supportNpc=false){
  const learnedSet=new Set(learned||[]);
  return (rows||[]).filter(a=>{
    if(a.group!=="Medical"&&a.disc!=="Medical")return true;
    return supportNpc||learnedSet.has(a.name);
  });
}
function patchRuntime(AF){
  if(!AF)return;
  AF.BAL.palmHealingOutputMult=META.palmHealingOutputMult;
  patchStaticCollections(AF);

  const prevZodiac=AF.zodiacAbilities;
  AF.zodiacAbilities=sign=>applyArray(prevZodiac(sign),sign);

  const prevGeneral=AF.generalArts;
  AF.generalArts=()=>applyGeneralRows(prevGeneral());

  const prevBuild=AF.buildLoadout;
  AF.buildLoadout=function(opt={}){
    const learned=opt.learnedMedical||[];
    let rows=prevBuild(opt);
    rows=rows.map(a=>applyRecord(a,canonicalForAbility(a)));
    return enforceMedicalAccess(rows,learned,false);
  };

  const prevEnemy=AF.enemyLoadout;
  AF.enemyLoadout=function(key){
    const support=AF.ENEMIES&&AF.ENEMIES[key]&&AF.ENEMIES[key].persona==="support";
    let rows=prevEnemy(key);
    rows=rows.map(a=>{
      let rec=canonicalForAbility(a);
      if(!rec&&(a.group==="Medical"||a.disc==="Medical")){
        const regen=(a.effects||[]).some(e=>e.k==="Status"&&e.status==="Regen");
        const transfer=(a.effects||[]).some(e=>e.k==="Res"&&e.res==="Chakra"&&e.amt>0);
        rec=record("Medical Kit","Medical",regen?"Cellular Activation":transfer?"Chakra Transfer":"Palm Healing");
      }
      return applyRecord(a,rec);
    });
    return enforceMedicalAccess(rows,[],support);
  };

  AF.CANONICAL_ABILITIES={META,ROWS,MEDICAL_NAMES,record,applyRecord};
  if(root.document){
    const sel=root.document.getElementById("learnedMedical");
    if(sel){
      sel.innerHTML='<option value="">None</option><option value="'+MEDICAL_NAMES.join("|")+'">Medical Kit</option>';
      const f=sel.closest&&sel.closest(".field"),l=f&&f.querySelector("label"),n=f&&f.querySelector("small.note");
      if(l)l.textContent="Learned Medical kit";
      if(n)n.textContent="Medical is a learned support kit. Players must learn it; only support-type NPCs may use Medical abilities.";
    }
  }
}
patchRuntime(root.AF);
if(typeof module!=="undefined"&&module.exports)module.exports={META,ROWS,MEDICAL_NAMES,record,applyRecord,patchRuntime};
})(typeof globalThis!=="undefined"?globalThis:this);
'''
    return (template.replace("__CANONICAL__", meta["canonicalName"])
                    .replace("__DRIVE_ID__", meta["driveFileId"])
                    .replace("__SHA__", source_sha)
                    .replace("__META__", js_json(meta))
                    .replace("__ROWS__", js_json(records)))

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("workbook", nargs="?", default="AstroFighters_Abilities.xlsx")
    ap.add_argument("output", nargs="?", default="web/af-abilities-generated.js")
    ap.add_argument("--check", action="store_true")
    args=ap.parse_args(argv)
    records, sha, mult=load_canonical(Path(args.workbook))
    text=render_module(records,sha,mult)
    out=Path(args.output)
    if args.check:
        current=out.read_text(encoding="utf-8") if out.exists() else ""
        if current != text:
            print(f"ERROR: {out} is out of date with {args.workbook}", file=sys.stderr)
            return 1
        print(f"OK: {out} matches {args.workbook} ({len(records)} records, {sha})")
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} ({len(records)} records, {sha})")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
