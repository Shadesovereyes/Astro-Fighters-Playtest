/* =========================================================================
   ASTRO FIGHTERS — core engine (chart + hex grid + combat), no DOM.
   Faithful JS port of the Unity trunk (astro-fighters-art-direction):
   AstroTime, SimpleEphemeris, PlanetEphemeris, ChartMath, ChartToLoadout,
   HexCoord, BattlefieldGrid, CombatMath, TurnResolver, AbilityEconomy,
   AspectCalculator, InitiativeRules + the content catalogs.
   Exposed on globalThis so the page and headless tests share one source.
   ========================================================================= */
(function(root){
"use strict";
const {round,floor,ceil,max,min,abs,sqrt,sin,cos,tan,atan2,PI,hypot}=Math;
const D2R=PI/180,R2D=180/PI;

/* ---- BalanceConfig.cs ---- */
const BAL={
  hpBase:100,hpPerFort:10,staminaBase:50,staminaPerFort:5,chakraBase:50,chakraPerCha:10,
  poisePerFort:10,poisePerCha:5,
  staminaRegenBase:5,staminaRegenPerFort:0.5,chakraRegenBase:5,chakraRegenPerCha:0.5,
  baseHitChance:75,accAgiWeight:0.7,accChaWeight:0.3,evaAgiWeight:0.7,evaChaWeight:0.3,
  blindAccuracyPenalty:-50,proneHitBonus:30,grappleHitBonus:30,clumsyHitPenalty:-40,clumsyDamageMultiplier:0.8,
  movementAgiBreakpoints:[6,20,40,80,100],movementTilesAtBreakpoint:[2,3,5,9,12],
  initDie:10,arenaRadius:5,casterKiteStandoffTiles:4,
  mitigationCap:0.75,mitigationPerPoint:0.015,
  shortBandTiles:1,mediumBandTiles:4,
  aoeFriendlyFireMultiplier:0.5,aoeFalloffPerTarget:0.05,ultimateAoeRadius:3,normalAoeRadiusCap:1,
  poiseRatioPhysical:1.0,poiseRatioElemental:0.5,poiseDmgMultMax:1.5,staggerCancelsNextAction:1,
  // Sheet ("Focus actions & poise regen"): passive poise regen is 10% of max per round (was 25%).
  poiseRegenMaxPercent:0.10,exhaustionDamageMultiplier:2,damageScale:0.7,
  confusionFizzleChance:35,
  slowInitiativePenalty:15,ccInitHeavy:25,ccInitLight:8,ccInitStealthBonus:10,
  slowMoveMult:0.5,snareMoveMult:0.5,
  initBaseActionCost:20,initPriorityWeight:8,initStanceExtra:12,initAoeExtra:10,initSummonExtra:30,
  initUltimateExtra:40,initPerExtraSlot:10,initMinWeight:8,initMaxWeight:70,
  ccBreakDefaultDC:14,ccBreakDecay:2,useCandidateDcModel:true,useCandidateEconomy:true,palmHealingOutputMult:0.70,
  repetitionFreeUses:2,repetitionStrainPerExtra:0.5,
  // AI sustainable-resource planning: a candidate's score is discounted by how much of its pool
  // an action would actually cost (including the repetitionExtra surcharge above) AND by how
  // depleted that pool already is — full pool, cheap action: barely touched; low pool, expensive
  // action: hit hard. A smooth curve rather than a hard reserve floor, so the AI still throws its
  // best remaining option when it has to, never freezing — see resourcePaceMult.
  aiResourcePacingWeight:2.5,aiResourcePacingFloor:0.35,
  // AI opponent-read: an ability this SPECIFIC foe has already beaten this fight (evaded,
  // parried, or denied a grapple/technique entry — see recordResisted) gets discounted per prior
  // failure against them, so the AI stops walking back into the same read. Floored, never zeroed
  // — a repeated failure is evidence to weigh, not proof the option can never work again.
  aiResistanceDiscountPerCount:0.25,aiResistanceDiscountFloor:0.25,
  // AI opponent-pattern-read: once a foe's actions this fight have been grapple-heavy past this
  // fraction, the AI leans away from trading holds with them (own Grapple/GrappleTech scores
  // discounted) and leans into punishing the pattern instead (Priority strikes — which already
  // land bonus value against a queued grapple entry via the "mid-entry" clash rule — get a boost).
  aiGrapplePatternThreshold:0.4,aiGrapplePatternPenalty:0.7,aiPriorityPatternBonus:1.15,
  elementalCostMult:1.75,elementalDamageMult:1.4,generalCostMult:1.0,generalDamageMult:1.0,
  eyeUpkeepChakraPerTurn:10,summonReservePerTier:15,trapUsesPerBattle:3,baseSupplies:5,
  strainOnActivate:10,strainPerTurnActive:5,strainPerEyeJutsu:15,strainDecayPerTurn:5,
  burnoutDurationTurns:3,burnoutAccuracyCap:5,
  // The old escape-check constants are gone with the auto-escape rule: relationships now end
  // only through an explicit effect, maintenance failure/release, or an invalid participant.
  grappleLandDC:12,grappleHoldUpkeepStamina:5,
  // System 3 — ability clashes: a kick or punch that misses grants the opponent's own queued
  // follow-up (Single Leg Shot / Clinch) a bonus DC via the existing GrappleSetup status, IF
  // that follow-up is their very next queued action. Same scale as the positionalDc* constants
  // below, deliberately larger than Judo Chop's own landed-hit mag of 1.
  kickWhiffShotBonus:2,punchWhiffClinchBonus:2,
  // Teep Kick's scoped anti-priority: without it, a Normal-speed (weight 20) Teep Kick almost
  // never gets to act before a Priority-tagged (weight 8) damaging rush, since that gap alone
  // is worth ~12 in the picking key (selOffset = initWeight-20). Sized to close exactly that
  // gap — a fair race against the rush it's reading, not a guaranteed win — deliberately not
  // reusing initStanceExtra even though the number matches; that constant means something
  // unrelated and tuning it for Stance balance shouldn't silently retune this too.
  teepAntiPriorityBonus:12,
  /* Positional combat (canonical Google Sheet "Positional Rules", 2026-08-14). */
  mountUpkeepStamina:10,
  /* A Maintained Submission has no passive upkeep and no reserved slot: the holder keeps it
     by re-queueing the submission ability every round. Each CONSECUTIVE round it is
     re-applied raises both its resource cost and its damage, so a long choke pays for
     itself and is self-limiting. */
  submissionCostEscalation:0.5,submissionDamageEscalation:0.5,
  /* A submission that has been worked for N turns lowers the DC of a contested positional
     escape (Reversal) proportionally, for the fighter caught in the hold. The contest denies on
     `defence + d20 >= attack + dc`, so a LOWER dc is harder for the escaper. This applies only
     to escapes that HAVE a check — Hip Escape is flat resource damage and is never gated. */
  submissionEscapeDcPerRound:2,
  positionalDcFree:0,positionalDcGrappling:1,positionalDcGrappled:1,positionalDcMounting:2,positionalDcMounted:-2,
  passiveStamFree:1,passiveStamGrappling:0.5,passiveStamGrappled:0.5,passiveStamMounting:0.25,passiveStamMounted:0.25,
  standingGrapplePriorityWeight:1,focusRestorePercent:0.20,recomposeCostPercent:0.10,actionSlotsPerRound:5,
  // Opponent/ally level scaling (2026-08-17): canonical ENEMIES stats are the level-20
  // baseline (scale ×1.0 exactly there) — that's the default in the setup UI, and every style-
  // NPC balance pass this session was tuned and round-robin-tested at that baseline, so picking
  // 20 must reproduce today's numbers unchanged. Linear outside that anchor; floored so a very
  // low level never rounds a stat to 0.
  enemyLevelAnchor:20,enemyLevelScaleAtAnchor:1,enemyLevelScalePerLevel:0.025,enemyLevelStatFloor:3,
  aiMaxProjectedChain:2,
  hauntUpkeepChakraPerTurn:8,hauntChakraPerAction:4,hauntTickMental:6,
  awarenessBaseTiles:3,awarenessPerPerception:0.2,stealthBaseDC:8,stealthDcPerRound:4,
  terrainWallHp:30,
  metersPerTile:2,
};

/* ---- seeded RNG ---- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
let RNG=mulberry32(0xC0FFEE);
const setSeed=s=>{RNG=mulberry32(s|0);};
const rand=()=>RNG();
const d=n=>1+floor(rand()*n);
const clamp=(v,lo,hi)=>max(lo,min(hi,v));
const lerp=(a,b,t)=>a+(b-a)*t;

/* =========================================================================
   ASTRONOMY  (AstroTime, SimpleEphemeris, PlanetEphemeris, ChartMath)
   ========================================================================= */
const J2000=2451545.0;
function julianDay(ms){ // ms = UTC epoch millis
  const dt=new Date(ms);
  let year=dt.getUTCFullYear(),month=dt.getUTCMonth()+1;
  const day=dt.getUTCDate()+(dt.getUTCHours()+(dt.getUTCMinutes()+(dt.getUTCSeconds()+dt.getUTCMilliseconds()/1000)/60)/60)/24;
  if(month<=2){year-=1;month+=12;}
  const a=floor(year/100),b=2-a+floor(a/4);
  return floor(365.25*(year+4716))+floor(30.6001*(month+1))+day+b-1524.5;
}
const centuries=jd=>(jd-J2000)/36525;
function norm360(x){x%=360;return x<0?x+360:x;}
function normSigned(x){x=norm360(x);return x>180?x-360:x;}
function gmstDeg(jd){const t=centuries(jd);return norm360(280.46061837+360.98564736629*(jd-J2000)+0.000387933*t*t-t*t*t/38710000);}
function obliquityDeg(jd){const t=centuries(jd);const s=21.448-t*(46.8150+t*(0.00059-t*0.001813));return 23+26/60+s/3600;}

function sunLon(jd){const t=centuries(jd);const l0=280.46646+36000.76983*t+0.0003032*t*t;const m=(357.52911+35999.05029*t-0.0001537*t*t)*D2R;
  const c=(1.914602-0.004817*t-0.000014*t*t)*sin(m)+(0.019993-0.000101*t)*sin(2*m)+0.000289*sin(3*m);return norm360(l0+c);}
const MOON_TERMS=[[0,0,1,0,6288774],[2,0,-1,0,1274027],[2,0,0,0,658314],[0,0,2,0,213618],[0,1,0,0,-185116],[0,0,0,2,-114332],[2,0,-2,0,58793],[2,-1,-1,0,57066],[2,0,1,0,53322],[2,-1,0,0,45758],[0,1,-1,0,-40923],[1,0,0,0,-34720],[0,1,1,0,-30383],[2,0,0,-2,15327],[0,0,1,2,-12528],[0,0,1,-2,10980],[4,0,-1,0,10675],[0,0,3,0,10034],[4,0,-2,0,8548],[2,1,-1,0,-7888],[2,1,0,0,-6766],[1,0,-1,0,-5163],[1,1,0,0,4987],[2,-1,1,0,4036],[2,0,2,0,3994],[4,0,0,0,3861],[2,0,-3,0,3665]];
function moonLon(jd){const t=centuries(jd);
  const lp=218.3164477+481267.88123421*t-0.0015786*t*t+t*t*t/538841-t*t*t*t/65194000;
  const dd=297.8501921+445267.1114034*t-0.0018819*t*t+t*t*t/545868-t*t*t*t/113065000;
  const m=357.5291092+35999.0502909*t-0.0001536*t*t+t*t*t/24490000;
  const mp=134.9633964+477198.8675055*t+0.0087414*t*t+t*t*t/69699-t*t*t*t/14712000;
  const f=93.2720950+483202.0175233*t-0.0036539*t*t-t*t*t/3526000+t*t*t*t/863310000;
  const e=1-0.002516*t-0.0000074*t*t;let sum=0;
  for(const[md,mm,mmp,mf,co]of MOON_TERMS){const arg=(md*dd+mm*m+mmp*mp+mf*f)*D2R;const mMul=abs(mm);const ef=mMul===1?e:mMul===2?e*e:1;sum+=co*ef*sin(arg);}
  return norm360(lp+sum/1e6);}

const PLANET_EL={
  Mercury:{a:0.38709927,aD:0.00000037,e:0.20563593,eD:0.00001906,I:7.00497902,ID:-0.00594749,L:252.25032350,LD:149472.67411175,w:77.45779628,wD:0.16047689,om:48.33076593,omD:-0.12534081},
  Venus:{a:0.72333566,aD:0.00000390,e:0.00677672,eD:-0.00004107,I:3.39467605,ID:-0.00078890,L:181.97909950,LD:58517.81538729,w:131.60246718,wD:0.00268329,om:76.67984255,omD:-0.27769418},
  Mars:{a:1.52371034,aD:0.00001847,e:0.09339410,eD:0.00007882,I:1.84969142,ID:-0.00813131,L:-4.55343205,LD:19140.30268499,w:-23.94362959,wD:0.44441088,om:49.55953891,omD:-0.29257343},
  Jupiter:{a:5.20288700,aD:-0.00011607,e:0.04838624,eD:-0.00013253,I:1.30439695,ID:-0.00183714,L:34.39644051,LD:3034.74612775,w:14.72847983,wD:0.21252668,om:100.47390909,omD:0.20469106},
  Saturn:{a:9.53667594,aD:-0.00125060,e:0.05386179,eD:-0.00050991,I:2.48599187,ID:0.00193609,L:49.95424423,LD:1222.49362201,w:92.59887831,wD:-0.41897216,om:113.66242448,omD:-0.28867794},
  Uranus:{a:19.18916464,aD:-0.00196176,e:0.04725744,eD:-0.00004397,I:0.77263783,ID:-0.00242939,L:313.23810451,LD:428.48202785,w:170.95427630,wD:0.40805281,om:74.01692503,omD:0.04240589},
  Neptune:{a:30.06992276,aD:0.00026291,e:0.00859048,eD:0.00005105,I:1.77004347,ID:0.00035372,L:-55.12002969,LD:218.45945325,w:44.96476227,wD:-0.32241464,om:131.78422574,omD:-0.00508664},
  Pluto:{a:39.48211675,aD:-0.00031596,e:0.24882730,eD:0.00005170,I:17.14001206,ID:0.00004818,L:238.92903833,LD:145.20780515,w:224.06891629,wD:-0.04062942,om:110.30393684,omD:-0.01183482},
};
const EARTH_EL={a:1.00000261,aD:0.00000562,e:0.01671123,eD:-0.00004392,I:-0.00001531,ID:-0.01294668,L:100.46457166,LD:35999.37244981,w:102.93768193,wD:0.32327364,om:0,omD:0};
function solveKepler(m,e){let ecc=m+e*sin(m);for(let i=0;i<12;i++){const dM=m-(ecc-e*sin(ecc));const dE=dM/(1-e*cos(ecc));ecc+=dE;if(abs(dE)<1e-9)break;}return ecc;}
function helio(el,t){const a=el.a+el.aD*t,e=el.e+el.eD*t,I=(el.I+el.ID*t)*D2R,L=el.L+el.LD*t,wbar=el.w+el.wD*t,om=(el.om+el.omD*t)*D2R;
  const argP=(wbar-el.om-el.omD*t)*D2R;const m=normSigned(L-wbar)*D2R;const ecc=solveKepler(m,e);
  const xp=a*(cos(ecc)-e),yp=a*sqrt(1-e*e)*sin(ecc);
  const cw=cos(argP),sw=sin(argP),co=cos(om),so=sin(om),ci=cos(I),si=sin(I);
  return{x:(cw*co-sw*so*ci)*xp+(-sw*co-cw*so*ci)*yp,y:(cw*so+sw*co*ci)*xp+(-sw*so+cw*co*ci)*yp};}
function planetLon(name,jd){const t=centuries(jd);const p=helio(PLANET_EL[name],t),ea=helio(EARTH_EL,t);return norm360(atan2(p.y-ea.y,p.x-ea.x)*R2D);}
function ascendantLon(jd,lat,lon){const ramc=norm360(gmstDeg(jd)+lon)*D2R;const eps=obliquityDeg(jd)*D2R;const phi=lat*D2R;
  const asc=atan2(cos(ramc),-(sin(ramc)*cos(eps)+tan(phi)*sin(eps)));return norm360(asc*R2D);}
function northNodeLon(jd){const t=centuries(jd);return norm360(125.0445479-1934.1362891*t+0.0020754*t*t+t*t*t/467441-t*t*t*t/60616000);}

const SIGNS=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"];
const PLANETS=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"];
const ELEM={Aries:"Fire",Leo:"Fire",Sagittarius:"Fire",Taurus:"Earth",Virgo:"Earth",Capricorn:"Earth",Gemini:"Air",Libra:"Air",Aquarius:"Air",Cancer:"Water",Scorpio:"Water",Pisces:"Water"};
const RULER={Aries:"Mars",Taurus:"Venus",Gemini:"Mercury",Cancer:"Moon",Leo:"Sun",Virgo:"Mercury",Libra:"Venus",Scorpio:"Mars",Sagittarius:"Jupiter",Capricorn:"Saturn",Aquarius:"Saturn",Pisces:"Jupiter"};
const GLYPH={Aries:"♈",Taurus:"♉",Gemini:"♊",Cancer:"♋",Leo:"♌",Virgo:"♍",Libra:"♎",Scorpio:"♏",Sagittarius:"♐",Capricorn:"♑",Aquarius:"♒",Pisces:"♓"};
const NAKSHATRA=["Ashwini (Horse)","Bharani (Elephant)","Krittika (Razor Goat)","Rohini (Serpent)","Mrigashira (Deer)","Ardra (Wolf)","Punarvasu (Cat)","Pushya (Ram)","Ashlesha (Naga)","Magha (Lion)","Purva Phalguni (Rat)","Uttara Phalguni (Bull)","Hasta (Buffalo)","Chitra (Tiger)","Swati (Bee Swarm)","Vishakha (Chimera)","Anuradha (Hare)","Jyeshtha (Boar)","Mula (Hound)","Purva Ashadha (Monkey)","Uttara Ashadha (Mongoose)","Shravana (Eagle)","Dhanishta (Dolphin)","Shatabhisha (Mare)","Purva Bhadrapada (Lioness)","Uttara Bhadrapada (Deep Serpent)","Revati (Fish)"];
const NAK_ROLE=["Scout","Tank","Bleed","Assassin","Scout","Support","DPS","Tank","DPS","DPS","Generic","Support","Tank","Assassin","Support","DPS","Tank","DPS","Scout","Generic","Support","Scout","Generic","Healer","DPS","Bleed","Support"];
const PADA=["Dharma","Artha","Kama","Moksha"]; // Fire, Earth, Air, Water

function signOf(lon){return SIGNS[floor(norm360(lon)/30)%12];}
function degInSign(lon){return norm360(lon)%30;}
function decanOf(lon){return floor(degInSign(lon)/10);}
function dwadOf(lon){return floor(degInSign(lon)/2.5);}
function nakOf(lon){return floor(norm360(lon)/(13+20/60))%27;}
function padaOf(lon){const into=norm360(lon)%(13+20/60);return floor(into/(3+20/60))%4;}

function buildChart(ms,lat,lon){
  const jd=julianDay(ms);const planets={};
  planets.Sun=sunLon(jd);planets.Moon=moonLon(jd);
  for(const p of["Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"])planets[p]=planetLon(p,jd);
  const placements={};for(const p of PLANETS)placements[p]=placement(planets[p]);
  const asc=placement(ascendantLon(jd,lat,lon));
  const node=placement(northNodeLon(jd));
  return{placements,asc,node,jd,lat,lon,ms};
}
function placement(lon){lon=norm360(lon);return{lon,sign:signOf(lon),deg:degInSign(lon),decan:decanOf(lon),dwad:dwadOf(lon),nak:nakOf(lon),pada:padaOf(lon)};}

const PLANET_BONUS={Sun:"Yang Output",Moon:"Healing / Defense",Mercury:"Casting Speed",Venus:"Resource Efficiency",Mars:"Physical Damage",Jupiter:"AoE / Luck",Saturn:"Crowd Control",Uranus:"Crit / Shield Break",Neptune:"Genjutsu Potency",Pluto:"True Damage"};
function chartToLoadout(chart){
  const unlocked=new Set(),planetSigns={},bonuses={};
  for(const p of PLANETS){const pl=chart.placements[p];planetSigns[p]=pl.sign;unlocked.add(pl.sign);const lab=PLANET_BONUS[p];bonuses[lab]=(bonuses[lab]||0)+1;}
  unlocked.add(chart.asc.sign);
  const moon=chart.placements.Moon;
  return{unlockedSigns:[...unlocked],planetSigns,bonuses,
    rising:chart.asc.sign,sun:chart.placements.Sun.sign,moon:moon.sign,
    summonNak:moon.nak,summonPada:moon.pada,summonSpecies:{name:NAKSHATRA[moon.nak],role:NAK_ROLE[moon.nak]},
    eyesEligible:PLANETS.slice()};
}

/* =========================================================================
   HEX GRID  (HexCoord + BattlefieldGrid)
   ========================================================================= */
const HEX_DIRS=[[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]];
const hx=(q,r)=>({q,r});
const hkey=c=>c.q+","+c.r;
function hdist(a,b){return(abs(a.q-b.q)+abs(a.q+a.r-b.q-b.r)+abs(a.r-b.r))/2;}
function neighbors(c){return HEX_DIRS.map(([dq,dr])=>hx(c.q+dq,c.r+dr));}
function cubeRound(q,r){let s=-q-r;let rq=Math.round(q),rr=Math.round(r),rs=Math.round(s);
  const dq=abs(rq-q),dr=abs(rr-r),ds=abs(rs-s);if(dq>dr&&dq>ds)rq=-rr-rs;else if(dr>ds)rr=-rq-rs;return hx(rq,rr);}

class Grid{
  constructor(radius){this.R=radius;this.center=hx(0,0);this.terrain=new Map();this.tRounds=new Map();this.tHp=new Map();this.hazard=new Map();}
  inBounds(c){return hdist(this.center,c)<=this.R;}
  cells(){const out=[];for(let q=-this.R;q<=this.R;q++)for(let r=max(-this.R,-q-this.R);r<=min(this.R,-q+this.R);r++)out.push(hx(q,r));return out;}
  terrainAt(c){return this.terrain.get(hkey(c))||"Open";}
  blocksMove(c){const t=this.terrainAt(c);return t==="Wall"||t==="Tree"||t==="Rock"||t==="FelledTree";}
  blocksSight(c){const t=this.terrainAt(c);return t!=="Open"&&t!=="Water"&&t!=="FelledTree"&&t!=="Spikes"&&t!=="Caltrops";}
  setHazard(c,data){this.hazard.set(hkey(c),data);}
  hazardAt(c){return this.hazard.get(hkey(c))||null;}
  set(c,kind,dur=0,hp=0){if(!this.inBounds(c))return;const k=hkey(c);if(kind==="Open"){this.terrain.delete(k);this.tRounds.delete(k);this.tHp.delete(k);this.hazard.delete(k);return;}this.terrain.set(k,kind);if(dur>0)this.tRounds.set(k,dur);else this.tRounds.delete(k);if(kind==="Wall"&&hp>0)this.tHp.set(k,hp);else this.tHp.delete(k);}
  damageTerrain(c,amt){const k=hkey(c);if(this.terrainAt(c)!=="Wall"||!this.tHp.has(k))return false;let hp=this.tHp.get(k)-amt;if(hp>0){this.tHp.set(k,hp);return false;}this.set(c,"Open");return true;}
  // AoE destruction: trees fall (stop blocking sight, still block move); bushes are cleared.
  blastTerrain(center,radius){let trees=0,bushes=0;for(const c of this.within(center,radius)){const t=this.terrainAt(c);if(t==="Tree"){this.set(c,"FelledTree");trees++;}else if(t==="Bush"){this.set(c,"Open");bushes++;}}return{trees,bushes};}
  tick(){for(const k of[...this.tRounds.keys()]){const v=this.tRounds.get(k)-1;if(v<=0){this.terrain.delete(k);this.tRounds.delete(k);this.tHp.delete(k);this.hazard.delete(k);}else this.tRounds.set(k,v);}}
  clearTerrain(){this.terrain.clear();this.tRounds.clear();this.tHp.clear();this.hazard.clear();}
  los(a,b){const n=hdist(a,b);if(n<=1)return true;for(let i=1;i<n;i++){const t=i/n;const q=a.q+(b.q-a.q)*t+1e-4,r=a.r+(b.r-a.r)*t+1e-4;const c=cubeRound(q,r);if(this.blocksSight(c))return false;}return true;}
  // "Hard cover" only — Wall/Rock, the two terrain kinds blastTerrain() never destroys. Tree and
  // Bush block ordinary los() but don't stop a Piercing-tagged shot (e.g. Called Shot), which is
  // meant to punch through destructible foliage and only be stopped by permanent obstacles.
  blocksSightHard(c){const t=this.terrainAt(c);return t==="Wall"||t==="Rock";}
  losHard(a,b){const n=hdist(a,b);if(n<=1)return true;for(let i=1;i<n;i++){const t=i/n;const q=a.q+(b.q-a.q)*t+1e-4,r=a.r+(b.r-a.r)*t+1e-4;const c=cubeRound(q,r);if(this.blocksSightHard(c))return false;}return true;}
  within(center,radius){const out=[];for(let dq=-radius;dq<=radius;dq++){const lo=max(-radius,-dq-radius),hi=min(radius,-dq+radius);for(let dr=lo;dr<=hi;dr++){const c=hx(center.q+dq,center.r+dr);if(this.inBounds(c))out.push(c);}}return out;}
  reachable(start,mp,blocked){const dist=new Map([[hkey(start),0]]);const cells=new Map([[hkey(start),start]]);const q=[start];while(q.length){const cur=q.shift();const cd=dist.get(hkey(cur));if(cd>=mp)continue;for(const n of neighbors(cur)){const k=hkey(n);if(!this.inBounds(n)||blocked(n)||dist.has(k))continue;dist.set(k,cd+1);cells.set(k,n);q.push(n);}}return{dist,cells};}
  bestApproach(start,target,mp,blocked){const{dist,cells}=this.reachable(start,mp,blocked);let best=start,bestCost=0,bestDist=hdist(start,target);for(const[k,c]of cells){const dt=hdist(c,target);const cost=dist.get(k);if(dt<bestDist||(dt===bestDist&&cost<bestCost)){best=c;bestCost=cost;bestDist=dt;}}return{cell:best,cost:bestCost};}
  nearestFree(origin,taken){if(this.inBounds(origin)&&!taken(origin))return origin;for(let radius=1;radius<=this.R*2;radius++)for(const c of this.within(origin,radius))if(hdist(origin,c)===radius&&this.inBounds(c)&&!taken(c))return c;return origin;}
}
function makeArena(radius){const g=new Grid(radius);return g;}

/* =========================================================================
   COMBAT MATH  (CombatMath.cs / DerivedResources.cs / AbilityEconomy.cs)
   ========================================================================= */
function mcurve(agi){const xs=BAL.movementAgiBreakpoints,ys=BAL.movementTilesAtBreakpoint,n=min(xs.length,ys.length);
  if(agi<=xs[0])return max(0,ys[0]);for(let i=1;i<n;i++)if(agi<=xs[i]){const t=(agi-xs[i-1])/max(1,xs[i]-xs[i-1]);return round(lerp(ys[i-1],ys[i],t));}
  const slope=n>=2?(ys[n-1]-ys[n-2])/max(1,xs[n-1]-xs[n-2]):0;return round(ys[n-1]+slope*(agi-xs[n-1]));}
const DR={
  maxHp:s=>BAL.hpBase+s.FORT*BAL.hpPerFort,maxStam:s=>BAL.staminaBase+s.FORT*BAL.staminaPerFort,
  maxChakra:s=>BAL.chakraBase+s.CHA*BAL.chakraPerCha,maxPoise:s=>s.FORT*BAL.poisePerFort+s.CHA*BAL.poisePerCha,
  acc:s=>s.AGI*BAL.accAgiWeight+s.CHA*BAL.accChaWeight,eva:s=>s.AGI*BAL.evaAgiWeight+s.CHA*BAL.evaChaWeight,
  mc:s=>mcurve(s.AGI),baseInit:s=>s.AGI,stamRegen:s=>round(BAL.staminaRegenBase+s.FORT*BAL.staminaRegenPerFort),
  chakRegen:s=>round(BAL.chakraRegenBase+s.CHA*BAL.chakraRegenPerCha),poiseRegen:s=>round(DR.maxPoise(s)*BAL.poiseRegenMaxPercent),
  // `perception` (CHA/INT blend) is the Stealth-detection contest stat — noticing a hidden
  // threat through insight, a distinct mechanic. `awareness` is raw vision RANGE and is CHA
  // only (owner ruling, 2026-08-18): a fighter must never perceive further than its own CHA
  // allows, regardless of INT.
  perception:s=>s.CHA*0.8+s.INT*0.2,awareness:s=>BAL.awarenessBaseTiles+round(s.CHA*BAL.awarenessPerPerception),
  physMit:str=>1-min(BAL.mitigationCap,str*BAL.mitigationPerPoint),elemMit:i=>1-min(BAL.mitigationCap,i*BAL.mitigationPerPoint),
};
function bandFor(dist){return dist<=BAL.shortBandTiles?"Short":dist<=BAL.mediumBandTiles?"Medium":"Long";}
function rangeMatrix(atk,band){switch(atk){case"Melee":return band==="Short"?100:0;case"Reach":return band==="Short"?70:band==="Medium"?100:0;
  case"Projectile":return band==="Short"?50:band==="Medium"?90:100;case"Magic":return band==="Short"?90:band==="Medium"?100:80;
  case"GenTouch":return band==="Short"?100:0;case"GenVisual":return band==="Short"?100:band==="Medium"?90:0;default:return 0;}}
function evalRange(ab,dist){const bandMod=rangeMatrix(ab.atk,bandFor(dist));if(dist>ab.maxR)return{outcome:"Impossible",bandMod};if(bandMod<=0)return{outcome:"Impossible",bandMod};if(dist<ab.minR)return{outcome:"Clumsy",bandMod};return{outcome:"Normal",bandMod};}
function baseDamage(type,power,atk,tgt,mit){if(type==="Physical")return max(0,round((power+atk.STR)*(mit?DR.physMit(tgt.STR):1)));if(type==="Elemental")return max(0,round((power+atk.INT)*(mit?DR.elemMit(tgt.INT):1)));if(type==="Mental")return max(0,round(power+atk.CHA+atk.INT));if(type==="True")return max(0,round(power+atk.STR));return 0;}
function poiseDamage(hp,type,pm,cap){const ratio=type==="Physical"?BAL.poiseRatioPhysical:type==="Elemental"?BAL.poiseRatioElemental:0;if(ratio<=0)return 0;return round(hp*ratio*clamp(pm||1,0,cap||BAL.poiseDmgMultMax));}
function aspectBetween(a,b){let s=((SIGNS.indexOf(b)-SIGNS.indexOf(a))%12+12)%12;const dist=s>6?12-s:s;return{0:"Conjunction",2:"Sextile",3:"Square",4:"Trine",6:"Opposition"}[dist]||"None";}
function affinity(self,opp){let dmgDone=1,healDone=1,dmgTaken=1;switch(aspectBetween(self,opp)){case"Square":dmgDone=.98;healDone=.98;break;case"Trine":healDone=1.05;dmgDone=.98;break;case"Opposition":dmgTaken=1.05;break;}return{dmgDone,healDone,dmgTaken,aspect:aspectBetween(self,opp)};}
function initWeight(ab){if(!ab)return BAL.initBaseActionCost;if(ab.tags.includes("Priority"))return BAL.initPriorityWeight;let w=BAL.initBaseActionCost;if(ab.tags.includes("Stance"))w+=BAL.initStanceExtra;if(ab.targeting==="PointRadius")w+=BAL.initAoeExtra;if(ab.effects.some(e=>e.k==="SpawnSummon"))w+=BAL.initSummonExtra;if(ab.tags.includes("Ultimate"))w+=BAL.initUltimateExtra;if(ab.slots>1)w+=(ab.slots-1)*BAL.initPerExtraSlot;return clamp(w,BAL.initMinWeight,BAL.initMaxWeight);}
const selOffset=ab=>initWeight(ab)-BAL.initBaseActionCost;
const depletion=ab=>initWeight(ab);
const isElemental=ab=>ab.dmg==="Elemental";
const costMult=ab=>isElemental(ab)?BAL.elementalCostMult:BAL.generalCostMult;
const dmgMult=ab=>isElemental(ab)?BAL.elementalDamageMult:BAL.generalDamageMult;

/* =========================================================================
   CONTENT — ability builders + catalogs
   ========================================================================= */
let ABID=0;

/* =========================================================================
   POSITIONAL COMBAT METADATA
   Canonical source: AstroFighters_Abilities Google Sheet → "Positional Rules"
   (ASTRO FIGHTERS — CANONICAL POSITIONAL COMBAT RULES, 2026-08-14).

   Relationships are DIRECTIONAL and structural: a fighter holds a role plus a
   reference to the paired combatant. Legality is resolved from structured
   metadata only — never by parsing an ability's display name.
   ========================================================================= */
const REL={FREE:"Free",GRAPPLING:"Grappling",GRAPPLED:"Grappled",MOUNTING:"Mounting",MOUNTED:"Mounted"};
const REL_ROLES=[REL.FREE,REL.GRAPPLING,REL.GRAPPLED,REL.MOUNTING,REL.MOUNTED];
const MOUNT_ACCESS={NEITHER:"Neither",MOUNTING_ONLY:"MountingOnly",MOUNTED_ONLY:"MountedOnly",BOTH:"Both"};
// Relationship prerequisite vocabulary used by ability metadata.
const REQ={NONE:null,STANDING:"StandingGrapple",GRAPPLING:"Grappling",GRAPPLED:"Grappled",MOUNT:"Mount",MOUNTING:"Mounting",MOUNTED:"Mounted"};
// Explicit transition behaviour, so a relationship-changing technique is never
// mistaken for ordinary movement and never blocked by the Mount-access gate.
const TRANSITION={ENTRY:"StandingGrappleEntry",TO_MOUNT:"TransitionToMount",VOLUNTARY_BOTTOM:"VoluntaryMounted",REPOSITION:"RelationshipReposition"};
const isMountRole=r=>r===REL.MOUNTING||r===REL.MOUNTED;
const isStandingRole=r=>r===REL.GRAPPLING||r===REL.GRAPPLED;
const inRelationship=r=>r&&r!==REL.FREE;

const NA=MOUNT_ACCESS.NEITHER,MO=MOUNT_ACCESS.MOUNTING_ONLY,MD=MOUNT_ACCESS.MOUNTED_ONLY,BO=MOUNT_ACCESS.BOTH;
// scope|ability → {access, req, transition, submission, positionalDc}
// Anything absent from this table is UNAUDITED: it receives no per-ability Mount
// override and must NOT become automatically illegal (Sheet: "Blank/unaudited content").
const POSITIONAL_RULES={
  "Martial|Boxing":{
    "Boxing Stance":{access:NA},"Jab-Cross":{access:NA},"Uppercut":{access:NA},"Haymaker":{access:NA},
    "Bob and Weave":{access:NA},"Defensive Stance":{access:NA},
    "Dirty Boxing":{access:NA,req:REQ.STANDING},"Body Shot":{access:NA},
  },
  "Martial|MuayThai":{
    "Muay Thai Stance":{access:BO},"Jab-Cross":{access:NA},"Uppercut":{access:NA},
    // Kicks need standing balance and distance a standing grapple denies (owner call,
    // 2026-08-15) — Elbow Strike and Knee Strikes are close-range and stay unaffected.
    "Roundhouse Kick":{access:NA,noStanding:true},"Teep Kick":{access:NA,noStanding:true},"Elbow Strike":{access:BO},
    "Calf Kick":{access:NA,positionalDc:true,noStanding:true},
    // Mount access is an explicit override of the standing-grapple prerequisite text.
    "Knee Strikes":{access:BO,req:REQ.STANDING},
  },
  "Martial|Judo":{
    "Judo Stance":{access:BO},
    "Judo Chop":{access:NA},
    "Hip Toss":{access:NA,req:REQ.STANDING},
    "Rolling Throw":{access:NA,req:REQ.STANDING,transition:TRANSITION.REPOSITION},
    "Sweeping Shoulder":{access:NA,req:REQ.STANDING,transition:TRANSITION.TO_MOUNT},
    "Cross Choke":{access:MO,req:REQ.MOUNTING,submission:true},
    "Hip Escape":{access:MD,req:REQ.MOUNTED},
  },
  "Martial|JiuJitsu":{
    "Jiu-Jitsu Stance":{access:BO},
    "Pull Guard":{access:NA,req:REQ.STANDING,transition:TRANSITION.VOLUNTARY_BOTTOM},
    "Strangle":{access:BO,req:REQ.MOUNT,submission:true},
    "Flying Triangle":{access:NA,req:REQ.STANDING,transition:TRANSITION.TO_MOUNT,submission:true},
    "Arm bar":{access:BO,req:REQ.MOUNT,submission:true},
  },
  "Martial|Karate":{
    "Karate Stance":{access:NA},"Karate Blitz":{access:NA},
    // Kicks need standing balance and distance a standing grapple denies (owner call,
    // 2026-08-15) — Hammer Fist is a strike, not a kick, and stays unaffected.
    "Sweeping Low":{access:NA,noStanding:true},"Side Kick":{access:NA,noStanding:true},
    "Horse Stance":{access:NA},"Hammer Fist":{access:NA},"Whirlwind Kick":{access:NA,noStanding:true},
  },
  "Martial|Wrestling":{
    "Wrestling Stance":{access:BO},
    "Single Leg Shot":{access:NA,transition:TRANSITION.ENTRY},
    "Sumo Palm":{access:MO},
    "Wrestler's Prowess":{access:BO},
    "Suplex":{access:NA,req:REQ.STANDING,transition:TRANSITION.TO_MOUNT},
    "Choke Slam":{access:NA,req:REQ.STANDING},
    // Owner-authored 2026-08-15, not yet in the Sheet's Positional Rules tab.
    "Ground and Pound":{access:MO,req:REQ.MOUNTING},
    "Reversal":{access:MD,req:REQ.MOUNTED,transition:TRANSITION.TO_MOUNT,escape:true},
  },
  "Martial|Shared":{"Clinch":{access:NA,transition:TRANSITION.ENTRY}},
  "Weapon|Kenjutsu":{
    "Kenjutsu Stance":{access:NA},"Kenjutsu Slash":{access:NA},"Parry":{access:NA},
    "Hilt Bash":{access:NA},"Precision Thrust":{access:NA},
  },
  "Weapon|Kyudo":{"Kyudo Stance":{access:NA},"Kyudo Shot":{access:NA},"Arrow Rain":{access:NA},
    "Double Nock":{access:NA},"Achilles Shot":{access:NA},"Called Shot":{access:NA}},
  "Weapon|KyoketsuShoge":{
    "Kyoketsu-Shoge Stance":{access:BO},
    // Directional standing exception: Grappling only, never Grappled, no Mount access.
    "Blade Throw":{access:NA,req:REQ.GRAPPLING},
    "Kusari Chain Snare":{access:NA,transition:TRANSITION.ENTRY},
    "Chain Yank":{access:NA,req:REQ.STANDING},
    "Sickle Strike":{access:BO},
    "Cord Garrote":{access:BO,req:REQ.MOUNT,submission:true},
  },
  "Sign|Aries":{"Shatter Punch":{access:MO}},
  "Sign|Leo":{"Sun Palm":{access:BO}},
  "Sign|Taurus":{"Iron Fist":{access:MO}},
  "Sign|Virgo":{"Silica Strike":{access:BO},"Wither Palm":{access:MO}},
  "Sign|Capricorn":{"Diamond Cutter":{access:BO}},
  "Sign|Aquarius":{"Nerve Disruptor":{access:BO,positionalDc:true},"Shock Palm":{access:BO}},
  "Sign|Libra":{"Aero Palm":{access:NA}},
  "Sign|Gemini":{"Echo Fist":{access:BO}},
  "Sign|Cancer":{"Hydro Cannon Palm":{access:MO}},
  // Numbing Strike's base save DC is NOT finalised; only the positional hook is wired.
  "Sign|Scorpio":{"Numbing Strike":{access:BO,positionalDc:true},"Kidney Shot":{access:MO}},
  "Sign|Pisces":{"Flow Strike":{access:NA}},
};
const UNAUDITED_POS=Object.freeze({access:null,req:null,transition:null,submission:false,positionalDc:false,escape:false,noStanding:false,audited:false});
function positionalMetaFor(scope,name){
  const row=POSITIONAL_RULES[scope]&&POSITIONAL_RULES[scope][name];
  if(!row)return UNAUDITED_POS;
  return Object.freeze({access:row.access||null,req:row.req||null,transition:row.transition||null,
    submission:!!row.submission,positionalDc:!!row.positionalDc,escape:!!row.escape,noStanding:!!row.noStanding,audited:true,scope});
}
// Stamp structured positional metadata onto a catalog ability (build-time join).
function withPos(ab,scope){ab.pos=positionalMetaFor(scope,ab.name);return ab;}

const E={
  dmg:p=>({k:"Damage",power:p}),st:(status,dur,tick=0,stacks=1)=>({k:"Status",status,dur,stacks,tick}),
  save:(status,dur,stat,dc,tick=0,stacks=1)=>({k:"Status",status,dur,stacks,tick,save:{stat,dc}}),
  mc:m=>({k:"MC",amt:m}),move:t=>({k:"Move",tiles:t}),heal:p=>({k:"Heal",power:p}),
  res:(res,amt,pct=0,overcap=false)=>({k:"Res",res,amt,pct,overcap}),buff:(stat,pct,dur)=>({k:"Buff",stat,pct,dur}),
  // Applies to the OWNER, not the target — the only effect kind that does. Used for combo
  // setups: a landed hit marks the user (not the foe) for a bonus their NEXT relevant action
  // consumes. Piggybacks on the ordinary hit/evade roll — applyEffects only runs on a hit, so
  // "if it lands" needs no extra check here.
  selfMark:(mark,dur,mag=0)=>({k:"SelfMark",mark,dur,mag}),
  grapple:(crush,resistStat,dc,dur,drain=0,lifesteal=false)=>({k:"Grapple",crush,resistStat,dc,dur,drain,lifesteal}),
  gtech:o=>({k:"GrappleTech",power:o.power||0,dc:o.dc||8,dur:o.dur||0,status:o.status||null,best:!!o.best,mount:!!o.mount,breakHold:!!o.breakHold,throw:o.throw||0,behind:!!o.behind,drain:o.drain||0,selfAgi:o.selfAgi||0,
    voluntaryBottom:!!o.voluntaryBottom,submission:!!o.submission,focusLock:o.focusLock||0,reversal:!!o.reversal}),
  // Takedown (Hip Toss, per the abilities sheet: "Prone 1rd; breaks the hold"): on a landed hit the target is thrown
  // to the cell `behind` hexes past the user on the far side from where it stood (user ruling 2026-10-15), Prone, and
  // the hold ends.
  takedown:(status,dur,behind=1)=>({k:"Takedown",status,dur,behind}),
  summon:()=>({k:"SpawnSummon",tier:"Guardian"}),haunt:()=>({k:"Haunt"}),eye:planet=>({k:"ActivateEye",planet}),
  // trigger: effects re-applied to whoever occupies the cell (placement instant, then every
  // round they remain, or whenever a fighter later steps onto it) — a lingering ground hazard
  // rather than a one-shot burst. Omit for inert cover terrain (Wall/Smoke).
  terrain:(kind,dur,trigger=null)=>({k:"Terrain",kind,dur,trigger}),wardNext:()=>({k:"WardNext"}),
  // Displaces the TARGET away from the owner, unconditional on a landed hit — no separate
  // save. Distinct from "move" above, which repositions the OWNER relative to a reference.
  push:tiles=>({k:"Push",tiles}),
};
function mk(o){o.id="A"+(ABID++);o.minR=o.minR??0;o.radius=o.radius??0;o.tags=o.tags||[];o.poiseMult=o.poiseMult||1;o.supply=o.supply||0;o.stamPct=o.stamPct||0;o.chakraPct=o.chakraPct||0;o.needsLoS=o.needsLoS??(o.atk==="Projectile"||o.atk==="Magic"||o.atk==="GenVisual");return o;}
// stamPct/chakraPct cost a % of the CASTER's own max pool instead of (or on top of) a flat
// number — Recompose is percent-only (0 flat + 10% max each) so it stays meaningful at every
// level, unlike a fixed number that gets trivial as max pools grow.
const pctCost=(ab,owner)=>({stam:round((ab.stamPct||0)*owner.maxStam),chakra:round((ab.chakraPct||0)*effMaxChakra(owner))});
function guardBreak(a){a.poiseMult=1.5;return a;}
function reskin(a,name,group){const c={...a,name,effects:a.effects.map(e=>({...e})),tags:[...a.tags]};if(group)c.group=group;c.id="A"+(ABID++);return c;}

const tai=(g,name,power,slots,stam,tags,...e)=>mk({group:g,disc:"Taijutsu",name,atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots,stam,chakra:0,tags,effects:[E.dmg(power),...e]});
const taiReach=(g,name,power,slots,stam,tags,...e)=>mk({group:g,disc:"Taijutsu",name,atk:"Melee",dmg:"Physical",maxR:1,reach:2,targeting:"SingleEnemy",slots,stam,chakra:0,tags,effects:[E.dmg(power),...e]});
const taiTrue=(g,name,power,slots,stam,tags,...e)=>mk({group:g,disc:"Taijutsu",name,atk:"Melee",dmg:"True",maxR:1,targeting:"SingleEnemy",slots,stam,chakra:0,tags,effects:[E.dmg(power),...e]});
const stanceZ=(g,name,slots,stam,tags,...e)=>mk({group:g,disc:"Taijutsu",name,atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots,stam,chakra:0,tags:["Stance",...tags],effects:e});
const nin=(g,name,power,slots,chakra,tags,...e)=>mk({group:g,disc:"Ninjutsu",name,atk:"Projectile",dmg:"Elemental",maxR:10,targeting:"SingleEnemy",slots,stam:0,chakra,tags,effects:[E.dmg(power),...e]});
const ninTrue=(g,name,power,slots,chakra,tags,...e)=>mk({group:g,disc:"Ninjutsu",name,atk:"Projectile",dmg:"Mental",maxR:10,targeting:"SingleEnemy",slots,stam:0,chakra,tags,effects:[E.dmg(power),...e]});
const ninZone=(g,name,power,slots,chakra,tags,...e)=>mk({group:g,disc:"Ninjutsu",name,atk:"Magic",dmg:"Elemental",maxR:10,targeting:"PointRadius",slots,stam:0,chakra,tags,effects:[E.dmg(power),...e]});
const ninSelf=(g,name,slots,chakra,tags,...e)=>mk({group:g,disc:"Ninjutsu",name,atk:"Magic",dmg:"None",maxR:1,targeting:"Self",slots,stam:0,chakra,tags,effects:e});
const gen=(g,name,saveStat,dc,status,dur,tick=0)=>mk({group:g,disc:"Genjutsu",name,atk:"GenVisual",dmg:"None",maxR:6,targeting:"SingleEnemy",slots:1,stam:0,chakra:18,tags:[],effects:[E.save(status,dur,saveStat,dc,tick)]});

const KITS={
  Aries:{tai:[tai("Taijutsu","Mach Lunge",14,1,10,["Priority","GapCloser"],E.mc(8),E.st("Burn",1,4)),guardBreak(tai("Taijutsu","Shatter Punch",20,1,12,[],E.save("Stun",1,"FORT",13))),stanceZ("Taijutsu","Inner Gate: Adrenaline",1,10,[],E.buff("AGI",30,3),E.buff("STR",10,3),E.st("Burn",3,3))],
    nin:[ninZone("Ninjutsu","Blast Wave",8,1,18,[]),nin("Ninjutsu","Explosive Runes",12,1,18,["Trap"]),ninZone("Ninjutsu","Meteor",35,2,40,["Ultimate","Charge"])],
    gen:[gen("Genjutsu","Blind Rage","INT",12,"Confusion",1),gen("Genjutsu","Killing Intent","STR",13,"Stun",1)]},
  Leo:{tai:[stanceZ("Taijutsu","King's Posture",1,8,[],E.buff("FORT",30,3)),tai("Taijutsu","Sun Palm",14,1,8,[],E.st("Burn",2,4)),tai("Taijutsu","Battle Roar",10,1,10,[],E.save("Slow",2,"STR",12))],
    nin:[nin("Ninjutsu","Solar Lance",22,1,25,[]),ninSelf("Ninjutsu","Radiance",2,20,["Stance"],E.buff("STR",10,3)),ninZone("Ninjutsu","Supernova",30,2,30,["Ultimate"])],
    gen:[gen("Genjutsu","Spotlight","INT",12,"Blind",1),gen("Genjutsu","Kneel","STR",14,"Stun",1)]},
  Sagittarius:{tai:[tai("Taijutsu","Spinning Top",8,1,12,[],E.res("Chakra",-15)),stanceZ("Taijutsu","Flow Dodge",1,8,[],E.buff("AGI",30,2),E.mc(5)),tai("Taijutsu","Leash Kick",12,1,10,[],E.save("Root",2,"AGI",12))],
    nin:[nin("Ninjutsu","Wisp Fire",10,1,15,[]),ninSelf("Ninjutsu","Cauterize",1,25,[],E.heal(15))],
    gen:[gen("Genjutsu","Dogma","INT",13,"Confusion",2),gen("Genjutsu","Soul Pressure","STR",12,"Silence",3)]},
  Taurus:{tai:[stanceZ("Taijutsu","Mountain Stance",1,8,[],E.buff("FORT",30,3)),tai("Taijutsu","Iron Fist",16,1,10,[],E.save("Slow",1,"FORT",12)),tai("Taijutsu","Bull Rush",14,1,12,["GapCloser","Priority"],E.mc(6))],
    nin:[ninSelf("Ninjutsu","Oak Flesh",2,18,[],E.buff("FORT",50,3)),ninSelf("Ninjutsu","Ironwood Kanabo",2,18,[],E.buff("STR",20,3)),ninSelf("Ninjutsu","Root Sanctuary",2,22,[],E.buff("FORT",20,2))],
    gen:[gen("Genjutsu","Material Fixation","INT",12,"Disarm",3),gen("Genjutsu","Planetary Pressure","STR",13,"Slow",2)]},
  Virgo:{tai:[tai("Taijutsu","Silica Strike",8,1,6,[],E.save("Blind",3,"INT",12)),stanceZ("Taijutsu","Flowing Sand Parry",1,8,["Counter"],E.buff("AGI",20,1)),tai("Taijutsu","Wither Palm",12,1,12,[],E.res("Stamina",-15))],
    nin:[ninZone("Ninjutsu","Sand Burial",22,1,22,[]),ninZone("Ninjutsu","Sandstorm",10,2,22,[],E.save("Blind",2,"INT",12),E.st("Bleed",2,4))],
    gen:[gen("Genjutsu","Phantom Plague","INT",12,"Psychosomatic",3,4),gen("Genjutsu","Coffin Syndrome","STR",13,"Confusion",1)]},
  Capricorn:{tai:[guardBreak(tai("Taijutsu","Adamantine Shin",16,1,12,[],E.st("Bleed",2,3))),taiTrue("Taijutsu","Diamond Cutter",14,1,10,[]),stanceZ("Taijutsu","Prismatic Skin",1,8,[],E.buff("FORT",50,2))],
    nin:[ninZone("Ninjutsu","Geode Blast",18,1,20,[]),nin("Ninjutsu","Mausoleum",6,1,22,[],E.save("Stun",2,"FORT",14)),ninZone("Ninjutsu","Stalactite Rain",30,2,30,["Ultimate","Charge"])],
    gen:[gen("Genjutsu","Atlas's Regret","STR",13,"Slow",2),gen("Genjutsu","Titan's Gaze","INT",12,"Slow",2)]},
  Aquarius:{tai:[tai("Taijutsu","Nerve Disruptor",10,1,8,[],E.save("Silence",1,"CHA",12)),stanceZ("Taijutsu","Static Shell",1,8,["Counter"],E.buff("FORT",10,1)),tai("Taijutsu","Shock Palm",16,1,12,[])],
    nin:[ninZone("Ninjutsu","Voltaic Orb",14,1,20,[]),ninTrue("Ninjutsu","Lightning Cutter",24,1,25,["Priority","GapCloser"],E.mc(6)),ninZone("Ninjutsu","EMP Field",6,2,22,[],E.save("Slow",2,"INT",12))],
    gen:[gen("Genjutsu","System Crash","STR",13,"Blind",2),gen("Genjutsu","Lag Switch","INT",12,"Slow",2)]},
  Libra:{tai:[taiReach("Taijutsu","Aero Palm",12,1,8,[],E.st("Bleed",2,3)),stanceZ("Taijutsu","Flow Parry",1,8,["Counter"],E.buff("AGI",20,1)),stanceZ("Taijutsu","Feather Step",1,6,[],E.buff("AGI",20,2),E.mc(5))],
    nin:[nin("Ninjutsu","Gale Slicer",16,1,18,[]),ninZone("Ninjutsu","Pressure Blast",8,1,18,[]),ninZone("Ninjutsu","Singularity Sphere",12,2,25,[],E.save("Root",1,"STR",12))],
    gen:[gen("Genjutsu","Indecision","INT",12,"Silence",1),gen("Genjutsu","Vertigo","STR",13,"Blind",2)]},
  Gemini:{tai:[stanceZ("Taijutsu","Mach Dash",1,8,[],E.mc(15),E.buff("AGI",10,1)),tai("Taijutsu","Echo Fist",14,1,10,[]),tai("Taijutsu","Sonic Sweep",10,1,12,[],E.save("Prone",1,"AGI",12))],
    nin:[ninZone("Ninjutsu","Howling Blast",8,1,18,[],E.save("Silence",1,"INT",12)),ninSelf("Ninjutsu","Mirage Clone",1,18,[],E.buff("AGI",50,2)),ninZone("Ninjutsu","Resonance Chamber",6,2,22,[])],
    gen:[gen("Genjutsu","Tinnitus","STR",12,"Bleed",3,4),gen("Genjutsu","Phantom Legion","INT",12,"Blind",1)]},
  Cancer:{tai:[tai("Taijutsu","Tidal Slam",16,1,12,["GapCloser"],E.mc(6),E.save("Slow",1,"FORT",12)),tai("Taijutsu","Vice Grip",12,1,12,[],E.res("Stamina",-15)),tai("Taijutsu","Hydro Cannon Palm",14,1,10,[],E.save("Stun",1,"STR",13))],
    nin:[nin("Ninjutsu","Water Cutter",20,1,22,[]),ninZone("Ninjutsu","Whirlpool",8,2,22,[],E.save("Root",1,"STR",12)),ninZone("Ninjutsu","Tsunami",28,2,30,["Ultimate","Charge"])],
    gen:[gen("Genjutsu","Regression","INT",12,"Slow",2),gen("Genjutsu","Pacification","STR",13,"Disarm",2)]},
  Scorpio:{tai:[tai("Taijutsu","Numbing Strike",14,1,8,[],E.st("Slow",2)),stanceZ("Taijutsu","Shadow Step",1,8,["Priority","GapCloser"],E.mc(10),E.st("Stealth",1)),tai("Taijutsu","Kidney Shot",16,1,10,[])],
    nin:[nin("Ninjutsu","Ice Shard",10,1,12,["Priority"]),ninSelf("Ninjutsu","Frost Armor",2,18,[],E.buff("FORT",20,2)),ninZone("Ninjutsu","Blizzard",10,2,25,[],E.save("Slow",2,"INT",12))],
    gen:[gen("Genjutsu","Paranoia","STR",13,"Confusion",2),gen("Genjutsu","Betrayal","INT",13,"Confusion",1)]},
  Pisces:{tai:[stanceZ("Taijutsu","Evasive Sway",1,8,[],E.buff("AGI",50,2)),stanceZ("Taijutsu","Slide Counter",1,8,["Counter"],E.mc(6)),taiTrue("Taijutsu","Flow Strike",14,1,10,[])],
    nin:[nin("Ninjutsu","Bubble Prison",6,1,22,[],E.save("Stun",2,"CHA",14)),ninSelf("Ninjutsu","Hidden Mist",1,20,[],E.st("Stealth",2)),nin("Ninjutsu","Water Dragon",22,1,25,[])],
    gen:[gen("Genjutsu","Siren's Lure","STR",13,"Fear",1),gen("Genjutsu","Escapism","INT",13,"Sleep",2)]},
};
function zodiacAbilities(sign){const k=KITS[sign];return[...k.tai,...k.nin,...k.gen].map(a=>withPos({...a,effects:a.effects.map(e=>({...e})),tags:[...a.tags],kitSign:sign,id:"A"+(ABID++)},"Sign|"+sign));}

function generalArts(){
  const g=o=>mk({group:o.group||"General",disc:o.disc,name:o.name,atk:o.atk,dmg:o.dmg,maxR:o.maxR??1,minR:0,targeting:o.tg,slots:o.slots||1,stam:o.stam||0,chakra:o.chakra||0,stamPct:o.stamPct||0,chakraPct:o.chakraPct||0,tags:o.tags||[],radius:o.radius||0,supply:o.supply||0,healOutputMult:o.healOutputMult??1,effects:o.fx});
  const L=[];
  L.push(g({disc:"Ninjutsu",name:"Chakra Bullet",atk:"Projectile",dmg:"Elemental",maxR:10,tg:"SingleEnemy",chakra:12,fx:[E.dmg(14)]}));
  // Canonical Focus behaviour: restore 20% of the channel's max pool, grant NO poise.
  L.push(g({disc:"Ninjutsu",name:"Charge Chakra",atk:"Magic",dmg:"None",tg:"Self",tags:["Focus"],fx:[E.res("Chakra",0,BAL.focusRestorePercent)]}));
  L.push(g({disc:"Taijutsu",name:"Catch Breath",atk:"Melee",dmg:"None",tg:"Self",tags:["Focus"],fx:[E.res("Stamina",0,BAL.focusRestorePercent)]}));
  // Third Focus action (2026-08-16, owner sheet update): unlike the two above, Recompose isn't
  // free — it costs a % of the caster's own max Stamina/Chakra to buy back Poise, the one pool
  // Focus never used to touch.
  L.push(g({disc:"Taijutsu",name:"Recompose",atk:"Melee",dmg:"None",tg:"Self",stamPct:BAL.recomposeCostPercent,chakraPct:BAL.recomposeCostPercent,tags:["Focus"],fx:[E.res("Poise",0,BAL.focusRestorePercent)]}));
  L.push(guardBreak(g({disc:"Taijutsu",name:"Iron Mountain",atk:"Melee",dmg:"Physical",tg:"SingleEnemy",stam:10,fx:[E.dmg(16)]})));
  L.push(g({disc:"Taijutsu",name:"Heavenly Kick",atk:"Melee",dmg:"Physical",tg:"SingleEnemy",stam:10,fx:[E.dmg(12),E.save("Stun",1,"FORT",13)]}));
  L.push(g({disc:"Ninjutsu",name:"Guardian Barrier",atk:"Magic",dmg:"None",tg:"AlliesInRadius",radius:4,chakra:18,fx:[E.st("Fortified",2,20)]}));
  L.push(g({disc:"Ninjutsu",name:"Solar Flare",atk:"Magic",dmg:"Elemental",maxR:3,tg:"SingleEnemy",chakra:15,fx:[E.dmg(6),E.st("Blind",1)]}));
  L.push(g({disc:"Taijutsu",name:"Viper Strike",atk:"Melee",dmg:"Physical",tg:"SingleEnemy",stam:8,fx:[E.dmg(8),E.st("Bleed",3,4)]}));
  L.push(g({disc:"Ninjutsu",name:"Chakra Drain",atk:"Magic",dmg:"Elemental",maxR:6,tg:"SingleEnemy",chakra:12,fx:[E.dmg(8),E.res("Chakra",-15)]}));
  L.push(g({disc:"Ninjutsu",name:"Gloom Shroud",atk:"Magic",dmg:"None",tg:"Self",chakra:18,fx:[E.st("Stealth",2)]}));
  L.push(g({disc:"Ninjutsu",name:"Earth Wall",atk:"Magic",dmg:"None",maxR:6,tg:"PointRadius",radius:2,chakra:20,fx:[E.terrain("Wall",3)]}));
  L.push(g({disc:"Ninjutsu",name:"Shadow Possession",atk:"Magic",dmg:"None",maxR:6,tg:"SingleEnemy",chakra:20,fx:[E.grapple(3,"FORT",13,2)]}));
  L.push(g({group:"Medical",disc:"Medical",name:"Palm Healing",atk:"Magic",dmg:"None",maxR:1,tg:"SingleAlly",chakra:25,healOutputMult:BAL.palmHealingOutputMult,fx:[E.heal(15)]}));
  L.push(g({group:"Medical",disc:"Medical",name:"Cellular Activation",atk:"Magic",dmg:"None",maxR:6,tg:"SingleAlly",chakra:18,fx:[E.st("Regen",3,8)]}));
  L.push(g({group:"Medical",disc:"Medical",name:"Chakra Transfer",atk:"Magic",dmg:"None",maxR:6,tg:"SingleAlly",fx:[E.res("Chakra",25)]}));
  L.push(g({group:"Medical",disc:"Medical",name:"Chakra Scalpel",atk:"Melee",dmg:"True",tg:"SingleEnemy",stam:8,fx:[E.dmg(8),E.save("Slow",2,"AGI",12)]}));
  L.push(g({group:"Medical",disc:"Medical",name:"Nerve Rupture",atk:"Melee",dmg:"None",tg:"SingleEnemy",stam:8,fx:[E.save("Confusion",1,"INT",13)]}));
  L.push(g({group:"Trap",disc:"Trap",name:"Explosive Tag",atk:"Magic",dmg:"Elemental",maxR:8,tg:"PointRadius",radius:1,chakra:15,tags:["Trap"],supply:1,fx:[E.dmg(16)]}));
  L.push(g({group:"Trap",disc:"Trap",name:"Flash Bomb",atk:"Magic",dmg:"None",maxR:8,tg:"PointRadius",radius:1,chakra:12,tags:["Priority","Trap"],supply:1,fx:[E.st("Blind",1)]}));
  // Owner-approved hazard spec (2026-08-14): 3-round lingering hazard, re-applying its damage
  // + status every round to whoever's standing in it. The per-round Root was explicitly
  // dropped — pinning someone in place every single round for the hazard's whole duration
  // was too oppressive, so only Bleed carries.
  L.push(g({group:"Trap",disc:"Trap",name:"Spike Pit",atk:"Magic",dmg:"Physical",maxR:5,tg:"PointRadius",radius:1,chakra:12,tags:["Trap"],supply:1,fx:[E.terrain("Spikes",3,[E.dmg(6),E.st("Bleed",1,3)])]}));
  L.push(g({group:"Trap",disc:"Trap",name:"Smoke Screen",atk:"Magic",dmg:"None",maxR:6,tg:"PointRadius",radius:2,chakra:12,tags:["Trap"],supply:1,fx:[E.terrain("Smoke",2)]}));
  L.push(g({group:"Trap",disc:"Trap",name:"Smoke Bomb",atk:"Magic",dmg:"None",tg:"Self",chakra:10,fx:[E.st("Stealth",2)]}));
  L.push(g({group:"Trap",disc:"Trap",name:"Caltrops",atk:"Magic",dmg:"Physical",maxR:5,tg:"PointRadius",radius:1,chakra:10,tags:["Trap"],supply:1,fx:[E.terrain("Caltrops",3,[E.dmg(4),E.save("Slow",1,"AGI",11)])]}));
  L.push(g({group:"Summon",disc:"Summon",name:"Summon Companion",atk:"Magic",dmg:"None",tg:"Self",chakra:50,fx:[E.summon()]}));
  L.push(g({group:"Genjutsu",disc:"Genjutsu",name:"Phantom Haunt",atk:"GenVisual",dmg:"None",maxR:6,tg:"SingleEnemy",slots:2,chakra:45,fx:[E.haunt()]}));
  return L;
}
/* Martial + Weapon catalogs. Names, powers, slots and base resources follow the
   canonical Google Sheet ("Live Canonical Roster" numbers, "Martial & Weapon
   Styles" authored identity); relationship legality comes from POSITIONAL_RULES. */
function martialStyles(){
  const t=(name,power,stam,tags,...e)=>mk({group:"Martial",disc:"Martial",name,atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots:1,stam,chakra:0,tags,effects:[E.dmg(power),...e]});
  const tSelf=(name,stam,tags,...e)=>mk({group:"Martial",disc:"Martial",name,atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots:1,stam,chakra:0,tags,effects:e});
  const stance=(name)=>mk({group:"Martial",disc:"Martial",name,atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots:1,stam:4,chakra:0,tags:["Stance","MartialStance"],effects:[E.res("Poise",0)]});
  const clinch=()=>mk({group:"Martial",disc:"Martial",name:"Clinch",atk:"Melee",dmg:"None",maxR:1,targeting:"SingleEnemy",slots:1,stam:15,chakra:0,tags:[],effects:[E.grapple(0,"AGI",13,5)]});
  const gfu=(name,stam,tech)=>mk({group:"Martial",disc:"Martial",name,atk:"Melee",dmg:tech.dmgType||(tech.power?"Physical":"None"),maxR:1,targeting:"SingleEnemy",slots:tech.slots||1,stam,chakra:0,tags:tech.tags||[],effects:[E.gtech(tech)]});
  const poise2=a=>{a.poiseMult=2;a.poiseCap=2;return a;};
  // "Guard Break only while in clinch": 1.5x poise damage while the user is the Grappling controller.
  const clinchGuardBreak=a=>{a.poiseMultWhenGrappling=1.5;return a;};
  const slots=(a,n)=>{a.slots=n;return a;};
  const uppercut=()=>clinchGuardBreak(t("Uppercut",12,12,[]));
  // System 3: two real strikes instead of one hit standing in for two — see resolveComboStrikes
  // in af-core.js. Balance pass (base hit rate 75%): jab lands at 0.75, the cross's effective
  // landing rate is 0.75×(2-0.75)=0.9375 (auto-hit after a landed jab, or its own independent
  // roll after a miss/parry) — 4/5 split ≈ 7.6875 expected damage, a small reliability bump
  // over the old single hit's 10×0.75=7.5, not a buff. Stamina nudged 8→9 to match.
  const jabCross=()=>mk({group:"Martial",disc:"Martial",name:"Jab-Cross",atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots:1,stam:9,chakra:0,tags:["Combo"],effects:[E.dmg(4),E.dmg(5)]});
  const dirty=t("Dirty Boxing",20,25,[]);
  const knee=guardBreak(t("Knee Strikes",20,30,[]));
  const pullGuard=gfu("Pull Guard",10,{dc:14,best:true,mount:true,voluntaryBottom:true,selfAgi:30});pullGuard.tags.push("Priority");
  // Redesigned as a combo starter (2026-08-15): a landed hit marks the user for a bonus-DC
  // Clinch attempt this round, opening the exchange rather than filling it. 2 slots (not 3)
  // keeps the action-economy tax from swinging Judoka's win rate too hard in either direction.
  // No hard oncePerRound cap: a player may deliberately queue it twice (e.g. to level the
  // ability) even though the second copy's setup mark is wasted — the planner devalues an
  // already-marked repeat (see planFor's usedSetup tracking) so the AI never does this on its
  // own initiative, without making a second use illegal.
  const judoChop=slots(t("Judo Chop",10,10,[],E.save("Slow",1,"AGI",12),E.selfMark("GrappleSetup",1,1)),2);
  const karateBlitz=mk({group:"Martial",disc:"Martial",name:"Karate Blitz",atk:"Melee",dmg:"Physical",maxR:1,reach:2,targeting:"SingleEnemy",slots:1,stam:12,chakra:0,tags:["Priority","GapCloser"],effects:[E.dmg(13)]});
  const singleLeg=mk({group:"Martial",disc:"Martial",name:"Single Leg Shot",atk:"Melee",dmg:"None",maxR:1,reach:2,targeting:"SingleEnemy",slots:1,stam:15,chakra:0,tags:[],effects:[E.grapple(0,"AGI",13,3)]});
  // Hip Escape: no damage; drains the fighter currently Mounting this actor; once per round.
  const hipEscape=mk({group:"Martial",disc:"Martial",name:"Hip Escape",atk:"Melee",dmg:"None",maxR:1,targeting:"SingleEnemy",slots:2,stam:20,chakra:0,tags:["OncePerRound"],effects:[E.res("Stamina",-15)],oncePerRound:true});
  const styles={
    Boxing:{stance:stance("Boxing Stance"),moves:[jabCross(),uppercut(),guardBreak(t("Haymaker",10,10,[])),tSelf("Bob and Weave",15,[],E.buff("AGI",20,1)),tSelf("Defensive Stance",15,[],E.res("Poise",0,0.25,true)),clinch(),dirty,t("Body Shot",8,10,[],E.res("Stamina",-10))]},
    // Teep Kick's Guard Break is conditional now (System 3, 2026-08-25) — it's earned by
    // reading a Priority-tagged damaging rush, not a flat property of the move. See
    // teepAntiPriorityBonus (resolveRound) and matchClashRules for the two halves.
    MuayThai:{stance:stance("Muay Thai Stance"),moves:[jabCross(),uppercut(),t("Roundhouse Kick",12,10,[]),t("Teep Kick",10,12,[],E.save("Slow",1,"AGI",12)),t("Elbow Strike",10,10,[],E.save("Bleed",2,"AGI",12,3)),t("Calf Kick",10,12,[],E.save("Slow",2,"AGI",13)),clinch(),knee]},
    Judo:{stance:stance("Judo Stance"),moves:[clinch(),
      // Judo Chop (Shuto Uchi, the knife-hand strike) is Judo's atemi-waza entry — its only
      // fully free-standing strike, usable with no grapple set up at all. Costed identically
      // to Muay Thai's Elbow Strike (10p/10s) with Teep Kick's exact Slow rider, so it adds a
      // neutral-range option without introducing a new mechanic or a new number band.
      // Once per round (like Hip Escape): a single precise strike, not a combo filler — without
      // the cap the AI spams it in place of the Clinch -> Sweeping Shoulder -> Cross Choke
      // chain entirely, which would erase Judo's established Cross Choke identity.
      judoChop,
      // Hip Toss is a clean standing-grapple strike in Choke Slam's mold — lighter power,
      // but a far better Stamina-per-power ratio (1.0 vs Choke Slam's 1.56).
      guardBreak(t("Hip Toss",15,22,[],E.takedown("Prone",1,1))),
      gfu("Rolling Throw",10,{power:8,dc:8,throw:3,behind:true,breakHold:true}),
      gfu("Sweeping Shoulder",10,{power:6,dc:8,mount:true}),
      gfu("Cross Choke",13,{power:36,dc:13,dur:2,status:"Silence",best:true,slots:2,focusLock:1,submission:true}),
      hipEscape]},
    JiuJitsu:{stance:stance("Jiu-Jitsu Stance"),moves:[clinch(),pullGuard,
      gfu("Strangle",11,{power:38,dc:13,dur:2,status:"Silence",best:true,slots:2,focusLock:1,submission:true}),
      gfu("Flying Triangle",19,{power:38,dc:13,dur:2,status:"Silence",best:true,mount:true,slots:2,focusLock:1,submission:true}),
      gfu("Arm bar",11,{power:36,dc:13,dur:2,status:"Cripple",best:true,submission:true})]},
    // Karate damage pass (2026-08-17, owner call): power raised across the kit, stamina left
    // untouched — Hammer Fist and Karate Blitz got the biggest share (the intended combo's
    // actual damage dealers), Sweeping Low a smaller one (its job is the Prone opener, not
    // raw damage — keeping it modest was deliberate so a landed Prone doesn't also hit
    // disproportionately hard). Round-robin testing showed this shifts the AI's own picks
    // toward Blitz -> Sweeping Low -> Hammer Fist -> Side Kick instead of Sweeping Low/Side
    // Kick spam, without increasing Sweeping Low's usage frequency.
    Karate:{stance:stance("Karate Stance"),moves:[t("Sweeping Low",7,20,[],E.save("Prone",1,"AGI",12)),karateBlitz,t("Side Kick",10,10,[],E.push(1)),tSelf("Horse Stance",15,[],E.buff("STR",20,1)),guardBreak(t("Hammer Fist",16,10,[])),mk({group:"Martial",disc:"Martial",name:"Whirlwind Kick",atk:"Melee",dmg:"Physical",maxR:1,targeting:"PointRadius",radius:1,slots:1,stam:15,chakra:0,tags:[],effects:[E.dmg(15)]})]},
    // Sumo Palm stays the Wrestling technique. It is NOT renamed to Iron Fist — that rename
    // belongs to the Taurus Sign ability. Wrestler's Prowess is the temporary-STR technique
    // and is a separate ability from Wrestling Stance.
    // Sumo Palm dropped its True damage type (2026-08-15, owner call): it is now Physical, so
    // it is mitigated by the target's STR and now deals poise damage at the standard 1.0
    // ratio, both unlike before. Power was kept low to offset the new poise pressure.
    Wrestling:{stance:stance("Wrestling Stance"),moves:[singleLeg,clinch(),
      mk({group:"Martial",disc:"Martial",name:"Sumo Palm",atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots:2,stam:15,chakra:0,tags:[],effects:[E.dmg(8)]}),
      tSelf("Wrestler's Prowess",15,[],E.buff("STR",20,1)),
      // Standard Guard Break (1.5x), not the 2x ceiling — that's reserved for Choke Slam alone.
      guardBreak(gfu("Suplex",40,{power:30,dc:13,slots:3,mount:true})),
      poise2(guardBreak(slots(t("Choke Slam",32,40,[]),2))),
      // Top-position ground striking. Adds a Stamina-sap rider (2026-08-17, owner call) so it
      // pressures a pinned foe's ability to pay Mount escape/upkeep costs, giving it a reason
      // to matter beyond raw damage during Wrestling's often-brief Mount windows.
      slots(t("Ground and Pound",12,10,[],E.res("Stamina",-12)),2),
      /* Reversal flips the user from the bottom to the top of the Mount on a DC 10 STR+AGI
         contest. It reuses the ordinary mount transition — the user becoming the top fighter
         IS enterMount(user, opponent) — so the forced entry breaks the new bottom fighter's
         Poise and clears any submission layered over the old relationship. */
      gfu("Reversal",30,{dc:10,mount:true,reversal:true,slots:3})]},
  };
  for(const key of Object.keys(styles)){
    const scope="Martial|"+key;
    withPos(styles[key].stance,scope);
    styles[key].moves.forEach(m=>withPos(m,m.name==="Clinch"?"Martial|Shared":scope));
  }
  return styles;
}
function weaponKits(){
  const w=(name,power,atk,dmg,maxR,slots,stam,tags,...e)=>mk({group:"Weapon",disc:"Weapon",name,atk,dmg,maxR,targeting:"SingleEnemy",slots,stam,chakra:0,tags,effects:[E.dmg(power),...e]});
  const wSelf=(name,stam,tags,...e)=>mk({group:"Weapon",disc:"Weapon",name,atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots:1,stam,chakra:0,tags,effects:e});
  const stance=(name)=>mk({group:"Weapon",disc:"Weapon",name,atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots:1,stam:4,chakra:0,tags:["Stance","WeaponStance"],effects:[E.res("Poise",0)]});
  const chainSnare=mk({group:"Weapon",disc:"Weapon",name:"Kusari Chain Snare",atk:"Projectile",dmg:"None",maxR:6,targeting:"SingleEnemy",slots:1,stam:20,chakra:0,tags:[],effects:[E.grapple(0,"AGI",13,2)]});
  const arrowRain=mk({group:"Weapon",disc:"Weapon",name:"Arrow Rain",atk:"Projectile",dmg:"Physical",maxR:10,targeting:"PointRadius",radius:2,slots:2,stam:25,chakra:0,tags:[],effects:[E.dmg(10),E.save("Slow",1,"AGI",12)]});
  // Twin arrows nocked and loosed as one motion — Kyudo's answer to Jab-Cross: the same
  // Combo-tag two-strike shape, just at range.
  const doubleNock=mk({group:"Weapon",disc:"Weapon",name:"Double Nock",atk:"Projectile",dmg:"Physical",maxR:10,targeting:"SingleEnemy",slots:2,stam:16,chakra:0,tags:["Combo"],effects:[E.dmg(6),E.dmg(7)]});
  // Cuts the tendon, not the flesh — a heavier Slow than Kyudo Shot trades for, Kyudo's dedicated
  // answer to mobility.
  const achillesShot=w("Achilles Shot",10,"Projectile","Physical",10,2,20,[],E.save("Slow",2,"AGI",13));
  // Called Shot: a single ability that spans two rounds, same UX as the Ultimate "Charge" tag
  // (Meteor/Tsunami/etc.) but aimed at one locked target instead of erupting as an AoE at a
  // cell — see resolveAction's Charge branch and resolveRound's chargeBeam eruption path.
  // Picking it roots the archer while they draw (rootWhileCharging) — ordinary chip damage
  // landed during that round does NOT cancel the draw (only a poise-break stagger or hard CC
  // does, and both already cancel any queued action for free — see applyDamage's `broke` branch
  // and applyStatus's Prone handling), so the real risk of drawing is being caught flat-footed by
  // something that actually breaks you, not being punished for merely getting hit. It then
  // auto-fires next round for a guaranteed crit + poise floor (see applyDamage's `drawnShot`) and
  // pierces destructible cover (Tree/Bush) on its way to the target — see "Piercing" and Grid.losHard.
  const calledShot=mk({group:"Weapon",disc:"Weapon",name:"Called Shot",atk:"Projectile",dmg:"Physical",maxR:10,targeting:"SingleEnemy",slots:2,stam:20,chakra:0,tags:["Charge","Piercing"],chargeBeam:true,rootWhileCharging:true,effects:[E.dmg(14)]});
  // Kyoketsu-Shoge (formerly Kobudo): the sole weapon style with Mount access.
  const cordGarrote=mk({group:"Weapon",disc:"Weapon",name:"Cord Garrote",atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots:2,stam:25,chakra:0,tags:[],
    effects:[E.gtech({power:10,dc:12,dur:1,status:"Silence",best:true,focusLock:1,submission:true})]});
  const kits={
    Kenjutsu:{stance:stance("Kenjutsu Stance"),moves:[w("Kenjutsu Slash",12,"Melee","Physical",1,1,20,[],E.save("Bleed",2,"AGI",12,3)),wSelf("Parry",35,["Counter"],E.wardNext()),guardBreak(w("Hilt Bash",5,"Melee","Physical",1,2,25,[],E.save("Stun",1,"FORT",12))),guardBreak(w("Precision Thrust",10,"Melee","True",1,1,25,[]))]},
    Kyudo:{stance:stance("Kyudo Stance"),moves:[w("Kyudo Shot",15,"Projectile","Physical",10,1,20,[]),arrowRain,doubleNock,achillesShot,calledShot]},
    KyoketsuShoge:{stance:stance("Kyoketsu-Shoge Stance"),moves:[
      w("Blade Throw",5,"Projectile","Physical",3,1,15,[],E.save("Bleed",2,"AGI",12,3)),
      chainSnare,
      w("Chain Yank",5,"Projectile","Physical",6,1,25,[]),
      w("Sickle Strike",8,"Melee","Physical",1,1,15,[],E.save("Bleed",2,"AGI",11,3)),
      cordGarrote]},
  };
  for(const key of Object.keys(kits)){
    const scope="Weapon|"+key;
    withPos(kits[key].stance,scope);
    kits[key].moves.forEach(m=>withPos(m,scope));
  }
  return kits;
}
const MARTIAL=martialStyles(),WEAPONS=weaponKits();
const EYES={
  Sun:{deity:"Amaterasu",arch:"Sun / Sniper",jutsu:{name:"Yata Beam",atk:"Projectile",dmg:"True",maxR:10,tg:"SingleEnemy",fx:[E.dmg(18)]}},
  Moon:{deity:"Tsukuyomi",arch:"Moon / Counter",jutsu:{name:"Lunar Bind",atk:"GenVisual",dmg:"None",maxR:6,tg:"SingleEnemy",fx:[E.save("Stun",1,"INT",13)]}},
  Mars:{deity:"Hachiman",arch:"Mars / Duelist",jutsu:{name:"Death Line",atk:"Projectile",dmg:"True",maxR:6,tg:"SingleEnemy",fx:[E.dmg(20)]}},
  Mercury:{deity:"Omoikane",arch:"Mercury / Speed",jutsu:{name:"Lag Spike",atk:"Projectile",dmg:"True",maxR:10,tg:"SingleEnemy",fx:[E.dmg(12),E.mc(8)]}},
  Jupiter:{deity:"Daikokuten",arch:"Jupiter / Tank",jutsu:{name:"Grand Cross",atk:"Magic",dmg:"Elemental",maxR:6,tg:"SingleEnemy",fx:[E.dmg(8),E.save("Root",2,"STR",14)]}},
  Venus:{deity:"Benzaiten",arch:"Venus / Support",jutsu:{name:"Red String",atk:"GenVisual",dmg:"None",maxR:6,tg:"SingleEnemy",fx:[E.save("Snare",2,"INT",13)]}},
  Saturn:{deity:"Taizan",arch:"Saturn / Warden",jutsu:{name:"Gravity Well",atk:"Magic",dmg:"Elemental",maxR:8,tg:"PointRadius",radius:1,fx:[E.dmg(14),E.save("Snare",2,"STR",13)]}},
  Uranus:{deity:"Raijin",arch:"Uranus / Tech",jutsu:{name:"Polarity Switch",atk:"Magic",dmg:"Elemental",maxR:8,tg:"SingleEnemy",fx:[E.dmg(12),E.save("Confusion",1,"INT",13)]}},
  Neptune:{deity:"Ryujin",arch:"Neptune / Scout",jutsu:{name:"Sleep Walk",atk:"GenVisual",dmg:"None",maxR:6,tg:"SingleEnemy",fx:[E.save("Sleep",2,"INT",13)]}},
  Pluto:{deity:"Izanami",arch:"Pluto / Reaper",jutsu:{name:"Soul Rip",atk:"Magic",dmg:"True",maxR:6,tg:"SingleEnemy",fx:[E.dmg(14),E.res("Chakra",-20)]}},
};
const EYE_PLANETS=Object.keys(EYES);
function eyeAbilities(planet){const e=EYES[planet];
  const open=mk({group:"Dojutsu",disc:"Dojutsu",name:"Open "+e.deity,atk:"Magic",dmg:"None",maxR:1,targeting:"Self",slots:1,stam:0,chakra:40,tags:["EyeOpen"],effects:[E.eye(planet)],eyePlanet:planet});
  const j=e.jutsu;const jutsu=mk({group:"Dojutsu",disc:"Dojutsu",name:j.name,atk:j.atk,dmg:j.dmg,maxR:j.maxR,radius:j.radius||0,targeting:j.tg,slots:1,stam:0,chakra:15,tags:["EyeJutsu"],effects:j.fx.map(x=>({...x})),eyePlanet:planet});
  return[open,jutsu];}
const BLOODLINES={
  Blaze:{name:"Blaze Release: Kagutsuchi",kind:"Zone",power:30,fx:[E.st("Burn",3,6)]},Steel:{name:"Steel Release: Impervious",kind:"Self",fx:[E.st("Fortified",3,25),E.st("Shield",3,30)]},
  Typhoon:{name:"Typhoon Release: Skysplitter",kind:"Zone",power:24,fx:[E.save("Slow",2,"FORT",14)]},Abyss:{name:"Abyss Release: Drowning Dark",kind:"Zone",power:24,fx:[E.save("Root",2,"STR",14)]},
  Lava:{name:"Lava Release: Molten Field",kind:"Zone",power:28,fx:[E.st("Burn",2,5),E.save("Slow",2,"FORT",13)]},Scorch:{name:"Scorch Release: Solar Mummification",kind:"Bolt",power:26,fx:[E.save("Blind",2,"FORT",13)]},
  Boil:{name:"Boil Release: Corrosive Vapor",kind:"Bolt",power:24,fx:[E.res("Stamina",-15)]},Crystal:{name:"Crystal Release: Jade Bulwark",kind:"Self",fx:[E.st("Fortified",3,20),E.st("Shield",3,40)]},
  Magnet:{name:"Magnet Release: Iron Verdict",kind:"Bolt",power:16,fx:[E.save("Disarm",2,"STR",14)]},Wood:{name:"Wood Release: World Tree",kind:"Self",fx:[E.heal(25),E.st("Regen",3,8)]},
  Explosion:{name:"Explosion Release: Landmine Fist",kind:"Zone",power:34,fx:[]},Sand:{name:"Sand Release: Desert Shroud",kind:"Zone",power:20,fx:[E.save("Blind",2,"INT",13)]},
  Ice:{name:"Ice Release: Absolute Zero",kind:"Bolt",power:20,fx:[E.save("Stun",1,"FORT",14)]},Corrosion:{name:"Corrosion Release: Rust Plague",kind:"Bolt",power:18,fx:[E.st("Poison",3,6)]},
  Flux:{name:"Flux Release: Ebb Tide",kind:"Bolt",power:20,fx:[E.res("Chakra",-20)]},Storm:{name:"Storm Release: Laser Circus",kind:"Zone",power:26,fx:[E.save("Slow",2,"AGI",13)]},
};
const BLOOD_KEYS=Object.keys(BLOODLINES);
function bloodlineAbility(key){const b=BLOODLINES[key];const isZone=b.kind==="Zone",isSelf=b.kind==="Self";const fx=[];if(b.power)fx.push(E.dmg(b.power));fx.push(...b.fx.map(x=>({...x})));
  return mk({group:"Bloodline",disc:"Ninjutsu",name:b.name,atk:isSelf?"Magic":isZone?"Magic":"Projectile",dmg:isSelf?"None":"Elemental",maxR:isSelf?1:10,radius:isZone?3:0,targeting:isSelf?"Self":isZone?"PointRadius":"SingleEnemy",slots:2,stam:0,chakra:35,tags:["Ultimate"],effects:fx});}

/* summon species table (for chart-derived + companion) */
const SUMMON_STATS={Tank:{STR:10,AGI:6,FORT:14,INT:4,CHA:6},DPS:{STR:16,AGI:16,FORT:8,INT:6,CHA:6},Assassin:{STR:16,AGI:18,FORT:6,INT:6,CHA:6},Bleed:{STR:12,AGI:14,FORT:8,INT:6,CHA:6},Healer:{STR:6,AGI:8,FORT:8,INT:12,CHA:14},Support:{STR:8,AGI:10,FORT:10,INT:8,CHA:10},Scout:{STR:10,AGI:16,FORT:8,INT:6,CHA:6},Generic:{STR:10,AGI:10,FORT:10,INT:6,CHA:6}};
function summonAbilities(sp){const pow={DPS:16,Assassin:16,Tank:8,Bleed:10,Healer:6}[sp.role]||12;const fx=[E.dmg(pow)];if(sp.role==="Bleed")fx.push(E.st("Bleed",2,3));
  const list=[mk({group:"Summon",disc:"Summon",name:sp.name.split(" ")[0]+" Strike",atk:"Melee",dmg:"Physical",maxR:1,targeting:"SingleEnemy",slots:1,stam:0,chakra:0,tags:[],effects:fx})];
  if(sp.role==="Tank"||sp.role==="Support")list.push(mk({group:"Summon",disc:"Summon",name:sp.name.split(" ")[0]+" Bulwark",atk:"Melee",dmg:"None",maxR:1,targeting:"Self",slots:1,stam:0,chakra:0,tags:[],effects:[E.st("Fortified",1,sp.role==="Tank"?20:12),E.mc(2)]}));
  if(sp.role==="Healer")list.push(mk({group:"Summon",disc:"Summon",name:sp.name.split(" ")[0]+" Mend",atk:"Magic",dmg:"None",maxR:6,targeting:"SingleAlly",slots:1,stam:0,chakra:0,tags:[],effects:[E.heal(16)]}));
  return list;}

function applyLiveBalanceAbility(a){
  if(!BAL.useCandidateEconomy||!root.AFDC||typeof root.AFDC.primaryTier!=="function")return a;
  if(a.group==="Dojutsu"||a.group==="Bloodline"||a.disc==="Dojutsu")return a;
  const tier=root.AFDC.primaryTier(a);if(!tier)return a;
  a._authoredStam=a.stam||0;a._authoredChakra=a.chakra||0;a._authoredSlots=a.slots||1;a.balanceTier=tier;
  a.slots=max(a.slots||1,root.AFDC.candidateSlots(a,tier)||1);
  const dual=(a.stam||0)>0&&(a.chakra||0)>0;
  if(!dual){const r=root.AFDC.candidateResource(a,tier);if(r&&r.channel)a[r.channel]=max(a[r.channel]||0,r.suggestedAuthored||0);}
  return a;
}

function buildLoadout(opt){
  const L=[];const signs=opt.unlockAll?SIGNS:(opt.signs||[opt.sign]);const seen=new Set();
  for(const s of signs)for(const a of zodiacAbilities(s)){if(seen.has(a.group+a.name))continue;seen.add(a.group+a.name);L.push(a);}
  const learnedMedical=new Set(opt.learnedMedical||[]);
  for(const a of generalArts()){
    if((a.name==="Palm Healing"||a.name==="Cellular Activation")&&!learnedMedical.has(a.name))continue;
    L.push(a);
  }
  const martialKeys=(opt.martials&&opt.martials.length)?opt.martials:(opt.martial?[opt.martial]:[]);
  const addedMartials=new Set();
  for(const key of martialKeys){if(!MARTIAL[key]||addedMartials.has(key))continue;addedMartials.add(key);L.push(MARTIAL[key].stance);MARTIAL[key].moves.forEach(m=>L.push(m));}
  if(opt.weapon&&WEAPONS[opt.weapon]){L.push(WEAPONS[opt.weapon].stance);WEAPONS[opt.weapon].moves.forEach(m=>L.push(m));}
  const eyes=opt.unlockAll?EYE_PLANETS:(opt.eye?[opt.eye]:[]);
  for(const p of eyes)for(const a of eyeAbilities(p))L.push(a);
  const bloods=opt.unlockAll?BLOOD_KEYS:(opt.bloodline?[opt.bloodline]:[]);
  for(const k of bloods)L.push(bloodlineAbility(k));
  return L.map(a=>applyLiveBalanceAbility({...a,effects:a.effects.map(e=>({...e})),tags:[...a.tags],id:"A"+(ABID++)}));
}

/* =========================================================================
   PVE ENEMY ROSTER — themed loadouts reskinned from the player ability pool,
   each with a FocusDiscipline persona + stat archetype (list grows freely).
   ========================================================================= */
// pull one built ability by name from a sign kit / general / martial / weapon and reskin it
function fromKit(sign,name){for(const grp of["tai","nin","gen"])for(const a of KITS[sign][grp])if(a.name===name)return a;return null;}
function fromGeneral(name){return generalArts().find(a=>a.name===name);}
function fromMartial(style,name){return MARTIAL[style].moves.concat([MARTIAL[style].stance]).find(a=>a.name===name);}
function fromWeapon(kit,name){return WEAPONS[kit].moves.concat([WEAPONS[kit].stance]).find(a=>a.name===name);}
function R(src,newName){return reskin(src,newName,src.group);}

const ENEMIES={
  StreetThug:{name:"Street Thug",glyph:"🗡",focus:"Taijutsu",persona:"brute",element:"Earth",
    stats:{STR:11,AGI:8,FORT:10,INT:6,CHA:6},
    moves:()=>[R(fromMartial("Boxing","Jab-Cross"),"Street Jab"),R(fromMartial("Boxing","Haymaker"),"Wild Swing"),R(fromGeneral("Iron Mountain"),"Headbutt"),R(fromGeneral("Viper Strike"),"Rusty Shiv"),R(fromMartial("Boxing","Clinch"),"Grab")]},
  Bandit:{name:"Bandit",glyph:"🏹",focus:"Weapon",persona:"skirmisher",element:"Air",
    stats:{STR:9,AGI:12,FORT:8,INT:7,CHA:6},
    // Shuriken Throw is no longer canon (Kyoketsu-Shoge kit is Blade Throw / Snare / Yank / Sickle /
    // Garrote). The bandit keeps a ranged option by reskinning the Kyudo shot instead.
    moves:()=>[R(fromWeapon("Kyudo","Kyudo Shot"),"Thrown Knife"),R(fromWeapon("Kenjutsu","Kenjutsu Slash"),"Machete Slash"),R(fromGeneral("Caltrops"),"Scatter Nails"),R(fromGeneral("Smoke Bomb"),"Smoke Escape"),R(fromMartial("Boxing","Haymaker"),"Cheap Shot")]},
  // A defensive, disciplined counterpoint to StreetThug's reckless brute pressure: leans on
  // Kenjutsu's own Parry (Counter tag, wardNext) reskinned as a shield block, high FORT over
  // AGI, and Guardian Barrier for a Fortified buff — persona:"defensive" already has scoring
  // hooks (score()'s Fortified/Terrain branches favor it unconditionally for this persona).
  Guard:{name:"Guard",glyph:"🛡",focus:"Weapon",persona:"defensive",element:"Water",
    stats:{STR:10,AGI:7,FORT:14,INT:7,CHA:8},
    moves:()=>[R(fromWeapon("Kenjutsu","Kenjutsu Slash"),"Blade Strike"),R(fromWeapon("Kenjutsu","Parry"),"Shield Block"),R(fromWeapon("Kenjutsu","Hilt Bash"),"Shield Bash"),R(fromWeapon("Kenjutsu","Precision Thrust"),"Spear Thrust"),R(fromGeneral("Guardian Barrier"),"Hold the Line")]},
  /* One NPC per martial style. Each carries its OWN stance plus that style's full canonical
     kit under canonical names, so the positional matrix is directly observable in play and
     each style's real Mount access / relationship behaviour is exercised.

     `archetype` records the OWNER RULING that striking and grappling styles are deliberate
     counter-play to one another. Balance comparisons are only meaningful WITHIN an archetype:
     striking vs striking and grappling vs grappling. A striker losing to a grappler (or the
     reverse) is the intended matchup dynamic, never a balance defect. */
  // Stat-budget normalization (2026-08-17, owner ruling): style-vs-style balance testing must
  // hold total stat points EQUAL across every style NPC — kits differ in how they use a stat
  // spread, not in how much of one they get. All six now total exactly 48; each style keeps
  // its own relative shape (Wrestler still leans STR/FORT, Karateka still leans AGI, etc.),
  // only the totals were brought into line. Prior to this pass the totals ranged 44-49
  // (MuayThaiFighter 44 was the extreme outlier that skewed the Boxer matchup independent of
  // either kit's own numbers). Enforced going forward by a regression test requiring an exact
  // match, not just a tolerance band.
  Boxer:{name:"Boxer",glyph:"🥊",focus:"Martial",persona:"aggressive",element:"Fire",
    martial:"Boxing",archetype:"striking",stats:{STR:12,AGI:12,FORT:11,INT:6,CHA:7}},
  MuayThaiFighter:{name:"Muay Thai Fighter",glyph:"🥋",focus:"Martial",persona:"aggressive",element:"Fire",
    martial:"MuayThai",archetype:"striking",stats:{STR:12,AGI:12,FORT:11,INT:6,CHA:7}},
  Judoka:{name:"Judoka",glyph:"🎽",focus:"Martial",persona:"brute",element:"Earth",
    martial:"Judo",archetype:"grappling",stats:{STR:13,AGI:11,FORT:11,INT:7,CHA:6}},
  Jiujiteiro:{name:"Jiu-Jitsu Fighter",glyph:"🩱",focus:"Martial",persona:"skirmisher",element:"Water",
    martial:"JiuJitsu",archetype:"grappling",stats:{STR:11,AGI:13,FORT:10,INT:8,CHA:6}},
  Karateka:{name:"Karateka",glyph:"👘",focus:"Martial",persona:"assassin",element:"Air",
    martial:"Karate",archetype:"striking",stats:{STR:11,AGI:14,FORT:10,INT:7,CHA:6}},
  Wrestler:{name:"Wrestler",glyph:"🤼",focus:"Martial",persona:"brute",element:"Earth",
    martial:"Wrestling",archetype:"grappling",stats:{STR:14,AGI:10,FORT:12,INT:6,CHA:6}},
  Sorcerer:{name:"Sorcerer",glyph:"🔮",focus:"Ninjutsu",persona:"caster",element:"Fire",
    stats:{STR:6,AGI:8,FORT:8,INT:14,CHA:9},
    moves:()=>[R(fromGeneral("Chakra Bullet"),"Arcane Bolt"),R(fromKit("Leo","Solar Lance"),"Fire Lance"),R(fromKit("Aries","Blast Wave"),"Force Nova"),R(fromGeneral("Earth Wall"),"Conjure Barrier"),R(fromKit("Aries","Meteor"),"Cataclysm")]},
  Hypnotist:{name:"Hypnotist",glyph:"🌀",focus:"Genjutsu",persona:"caster",element:"Water",
    stats:{STR:6,AGI:9,FORT:8,INT:10,CHA:13},
    moves:()=>[R(fromKit("Leo","Spotlight"),"Mesmerize"),R(fromKit("Aries","Killing Intent"),"Dread Gaze"),R(fromKit("Pisces","Escapism"),"Lull to Sleep"),R(fromKit("Scorpio","Paranoia"),"Fracture Mind"),R(fromGeneral("Phantom Haunt"),"Waking Nightmare")]},
  Cultist:{name:"Cultist",glyph:"🕯",focus:"Ninjutsu",persona:"support",element:"Water",
    stats:{STR:7,AGI:8,FORT:9,INT:11,CHA:11},summon:{name:"Summoned Familiar",role:"DPS"},
    moves:()=>[R(fromGeneral("Palm Healing"),"Dark Communion"),R(fromGeneral("Guardian Barrier"),"Warding Sigil"),R(fromGeneral("Chakra Drain"),"Siphon Rite"),R(fromKit("Capricorn","Mausoleum"),"Binding Curse"),R(fromGeneral("Summon Companion"),"Summon Familiar")]},
  Bear:{name:"Bear",glyph:"🐻",focus:"Taijutsu",persona:"brute",element:"Earth",
    stats:{STR:15,AGI:7,FORT:14,INT:4,CHA:5},
    moves:()=>[R(fromMartial("Boxing","Haymaker"),"Maul"),R(fromKit("Taurus","Bull Rush"),"Charge"),R(fromMartial("Boxing","Clinch"),"Bear Hug"),R(fromGeneral("Iron Mountain"),"Heavy Swipe"),R(fromMartial("Boxing","Dirty Boxing"),"Crushing Bite")]},
  Tiger:{name:"Tiger",glyph:"🐯",focus:"Taijutsu",persona:"assassin",element:"Fire",
    stats:{STR:13,AGI:17,FORT:8,INT:5,CHA:6},
    moves:()=>[R(fromKit("Scorpio","Shadow Step"),"Pounce"),R(fromKit("Scorpio","Kidney Shot"),"Rake"),R(fromKit("Scorpio","Numbing Strike"),"Hamstring Claw"),R(fromGeneral("Viper Strike"),"Fang Bite")]},
  GiantCrab:{name:"Giant Crab",glyph:"🦀",focus:"Taijutsu",persona:"defensive",element:"Water",
    stats:{STR:12,AGI:5,FORT:16,INT:6,CHA:6},
    moves:()=>[R(fromKit("Capricorn","Prismatic Skin"),"Carapace"),R(fromMartial("Wrestling","Sumo Palm"),"Pincer Crush"),R(fromKit("Cancer","Whirlpool"),"Bubble Blast"),R(fromMartial("Boxing","Clinch"),"Claw Grip")]},
  Zombie:{name:"Zombie",glyph:"🧟",focus:"Taijutsu",persona:"brute",element:"Earth",
    stats:{STR:11,AGI:5,FORT:15,INT:4,CHA:5},
    moves:()=>[R(fromGeneral("Viper Strike"),"Rotting Bite"),R(fromKit("Capricorn","Adamantine Shin"),"Clawing Grasp"),R(fromMartial("Boxing","Clinch"),"Death Grip"),R(fromMartial("Boxing","Haymaker"),"Lumbering Smash")]},
  Wraith:{name:"Wraith",glyph:"👻",focus:"Genjutsu",persona:"skirmisher",element:"Air",
    stats:{STR:8,AGI:15,FORT:7,INT:10,CHA:12},
    moves:()=>[R(fromGeneral("Gloom Shroud"),"Phase Out"),R(fromGeneral("Chakra Scalpel"),"Spectral Touch"),R(fromGeneral("Shadow Possession"),"Grasp of the Dead"),R(fromKit("Scorpio","Betrayal"),"Whisper of Madness")]},
  Banshee:{name:"Banshee",glyph:"🦇",focus:"Genjutsu",persona:"caster",element:"Air",
    stats:{STR:6,AGI:10,FORT:8,INT:9,CHA:14},
    moves:()=>[R(fromKit("Gemini","Howling Blast"),"Wailing Scream"),R(fromKit("Pisces","Siren's Lure"),"Death Wail"),R(fromKit("Pisces","Escapism"),"Keening Lullaby"),R(fromKit("Gemini","Tinnitus"),"Piercing Shriek")]},
};
const ENEMY_KEYS=Object.keys(ENEMIES);
/* A style NPC's kit is annotated exactly like a player's trained style, so the same
   stance-child gating, positional legality and plan sanitation apply to both. */
function martialKitFor(styleKey){
  const S=MARTIAL[styleKey];if(!S)return[];
  const mark=(a,stance)=>({...a,sourceKind:"Martial",sourceKey:styleKey,styleKey,parentStyles:[styleKey],
    ...(stance?{isStyleStance:true}:{isStyleTechnique:true})});
  return[mark(S.stance,true),...S.moves.map(m=>mark(m,false))];
}
function enemyLoadout(key){const e=ENEMIES[key];const L=e.martial?martialKitFor(e.martial):e.moves();
  // every fighter can catch breath / charge chakra / recompose
  L.push(R(fromGeneral("Catch Breath"),"Catch Breath"),R(fromGeneral("Charge Chakra"),"Focus"),R(fromGeneral("Recompose"),"Recompose"));
  return L.map(a=>applyLiveBalanceAbility({...a,effects:a.effects.map(x=>({...x})),tags:[...a.tags],id:"A"+(ABID++)}));}

/* =========================================================================
   COMBATANT + RESOLVER  (2-D hex; positions are HexCoord)
   ========================================================================= */
// Scales a canonical ENEMIES stat block for a chosen opponent/ally level. Preserves each
// style's relative shape (a Wrestler still leans STR/FORT after scaling) since every stat is
// scaled by the same factor; only the overall power level moves. level=BAL.enemyLevelAnchor
// (20) reproduces the input unchanged.
function scaleEnemyStats(stats,level){
  const lvl=clamp(round(Number(level)||BAL.enemyLevelAnchor),1,100);
  const factor=BAL.enemyLevelScaleAtAnchor+(lvl-BAL.enemyLevelAnchor)*BAL.enemyLevelScalePerLevel;
  const out={};
  for(const k of Object.keys(stats))out[k]=max(BAL.enemyLevelStatFloor,round(stats[k]*factor));
  return out;
}
function makeFighter(o){
  // o: {name,sign,stats,faction,cell,abilities,glyph,focus,persona,summonSpecies,isPlayer}
  const s=o.stats;
  const f={name:o.name,sign:o.sign,faction:o.faction,stats:s,cell:o.cell,abilities:o.abilities||[],glyph:o.glyph||GLYPH[o.sign]||"◆",
    focus:o.focus||null,persona:o.persona||"balanced",isPlayer:!!o.isPlayer,summonSpecies:o.summonSpecies||null,
    statuses:[],buffs:[],pendingSkips:0,chargingAction:null,chargeTargetCell:null,chargeTargetFighter:null,repeat:{},trapUses:{},
    // System 3 — ability clashes: pending consequences a Tier 1/2 clash rule leaves on this
    // fighter for their OWN next queued action (or, for pendingPoiseFloor, the current hit
    // when set from applyGrapple's clash hook). Same one-shot shape as pendingSkips.
    pendingClashMult:1,pendingClashNegate:false,pendingPoiseFloor:0,
    strain:0,wardNext:0,eyeActive:false,activeEye:null,noChakraRegen:0,chakraReserved:0,activeSummon:null,
    grappledBy:null,grappleTarget:null,grappleAge:0,grappleLanded:false,grappleAttempts:0,
    // Structural, directional relationship state. `role` is one of REL.*, `partner` is the
    // paired combatant. Standing Grapple and Mount are mutually exclusive.
    rel:{role:REL.FREE,partner:null,rounds:0,voluntary:false},
    submission:null,releaseIntent:false,roundUses:{},
    hauntTarget:null,hauntedBy:null,stealthAge:0,poiseRecoverDelay:0,isSummon:!!o.isSummon,supplies:BAL.baseSupplies,
    // Last-known cell of each enemy this fighter has actually perceived (awareness range + LoS,
    // not Stealthed) — a real fog-of-war memory, not omniscient tracking. Refreshed once per
    // round in planFor(); an enemy dropping out of perception leaves its last remembered spot
    // stale on purpose, so a fighter chasing a memory can arrive to find no one there.
    enemyMemory:new Map(),resisted:new Map()};
  f.maxHp=DR.maxHp(s);f.hp=f.maxHp;f.maxStam=DR.maxStam(s);f.stam=f.maxStam;
  f.maxChakra=DR.maxChakra(s);f.chakra=f.maxChakra;f.maxPoise=DR.maxPoise(s);f.poise=f.maxPoise;
  return f;
}
const alive=f=>f.hp>0;
function eff(f){const s={...f.stats};for(const b of f.buffs)s[b.stat]=round(s[b.stat]*(1+b.pct/100));return s;}
const hasStatus=(f,k)=>f.statuses.some(s=>s.kind===k);
const getStatus=(f,k)=>f.statuses.find(s=>s.kind===k);
const removeStatus=(f,k)=>{f.statuses=f.statuses.filter(s=>s.kind!==k);};
const isExhausted=f=>f.stam<=0;

/* ---- directional relationship state -------------------------------------
   `f.rel.role` is the single source of truth. The matching status entries are
   mirrors kept in sync purely for display / legacy consumers; nothing reads
   legality from them. Mounting NEVER implies Grappling. */
const relRole=f=>(f&&f.rel&&f.rel.role)||REL.FREE;
const relPartner=f=>(f&&f.rel&&f.rel.partner)||null;
const isGrappling=f=>relRole(f)===REL.GRAPPLING;
const isGrappled=f=>relRole(f)===REL.GRAPPLED;
const isMounting=f=>relRole(f)===REL.MOUNTING;
const isMounted=f=>relRole(f)===REL.MOUNTED;
const inMount=f=>isMountRole(relRole(f));
const inStandingGrapple=f=>isStandingRole(relRole(f));
const isEngaged=f=>inRelationship(relRole(f));
const REL_STATUS_KINDS=[REL.GRAPPLING,REL.GRAPPLED,REL.MOUNTING,REL.MOUNTED];
function syncRelStatuses(f){
  f.statuses=f.statuses.filter(s=>!REL_STATUS_KINDS.includes(s.kind));
  const role=relRole(f);
  if(role!==REL.FREE)f.statuses.push({kind:role,rounds:1,stacks:1,tick:0,mag:0,relationship:true,source:relPartner(f)});
  // legacy mirrors so older consumers (AI scoring, indicators) keep working
  if(role===REL.GRAPPLING||role===REL.MOUNTING){f.grappleTarget=relPartner(f);f.grappledBy=null;}
  else if(role===REL.GRAPPLED||role===REL.MOUNTED){f.grappledBy=relPartner(f);f.grappleTarget=null;}
  else{f.grappleTarget=null;f.grappledBy=null;}
}
function setRelationship(a,roleA,b,roleB,opt={}){
  a.rel={role:roleA,partner:b,rounds:opt.rounds??0,voluntary:!!opt.voluntary};
  b.rel={role:roleB,partner:a,rounds:opt.rounds??0,voluntary:!!opt.voluntary};
  syncRelStatuses(a);syncRelStatuses(b);
}
function clearRelationship(f){
  const p=relPartner(f);
  f.rel={role:REL.FREE,partner:null,rounds:0,voluntary:false};
  f.submission=null;f.releaseIntent=false;f.grappleAge=0;f.grappleLanded=false;f.grappleAttempts=0;
  syncRelStatuses(f);
  if(p&&relPartner(p)===f){p.rel={role:REL.FREE,partner:null,rounds:0,voluntary:false};p.submission=null;p.releaseIntent=false;p.grappleAge=0;p.grappleLanded=false;p.grappleAttempts=0;syncRelStatuses(p);}
}
// The active Maintained Submission covering this fighter's relationship, if any.
function activeSubmission(f){const s=f&&f.submission;return s&&s.holder&&s.receiver?s:null;}
function setSubmission(holder,receiver,ab,name,round){
  const rec={holder,receiver,name:name||(ab&&ab.name)||"submission",ability:ab||null,
    consecutive:0,appliedRound:round??0};
  holder.submission=rec;receiver.submission=rec;return rec;
}
/* The live submission this ability would CONTINUE rather than establish: same holder, same
   partner, same authored technique. Continuations escalate; a different technique starts over. */
function continuedSubmission(actor,ab){
  const sub=activeSubmission(actor);
  if(!sub||sub.holder!==actor||!ab)return null;
  if(sub.receiver!==relPartner(actor))return null;
  return sub.name===ab.name?sub:null;
}
/* Escalation multipliers for CONTINUING a hold. `consecutive` counts rounds maintained past
   the establishing one, so the next application is always charged one step above the last:
   establish x1, then x1.5, x2.0, x2.5 ... Passing no record (a fresh hold) is face value. */
const submissionStep=sub=>sub?((sub.consecutive||0)+1):0;
/* Turns the submission holding THIS fighter has been worked (1 on the round it was locked in).
   Only the fighter caught in the hold is resisted — the holder is not escaping anything.
   Feeds the escape DC reduction; it never gates an uncontested ability. */
function submissionEscapeTurns(actor){
  const sub=activeSubmission(actor);
  if(!sub||sub.receiver!==actor)return 0;
  return (sub.consecutive||0)+1;
}
const submissionEscapeResistance=actor=>BAL.submissionEscapeDcPerRound*submissionEscapeTurns(actor);
const submissionCostMult=sub=>1+BAL.submissionCostEscalation*submissionStep(sub);
const submissionDamageMult=sub=>1+BAL.submissionDamageEscalation*submissionStep(sub);
function clearSubmission(f){const s=activeSubmission(f);if(!s)return null;s.holder.submission=null;s.receiver.submission=null;return s;}

const isRooted=f=>hasStatus(f,"Root")||isEngaged(f);

/* ---- structured positional legality --------------------------------------
   Resolves an ability's legality from its POSITIONAL_RULES metadata against a
   relationship role. Never parses display names. `role` may be supplied so the
   planner can project a role the queue has not reached yet. */
const posMeta=ab=>(ab&&ab.pos)||UNAUDITED_POS;
const isFocusAbility=ab=>!!ab&&ab.tags.includes("Focus");
// Ordinary voluntary movement: gap-closers, teleports and self-relocation. Authored
// relationship techniques (throws, transitions) are NOT ordinary movement.
function isGenericMovementAbility(ab){
  if(!ab)return false;
  const m=posMeta(ab);
  if(m.transition||ab.effects.some(e=>e.k==="GrappleTech"))return false;
  return ab.tags.includes("GapCloser")||ab.tags.includes("Teleport")||ab.effects.some(e=>e.k==="Move");
}
const REL_LABEL={[REL.GRAPPLING]:"Grappling",[REL.GRAPPLED]:"Grappled",[REL.MOUNTING]:"Mounting",[REL.MOUNTED]:"Mounted"};
function positionalLegality(actor,ab,roleOverride){
  const role=roleOverride||relRole(actor);
  if(!ab)return{ok:true};
  const m=posMeta(ab);
  // Focus is never blocked by the relationship itself — only by explicit Focus denial.
  if(isFocusAbility(ab)){
    if(hasStatus(actor,"FocusLock"))return{ok:false,code:"focus-denied",reason:"Focus actions are locked"};
    return{ok:true};
  }
  if(ab.oncePerRound&&(actor.roundUses&&actor.roundUses[ab.id]))return{ok:false,code:"once-per-round",reason:`${ab.name} is once per round`};
  if(inRelationship(role)&&isGenericMovementAbility(ab))
    return{ok:false,code:"movement-blocked",reason:isMountRole(role)?"No movement while in Mount":"No movement while grappling"};
  if(isMountRole(role)){
    // Blank/unaudited abilities receive no new per-ability override and stay legal.
    if(m.access===MOUNT_ACCESS.NEITHER)return{ok:false,code:"mount-illegal",reason:"Cannot be used in Mount"};
    if(m.access===MOUNT_ACCESS.MOUNTING_ONLY&&role!==REL.MOUNTING)return{ok:false,code:"requires-mounting",reason:"Requires Mounting"};
    if(m.access===MOUNT_ACCESS.MOUNTED_ONLY&&role!==REL.MOUNTED)return{ok:false,code:"requires-mounted",reason:"Requires Mounted"};
    return{ok:true};
  }
  // Outside Mount the relationship prerequisite governs. Kicks specifically need standing
  // balance and distance a standing grapple denies — punches, elbows and knees stay legal in
  // a clinch, but a kicking technique does not (owner call).
  if(m.noStanding&&isStandingRole(role))return{ok:false,code:"grapple-illegal",reason:"Cannot be used while grappling"};
  switch(m.req){
    case REQ.STANDING:if(!isStandingRole(role))return{ok:false,code:"requires-standing-grapple",reason:"Requires standing Grapple"};break;
    case REQ.GRAPPLING:if(role!==REL.GRAPPLING)return{ok:false,code:"requires-grappling",reason:"Requires Grappling"};break;
    case REQ.GRAPPLED:if(role!==REL.GRAPPLED)return{ok:false,code:"requires-grappled",reason:"Requires Grappled"};break;
    case REQ.MOUNT:return{ok:false,code:"requires-mount",reason:"Requires Mounting or Mounted"};
    case REQ.MOUNTING:return{ok:false,code:"requires-mounting",reason:"Requires Mounting"};
    case REQ.MOUNTED:return{ok:false,code:"requires-mounted",reason:"Requires Mounted"};
    default:break;
  }
  return{ok:true};
}
// Additive positional save-DC modifier, applied AFTER the normal live DC calculation and
// only to abilities explicitly flagged for positional DC scaling.
function positionalDcModifier(actor,ab){
  if(!posMeta(ab).positionalDc)return 0;
  switch(relRole(actor)){
    case REL.GRAPPLING:return BAL.positionalDcGrappling;
    case REL.GRAPPLED:return BAL.positionalDcGrappled;
    case REL.MOUNTING:return BAL.positionalDcMounting;
    case REL.MOUNTED:return BAL.positionalDcMounted;
    default:return BAL.positionalDcFree;
  }
}
function passiveStaminaFactor(role){
  switch(role){
    case REL.GRAPPLING:return BAL.passiveStamGrappling;
    case REL.GRAPPLED:return BAL.passiveStamGrappled;
    case REL.MOUNTING:return BAL.passiveStamMounting;
    case REL.MOUNTED:return BAL.passiveStamMounted;
    default:return BAL.passiveStamFree;
  }
}
/* Relationship role a fighter will hold after `ab` resolves, used for slot-order-aware
   projection by both the AI planner and the plan sanitizer. */
function advanceProjectedRole(role,ab){
  if(!ab)return role;
  const gt=(ab.effects||[]).find(e=>e.k==="GrappleTech");
  if((ab.effects||[]).some(e=>e.k==="Grapple"))return role===REL.FREE?REL.GRAPPLING:role;
  if((ab.effects||[]).some(e=>e.k==="Takedown"))return REL.FREE;
  if(!gt)return role;
  if(gt.mount)return gt.voluntaryBottom?REL.MOUNTED:REL.MOUNTING;
  if(gt.throw>0||gt.breakHold)return REL.FREE;
  return role;
}
// Every fighter programmes the full slate each round; submissions no longer reserve a slot.
const availableSlots=()=>BAL.actionSlotsPerRound;
/* Standing-grapple Priority: the Grappling controller acts ahead of the fighter they
   have Grappled, for actions involving THAT opponent only. This is not a global
   initiative buff, and Mount grants no equivalent generic bonus. */
function standingGrapplePriority(owner,entry){
  if(relRole(owner)!==REL.GRAPPLING)return 0;
  const partner=relPartner(owner);if(!partner)return 0;
  const ab=entry&&entry.ability?entry.ability:entry;
  const chosen=entry&&entry.ability?entry.target:null;
  if(!ab)return 0;
  const involvesPartner=chosen?chosen===partner:(ab.targeting==="SingleEnemy"||!!relationshipRequirement(ab));
  if(!involvesPartner)return 0;
  return BAL.standingGrapplePriorityWeight*BAL.initPriorityWeight;
}
// System 3 (scoped anti-priority): Teep Kick specifically races for priority against whichever
// opposing action currently holds the best picking key — the same closest-priority
// opposing-faction approximation the shelved System 1 Counter-tag proposal used, not a claim
// about which enemy Teep Kick will actually resolve against once targeting happens for real.
// Only fires when that action is a damaging, Priority-tagged rush (isDamagingRush + Priority) —
// against Tidal Slam (damaging but Normal speed) this is already a fair AGI+d10 race and needs
// no help; against a Priority rush it's the difference between never getting to act as a
// counter at all and a genuine coin-flip.
function teepAntiPriorityBonus(s,entry,sched){
  const ab=actAbility(entry);
  if(ab.name!=="Teep Kick")return 0;
  let bestTag=null,bestKey=-1e9;
  for(const t of sched){
    if(t.owner.faction===s.owner.faction)continue;
    if(t.next>=t.actions.length||!alive(t.owner))continue;
    const oab=actAbility(t.actions[t.next]);
    const okey=t.init-ccInitPenalty(t.owner)-selOffset(oab)+standingGrapplePriority(t.owner,t.actions[t.next]);
    if(okey>bestKey){bestKey=okey;bestTag=oab;}
  }
  return(bestTag&&isDamagingRush(bestTag)&&bestTag.tags.includes("Priority"))?BAL.teepAntiPriorityBonus:0;
}
const effMaxChakra=f=>max(0,f.maxChakra-f.chakraReserved);
function ccInitPenalty(f){let p=0;for(const s of f.statuses){if(s.kind==="Slow"||s.kind==="Confusion"||s.kind==="Root")p+=BAL.slowInitiativePenalty;else if(s.kind==="Prone")p+=BAL.ccInitHeavy;else if(s.kind==="Snare"||s.kind==="Blind")p+=BAL.ccInitLight;else if(s.kind==="Stealth")p-=BAL.ccInitStealthBonus;}if(isExhausted(f))p+=BAL.ccInitHeavy;return p;}

// Battle state container so tests + UI share resolution
class Battle{
  constructor(fighters,grid){this.all=fighters;this.grid=grid;this.round=1;this.log=[];this.pending=[];this.god=false;this.onLog=null;this.xp=new Map();this.events=[];this.history=[];
    // Combatants have at least glimpsed each other take the field, so every fighter's
    // fog-of-war memory starts seeded with each enemy's spawn cell — a one-time "saw them line
    // up" grant, not ongoing tracking. Without this, a start further apart than anyone's
    // awareness range (a real case now that maps scale up) would leave the AI with genuinely no
    // information and nothing to move toward, freezing in place forever. From here on, memory
    // only ever updates from what's actually perceived — see Battle.updateEnemyMemory.
    for(const f of fighters)for(const e of fighters)if(e!==f&&e.faction!==f.faction)f.enemyMemory.set(e,{...e.cell});}
  line(t,cls,calc){this.log.push({text:t,cls,calc});if(this.onLog)this.onLog(t,cls);}
  // Structured record of what happened this round, in order, for presentation layers (the sprite
  // replay). Purely observational: it consumes no RNG and nothing in the engine reads it back.
  ev(type,data){this.events.push({type,round:this.round,...data});}
  enemies(f){return this.all.filter(c=>alive(c)&&c.faction!==f.faction);}
  allies(f){return this.all.filter(c=>alive(c)&&c.faction===f.faction);}
  occupied(cell,except){if(this.grid.blocksMove(cell))return true;return this.all.some(c=>c!==except&&alive(c)&&c.cell.q===cell.q&&c.cell.r===cell.r);}
  // piercing: a Called Shot can be aimed through the same destructible brush (Tree/Bush) its
  // own attack roll ignores — see Grid.losHard — without that relaxing awareness/fog-of-war for
  // anything else. Stealth and the awareness-radius check are untouched either way.
  perceives(o,t,piercing){if(o===t)return true;if(hasStatus(t,"Stealth"))return false;const dist=hdist(o.cell,t.cell);if(dist>DR.awareness(eff(o)))return false;return piercing?this.grid.losHard(o.cell,t.cell):this.grid.los(o.cell,t.cell);}
  nearestEnemy(f){let best=null,bd=1e9;for(const e of this.enemies(f)){const dd=hdist(f.cell,e.cell);if(dd<bd){bd=dd;best=e;}}return best;}
  nearestPerceivedEnemy(f,piercing){let best=null,bd=1e9;for(const e of this.enemies(f)){if(!this.perceives(f,e,piercing))continue;const dd=hdist(f.cell,e.cell);if(dd<bd){bd=dd;best=e;}}return best;}
  // Refreshes f's fog-of-war memory from what it actually perceives right now. Called once per
  // round, at planning time, before any decision reads that memory — never mid-decision, so a
  // fighter can't "peek" partway through its own turn.
  updateEnemyMemory(f){for(const e of this.enemies(f))if(this.perceives(f,e))f.enemyMemory.set(e,{...e.cell});}
  decided(){const fac=new Set(this.all.filter(alive).map(c=>c.faction));return fac.size<=1;}
}
const RED=n=>`<span class="dm">${n}</span>`,GRN=n=>`<span class="hl">${n}</span>`;

// Effective movement tiles this round after crowd-control: Root stops movement,
// Snare and Slow each cut it (they compound if both are present).
function moveBudget(f){let m=DR.mc(eff(f));if(isRooted(f))return 0;if(hasStatus(f,"Snare"))m=floor(m*BAL.snareMoveMult);if(hasStatus(f,"Slow"))m=floor(m*BAL.slowMoveMult);return max(0,m);}
function startRound(B,f){if(!alive(f))return;
  // A broken guard is not a free full reset — it climbs back at the same 10%/round passive
  // rate as any partial poise, after a 1-round recovery delay (owner ruling: only Pull Guard's
  // voluntary-bottom transition preserves current poise; nothing restores lost/broken poise).
  if(isMounted(f)){/* no poise recovery while Mounted; entry already resolved the break */}else if(f.poiseRecoverDelay>0)f.poiseRecoverDelay--;else f.poise=min(f.maxPoise,f.poise+DR.poiseRegen(f.stats));
  const full=DR.mc(eff(f));f.mc=moveBudget(f);
  if(B&&f.mc<full&&!isRooted(f)&&(hasStatus(f,"Slow")||hasStatus(f,"Snare")))B.line(`${f.name} is ${hasStatus(f,"Slow")?"Slowed":"Snared"} — movement ${full} → ${f.mc}.`,"sys");
  f.repeat={};f.roundUses={};if(hasStatus(f,"Dazed")){f.pendingSkips+=1;removeStatus(f,"Dazed");}
}
function repetitionExtra(f,ab){const uses=f.repeat[ab.id]||0;if(uses<BAL.repetitionFreeUses)return{stam:0,chak:0};const over=uses-BAL.repetitionFreeUses+1;return{stam:round(ab.stam*BAL.repetitionStrainPerExtra*over),chak:round(ab.chakra*BAL.repetitionStrainPerExtra*over)};}
// AI sustainable-resource planning: discounts a candidate's score by how much of its pool the
// pick would actually cost (effStam/effChak — already includes the repetitionExtra surcharge)
// and by how depleted that pool already is. costFrac alone would make an expensive move always
// look bad even at full resources; scarcity alone would make every move look bad once low on
// resources regardless of its own cost — multiplying them together means a cheap move barely
// suffers even when the pool is nearly empty, and an expensive move barely suffers while the
// pool is still full. Floored, not zeroed, so the AI never refuses to act at all.
function resourcePaceMult(effStam,effChak,stamPool,chakPool,maxStam,maxChak){
  const stamFrac=maxStam>0?effStam/maxStam:0,chakFrac=maxChak>0?effChak/maxChak:0;
  const costFrac=max(stamFrac,chakFrac);
  if(costFrac<=0)return 1;
  const remainFrac=stamFrac>=chakFrac?(maxStam>0?stamPool/maxStam:1):(maxChak>0?chakPool/maxChak:1);
  const scarcity=clamp(1-remainFrac,0,1);
  return clamp(1-BAL.aiResourcePacingWeight*costFrac*scarcity,BAL.aiResourcePacingFloor,1);
}
// AI opponent-read: records that `attacker`'s `ab` was just beaten by `defender` — evaded,
// parried, or denied a grapple/technique entry — so future scoring can discount throwing the
// same thing at the same foe again. Keyed per-defender (not just per-ability) since a fighter
// juggling multiple opponents may read one of them well and not the other.
function recordResisted(attacker,defender,ab){
  let m=attacker.resisted.get(defender);if(!m){m=new Map();attacker.resisted.set(defender,m);}
  m.set(ab.name,(m.get(ab.name)||0)+1);
}
function isGrappleAbility(ab){return ab.effects.some(e=>e.k==="Grapple"||e.k==="GrappleTech");}
// AI opponent-pattern-read: what fraction of `foe`'s own actions THIS FIGHT have been a
// Grapple/GrappleTech attempt. Reads foe.repeat directly (already tracked for the repetition
// surcharge) rather than a separate observation log — the planner already treats a foe's full
// kit as known for scoring purposes elsewhere, so this is consistent with that, not a new
// omniscience.
function foeGrappleFraction(foe){
  let total=0,grap=0;
  for(const ab of foe.abilities){const uses=foe.repeat[ab.id]||0;if(!uses)continue;total+=uses;if(isGrappleAbility(ab))grap+=uses;}
  return total?grap/total:0;
}
function savingThrow(def,stat,dc){return eff(def)[stat]+d(20)>=dc;}

// A planned action is either a bare ability or a rich {ability,target,point} entry
// (target = a chosen creature, point = a chosen cell). These normalize either form.
const actAbility=e=>e&&e.ability?e.ability:e;
const actTarget=e=>e&&e.ability?(e.target||null):null;
const actPoint=e=>e&&e.ability?(e.point||null):null;
function resolveAction(B,owner,ab,opts={}){
  const cls="f"+owner.faction;if(!ab)return;let target=null;
  if(deniedByCc(B,owner))return;
  /* Structured positional legality. Execution ALWAYS revalidates against the real
     relationship state, so a failed transition earlier in the queue cannot let a
     follow-up run illegally. There is no auto-escape substitution: a Grappled or
     Mounted fighter simply cannot run an action their position forbids. */
  const legal=positionalLegality(owner,ab);
  if(!legal.ok){B.line(`${owner.name} can't use ${ab.name} — ${legal.reason} (currently ${relRole(owner)}).`,cls);return;}
  if(relationshipRequirement(ab)){
    const linked=relPartner(owner);
    if(!linked||!alive(linked)){B.line(`${owner.name} has no live relationship — ${ab.name} needs body contact.`,cls);return;}
    target=linked;
  }
  if(ab.tags.includes("EyeJutsu")&&!owner.eyeActive){B.line(`${owner.name} can't use ${ab.name} — no eye is open.`,cls);return;}
  if(hasStatus(owner,"Silence")&&(ab.chakra>0||ab.chakraPct>0)){B.line(`${owner.name} is Silenced — ${ab.name} won't channel.`,cls);return;}
  if(hasStatus(owner,"Disarm")&&ab.disc==="Weapon"){B.line(`${owner.name} is Disarmed.`,cls);return;}
  if(hasStatus(owner,"Confusion")&&rand()*100<BAL.confusionFizzleChance){B.line(`${owner.name} is too disoriented — ${ab.name} goes nowhere.`,cls);return;}
  if(ab.tags.includes("Trap")&&(owner.trapUses[ab.id]||0)>=BAL.trapUsesPerBattle){B.line(`${owner.name} reaches for another ${ab.name} — the pouch is empty.`,cls);return;}
  const ex=repetitionExtra(owner,ab);
  // Continuing a submission costs more every consecutive round it has been held.
  const subMult=submissionCostMult(continuedSubmission(owner,ab));
  const pc=pctCost(ab,owner);
  const needStam=round((ab.stam+pc.stam)*costMult(ab)*subMult)+ex.stam,needChak=round((ab.chakra+pc.chakra)*costMult(ab)*subMult)+ex.chak;
  if(owner.stam<needStam||owner.chakra<needChak||owner.supplies<ab.supply){B.line(`${owner.name}'s ${ab.name} fizzles (not enough resources).`,cls);return;}
  owner.stam-=needStam;owner.chakra-=needChak;owner.supplies-=ab.supply;owner.repeat[ab.id]=(owner.repeat[ab.id]||0)+1;
  // System 3: a Tier 2 clash negate (e.g. Uppercut stuffing a queued Single Leg Shot) pays its
  // full cost — deducted above — then never executes. Deliberately not the same spot as
  // pendingSkips in the picking loop, which is why that one is free and this one is costly.
  if(owner.pendingClashNegate){owner.pendingClashNegate=false;B.line(`${owner.name}'s ${ab.name} is read and stopped cold before it can begin!`,cls);return;}
  if(ab.oncePerRound){owner.roundUses=owner.roundUses||{};owner.roundUses[ab.id]=(owner.roundUses[ab.id]||0)+1;}
  if(ab.tags.includes("Trap"))owner.trapUses[ab.id]=(owner.trapUses[ab.id]||0)+1;
  if(ab.tags.includes("MartialStance")){owner.activeMartial=ab;owner.activeWeapon=null;}
  if(ab.tags.includes("WeaponStance")){owner.activeWeapon=ab;owner.activeMartial=null;}
  if(ab.tags.includes("Charge")){
    // A player-chosen SingleEnemy target (opts.target) is honored over the generic
    // nearest-perceived-enemy fallback the AoE Ultimates have always used — those never set
    // opts.target (their targeting is PointRadius), so this only changes behavior for
    // single-target locked charges like Called Shot, where who you aim at is the whole point.
    const t=(opts.target&&alive(opts.target))?opts.target:(opts.point?null:B.nearestPerceivedEnemy(owner));
    owner.chargingAction=ab;owner.chargeTargetCell=opts.point?{...opts.point}:(t?{...t.cell}:{...owner.cell});
    owner.chargeTargetFighter=t||null;
    if(ab.rootWhileCharging)owner.statuses.push({kind:"Root",rounds:2,stacks:1,tick:0,mag:0});
    B.line(ab.chargeBeam?`${owner.name} draws — it looses at the start of next round!`:`${owner.name} begins channelling ${ab.name} — it erupts at the start of next round!`,cls);
  }
  else if(executeAbility(B,owner,ab,target||opts.target||null,opts.point||null)===false){
    // The action never actually got attempted — a structurally impossible target (no
    // perception, out of range, unreachable ally, etc.), not a missed roll or a parried hit.
    // Refund the cost so the fighter isn't charged for something that was never a real chance
    // to begin with, instead of just logging the failure after already paying for it.
    owner.stam+=needStam;owner.chakra+=needChak;owner.supplies+=ab.supply;
    owner.repeat[ab.id]=max(0,(owner.repeat[ab.id]||0)-1);
    if(ab.oncePerRound&&owner.roundUses)owner.roundUses[ab.id]=max(0,(owner.roundUses[ab.id]||0)-1);
    if(ab.tags.includes("Trap"))owner.trapUses[ab.id]=max(0,(owner.trapUses[ab.id]||0)-1);
  }
  // Zero Stamina is NEVER an escape: relationships are only re-evaluated during the
  // Relationship Maintenance phase or by an explicit relationship-changing effect.
  if(owner.hauntTarget){owner.chakra=max(0,owner.chakra-BAL.hauntChakraPerAction);if(owner.chakra<=0)dispelHaunt(B,owner,"its caster's chakra has run dry");}
}
// True when the ability's authored metadata binds it to the actor's current partner.
function relationshipRequirement(ab){const r=posMeta(ab).req;return r?r:null;}
// Returns false when the ability never got a genuine chance to resolve (no valid/perceived/
// reachable target), so resolveAction can refund the cost it already paid. Returns true (or a
// truthy undefined) for every other outcome, including a miss or a parry — those are real,
// legitimately-paid-for attempts, not a waste.
function executeAbility(B,owner,ab,forced,point){
  const cls="f"+owner.faction;const quiet=ab.tags.includes("Focus")||ab.tags.includes("MartialStance")||ab.tags.includes("WeaponStance");
  if(hasStatus(owner,"Stealth")&&!quiet){removeStatus(owner,"Stealth");owner.stealthAge=0;}
  let landed=true;
  if(ab.targeting==="Self"){B.line(`${owner.name} flows into ${ab.name}.`,cls);applyEffects(B,owner,ab,owner,1,false,point);}
  else if(ab.targeting==="SingleAlly"){
  const reach=max(1,ab.maxR||1),inRange=t=>hdist(owner.cell,t.cell)<=reach,valid=forced&&forced.faction===owner.faction&&alive(forced);
  if(valid&&!inRange(forced)){B.line(`${owner.name}'s ${ab.name} cannot reach ${forced.name}.`,cls);landed=false;}
  else{const chosen=valid?forced:null,allies=B.allies(owner).filter(inRange).sort((a,b)=>(a.hp/a.maxHp)-(b.hp/b.maxHp)),t=chosen||allies[0]||owner;
  B.line(`${owner.name} channels ${ab.name} into ${t.name}.`,cls);applyEffects(B,owner,ab,t,1,false);}
}
  else if(ab.targeting==="AlliesInRadius"){const reach=max(1,round(ab.radius));B.line(`${owner.name} projects ${ab.name} over nearby allies.`,cls);for(const c of B.allies(owner))if(hdist(c.cell,owner.cell)<=reach)applyEffects(B,owner,ab,c,1,false);}
  else if(ab.targeting==="PointRadius")landed=resolveAoe(B,owner,ab,point)!==false;
  else landed=resolveSingleEnemy(B,owner,ab,forced,point)!==false;
  if(ab.tags.includes("EyeJutsu")&&owner.eyeActive){owner.strain+=BAL.strainPerEyeJutsu;checkBurnout(B,owner);}
  return landed;
}
function approach(B,owner,targetCell,keepDist){ // move up to mc toward (or to standoff of) targetCell
  if(isRooted(owner)||owner.mc<=0)return;
  const blocked=c=>B.occupied(c,owner);
  if(keepDist){ // kite: reachable cell closest to desired standoff, prefers LoS
    const{cells,dist}=B.grid.reachable(owner.cell,owner.mc,blocked);let best=owner.cell,bg=1e9,bc=0;
    for(const[k,c]of cells){const dd=hdist(c,targetCell);if(dd<2)continue;const los=B.grid.los(c,targetCell);const gap=los?abs(dd-keepDist):1000+dd;const cost=dist.get(k);if(gap<bg||(gap===bg&&cost<bc)){best=c;bg=gap;bc=cost;}}
    if(best!==owner.cell){owner.mc-=bc;owner.cell=best;}
  } else {const{cell,cost}=B.grid.bestApproach(owner.cell,targetCell,owner.mc,blocked);if(cell!==owner.cell){owner.cell=cell;owner.mc-=cost;}}
}
// Reach gap-close: if the target sits within a reach ability's catch radius, snap the user to a
// free tile adjacent to the target (their melee range). This does NOT spend movement — it is the
// ability's built-in lunge, separate from the fighter's normal per-round movement. A target that
// has already moved beyond the radius (typically via superior AGI/movement) can't be caught.
function gapClose(B,owner,target){
  if(isRooted(owner))return false;
  const spots=neighbors(target.cell).filter(c=>B.grid.inBounds(c)&&!B.occupied(c,owner));
  if(!spots.length)return false;
  spots.sort((a,b)=>hdist(owner.cell,a)-hdist(owner.cell,b));
  owner.cell={...spots[0]};
  return true;
}
// A queued single-target action whose chosen enemy is defeated before it resolves swaps to the
// weakest reachable foe: among perceived enemies inside the ability's strike range, the one with
// the lowest current HP (nearest breaks ties). If none are in range, fall back to the weakest
// perceived enemy overall so the action still resolves instead of fizzling with "no target".
function retargetDefeated(B,owner,ab){
  const perceived=B.enemies(owner).filter(e=>B.perceives(owner,e)&&!hasStatus(e,"Stealth"));
  if(!perceived.length)return null;
  const reach=max(1,(ab.reach>0?max(ab.reach,ab.maxR||1):(ab.maxR||1)));
  const byWeak=list=>list.slice().sort((a,b)=>(a.hp-b.hp)||(hdist(owner.cell,a.cell)-hdist(owner.cell,b.cell)))[0];
  const inRange=perceived.filter(e=>hdist(owner.cell,e.cell)<=reach);
  return byWeak(inRange.length?inRange:perceived);
}
function resolveSingleEnemy(B,owner,ab,forced,point){
  const cls="f"+owner.faction;
  if(forced&&!alive(forced)){const swap=retargetDefeated(B,owner,ab);if(swap){B.line(`${forced.name} is down — ${owner.name} redirects ${ab.name} to ${swap.name}.`,cls);forced=swap;}}
  const piercing=ab.tags.includes("Piercing");
  let target=forced||((isEngaged(owner)&&relPartner(owner)&&alive(relPartner(owner)))?relPartner(owner):B.nearestPerceivedEnemy(owner,piercing));
  if(!target||!alive(target)){B.line(`${owner.name}'s ${ab.name} has no target.`,cls);return false;}
  if(hasStatus(target,"Stealth")){B.line(`${owner.name} can't find ${target.name} to strike.`,cls);return false;}
  let dist=hdist(owner.cell,target.cell);
  const losCheck=(a,b)=>piercing?B.grid.losHard(a,b):B.grid.los(a,b);
  // AI reposition (players move themselves pre-round); casters kite
  if(!owner.isPlayer&&!isRooted(owner)&&owner.mc>0){
    if((owner.persona==="caster"||owner.persona==="skirmisher")&&ab.maxR>=2&&dist<Math.max(2,Math.min(ab.maxR,BAL.casterKiteStandoffTiles))){approach(B,owner,target.cell,Math.min(ab.maxR,BAL.casterKiteStandoffTiles));}
    else if(dist>ab.maxR||!losCheck(owner.cell,target.cell)){approach(B,owner,target.cell,0);}
    dist=hdist(owner.cell,target.cell);
  } else if(owner.isPlayer&&!isRooted(owner)&&owner.mc>0&&(dist>ab.maxR||!losCheck(owner.cell,target.cell))){approach(B,owner,target.cell,0);dist=hdist(owner.cell,target.cell);}
  if(!B.perceives(owner,target,piercing)){B.line(`${owner.name} has no clear line to ${target.name}.`,cls);return false;}
  if(ab.needsLoS&&!losCheck(owner.cell,target.cell)){B.line(`${owner.name}'s ${ab.name} has no line of sight to ${target.name}.`,cls);return false;}
  if(ab.reach>0&&dist>1){ // reach = melee attack with a conditional gap-closing lunge
    if(dist>ab.reach||isRooted(owner)){B.line(`${owner.name}'s ${ab.name} falls short — ${target.name} stayed out of reach.`,cls);return false;}
    if(gapClose(B,owner,target)){dist=hdist(owner.cell,target.cell);B.line(`${owner.name} lunges in on ${target.name} with ${ab.name}.`,cls);}
  }
  const{outcome,bandMod}=evalRange(ab,dist);
  if(outcome==="Impossible"){B.line(`${owner.name} is too far to land ${ab.name} on ${target.name}.`,cls);return false;}
  // System 3: Jab-Cross (and any future Combo-tagged ability) resolves as two real strikes
  // instead of one hit standing in for two — see resolveComboStrikes. Every other ability keeps
  // running through the exact same resolveStrike() call this always made, just factored out so
  // the combo path can reuse it instead of reimplementing wardNext/accuracy/evasion a second time.
  if(ab.tags.includes("Combo")){resolveComboStrikes(B,owner,ab,target,bandMod,outcome,point);return;}
  resolveStrike(B,owner,ab,target,bandMod,outcome,point);
}
// The extracted core of a single strike: one wardNext check, one accuracy roll, one effect
// application. Returns true if the strike landed — used by resolveComboStrikes to decide
// whether the cross auto-hits or has to earn its own roll. NOT resolveSingleEnemy's own return
// value/contract (false there means "refund the cost," which a miss or parry must never do) —
// callers of resolveSingleEnemy never see this return value, only resolveComboStrikes does.
function resolveStrike(B,owner,ab,target,bandMod,outcome,point,effectOverride){
  const cls="f"+owner.faction;
  if((target.wardNext||0)>0&&target.faction!==owner.faction){
    target.wardNext--;
    B.line(`${target.name} parries ${owner.name}'s ${ab.name}!`,"f"+target.faction);B.ev("parry",{who:target,by:owner,ab});
    matchWardClashRules(B,target,owner,ab);
    recordResisted(owner,target,ab);
    return false;
  }
  const clumsy=outcome==="Clumsy";
  if(ab.dmg!=="None"){
    let sm=hasStatus(owner,"Blind")?BAL.blindAccuracyPenalty:0;if(hasStatus(target,"Prone"))sm+=BAL.proneHitBonus;if(isGrappled(target)||isMounted(target))sm+=BAL.grappleHitBonus;if(clumsy)sm+=BAL.clumsyHitPenalty;
    const acc=DR.acc(eff(owner)),eva=DR.eva(eff(target)),hit=clamp(BAL.baseHitChance+acc-eva+sm,0,100)*(bandMod/100),roll=rand()*100;
    if(!(roll<hit)){
      const calc=`Hit chance = base ${BAL.baseHitChance} + ACC ${round(acc)} − EVA ${round(eva)}${sm?` ${sm>=0?"+":""}${sm} situational`:""}${bandMod!==100?`, ×${bandMod}% range`:""} = ${round(hit)}%\nRoll ${round(roll)} ≥ ${round(hit)}% → evaded`;
      B.line(`${owner.name}'s ${ab.name} is evaded by ${target.name}.`,cls,calc);B.ev("evade",{who:target,by:owner,ab});
      // System 3: a missed kick/punch grants the OPPONENT — target, the fighter who dodged, not
      // the one who missed — a bonus DC on their own queued Single Leg Shot/Clinch, but only if
      // it's their very next queued action. peekNextQueued(B,target) here is opponent-reactive,
      // the same shape it was built for — not the misser's own queue.
      const opp=peekNextQueued(B,target);
      if(isKick(ab)&&opp&&opp.name==="Single Leg Shot"){
        target.statuses.push({kind:"GrappleSetup",rounds:1,stacks:1,tick:0,mag:BAL.kickWhiffShotBonus});
        B.line(`${target.name} reads the miss — the takedown is wide open.`,"f"+target.faction);
      }else if(isPunch(ab)&&opp&&opp.name==="Clinch"){
        target.statuses.push({kind:"GrappleSetup",rounds:1,stacks:1,tick:0,mag:BAL.punchWhiffClinchBonus});
        B.line(`${target.name} reads the miss — the clinch is wide open.`,"f"+target.faction);
      }
      recordResisted(owner,target,ab);
      return false;
    }
  }
  if(effectOverride)applyDamage(B,owner,ab,target,effectOverride,1,clumsy);
  else applyEffects(B,owner,ab,target,1,clumsy,point);
  return true;
}
// Called Shot travels as a beam, not a bolt at one man: anyone standing between the archer and
// the aimed target catches it too. Runs after the aimed shot resolves (hit or miss — a called
// shot that whiffs its precise mark still flies clean through anyone in its way). No separate
// evasion roll for the incidental hits, same convention as every other multi-target burst
// (Arrow Rain, Whirlwind Kick, the Ultimate eruptions) — friendly fire is scaled down, not
// prevented, via the same BAL.aoeFriendlyFireMultiplier those use.
function calledShotBeam(B,owner,ab,primary,aimCell){
  aimCell=aimCell||(primary&&primary.cell);if(!aimCell)return;
  const n=hdist(owner.cell,aimCell);if(n<=1)return;
  const path=new Set();
  for(let i=1;i<n;i++){const t=i/n;const q=owner.cell.q+(aimCell.q-owner.cell.q)*t+1e-4,r=owner.cell.r+(aimCell.r-owner.cell.r)*t+1e-4;path.add(hkey(cubeRound(q,r)));}
  const caught=B.all.filter(f=>alive(f)&&f!==owner&&f!==primary&&path.has(hkey(f.cell)));
  for(const t of caught){
    const scale=t.faction===owner.faction?BAL.aoeFriendlyFireMultiplier:1;
    B.line(`  ${t.name} is caught in the arrow's path!`,"sys");
    for(const e of ab.effects)if(e.k==="Damage")applyDamage(B,owner,ab,t,e,scale,false,true);
    if(B.decided())break;
  }
}
// Jab, then a cross that's automatic if the jab landed (too fast to react to twice — a fresh
// Parry charge arriving at exactly the right instant still can't stop it) and gets its own
// honest, independent roll if the jab missed or got parried. Beating a single Parry charge
// falls out of this for free: the jab's own resolveStrike call burns the charge, and the cross's
// separate resolveStrike call checks wardNext again and finds it already spent.
function resolveComboStrikes(B,owner,ab,target,bandMod,outcome,point){
  const[jabFx,crossFx]=ab.effects;
  const jabLanded=resolveStrike(B,owner,ab,target,bandMod,outcome,point,jabFx);
  if(jabLanded){
    if(alive(target)){
      B.line(`${owner.name}'s cross follows through automatically!`,"f"+owner.faction);
      applyDamage(B,owner,ab,target,crossFx,1,outcome==="Clumsy");
    }
  }else{
    resolveStrike(B,owner,ab,target,bandMod,outcome,point,crossFx);
  }
}
function blastFoliage(B,center,radius,cls){const d=B.grid.blastTerrain(center,radius);if(d.trees||d.bushes){const parts=[];if(d.trees)parts.push(`fells ${d.trees} tree${d.trees>1?"s":""}`);if(d.bushes)parts.push(`clears ${d.bushes} bush${d.bushes>1?"es":""}`);B.line(`  The blast ${parts.join(" and ")}.`,cls);}}
// A ground hazard (Spike Pit, Caltrops, ...) goes off against whoever occupies its cell: once
// the instant it's laid, then again each round anyone remains on it. Never hurts its own owner.
function triggerHazard(B,fighter){
  if(!alive(fighter))return;const hz=B.grid.hazardAt(fighter.cell);if(!hz||hz.owner===fighter)return;
  const cls="f"+hz.owner.faction;let scale=1;if(fighter.faction===hz.owner.faction)scale*=BAL.aoeFriendlyFireMultiplier;
  B.line(`${fighter.name} sets off ${hz.owner.name}'s ${hz.name}!`,cls);
  applyEffects(B,hz.owner,{name:hz.name,dmg:hz.dmg,poiseMult:hz.poiseMult,poiseCap:hz.poiseCap,tags:["Trap"],effects:hz.effects},fighter,scale,false);
}
function resolveAoe(B,owner,ab,point){
  const cls="f"+owner.faction;const target=point?null:B.nearestPerceivedEnemy(owner);const center=point?{...point}:(target?target.cell:owner.cell);
  const radius=ab.tags.includes("Ultimate")?BAL.ultimateAoeRadius:(ab.effects.some(e=>e.k==="Terrain")?max(0,round(ab.radius)):BAL.normalAoeRadiusCap);
  if(!owner.isPlayer&&owner.mc>0&&hdist(owner.cell,center)>ab.maxR&&!isRooted(owner))approach(B,owner,center,0);
  if(evalRange(ab,hdist(owner.cell,center)).outcome==="Impossible"){B.line(`${owner.name}'s ${ab.name} can't reach that area.`,cls);return false;}
  // terrain-placing effects
  for(const te of ab.effects)if(te.k==="Terrain"){const placedCells=[];for(const c of B.grid.within(center,radius)){if(te.kind==="Wall"&&B.occupied(c,null))continue;B.grid.set(c,te.kind,te.dur,te.kind==="Wall"?BAL.terrainWallHp:0);if(te.trigger)B.grid.setHazard(c,{effects:te.trigger,dmg:ab.dmg,poiseMult:ab.poiseMult,poiseCap:ab.poiseCap,name:ab.name,owner});placedCells.push(c);}
    if(placedCells.length)B.line(`${owner.name}'s ${ab.name} reshapes ${placedCells.length} cells (${te.kind}).`,cls);
    // a hazard trap can go off the instant it's laid, if someone's already standing on it
    if(te.trigger)for(const c of placedCells)for(const f of B.all)if(alive(f)&&f.cell.q===c.q&&f.cell.r===c.r)triggerHazard(B,f);}
  // damaging AoE destroys foliage: fells trees (sight opens) and clears bushes
  if(ab.effects.some(e=>e.k==="Damage"))blastFoliage(B,center,radius,cls);
  const hits=B.all.filter(c=>alive(c)&&hdist(c.cell,center)<=radius&&c!==owner);
  if(hits.length>=2)B.line(`${owner.name} unleashes ${ab.name}, catching ${hits.length} in the blast!`,cls);
  hits.forEach((t,i)=>{const wasHidden=hasStatus(t,"Stealth");let scale=1-BAL.aoeFalloffPerTarget*i;if(t.faction===owner.faction)scale*=BAL.aoeFriendlyFireMultiplier;applyEffects(B,owner,ab,t,max(0.1,scale),false);if(wasHidden&&alive(t)){removeStatus(t,"Stealth");t.stealthAge=0;B.line(`${t.name} is blasted out of hiding!`,cls);}});
}
/* Progression accrual: ability XP is keyed by a STABLE identity (disc|name),
   not the per-build runtime id. The engine only records raw effect output into
   B.xp; the curve/commit logic lives in the AFUI progression layer. */
function abilityKey(ab){return (ab.disc||"?")+"|"+ab.name;}
function awardAbilityXp(B,owner,ab,raw){if(!B||!B.xp||!owner||!ab||!(raw>0))return;let m=B.xp.get(owner);if(!m){m=new Map();B.xp.set(owner,m);}const k=abilityKey(ab);m.set(k,(m.get(k)||0)+raw);}

/* ---- System 3: ability clashes -------------------------------------------
   Specific abilities reacting to specific abilities when they land in a specific order, on
   top of the initiative system that already exists. Three trigger points, matching the three
   moments an attack can "happen": a landed hit (matchClashRules, from applyDamage), a parried
   hit (matchWardClashRules, from resolveStrike's wardNext branch), and a landed grapple entry
   (matchGrappleClashRules, from applyGrapple). All three read peekNextQueued to see what the
   OTHER fighter has queued next — never a guess, since B.sched holds the live schedule. */
// resolveRound builds `sched` fresh every round and drives its own picking loop off it; exposing
// the same array/objects on B lets anything holding a Battle reference peek at (or, for
// stealInitiative/grantInitiative, mutate) the live schedule without changing any call signature.
function peekNextQueued(B,fighter){
  if(!B.sched)return null;
  const s=B.sched.find(x=>x.owner===fighter);
  if(!s||s.next>=s.actions.length)return null;
  return actAbility(s.actions[s.next]);
}
// A GapCloser that also swings (damage) vs. one that's pure repositioning (Shadow Step, Mach
// Dash, ...). Rewarding a read against the latter is rewarding a fighter for stopping a
// relocation, not for reading an attack — the roster already draws this line, this just reads it.
const isDamagingRush=ab=>ab.tags.includes("GapCloser")&&ab.effects.some(e=>e.k==="Damage");
const isMobilityRush=ab=>ab.tags.includes("GapCloser")&&!isDamagingRush(ab);
// Reuses posMeta(ab).noStanding — verified true on exactly six abilities, all kicks (a kick
// needs a planted base leg, the same reason it can't be thrown mid-grapple either).
const isKick=ab=>!!posMeta(ab).noStanding;
// No equivalent implicit signal for punches, so an explicit name list — checked against every
// kit that carries Clinch (Boxing, Muay Thai, Judo, JiuJitsu): every strike in those kits that
// isn't itself Clinch, a kick, a stance, an elbow/knee, or Dirty Boxing (which requires an
// existing standing grapple via req:REQ.STANDING, so it can never precede a Clinch attempt).
const isPunch=ab=>["Jab-Cross","Uppercut","Haymaker","Body Shot","Judo Chop"].includes(ab.name);
// Checked from inside applyDamage. Tier 2 (literal name pairs, bespoke) first, Tier 1
// (structural predicates) as the fallback, null for the common case. Returns a flat result
// object rather than an effects array — this ships with four total rules, not a rule engine.
function matchClashRules(B,owner,ab,target){
  const next=peekNextQueued(B,target);
  // Tier 2 — the flagship signature: a clean uppercut on an incoming shot is decisive, not a
  // little unlucky. poiseFloor is guard-break-caliber (matches Choke Slam's 2.0 — the roster's
  // one true ceiling; Suplex is a standard 1.5x Guard Break, not this tier) even
  // though no grapple state is active — the read itself is what earns it.
  if(ab.name==="Uppercut"&&next&&next.name==="Single Leg Shot")
    return{bonusDamageMult:1.4,poiseFloor:2.0,negateNext:true,
      log:`${owner.name} catches the shot with a critical uppercut — stuffed cold!`};
  // Name-specific attacker, structural defender (same shape as "Hilt Bash catches a Stance
  // opener"): Teep Kick's Guard Break is earned here, not authored as a flat property of the
  // move — only when it actually lands while the target's own next queued action is a
  // damaging, Priority-tagged rush, the same condition teepAntiPriorityBonus checks to let it
  // win that race in the first place. Floored at 1.5, its old unconditional value — this
  // isn't a buff, it's the same number made conditional.
  if(ab.name==="Teep Kick"&&next&&isDamagingRush(next)&&next.tags.includes("Priority"))
    return{poiseFloor:1.5,log:`${owner.name} reads the rush and catches it clean!`};
  // Tier 1 — caught mid-entry: a damage hit lands on a fighter about to grapple.
  if(next&&ab.effects.some(e=>e.k==="Damage")&&next.effects.some(e=>e.k==="Grapple"||e.k==="GrappleTech"))
    return{bonusDamageMult:1.3,weakenNextMult:0.5,log:`${owner.name} catches ${target.name} mid-entry!`};
  // Deliberately no "any damaging hit interrupts a Stance/Charge wind-up" rule (removed
  // 2026-08-25, owner call): ordinary chip damage must NOT cancel a commitment. Only a poise
  // break (stagger) or hard CC (Stun/Fear via deniedByCc, Prone's own pendingSkips) should —
  // and both of those already cancel the target's next queued action universally, with no clash
  // rule needed at all. See applyDamage's `broke` branch and applyStatus's Prone handling.
  // Tier 1 — off-balance: a Push lands on a fighter about to answer with a melee reprisal.
  if(ab.effects.some(e=>e.k==="Push")&&next&&next.atk==="Melee"&&next.targeting==="SingleEnemy")
    return{weakenNextMult:0.7,log:`${target.name} is off-balance from the shove!`};
  return null;
}
// Checked from resolveStrike's wardNext branch — a successful parry negates for free, this is
// the reward for reading something worth reading (or, for Jab-Cross, why it isn't a full block).
function matchWardClashRules(B,target,owner,ab){
  if(ab.name==="Karate Blitz"){
    const os=B.sched&&B.sched.find(s=>s.owner===owner),ts=B.sched&&B.sched.find(s=>s.owner===target);
    if(ts)ts.init-=14;if(os)os.init+=14;
    B.line(`  ${target.name} punishes the read!`,"sys");
  }
}
// Checked from applyGrapple's success branch — a landed shot commits the wrestler's own head
// and hands to the entry, which is its own liability if the striker has an uppercut queued.
function matchGrappleClashRules(B,owner,target,ab){
  if(ab.name!=="Single Leg Shot")return;
  const next=peekNextQueued(B,target);
  if(next&&next.name==="Uppercut"){
    target.pendingPoiseFloor=2.0;
    B.line(`  ${owner.name}'s guard is wide open from the clinch.`,"sys");
  }
}

function applyEffects(B,owner,ab,target,extraScale,clumsy,point){
  for(const e of ab.effects){switch(e.k){
    case"Damage":applyDamage(B,owner,ab,target,e,extraScale,clumsy);break;
    case"Heal":{const h=max(0,round(e.power*(ab.healOutputMult??1)*affinity(owner.sign,target.sign).healDone));const before=target.hp;target.hp=min(target.maxHp,target.hp+h);awardAbilityXp(B,owner,ab,target.hp-before);B.line(`${owner.name} mends ${target.name}, restoring ${GRN(h)}.`,"f"+owner.faction);break;}
    case"Status":if(applyStatus(B,owner,target,e,ab)&&owner!==target)awardAbilityXp(B,owner,ab,BAL.xpControlRaw||8);break;case"Res":applyResource(B,target,e);break;
    case"MC":if(!isRooted(owner))owner.mc=(owner.mc||0)+round(e.amt);break;
    case"Move":moveSelf(B,owner,target,e.tiles);break;case"Push":pushTarget(B,owner,target,e.tiles);break;case"Buff":target.buffs.push({stat:e.stat,pct:e.pct,rounds:max(1,e.dur)});break;
    case"SelfMark":owner.statuses.push({kind:e.mark,rounds:e.dur,stacks:1,tick:0,mag:e.mag||0});break;
    case"Grapple":applyGrapple(B,owner,target,e,ab);break;case"Takedown":applyTakedown(B,owner,target,e,ab);break;case"GrappleTech":applyGrappleTech(B,owner,target,e,ab,point);break;
    case"WardNext":target.wardNext=(target.wardNext||0)+1;B.line(`${target.name} braces to parry the next targeted hostile ability.`,"f"+target.faction);break;
    case"SpawnSummon":spawnSummon(B,owner,point);break;case"Haunt":applyHaunt(B,owner,target);break;case"ActivateEye":activateEye(B,owner,e.planet);break;
  }}
}
function applyDamage(B,owner,ab,target,e,extraScale,clumsy,beamSecondary){
  if(B.god&&target.isPlayer)return;const os=eff(owner),ts=eff(target);const mit=target.poise>0;const base=baseDamage(ab.dmg,e.power,os,ts,mit);
  const clash=matchClashRules(B,owner,ab,target);
  // Called Shot always resolves through the Charge/erupt path (see resolveRound's chargeBeam
  // branch), so reaching applyDamage at all already means the archer held the draw — the crit
  // + poise floor is unconditional on the aimed target, never on a beamSecondary hit (anyone
  // else caught in the shot's path, see calledShotBeam).
  const drawnShot=ab.name==="Called Shot"&&!beamSecondary;
  let mult=extraScale*affinity(owner.sign,target.sign).dmgDone*affinity(target.sign,owner.sign).dmgTaken;
  if(ab.dmg==="Physical"){const cripple=owner.statuses.filter(s=>s.kind==="Cripple").reduce((n,s)=>n+(s.stacks||1),0);if(cripple>0)mult*=max(0,1-0.05*min(3,cripple));}
  if(clumsy)mult*=BAL.clumsyDamageMultiplier;if(isExhausted(target))mult*=BAL.exhaustionDamageMultiplier;mult*=BAL.damageScale;mult*=dmgMult(ab);
  // System 3: a weakenNext consequence from an earlier clash lands on this fighter's OWN next
  // action, read once and reset — then this hit's own clash bonus (if any) on top of that.
  if(owner.pendingClashMult&&owner.pendingClashMult!==1){mult*=owner.pendingClashMult;owner.pendingClashMult=1;}
  if(clash&&clash.bonusDamageMult)mult*=clash.bonusDamageMult;
  if(drawnShot)mult*=1.6;
  const fort=getStatus(target,"Fortified");if(fort)mult*=clamp(1-fort.mag/100,0,1);
  const dmg=max(0,round(base*mult));const poiseBasis=mit?max(0,round(baseDamage(ab.dmg,e.power,os,ts,false)*mult)):dmg;
  let pm=(ab.poiseMultWhenGrappling&&isGrappling(owner))?max(ab.poiseMult||1,ab.poiseMultWhenGrappling):ab.poiseMult;
  // System 3: poiseFloorNext (a pending flag set by an earlier clash, e.g. a landed grapple) and
  // poiseFloor (from THIS hit's own clash match) both fold in via the same max() idiom already
  // used for poiseMultWhenGrappling — floor, not add, so they never stack additively.
  pm=max(pm,owner.pendingPoiseFloor||0);owner.pendingPoiseFloor=0;
  if(clash&&clash.poiseFloor)pm=max(pm,clash.poiseFloor);
  if(drawnShot)pm=max(pm,1.75);
  // poiseDamage clamps pm to ab.poiseCap||BAL.poiseDmgMultMax (1.5) internally — a floor above
  // that default ceiling needs the cap raised to match, or it's clamped away to nothing. Only
  // ever raises the cap (never lowers it), so every ability without an active poiseFloor keeps
  // its exact existing ceiling — this is a no-op there, same as Choke Slam, the one ability that
  // already pairs poiseMult:2 with its own explicit poiseCap:2.
  const pd=poiseDamage(poiseBasis,ab.dmg,pm,max(ab.poiseCap||BAL.poiseDmgMultMax,pm));let broke=false;if(pd>0){target.poise-=pd;if(target.poise<=0){target.poise=0;broke=true;target.poiseRecoverDelay=1;}}
  let hpDmg=dmg;const sh=target.statuses.find(s=>s.kind==="Shield"&&s.mag>0);if(sh&&hpDmg>0){const soak=min(hpDmg,round(sh.mag));sh.mag-=soak;hpDmg-=soak;B.line(`  ${target.name}'s shield absorbs ${soak}.`);if(sh.mag<=0)sh.rounds=0;}
  target.hp=max(0,target.hp-hpDmg);target._flash=true;const killed=!alive(target);awardAbilityXp(B,owner,ab,hpDmg);
  B.line(`${owner.name} · ${ab.name} → ${target.name} for ${RED(hpDmg)}${killed?" — <b class='k'>DOWN</b>":""}.`,"f"+owner.faction);
  if(clash&&clash.log)B.line(`  ${clash.log}`,"sys");
  B.ev("hit",{who:target,by:owner,ab,hp:hpDmg,poise:pd,guarded:mit,broke,killed});
  if(pd>0&&alive(target))B.line(`  ${target.name}'s guard loses ${pd} poise (${max(0,target.poise)}/${target.maxPoise}).`);
  if(hpDmg>0&&hasStatus(target,"Sleep")){removeStatus(target,"Sleep");B.line(`${target.name} jolts awake!`);}
  if(broke){target.pendingSkips+=BAL.staggerCancelsNextAction;B.line(`${target.name} reels — their guard shatters!`,"sys");}
  // System 3: the late consequences apply only if the target is still standing to carry them.
  if(clash&&alive(target)){
    if(clash.negateNext)target.pendingClashNegate=true;
    if(clash.weakenNextMult)target.pendingClashMult=clash.weakenNextMult;
    if(clash.stealInitiative||clash.grantInitiative){
      const os2=B.sched&&B.sched.find(s=>s.owner===owner),ts2=B.sched&&B.sched.find(s=>s.owner===target);
      if(clash.stealInitiative&&ts2)ts2.init-=clash.stealInitiative;
      if(clash.grantInitiative&&os2)os2.init+=clash.grantInitiative;
    }
  }
}
function applyStatus(B,owner,target,e,ab){
  if(e.status==="Blind"&&target.eyeActive&&target.activeEye==="Sun"){B.line(`  ${target.name}'s solar eye burns through the dark — Blind resisted.`);return false;}
  let saveCalc=null,appliedBreakDC=null;
  const dcScope=ab&&ab.group!=="Dojutsu"&&ab.group!=="Bloodline"&&ab.disc!=="Dojutsu";
  const model=(BAL.useCandidateDcModel&&dcScope&&owner!==target&&root.AFDC&&typeof root.AFDC.statusTier==="function"&&root.AFDC.statusTier(e))?root.AFDC:null;
  if(model){
    const tier=model.statusTier(e),svStat=model.saveStat(e),cs=model.controlStat(ab,e),os=eff(owner),ts=eff(target),roll=d(20);
    if(!svStat||!cs){B.line(`${target.name} resists ${e.status} — candidate DC metadata is incomplete.`,"sys");return false;}
    const atk=os[cs]??0,def=ts[svStat]??0,base=model.resolveCandidateSave({tier,attackerStat:atk,defenderStat:def,abilityLevel:ab?.abilityLevel||0,roll});
    const posBonus=positionalDcModifier(owner,ab),dc=base.dc+posBonus;
    const landed=roll===1?true:roll===20?false:roll<dc;appliedBreakDC=dc;
    const posNote=posBonus?` (positional ${posBonus>=0?"+":""}${posBonus} from ${relRole(owner)})`:"";
    if(!landed){B.line(`${target.name} resists ${e.status}.`,"sys",`Candidate save vs ${e.status} [${tier}]: ${svStat} defense ${def}; ${cs} control ${atk}; d20 ${roll} vs DC ${dc}${posNote} → resisted`);return false;}
    saveCalc=`Candidate save vs ${e.status} [${tier}]: ${svStat} defense ${def}; ${cs} control ${atk}; d20 ${roll} vs DC ${dc}${posNote} → failed`;
  }else if(e.save){let dc=e.save.dc+positionalDcModifier(owner,ab);const sv=eff(target)[e.save.stat],roll=d(20),total=sv+roll;appliedBreakDC=dc;
    if(total>=dc){B.line(`${target.name} resists ${e.status}.`,"sys",`Save vs ${e.status}: ${e.save.stat} ${sv} + d20 ${roll} = ${total} ≥ DC ${dc} → resisted`);return false;}
    saveCalc=`Save vs ${e.status}: ${e.save.stat} ${sv} + d20 ${roll} = ${total} · DC ${dc} not met → failed`;}
  const st={kind:e.status,rounds:e.dur,stacks:max(1,e.stacks),tick:e.tick||0,mag:e.tick||0,source:owner};
  if(["Stun","Fear","Sleep"].includes(e.status))st.breakDC=appliedBreakDC??(e.save?e.save.dc:BAL.ccBreakDefaultDC);
  if(["Stun","Fear"].includes(e.status))st.freeDenials=max(1,e.stacks);
  const wasHidden=hasStatus(target,"Stealth");target.statuses.push(st);
  if(e.status==="Prone")target.pendingSkips+=1;if(e.status==="Stealth"&&!wasHidden)target.stealthAge=0;
  if(target.hauntTarget&&["Stun","Fear","Sleep","Confusion","Prone"].includes(e.status))dispelHaunt(B,target,"its caster's concentration is shattered");
  B.line(owner===target?`${target.name} takes on ${e.status}.`:`${target.name} is gripped by ${e.status}.`,"sys",saveCalc);
  return true;
}
function applyResource(B,c,e){let amt=e.amt+(e.pct?round(maxRes(c,e.res)*e.pct):0);
  if(e.res==="Hp")c.hp=clamp(c.hp+amt,0,c.maxHp);else if(e.res==="Stamina")c.stam=clamp(c.stam+amt,0,c.maxStam);else if(e.res==="Chakra")c.chakra=clamp(c.chakra+amt,0,effMaxChakra(c));
  else if(e.res==="Poise"){if(amt>0&&hasStatus(c,"Mounted"))return;const wasUp=c.poise>0;const cap=(e.overcap&&c.poise>=c.maxPoise)?c.maxPoise+amt:c.maxPoise;c.poise=amt>0?min(cap,c.poise+amt):c.poise+amt;if(wasUp&&c.poise<=0){c.poiseRecoverDelay=1;c.pendingSkips+=BAL.staggerCancelsNextAction;B.line(`${c.name}'s guard is crushed outright!`);}}}
function maxRes(c,r){return r==="Hp"?c.maxHp:r==="Stamina"?c.maxStam:r==="Chakra"?effMaxChakra(c):r==="Poise"?c.maxPoise:0;}
function moveSelf(B,owner,ref,tiles){if(isRooted(owner))return;const steps=round(abs(tiles));if(steps<=0)return;if(tiles<0){approach(B,owner,ref.cell,0);}else{const{cells,dist}=B.grid.reachable(owner.cell,steps,c=>B.occupied(c,owner));let best=owner.cell,bd=hdist(owner.cell,ref.cell);for(const[,c]of cells){const dd=hdist(c,ref.cell);if(dd>bd){bd=dd;best=c;}}owner.cell=best;}}
// Knockback: steps the TARGET directly away from the owner one hex at a time, sliding to the
// nearest free cell each step (matches Rolling Throw's default unaimed-throw direction). Stops
// early if the target is boxed in. A forced displacement, not the target's own movement, so it
// isn't blocked by Root/Slow.
function pushTarget(B,owner,target,tiles){
  const steps=round(abs(tiles));
  for(let i=0;i<steps;i++){
    if(target.cell.q===owner.cell.q&&target.cell.r===owner.cell.r)break;
    const aim=hx(target.cell.q+(target.cell.q-owner.cell.q),target.cell.r+(target.cell.r-owner.cell.r));
    const dest=B.grid.nearestFree(aim,c=>B.occupied(c,target));
    if(B.occupied(dest,target))break;
    target.cell=dest;
  }
}
function applyGrapple(B,owner,target,e,ab){const cls="f"+owner.faction;
  if(isEngaged(owner)){B.line(`${owner.name} is already locked into a position.`,cls);return;}
  if(isEngaged(target)){B.line(`${target.name} is already tied up in another hold.`,cls);return;}
  const os=eff(owner),ts=eff(target);
  // A landed combo-starter (e.g. Judo Chop) marks the user for one bonus-DC grapple attempt.
  // Spent on the first attempt either way, win or lose — it is an opening, not insurance.
  const setup=getStatus(owner,"GrappleSetup");const bonus=setup?setup.mag:0;
  if(setup)removeStatus(owner,"GrappleSetup");
  if(ts.STR+ts.AGI+d(20)>=os.STR+os.AGI+BAL.grappleLandDC+bonus){B.line(`${target.name} shrugs off ${owner.name}'s grab${bonus?` (DC ${BAL.grappleLandDC}+${bonus})`:""}.`,cls);recordResisted(owner,target,ab);return;}
  awardAbilityXp(B,owner,ab,BAL.xpControlRaw||8);
  matchGrappleClashRules(B,owner,target,ab); // System 3 — fires only on a landed grapple, before the relationship actually changes
  enterStandingGrapple(B,owner,target,max(1,e.dur),{crush:e.crush,drain:e.drain,lifesteal:e.lifesteal});
}
// Standing Grapple: controller = Grappling, controlled = Grappled.
function enterStandingGrapple(B,controller,controlled,rounds,hold={}){
  setRelationship(controller,REL.GRAPPLING,controlled,REL.GRAPPLED,{rounds:max(1,rounds||1)});
  controlled.grappleLanded=true;controlled.grappleAge=0;controlled.grappleAttempts=0;
  controller.rel.hold={crush:hold.crush||0,drain:hold.drain||0,lifesteal:!!hold.lifesteal};
  controlled.rel.hold=controller.rel.hold;
  controller.mc=0;controlled.mc=0;
  if(B&&B.ev)B.ev("grapple",{who:controller,target:controlled});   // observational: the sprite replay pairs them
  if(B)B.line(`${controller.name} locks ${controlled.name} in a standing grapple — ${controller.name} is Grappling, ${controlled.name} is Grappled.`,"f"+controller.faction);
}
/* Ground Mount: top = Mounting, bottom = Mounted. Entering Mount CLEARS any standing
   Grappling/Grappled roles — the two relationship families are mutually exclusive, and
   Mounting never implies Grappling. Forced entry breaks the bottom fighter's Poise; a
   voluntary bottom transition (Pull Guard) preserves the user's CURRENT Poise. */
function enterMount(B,top,bottom,opt={}){
  clearRelationship(top);clearRelationship(bottom);
  setRelationship(top,REL.MOUNTING,bottom,REL.MOUNTED,{voluntary:!!opt.voluntary});
  bottom.grappleLanded=true;bottom.grappleAge=0;bottom.grappleAttempts=0;
  top.mc=0;bottom.mc=0;
  if(opt.voluntary){
    // Preserve means preserve, never restore: whatever Poise the fighter has, they keep.
    if(B)B.line(`${bottom.name} voluntarily pulls guard — ${bottom.name} is Mounted, ${top.name} is Mounting (Poise ${bottom.poise}/${bottom.maxPoise} preserved).`,"f"+bottom.faction);
  }else{
    bottom.poise=0;bottom.poiseRecoverDelay=1;
    // A forced Mount entry off a technique that also dealt damage (Suplex, Sweeping Shoulder,
    // Flying Triangle — not the 0-power Reversal) staggers the same way any other poise break
    // does elsewhere in the engine. The poise-zero here is unconditional either way; this is
    // only about whether it ALSO earns the free stagger-cancel on top of it.
    if(opt.stagger)bottom.pendingSkips+=BAL.staggerCancelsNextAction;
    // A reversal announces itself; suppress the generic entry line so the log reads once.
    if(B&&!opt.reversal)B.line(`${top.name} takes mount on ${bottom.name}, guard shattered — ${top.name} is Mounting, ${bottom.name} is Mounted.`,"f"+top.faction);
  }
}
// End a relationship (and any submission over it). Both fighters become Free at melee range.
function endRelationship(B,f,reason){
  const p=relPartner(f);if(!relRole(f)||relRole(f)===REL.FREE)return;
  const sub=clearSubmission(f);
  clearRelationship(f);
  if(B&&B.ev&&p)B.ev("release",{who:f,partner:p});   // observational: the sprite replay separates them
  if(B&&p)B.line(`${f.name} and ${p.name} break apart${reason?` — ${reason}`:""}. Both are Free at melee range.${sub?` The ${sub.name} is released.`:""}`,"sys");
}
// the cell n hexes past `from` on the far side from `away` (the hex line away -> from, extended)
function cellBehind(from,away,n){
  const d=max(1,hdist(from,away)),u=cubeRound((from.q-away.q)/d,(from.r-away.r)/d);
  return hx(from.q+u.q*n,from.r+u.r*n);
}
function applyTakedown(B,owner,target,e,ab){
  if(!alive(target))return;const cls="f"+owner.faction;
  const dest=B.grid.nearestFree(cellBehind(owner.cell,target.cell,e.behind),c=>B.occupied(c,target));
  if(!B.occupied(dest,target))target.cell=dest;
  if(e.status&&e.dur>0&&!hasStatus(target,e.status)){target.statuses.push({kind:e.status,rounds:e.dur,stacks:1,tick:0,mag:0,source:owner});if(e.status==="Prone")target.pendingSkips+=1;}
  B.line(`  ${target.name} is thrown down behind ${owner.name} — ${e.status||"down"}.`,cls);
  if(relPartner(owner)===target)endRelationship(B,owner,`${ab.name} breaks the hold`);
}
function applyGrappleTech(B,owner,target,e,ab,point){const cls="f"+owner.faction;
  const partner=relPartner(owner);
  if(!(partner===target&&relPartner(target)===owner)){B.line(`${owner.name}'s ${ab.name} needs a live relationship with ${target.name}.`,cls);return;}
  const os=eff(owner),ts=eff(target);const atk=e.best?max(os.STR+os.AGI,os.AGI+os.INT):os.STR+os.AGI;const def=e.best?max(ts.STR+ts.AGI,ts.AGI+ts.INT):ts.STR+ts.AGI;
  // A positional escape gets harder the longer the submission on the actor has been worked.
  const resist=posMeta(ab).escape?submissionEscapeResistance(owner):0;
  const dc=e.dc-resist;
  if(def+d(20)>=atk+dc){B.line(`${target.name} denies ${owner.name}'s ${ab.name}.${resist?` The ${activeSubmission(owner).name} has been locked in ${submissionEscapeTurns(owner)} turn${submissionEscapeTurns(owner)>1?"s":""} — escape DC ${e.dc} → ${dc}.`:""}`,cls);recordResisted(owner,target,ab);return;}
  // A submission being continued hits harder each consecutive round it has been held.
  const cont=e.submission?continuedSubmission(owner,ab):null;
  const powerMult=submissionDamageMult(cont);
  if(e.power>0)applyDamage(B,owner,ab,target,{power:round(e.power*powerMult)},1,false);
  if(e.dur>0&&e.status){const st={kind:e.status,rounds:e.dur,stacks:1,tick:0,mag:0,source:owner};if(e.status==="Sleep")st.breakDC=e.dc+4;target.statuses.push(st);B.line(`${target.name} is gripped by ${e.status}.`,cls);}
  if(e.focusLock>0){target.statuses.push({kind:"FocusLock",rounds:e.focusLock,stacks:1,tick:0,mag:0,source:owner});B.line(`  ${target.name} cannot draw breath — Focus actions are denied.`,cls);}
  if(e.drain>0){target.stam=max(0,target.stam-e.drain);B.line(`  ${ab.name} drains ${e.drain} stamina from ${target.name}.`);}
  if(e.selfAgi>0){owner.buffs.push({stat:"AGI",pct:e.selfAgi,rounds:1});B.line(`  ${owner.name} gains the angle.`);}
  // Relationship transitions resolve before submission establishment so the submission
  // is layered over the relationship that actually exists afterwards.
  if(e.mount){
    if(e.voluntaryBottom)enterMount(B,target,owner,{voluntary:true}); // Pull Guard: the USER goes to bottom
    else{
      // A reversal inverts an existing Mount; any submission over it dies with the old position.
      const lost=e.reversal?activeSubmission(owner):null;
      const wasMounted=e.reversal&&isMounted(owner);
      enterMount(B,owner,target,{voluntary:false,reversal:wasMounted,stagger:e.power>0});
      if(wasMounted)B.line(`${owner.name} reverses the position — ${owner.name} is now Mounting, ${target.name} is Mounted, guard shattered.${lost?` The ${lost.name} is broken.`:""}`,cls);
    }
  }
  if(e.submission&&inMount(owner)&&relPartner(owner)===target){
    if(cont){
      /* Escalation is per consecutive ROUND, not per use: working the hold twice in one round
         does not ratchet it twice. Repeat uses inside a round pay ordinary repetition strain. */
      if(cont.appliedRound!==B.round){
        cont.consecutive++;cont.appliedRound=B.round;
        B.line(`  ${owner.name} cranks ${ab.name} tighter — round ${cont.consecutive+1} of the hold; next round ×${submissionCostMult(cont).toFixed(1)} cost, ×${submissionDamageMult(cont).toFixed(1)} damage.`,cls);
      }else B.line(`  ${owner.name} works ${ab.name} again — the hold is already at round ${cont.consecutive+1} pressure.`,cls);
    }else{
      const rec=setSubmission(owner,target,ab,ab.name,B.round);
      B.line(`  ${owner.name} locks in ${ab.name} as a Maintained Submission from ${relRole(owner)}. Re-queue it every round or the hold is released.`,cls);
      rec.appliedRound=B.round;
    }
  }
  if(e.throw>0){
    // Default (AI, or no aim given): straight-line away from the owner, as before. A player
    // may instead aim the throw anywhere within the ability's authored throw range of the
    // target's CURRENT cell — e.g. onto a hazard tile. An out-of-range point is ignored
    // rather than trusted, since the UI is expected to only ever offer in-range cells.
    // behind: the doc's "3 tiles away from user", landing on the user's far side (user ruling 2026-10-15)
    let aim=e.behind?cellBehind(owner.cell,target.cell,e.throw):hx(target.cell.q+(target.cell.q-owner.cell.q),target.cell.r+(target.cell.r-owner.cell.r));
    if(point&&hdist(target.cell,point)<=e.throw)aim=point;
    const dest=B.grid.nearestFree(aim,c=>B.occupied(c,target));if(!B.occupied(dest,target))target.cell=dest;
    B.line(`${target.name} is thrown clear!`,cls);endRelationship(B,owner,"the throw lands");}
  else if(e.breakHold)endRelationship(B,owner,`${ab.name} breaks the hold`);}
function applyHaunt(B,owner,target){if(owner.hauntTarget){B.line(`${owner.name}'s phantom is already bound.`,"f"+owner.faction);return;}if(target.hauntedBy){B.line(`${target.name} is already haunted.`);return;}owner.hauntTarget=target;target.hauntedBy=owner;B.line(`Something slips out of ${target.name}'s shadow — a phantom only they and ${owner.name} can see.`,"f"+owner.faction);}
function dispelHaunt(B,caster,reason){const v=caster.hauntTarget;if(!v)return;caster.hauntTarget=null;if(v.hauntedBy===caster)v.hauntedBy=null;B.line(`${caster.name}'s phantom unravels — ${reason}.`);}
function deniedByCc(B,owner){const stun=getStatus(owner,"Stun");if(stun&&denyOne(B,owner,stun,null))return true;const fear=getStatus(owner,"Fear");if(fear&&denyOne(B,owner,fear,fear.source))return true;return false;}
function denyOne(B,owner,s,fleeFrom){if((s.freeDenials||0)<=0&&eff(owner).STR+d(20)>=s.breakDC){removeStatus(owner,s.kind);B.line(`${owner.name} shakes off the ${s.kind}!`);return false;}if(s.freeDenials>0)s.freeDenials--;else s.breakDC-=BAL.ccBreakDecay;
  if(fleeFrom&&alive(fleeFrom)){const away=B.grid.nearestFree(hx(owner.cell.q+(owner.cell.q-fleeFrom.cell.q),owner.cell.r+(owner.cell.r-fleeFrom.cell.r)),c=>B.occupied(c,owner));if(!B.occupied(away,owner))owner.cell=away;B.line(`${owner.name} recoils from ${fleeFrom.name} in fear.`);}else B.line(`${owner.name} is ${s.kind} — the action is lost.`);return true;}
function activateEye(B,owner,planet){owner.activeEye=planet;owner.eyeActive=true;owner.strain+=BAL.strainOnActivate;B.line(`  ${owner.name} opens the ${EYES[planet].deity} (strain ${round(owner.strain)}%).`,"f"+owner.faction);checkBurnout(B,owner);}
function checkBurnout(B,c){if(c.strain<100)return;c.strain=100;c.eyeActive=false;c.activeEye=null;c.statuses.push({kind:"Blind",rounds:BAL.burnoutDurationTurns,stacks:1,tick:0,mag:0});c.noChakraRegen=BAL.burnoutDurationTurns;B.line(`  ${c.name}'s optic nerves scorch — Burnout! Blinded ${BAL.burnoutDurationTurns} rounds.`);}
function spawnSummon(B,owner,point){if(owner.isSummon)return;if(owner.activeSummon&&alive(owner.activeSummon)){B.line(`  ${owner.name}'s ${owner.activeSummon.name} is already out.`);return;}
  const sp=owner.summonSpecies||{name:"Guardian Spirit",role:"DPS"};const st=SUMMON_STATS[sp.role]||SUMMON_STATS.Generic;
  const cell=B.grid.nearestFree(point||owner.cell,c=>B.occupied(c,null));
  const s=makeFighter({name:sp.name.split(" ")[0],sign:owner.sign,stats:{...st},faction:owner.faction,cell,glyph:"✦",isSummon:true});s.role=sp.role;s.abilities=summonAbilities(sp);s.persona="aggressive";
  owner.activeSummon=s;owner.chakraReserved=2*BAL.summonReservePerTier;owner.chakra=min(owner.chakra,effMaxChakra(owner));B.pending.push(s);
  B.line(`  ${owner.name} summons ${s.name}! (chakra reserved ${owner.chakraReserved})`,"f"+owner.faction);}
/* =========================================================================
   CANONICAL END-OF-ROUND ORDER (Sheet: "Maintenance order")
     1. resolve normal round actions
     2. Post-Round Effects / status ticks   -> postRoundEffects()
     3. Relationship Maintenance            -> relationshipMaintenance()
     4. Passive Resource Recovery           -> passiveRecovery()
     5. next-round planning
   Maintenance runs BEFORE recovery, so a fighter can never rely on the regen
   that is about to happen in order to pay this cycle's upkeep.
   ========================================================================= */
function postRoundEffects(B,c){if(!alive(c))return;
  for(let i=c.statuses.length-1;i>=0;i--){const s=c.statuses[i];
    if(s.relationship)continue; // relationship mirrors never decay on the status clock
    if(["Bleed","Burn","Poison","Psychosomatic"].includes(s.kind)&&s.tick>0){const t=round(s.tick*s.stacks);c.hp=max(0,c.hp-t);B.line(`${s.kind} gnaws at ${c.name} for ${RED(t)}.`);}
    else if(s.kind==="Regen"&&s.tick>0)c.hp=min(c.maxHp,c.hp+round(s.tick*s.stacks));if(s.kind!=="Stealth"&&--s.rounds<=0)c.statuses.splice(i,1);}
  if(hasStatus(c,"Stealth")){c.stealthAge++;const det=B.enemies(c).sort((a,b)=>DR.perception(eff(b))-DR.perception(eff(a)))[0];
    if(det&&c.stealthAge>=2){const hide=DR.perception(eff(c))+d(20);const dc=DR.perception(eff(det))+BAL.stealthBaseDC+(c.stealthAge-2)*BAL.stealthDcPerRound;if(hide<dc){removeStatus(c,"Stealth");c.stealthAge=0;B.line(`  ${det.name} sees through ${c.name}'s concealment!`);}}}else c.stealthAge=0;
  const sleep=getStatus(c,"Sleep");if(sleep){if(eff(c).FORT+d(20)>=sleep.breakDC){removeStatus(c,"Sleep");B.line(`  ${c.name} stirs awake.`);}else sleep.breakDC-=BAL.ccBreakDecay;}
  if(c.hauntTarget){if(!alive(c)||!alive(c.hauntTarget))dispelHaunt(B,c,"its anchor is gone");else{const v=c.hauntTarget;const claw=round((BAL.hauntTickMental+eff(c).CHA*0.5)*BAL.damageScale);v.hp=max(0,v.hp-claw);B.line(`The phantom claws at ${v.name} for ${RED(claw)} — no guard can turn what only they can see.`);c.chakra=max(0,c.chakra-BAL.hauntUpkeepChakraPerTurn);if(c.chakra<=0)dispelHaunt(B,c,"its caster's chakra has run dry");}}
  for(let i=c.buffs.length-1;i>=0;i--)if(--c.buffs[i].rounds<=0)c.buffs.splice(i,1);
}

/* ---- Relationship Maintenance -------------------------------------------
   Processes each live relationship exactly once, from the controlling side.
   Order per pair: validity -> standing-hold upkeep/ticks -> submission upkeep
   -> ordinary Mount upkeep. Successful submission upkeep REPLACES Mount upkeep
   for that cycle; the two are never charged together. */
function relationshipPairs(B){
  const pairs=[],seen=new Set();
  for(const f of B.all){
    const role=relRole(f),p=relPartner(f);
    if(role!==REL.GRAPPLING&&role!==REL.MOUNTING)continue;
    if(!p||seen.has(f)||seen.has(p))continue;
    seen.add(f);seen.add(p);pairs.push({top:f,bottom:p,role});
  }
  return pairs;
}
function relationshipMaintenance(B){
  // Snapshot every fighter's role at the START of the phase: that snapshot drives this
  // cycle's passive recovery even if the relationship collapses during maintenance.
  const snapshot=new Map(B.all.map(f=>[f,relRole(f)]));
  for(const{top,bottom,role} of relationshipPairs(B)){
    if(!alive(top)||!alive(bottom)){endRelationship(B,top,"a participant is down");continue;}
    if(role===REL.GRAPPLING){maintainStandingGrapple(B,top,bottom);continue;}
    maintainMount(B,top,bottom);
  }
  return snapshot;
}
function maintainStandingGrapple(B,controller,controlled){
  const hold=controller.rel.hold||{};
  if(controller.releaseIntent){endRelationship(B,controller,`${controller.name} lets go`);return;}
  if(controller.stam<BAL.grappleHoldUpkeepStamina){
    B.line(`${controller.name} cannot pay the ${BAL.grappleHoldUpkeepStamina}-Stamina hold upkeep.`,"sys");
    endRelationship(B,controller,"the hold is not maintained");return;}
  controller.stam-=BAL.grappleHoldUpkeepStamina;
  controlled.grappleAge++;
  if(hold.crush>0){const crush=round(hold.crush);controlled.hp=max(0,controlled.hp-crush);B.line(`${controller.name} crushes ${controlled.name} for ${RED(crush)}.`);
    if(hold.lifesteal){controller.hp=min(controller.maxHp,controller.hp+crush);B.line(`  ${controller.name} drinks the strength from the hold (+${GRN(crush)}).`);}}
  if(hold.drain>0){controlled.stam=max(0,controlled.stam-round(hold.drain));B.line(`  The hold wrings ${round(hold.drain)} stamina out of ${controlled.name}.`);}
  if(controller.rel.rounds>0){
    controller.rel.rounds--;controlled.rel.rounds=controller.rel.rounds;
    if(controller.rel.rounds<=0){endRelationship(B,controller,"the hold runs out");return;}
  }
}
/* A Maintained Submission is kept by USE, not by upkeep: the holder must re-queue the
   submission ability every round. A round that passes without it releases the hold. There is
   no passive payment, no reserved slot and no separate release control — simply not queueing
   it is the release. Mount upkeep still resolves afterwards on its own terms. */
function maintainMount(B,top,bottom){
  /* Submission first, then Mount. The prompt's "submission upkeep replaces Mount upkeep" rule
     existed to stop TWO passive charges stacking; the submission no longer has a passive
     charge at all, so Mount upkeep now always resolves on its own terms and the submission is
     paid purely through its escalating action cost. */
  const sub=activeSubmission(top);
  let submissionLive=false;
  if(sub&&sub.holder&&alive(sub.holder)){
    const holder=sub.holder;
    if(sub.appliedRound===B.round){
      submissionLive=true;
      B.line(`${holder.name} keeps ${sub.name} locked from ${relRole(holder)} — ${sub.consecutive+1} consecutive round${sub.consecutive?"s":""}; next round costs ×${submissionCostMult(sub).toFixed(1)} and hits ×${submissionDamageMult(sub).toFixed(1)}.`,"sys");
    }else{
      B.line(`${holder.name} did not work ${sub.name} this round — the hold is released.`,"sys");
      clearSubmission(holder);
    }
  }
  if(!inMount(top)||!relPartner(top))return;
  // Submission Lock: a live submission cannot be erased by voluntarily dropping Mount.
  if(top.releaseIntent){
    if(submissionLive)B.line(`  ${top.name} cannot give up the mount while ${sub.name} is locked in.`,"sys");
    else{endRelationship(B,top,`${top.name} gives up the mount`);return;}
  }
  if(top.stam<BAL.mountUpkeepStamina){
    B.line(`${top.name} cannot pay the ${BAL.mountUpkeepStamina}-Stamina Mount upkeep.`,"sys");
    endRelationship(B,top,"Mount is not maintained");return;}
  top.stam-=BAL.mountUpkeepStamina;
  B.line(`${top.name} pays ${BAL.mountUpkeepStamina} Stamina to hold the mount on ${bottom.name}.`,"sys");
}

/* ---- Passive Resource Recovery ------------------------------------------
   Canonical passive Stamina regen is computed first, then multiplied by the
   relationship factor from the maintenance-phase snapshot, then rounded. */
function passiveRecovery(B,c,snapshotRole){
  if(!alive(c))return;
  const role=snapshotRole||relRole(c);
  const base=DR.stamRegen(c.stats),factor=passiveStaminaFactor(role),gain=round(base*factor);
  if(gain>0)c.stam=min(c.maxStam,c.stam+gain);
  if(role!==REL.FREE)B.line(`  ${c.name} recovers ${gain} stamina (${role} ${Math.round(factor*100)}% of ${base}).`,"sys");
  if(c.noChakraRegen<=0&&!c.eyeActive)c.chakra=min(effMaxChakra(c),c.chakra+DR.chakRegen(c.stats));
  if(c.eyeActive){if(c.chakra>=BAL.eyeUpkeepChakraPerTurn){c.chakra-=BAL.eyeUpkeepChakraPerTurn;c.strain=min(100,c.strain+BAL.strainPerTurnActive);checkBurnout(B,c);}else{c.eyeActive=false;c.activeEye=null;B.line(`  ${c.name}'s eye flickers shut — not enough chakra.`);}}
  else if(c.strain>0)c.strain=max(0,c.strain-BAL.strainDecayPerTurn);
  if(c.activeSummon&&!alive(c.activeSummon)){c.activeSummon=null;c.chakraReserved=0;B.line(`  ${c.name}'s summon falls; reserved chakra returns.`);}
  if(c.noChakraRegen>0)c.noChakraRegen--;}

// Kept for callers that want the whole tail of a round in canonical order.
function endOfRound(B){
  B.all.forEach(c=>postRoundEffects(B,c));
  const snapshot=relationshipMaintenance(B);
  B.all.forEach(c=>passiveRecovery(B,c,snapshot.get(c)));
}

// Wraps one action so the event record shows it: an act event, the actor's own repositioning
// (approach, lunge) placed before it, and anyone else it displaced (push, throw) after it.
function traceAction(B,o,ab,entry,run){
  const before=new Map(B.all.map(f=>[f,f.cell])),at=B.events.length;
  B.ev("act",{who:o,ab,target:actTarget(entry)||null,point:actPoint(entry)||null});
  run();
  const moved=f=>before.has(f)&&hkey(before.get(f))!==hkey(f.cell);
  if(moved(o))B.events.splice(at,0,{type:"move",round:B.round,who:o,from:before.get(o),to:o.cell,phase:"action"});
  for(const f of B.all)if(f!==o&&moved(f))B.ev("knock",{who:f,by:o,from:before.get(f),to:f.cell});
}
function resolveRound(B,plans){
  B.line(`Round ${B.round}`,"round-sep");B.events=[];
  // the whole fight, round by round, for the post-fight recap: where everyone stood as the round began, then its event record
  (B.history||(B.history=[])).push({round:B.round,events:B.events,start:B.all.map(f=>({f,cell:{...f.cell},alive:alive(f),stam:f.stam,activeWeapon:f.activeWeapon,rel:f.rel&&f.rel.partner?{role:f.rel.role,partner:f.rel.partner}:null}))});
  B.pending=[];B.all.forEach(f=>startRound(B,f));const live=!B.decided();
  // Planned moves (players/AI move to a chosen destination cell within mc) resolve completely
  // before any action does — a real movement sub-phase, not interleaved with the action
  // sub-phase. Priority-ordered by current AGI (ties keep original plan order — a stable
  // sort): the highest-AGI mover gets first claim on any cell. If a fighter's chosen cell is
  // already taken by the time its turn comes (whether by direct contention over the same
  // target or incidental blocking), it instead claims whichever cell adjacent to its ORIGINAL
  // target is closest to it and still reachable. This replaces the old plans-array-order
  // resolution, where the fighter processed later always silently failed to move at all if its
  // target got claimed first — leaving its full movement budget unspent, which the separate
  // mid-action "still out of range, approach anyway" fallback could then spend to reach full
  // melee range a round sooner than the fighter who "won" the contested cell.
  const movers=plans.filter(p=>p.moveTo&&!isRooted(p.owner));
  movers.sort((x,y)=>eff(y.owner).AGI-eff(x.owner).AGI);
  for(const p of movers){
    const o=p.owner;
    const{cells,dist}=B.grid.reachable(o.cell,o.mc,c=>B.occupied(c,o));
    const k=hkey(p.moveTo),from=o.cell;
    if(cells.has(k)){o.cell=cells.get(k);o.mc-=dist.get(k);if(hkey(from)!==k)B.ev("move",{who:o,from,to:o.cell,phase:"move"});continue;}
    const alt=neighbors(p.moveTo).filter(c=>B.grid.inBounds(c)&&cells.has(hkey(c)))
      .sort((a,b)=>dist.get(hkey(a))-dist.get(hkey(b)))[0];
    if(alt){const ak=hkey(alt);o.cell=cells.get(ak);o.mc-=dist.get(ak);if(hkey(from)!==ak)B.ev("move",{who:o,from,to:o.cell,phase:"move"});}
  }
  // ground hazards (Spike Pit, Caltrops, ...) go off against whoever is standing on them once
  // positions for the round are settled, whether they just stepped in or never left
  for(const f of B.all)triggerHazard(B,f);
  // charges erupt
  for(const c of B.all){if(!alive(c)||!c.chargingAction)continue;const ab=c.chargingAction;c.chargingAction=null;
    // Single-target locked charges (Called Shot) fire a beam at the locked fighter's CURRENT
    // cell instead of blasting a fixed-radius area — the AoE Ultimates' eruption below is
    // otherwise universal for every Charge-tagged ability regardless of Ultimate tag, which
    // would turn a "called shot" into a 3-tile blast if it went through that path unchanged.
    if(ab.chargeBeam){B.ev("act",{who:c,ab,point:c.chargeTargetCell||c.cell});
      const fighterTarget=c.chargeTargetFighter;c.chargeTargetFighter=null;
      // Still tracking the locked target: keep the aim point glued to their CURRENT cell (they
      // may have moved since the draw). Lost them — dead, out of LoS, vanished into Stealth —
      // and the archer does NOT get a free retarget onto some other enemy: the shot goes to the
      // last place they were actually seen (c.chargeTargetCell, refreshed below every round
      // they're still tracked, so it's a real "last known", not just the cast-time snapshot).
      const tracked=fighterTarget&&alive(fighterTarget)&&B.perceives(c,fighterTarget,true);
      if(tracked)c.chargeTargetCell={...fighterTarget.cell};
      const aimCell=c.chargeTargetCell||c.cell;
      if(!B.grid.losHard(c.cell,aimCell)){B.line(`${c.name}'s ${ab.name} has no line of sight to the aim point.`,"f"+c.faction);continue;}
      // Whoever is tracked stays the primary hit. Otherwise the arrow still flies to that last
      // known cell and hits whoever happens to be standing there now — same as an Ultimate's
      // locked-cell eruption — rather than fizzling or picking a different target out of thin air.
      const primary=tracked?fighterTarget:B.all.find(x=>alive(x)&&x!==c&&hkey(x.cell)===hkey(aimCell));
      if(primary){
        B.line(`${c.name}'s drawn shot finds its mark!`,"f"+c.faction);
        for(const e of ab.effects)if(e.k==="Damage")applyDamage(B,c,ab,primary,e,1,false);
        calledShotBeam(B,c,ab,primary,aimCell);
      }else{
        B.line(`${c.name}'s drawn shot flies to ${fighterTarget?`${fighterTarget.name}'s`:"its"} last known position — but no one is there.`,"f"+c.faction);
        calledShotBeam(B,c,ab,null,aimCell);
      }
      if(live&&B.decided())break;
      continue;
    }
    B.line(`${c.name}'s ${ab.name} erupts!`,"f"+c.faction);B.ev("act",{who:c,ab,point:c.chargeTargetCell||c.cell});
    const center=c.chargeTargetCell||c.cell;const radius=BAL.ultimateAoeRadius;const hits=B.all.filter(x=>alive(x)&&hdist(x.cell,center)<=radius&&x!==c);
    if(ab.effects.some(e=>e.k==="Damage"))blastFoliage(B,center,radius,"f"+c.faction);
    hits.forEach((t,i)=>{let scale=1-BAL.aoeFalloffPerTarget*i;if(t.faction===c.faction)scale*=BAL.aoeFriendlyFireMultiplier;applyEffects(B,c,ab,t,max(0.1,scale),false);});
    if(live&&B.decided())break;}
  const sched=plans.filter(p=>alive(p.owner)&&p.actions.length).map(p=>({owner:p.owner,actions:p.actions.slice(),next:0,init:DR.baseInit(eff(p.owner))+d(BAL.initDie)}));
  B.sched=sched; // System 3: exposes the live schedule so peekNextQueued/matchClashRules can read (and mutate, for stealInitiative/grantInitiative) it from anywhere holding a Battle reference.
  // On an exact initiative-key tie, the higher CURRENT AGI acts first — same rule as the
  // movement phase's contested-cell priority, rather than favoring whoever's earlier in the
  // plans array. A remaining tie (AGI also equal) falls back to that array order, same as
  // before: the least-surprising default, not a claim that it's the "correct" tiebreak.
  while(true){if(live&&B.decided())break;let best=null,bk=-1e9,bagi=-1e9;for(const s of sched){if(s.next>=s.actions.length||!alive(s.owner))continue;const entry=s.actions[s.next];const key=s.init-ccInitPenalty(s.owner)-selOffset(actAbility(entry))+standingGrapplePriority(s.owner,entry)+teepAntiPriorityBonus(s,entry,sched);const agi=eff(s.owner).AGI;if(key>bk||(key===bk&&agi>bagi)){bk=key;bagi=agi;best=s;}}
    if(!best)break;const entry=best.actions[best.next];best.next++;const ab=actAbility(entry),o=best.owner;
    if(hasStatus(o,"Sleep")){B.line(`${o.name} is fast asleep.`);best.next=best.actions.length;continue;}
    if(o.pendingSkips>0){o.pendingSkips--;o.pendingClashNegate=false;B.line(`${o.name} is staggered — action canceled.`,"sys");continue;}
    best.init-=depletion(ab);traceAction(B,o,ab,entry,()=>resolveAction(B,o,ab,{target:actTarget(entry),point:actPoint(entry)}));if(live&&B.decided())break;}
  if(!(live&&B.decided()))endOfRound(B);
  B.grid.tick();
  if(B.pending.length){B.all.push(...B.pending);B.pending=[];}
}

/* AI planner — persona/FocusDiscipline driven */
/* An ability gated behind a martial/weapon stance is only plannable when that stance is
   already active on the fighter or earlier in the plan being built. This mirrors the V3
   plan sanitizer so AI plans never contain actions the player validator would reject.
   NOTE: the AI does not yet *seek out* a stance — see the handoff's known-gaps list. */
function stanceReadyFor(actor,ab,plan){
  const active=k=>(actor.activeMartial&&(actor.activeMartial.styleKey||actor.activeMartial.sourceKey)===k)
    ||(plan||[]).some(a=>a.tags.includes("MartialStance")&&a.styleKey===k);
  const activeW=k=>(actor.activeWeapon&&(actor.activeWeapon.weaponKey||actor.activeWeapon.sourceKey)===k)
    ||(plan||[]).some(a=>a.tags.includes("WeaponStance")&&a.weaponKey===k);
  if(ab.isStyleTechnique&&ab.parentStyles&&ab.parentStyles.length&&!ab.parentStyles.some(active))return false;
  if(ab.isWeaponTechnique&&ab.parentWeapons&&ab.parentWeapons.length&&!ab.parentWeapons.some(activeW))return false;
  return true;
}
/* If a fighter's kit is gated behind a martial/weapon stance and none of it is currently
   usable, open with the stance that unlocks the most legal techniques. This is legality
   plumbing, not strategy: without it a style NPC's entire kit is unreachable and the plan
   sanitizer would strip everything it queued. The stance itself must be positionally legal,
   so a Mount-illegal stance is never queued from Mount. */
function stanceOpener(actor,slotCap){
  const gated=actor.abilities.filter(a=>(a.isStyleTechnique&&a.parentStyles&&a.parentStyles.length)
    ||(a.isWeaponTechnique&&a.parentWeapons&&a.parentWeapons.length));
  if(!gated.length)return null;
  if(gated.some(a=>stanceReadyFor(actor,a,[])&&positionalLegality(actor,a).ok))return null;
  let best=null,bestUnlocked=0;
  for(const st of actor.abilities){
    if(!st.tags.includes("MartialStance")&&!st.tags.includes("WeaponStance"))continue;
    if((st.slots||1)>slotCap)continue;
    if(round(st.stam*costMult(st))>actor.stam||round(st.chakra*costMult(st))>actor.chakra)continue;
    if(!positionalLegality(actor,st).ok)continue;
    const n=gated.filter(a=>stanceReadyFor(actor,a,[st])&&positionalLegality(actor,a).ok).length;
    if(n>bestUnlocked){bestUnlocked=n;best=st;}
  }
  return best;
}
/* Stamina/Chakra a queued self-targeted action gives back when it resolves. The engine
   applies Focus restores mid-round, so the planner must credit them or it will refuse
   plans the engine would happily complete (mirrors AFUI.selfRestore on the player side). */
function plannerSelfRestore(ab,actor){
  let stam=0,chak=0;
  if(ab.targeting==="Self")for(const e of ab.effects||[]){
    if(e.k!=="Res")continue;
    if(e.res==="Stamina"){const g=(e.amt||0)+(e.pct?round(actor.maxStam*e.pct):0);if(g>0)stam+=g;}
    else if(e.res==="Chakra"){const g=(e.amt||0)+(e.pct?round(effMaxChakra(actor)*e.pct):0);if(g>0)chak+=g;}
  }
  return{stam,chak};
}
/* (B) The explicit release path, for NPCs. A fighter holding a position it gains nothing
   from would otherwise pay upkeep forever — the Focus-loop stalemate. Recomputed every
   planning pass; Submission Lock is still enforced during maintenance, so setting the
   intent can never bypass an opponent's maintained submission. */
function decideRelease(actor,plan){
  actor.releaseIntent=false;
  const role=relRole(actor);
  // Only the controlling side of a position can let go; a submission is released simply by
  // not re-queueing it, so it needs no release decision of its own.
  if(role!==REL.MOUNTING&&role!==REL.GRAPPLING)return;
  const productive=(plan||[]).some(ab=>ab.effects.some(e=>e.k==="Damage"||e.k==="GrappleTech"||(e.k==="Res"&&e.amt<0)));
  if(productive)return;
  // Nothing this position can convert into pressure: stop paying for it.
  const anyLegalOffense=actor.abilities.some(ab=>positionalLegality(actor,ab).ok&&stanceReadyFor(actor,ab,plan||[])
    &&ab.effects.some(e=>e.k==="Damage"||e.k==="GrappleTech"));
  if(!anyLegalOffense)actor.releaseIntent=true;
}
function planFor(B,actor,difficulty){
  // Fog-of-war memory refresh: only what's actually perceived right now updates what this
  // fighter remembers about where enemies are — never a live, omniscient read.
  B.updateEnemyMemory(actor);
  // Prefer a foe the actor can actually perceive (Stealth / awareness range / line of sight),
  // matching what execution will actually target — an AI should not plan or attack against
  // someone it cannot see. If nothing is currently perceived, fall back to the closest enemy
  // this fighter has ever actually SEEN before — its own remembered last-known cell, not that
  // enemy's true current position — so movement still has somewhere sensible to head instead of
  // freezing in place. The enemy may well have moved on since; the fighter finds that out on
  // arrival rather than beelining to a live location it has no way of actually knowing.
  const seen=B.nearestPerceivedEnemy(actor);
  let foe=seen,targetCell=seen?seen.cell:null;
  if(!foe){
    let bd=1e9;
    for(const[e,cell] of actor.enemyMemory){if(!alive(e))continue;const dd=hdist(actor.cell,cell);if(dd<bd){bd=dd;foe=e;targetCell=cell;}}
  }
  if(!foe)return{owner:actor,actions:[],moveTo:null};
  const plan=[];let slots=0,stam=actor.stam,chak=actor.chakra;const dist0=hdist(actor.cell,targetCell);const usedSelf=new Set();
  // Abilities flagged oncePerRound are only enforced by positionalLegality at execution time,
  // so the planner must track its own picks or it happily queues four copies of a move that
  // can only ever resolve once.
  const usedOnce=new Set();
  // A SelfMark's payoff does not stack: a second grant of the same mark this round is wasted,
  // since only one follow-up action can consume it. Not a hard cap (a player may deliberately
  // queue a repeat, e.g. to level the ability) — just a heavy score penalty so the AI never
  // does this on its own initiative.
  const usedSetup=new Set();
  const A=affinity(actor.sign,foe.sign);const noise=difficulty;const persona=actor.persona;
  const aggressive=persona==="aggressive"||persona==="brute"||persona==="assassin";
  const caster=persona==="caster"||persona==="support";
  // How close can the actor genuinely get to `foe` this round, given its real movement budget —
  // used so melee scoring reflects real reachability instead of the old check, which evaluated
  // every melee ability as if it were already at point-blank range regardless of actual
  // distance. Mirrors the closest-reachable-cell search the movement-planning block below
  // already does. Takes an extra-movement argument rather than being a fixed constant, so a
  // Movement Credit ("MC") self-buff queued earlier in THIS plan (Shadow Step, Mach Dash, ...)
  // genuinely shrinks it for every slot scored afterward — without this, the planner could
  // queue a gap-closing buff and then still refuse to queue the very attack it just enabled,
  // because reachability was only ever checked against the round's base movement budget.
  const approachDistWith=extraMc=>{
    if(dist0<=1||isRooted(actor))return dist0;
    const mc=DR.mc(eff(actor))+extraMc;
    const{cells}=B.grid.reachable(actor.cell,mc,c=>B.occupied(c,actor));
    let best=dist0;for(const[,c]of cells){const dd=hdist(c,targetCell);if(dd<best)best=dd;}
    return best;
  };
  let mcBonus=0;
  const approachDist=()=>approachDistWith(mcBonus);
  /* Slot-order-aware projection: an entry queued earlier changes what is legal later, and
     stops the planner from re-picking a grapple entry it has already spent.

     A projected transition is not a guarantee — the grapple can be shrugged off, or fall
     short of range — and execution revalidates. So the planner only stakes a bounded number
     of actions on a projection it has not actually realised; past that it falls back to the
     fighter's REAL role, leaving the rest of the round useful when the entry misses. */
  const realRole=relRole(actor);
  let projRole=realRole,projectedPicks=0;
  /* Every pick must be legal under the PROJECTED role, so the planner and the shared plan
     sanitizer always agree. Past the chain cap a pick must additionally be legal under the
     fighter's REAL role, so those slots still do something if the entry never lands. */
  function positionallyPickable(ab){
    if(!positionalLegality(actor,ab,projRole).ok)return false;
    if(projRole!==realRole&&projectedPicks>=BAL.aiMaxProjectedChain)return positionalLegality(actor,ab,realRole).ok;
    return true;
  }
  function score(ab){
    if(!positionallyPickable(ab))return -1;
    if(ab.oncePerRound&&usedOnce.has(ab.name))return -1;
    // Do not plan what the shared validator would reject: a style technique whose parent
    // stance is neither active nor already queued is stripped before resolution.
    if(!stanceReadyFor(actor,ab,plan))return -1;
    if(ab.tags.includes("EyeJutsu")&&!actor.eyeActive)return -1;
    if(ab.tags.includes("Trap")&&(actor.trapUses[ab.id]||0)>=BAL.trapUsesPerBattle)return -1;
    if((ab.targeting==="Self"||ab.targeting==="AlliesInRadius")&&usedSelf.has(ab.name))return -1;
    // A SingleEnemy-targeted ability can only ever land on a foe the actor actually perceives,
    // and a melee strike (including reach/gap-closer abilities) only lands if the actor can
    // genuinely close to its strike range this round. Both mirror real resolution-time checks
    // (resolveSingleEnemy's perception gate and reach/approach logic) — without this the planner
    // happily queued full-value attacks against an unseen or unreachable foe, which then just
    // fizzled at resolution after Stamina/Chakra were already spent. Relationship-required
    // abilities (Cross Choke, Strangle, ...) are exempt: they force-target the established
    // partner, not `foe`, so perception of `foe` specifically is irrelevant to them.
    if(ab.targeting==="SingleEnemy"&&!relationshipRequirement(ab)){
      if(!B.perceives(actor,foe))return 0.2;
      if(ab.atk==="Melee"&&approachDist()>max(1,ab.reach||1))return 0.2;
    }
    let s=0;const de=ab.effects.find(e=>e.k==="Damage");
    if(de&&ab.dmg!=="None"){const dEval=min(ab.maxR>=dist0?dist0:ab.maxR,ab.maxR)||1;const rr=evalRange(ab,ab.atk==="Melee"?1:dEval);
      if(rr.outcome==="Impossible")return 0.2;
      const base=baseDamage(ab.dmg,de.power,eff(actor),eff(foe),foe.poise>0)*BAL.damageScale*dmgMult(ab)*A.dmgDone;
      const hit=clamp(BAL.baseHitChance+DR.acc(eff(actor))-DR.eva(eff(foe)),0,100)/100*(rr.bandMod||60)/100;
      s=base*(0.4+hit)+(ab.tags.includes("Ultimate")?18:0);if(aggressive)s*=1.15;
      // Guard Break's poise damage isn't part of `base` (poise and HP are scored/dealt
      // separately) but it's real tempo denial: breaking poise skips the target's next action
      // exactly like a hard CC, and even a partial chip pressures them toward spending an
      // action on Recompose instead of attacking. Left unscored, a Guard Break with no status
      // rider (Hammer Fist: power 10, nothing else) always lost to a weaker hit that happened
      // to carry any status at all.
      const pm=(ab.poiseMultWhenGrappling&&isGrappling(actor))?max(ab.poiseMult||1,ab.poiseMultWhenGrappling):ab.poiseMult;
      if(pm>1&&foe.poise>0){const estPoise=poiseDamage(base,ab.dmg,pm,ab.poiseCap);s+=estPoise>=foe.poise?14:clamp(estPoise*0.15,2,8);}}
    {for(const e of ab.effects){
      if(e.k==="Status"&&!hasStatus(foe,e.status)&&(ab.targeting==="SingleEnemy"||ab.targeting==="PointRadius")){
        let rider=["Stun","Sleep","Fear"].includes(e.status)?15:["Silence","Slow","Blind","Confusion","Root"].includes(e.status)?8:4;
        if(BAL.useCandidateDcModel&&root.AFDC&&root.AFDC.statusTier(e)){const tier=root.AFDC.statusTier(e),sv=root.AFDC.saveStat(e),cs=root.AFDC.controlStat(ab,e),as=eff(actor),ds=eff(foe);if(sv&&cs){const rate=root.AFDC.exactLandingRate(tier,as[cs]||0,ds[sv]||0,ab.abilityLevel||0),value=({S:40,A:28,B:18,C:10}[tier]||10);rider=value*rate;}}
        s+=rider;}
      // A flat score ignored magnitude and duration, and never checked whether the buff was
      // already up — a fighter would rate re-casting a live 1rd buff the same as first landing
      // it. Scale with the real payoff (pct and how many rounds it lasts) so a buff can compete
      // with an attack when it's actually worth more than one, and heavily discount refreshing
      // a stat that's already buffed.
      if(e.k==="Buff"){const already=actor.buffs.some(bf=>bf.stat===e.stat);s+=already?0.5:clamp(2+e.pct*0.3+2*(max(1,e.dur||1)-1),3,16);}
      if(e.k==="Push")s+=5;
      // Movement Credit (Shadow Step, Mach Dash, ...) is worth real points specifically when it
      // closes ground the fighter's normal movement budget wouldn't — i.e. while it's still too
      // far away to attack this round. Comparing approachDist with/without this specific credit
      // (on top of whatever's already queued) directly rewards using it to actually enable an
      // attack, rather than scoring it as a flat, distance-blind bonus.
      if(e.k==="MC"){const before=approachDistWith(mcBonus),after=approachDistWith(mcBonus+e.amt),closed=before-after;s+=closed>0?clamp(closed*1.5,2,12):0.5;}
      if(e.k==="Heal"){
      const rr=max(1,ab.maxR||1),hurt=B.allies(actor).some(c=>hdist(actor.cell,c.cell)<=rr&&c.hp<c.maxHp*0.55);
      if(hurt)s+=e.power*(ab.healOutputMult??1)*(persona==="support"?1.3:1.0);
    }
      if(e.k==="Status"&&e.status==="Fortified")s+=(actor.hp<actor.maxHp*0.55||persona==="defensive")?8:1;
      if(e.k==="Status"&&e.status==="Stealth"&&actor.hp<actor.maxHp*0.45)s+=10;
      if(e.k==="Grapple"&&projRole===REL.FREE)s+=(eff(actor).STR>eff(foe).STR?9:3)+(persona==="brute"?3:0);
      /* Relationship techniques are the point of a grappling kit. Taking top mount and
         voluntarily going to bottom are structurally opposite outcomes, so they must not
         score alike: a voluntary bottom transition is only worth it to a fighter who can
         actually work a submission from underneath. */
      if(e.k==="GrappleTech"){
        /* Grapple-tech damage lives on the effect, not in a Damage effect, so the planner has
           to value it explicitly or a 25-power Cross Choke reads as worth less than a jab. */
        const cont=e.submission?continuedSubmission(actor,ab):null;
        if(e.power>0)s+=baseDamage(ab.dmg==="None"?"Physical":ab.dmg,round(e.power*submissionDamageMult(cont)),eff(actor),eff(foe),foe.poise>0)*BAL.damageScale;
        /* A held submission is a resource that expires this round: not re-queueing it drops the
           hold and forfeits the escalation already paid for. */
        if(cont)s+=12+4*cont.consecutive;
        if(e.mount&&e.voluntaryBottom){
          const bottomGame=actor.abilities.some(x=>x.effects.some(y=>y.k==="GrappleTech"&&y.submission)
            &&positionalLegality(actor,x,REL.MOUNTED).ok);
          s+=bottomGame?7:-8;
        }
        else s+=e.mount?14:e.submission?12:6;
      }
      /* A takedown (Hip Toss) ends the hold: a fighter with a mount transition available from the
         current standing grapple keeps the hold for that chain instead of throwing it away. */
      if(e.k==="Takedown"){
        const chain=actor.abilities.some(x=>x.effects.some(y=>y.k==="GrappleTech"&&y.mount&&!y.voluntaryBottom)
          &&positionalLegality(actor,x,projRole).ok);
        s+=chain?-14:4;
      }
      // Hip Escape pressures the Mounter's ability to pay future upkeep; value the drain
      // against what they still need for maintenance.
      if(e.k==="Res"&&e.res==="Stamina"&&e.amt<0&&isMounted(actor)&&relPartner(actor)===foe){
        const shortfall=foe.stam+(-e.amt)-BAL.mountUpkeepStamina;s+=shortfall<=0?18:6;}
      if(e.k==="SpawnSummon"&&!actor.activeSummon)s+=(persona==="support"?16:10);
      if(e.k==="ActivateEye"&&!actor.eyeActive&&actor.strain<30)s+=9;
      if(e.k==="Haunt"&&!actor.hauntTarget&&eff(actor).CHA>=11)s+=13;
      if(e.k==="Terrain"){s+=persona==="defensive"?7:2;
        // A hazard's real payoff lives in its trigger, not the bare "place terrain" effect —
        // score it like the damage/status it is, discounted for the chance the foe never
        // steps on it. Aimed at the foe's own cell it goes off immediately, so this is a floor.
        if(e.trigger){const td=e.trigger.find(x=>x.k==="Damage");
          if(td)s+=baseDamage(ab.dmg,td.power,eff(actor),eff(foe),foe.poise>0)*BAL.damageScale*dmgMult(ab)*A.dmgDone*0.6;
          for(const x of e.trigger)if(x.k==="Status"&&!hasStatus(foe,x.status))s+=5;}}}
      // These three self-restores must score against how much is actually missing, not a flat
      // floor — a fighter at full Stamina/Chakra/Poise (e.g. the opening rounds of a fresh
      // fight, or any round nothing was spent) has nothing to gain from "restoring" a pool
      // that's already topped off, and previously still scored 1.5 regardless, occasionally
      // outscoring genuine 0-or-negative options and burning the whole action budget on
      // no-op self-care before a single attack landed.
      // 2026-08-25: the "mild" threshold was 0.02 (missing just 2% of max) — since every
      // ability pays its cost upfront whether it hits or misses, ONE whiffed swing (typically
      // 8-15% of a fighter's Stamina) was already enough to outscore an out-of-reach attack
      // (0.2) and read as bizarrely flinchy self-care right after a single stray hit. Raised to
      // 0.2 so it takes roughly two spent actions' worth of drain — a fighter actually getting
      // winded — before the mild self-care score kicks in at all.
      if(ab.name==="Focus"||ab.name==="Charge Chakra"){const missing=1-chak/actor.maxChakra;s=missing>0.7?9:missing>0.2?1.5:0;}
      if(ab.name==="Catch Breath"){const missing=1-stam/actor.maxStam;s=missing>0.7?9:missing>0.2?1.5:0;}
      if(ab.name==="Recompose"){const missing=actor.maxPoise?1-actor.poise/actor.maxPoise:0;s=(missing>0.7&&!hasStatus(actor,"Mounted"))?9:(missing>0.2&&!hasStatus(actor,"Mounted"))?1.5:0;}}
    if(actor.focus&&ab.disc===actor.focus)s*=1.25;
    if(caster&&ab.disc==="Taijutsu"&&ab.maxR<=1)s*=0.6;
    if(ab.tags.includes("Priority"))s+=3;
    // Escapes lose value as the submission on the actor tightens, so a pinned fighter
    // prefers the cheaper attempt rather than burning its whole slate on a hopeless one.
    if(posMeta(ab).escape){const t=submissionEscapeTurns(actor);if(t>0)s*=max(0.2,1-0.18*t);}
    // A repeat SelfMark this round is a wasted setup — heavily devalue it so the AI never
    // chooses a redundant second copy on its own, without making the choice illegal.
    if(ab.effects.some(e=>e.k==="SelfMark"&&usedSetup.has(e.mark)))s*=0.1;
    // Opponent-read: this exact foe has already beaten this exact ability this fight (evaded,
    // parried, or denied its grapple/technique entry — see recordResisted) — discount per prior
    // failure against THEM specifically rather than trying the same read again.
    const resistCount=actor.resisted.get(foe)?.get(ab.name)||0;
    if(resistCount>0)s*=max(BAL.aiResistanceDiscountFloor,1-BAL.aiResistanceDiscountPerCount*resistCount);
    // Opponent-pattern-read: a foe who has been grappling heavily this fight gets traded with
    // less (own Grapple/GrappleTech discounted) in favor of punishing the pattern instead
    // (Priority strikes, which already earn bonus value against a queued grapple entry via the
    // "mid-entry" clash rule at matchClashRules).
    if(foeGrappleFraction(foe)>=BAL.aiGrapplePatternThreshold){
      if(isGrappleAbility(ab))s*=BAL.aiGrapplePatternPenalty;
      else if(ab.tags.includes("Priority"))s*=BAL.aiPriorityPatternBonus;
    }
    return s*(1+(rand()*2-1)*noise);
  }
  const slotCap=availableSlots(actor);
  const opener=stanceOpener(actor,slotCap);
  if(opener){plan.push(opener);slots+=opener.slots;stam-=round(opener.stam*costMult(opener));chak-=round(opener.chakra*costMult(opener));usedSelf.add(opener.name);for(const e of opener.effects)if(e.k==="MC")mcBonus+=e.amt;}
  for(let g=0;g<9&&slots<slotCap;g++){let best=null,bs=1.0;for(const ab of actor.abilities){if(slots+ab.slots>slotCap)continue;const ex=repetitionExtra(actor,ab);const sm=submissionCostMult(continuedSubmission(actor,ab));const pc=pctCost(ab,actor);
      const effStam=round((ab.stam+pc.stam)*costMult(ab)*sm)+ex.stam,effChak=round((ab.chakra+pc.chakra)*costMult(ab)*sm)+ex.chak;
      if(stam<effStam||chak<effChak)continue;
      const sc=score(ab)*resourcePaceMult(effStam,effChak,stam,chak,actor.maxStam,effMaxChakra(actor));
      if(sc>bs){bs=sc;best=ab;}}
    if(!best)break;plan.push(best);slots+=best.slots;
    // Real deduction must match resolveAction's actual cost (needStam/needChak there also folds
    // in the repetitionExtra surcharge) — the planner's own running ledger under-tracking that
    // surcharge would make it think it had more left than it really will once this round
    // actually resolves, undermining the whole point of pacing against a real remaining pool.
    {const ex=repetitionExtra(actor,best);const sm=submissionCostMult(continuedSubmission(actor,best));const pc=pctCost(best,actor);stam-=round((best.stam+pc.stam)*costMult(best)*sm)+ex.stam;chak-=round((best.chakra+pc.chakra)*costMult(best)*sm)+ex.chak;}
    {const r=plannerSelfRestore(best,actor);stam=min(actor.maxStam,stam+r.stam);chak=min(effMaxChakra(actor),chak+r.chak);}
    {const next=advanceProjectedRole(projRole,best);
     if(projRole!==realRole)projectedPicks++;
     projRole=next;}if(best.targeting==="Self"||best.targeting==="AlliesInRadius")usedSelf.add(best.name);if(best.oncePerRound)usedOnce.add(best.name);for(const e of best.effects){if(e.k==="SelfMark")usedSetup.add(e.mark);if(e.k==="MC")mcBonus+=e.amt;}if(best.tags.includes("Charge"))break;}
  // aggression floor — the same perception/reach gate as score() applies here too, or this
  // fallback would just force-queue the exact wasted, unreachable/unseen attack the gate above
  // was added to stop.
  if(!plan.some(a=>a.effects.some(e=>e.k==="Damage")&&a.dmg!=="None")){let best=null,bv=-1;for(const ab of actor.abilities){const de=ab.effects.find(e=>e.k==="Damage");if(!de||ab.dmg==="None")continue;if(round(ab.stam*costMult(ab))>actor.stam||round(ab.chakra*costMult(ab))>actor.chakra)continue;if(!positionalLegality(actor,ab,relRole(actor)).ok||!stanceReadyFor(actor,ab,[])||(ab.tags.includes("EyeJutsu")&&!actor.eyeActive))continue;
    if(ab.targeting==="SingleEnemy"&&!relationshipRequirement(ab)){if(!B.perceives(actor,foe))continue;if(ab.atk==="Melee"&&approachDist()>max(1,ab.reach||1))continue;}
    const v=baseDamage(ab.dmg,de.power,eff(actor),eff(foe),foe.poise>0)*dmgMult(ab);if(v>bv){bv=v;best=ab;}}if(best){while(plan.length&&plan.reduce((n,a)=>n+a.slots,0)+best.slots>slotCap)plan.pop();if(plan.reduce((n,a)=>n+a.slots,0)+best.slots<=slotCap)plan.unshift(best);}}
  // movement plan: casters/skirmishers pick a standoff cell; others close in
  let moveTo=null;
  if(!isRooted(actor)){const mc=DR.mc(eff(actor));const{cells,dist}=B.grid.reachable(actor.cell,mc,c=>B.occupied(c,actor));
    if(caster||persona==="skirmisher"){let best=actor.cell,bg=1e9;for(const[k,c]of cells){const dd=hdist(c,targetCell);if(dd<2)continue;const los=B.grid.los(c,targetCell);const gap=los?abs(dd-BAL.casterKiteStandoffTiles):1000+dd;if(gap<bg){bg=gap;best=c;}}moveTo=best;}
    else{let best=actor.cell,bd=hdist(actor.cell,targetCell);for(const[,c]of cells){const dd=hdist(c,targetCell);if(dd<bd){bd=dd;best=c;}}moveTo=best;}
    if(moveTo&&moveTo.q===actor.cell.q&&moveTo.r===actor.cell.r)moveTo=null;}
  decideRelease(actor,plan);
  return{owner:actor,actions:plan,moveTo};
}

/* =========================================================================
   TERRAIN GENERATION — scatter cover on a fresh arena
   ========================================================================= */
/* Caravan objective (escort scenario): a non-combatant with its own HP that advances a
   fixed path each round; a heavy caravan also fires at a random enemy in range. */
function caravanFire(B,car){
  if(!car.caravanAttack)return;
  const {power,radius}=car.caravanAttack;
  const foes=B.all.filter(f=>alive(f)&&f.faction!==car.faction&&!f.isCaravan&&hdist(car.cell,f.cell)<=radius&&B.grid.los(car.cell,f.cell));
  if(!foes.length)return;
  const target=foes[floor(rand()*foes.length)];
  const ab={name:"Caravan Bolt",disc:"Caravan",dmg:"Physical",poiseMult:1,tags:[],effects:[E.dmg(power)]};
  applyDamage(B,car,ab,target,E.dmg(power),1,false);
}
function stepCaravan(B,car){
  if(!car||!alive(car))return{alive:false,reachedGoal:false};
  caravanFire(B,car);
  if(car.path&&car.path.length){car.pathIndex=min(car.path.length-1,(car.pathIndex||0)+(car.speed||1));car.cell={...car.path[car.pathIndex]};}
  return{alive:true,reachedGoal:!!(car.path&&car.pathIndex>=car.path.length-1)};
}
function generateTerrain(grid,avoidCells){
  grid.clearTerrain();const kinds=["Tree","Rock","Bush","Rubble","Water"];const cells=grid.cells();const avoid=new Set(avoidCells.map(hkey));
  const n=round(cells.length*0.14);let placed=0;
  for(let i=0;i<cells.length&&placed<n;i++){const c=cells[Math.floor(rand()*cells.length)];const k=hkey(c);if(avoid.has(k)||grid.terrainAt(c)!=="Open")continue;if(hdist(grid.center,c)===0)continue;grid.set(c,kinds[Math.floor(rand()*kinds.length)]);placed++;}
  ensureNavigable(grid);
}
// Anti-trap: guarantee every walkable cell is one connected region (no move-blocking
// cluster can seal a fighter in or wall off a pocket). Opens the fewest boundary blockers
// needed to reconnect any isolated walkable area.
function ensureNavigable(grid){
  const cells=grid.cells(),walkable=cells.filter(c=>!grid.blocksMove(c));
  if(walkable.length<2)return;
  const start=grid.blocksMove(grid.center)?walkable[0]:grid.center;
  for(let guard=0;guard<300;guard++){
    const reached=new Set([hkey(start)]),q=[start];
    while(q.length){const cur=q.shift();for(const nb of neighbors(cur)){if(!grid.inBounds(nb)||grid.blocksMove(nb))continue;const k=hkey(nb);if(!reached.has(k)){reached.add(k);q.push(nb);}}}
    const unreached=walkable.filter(c=>!reached.has(hkey(c)));
    if(!unreached.length)return;
    // open a move-blocking cell that borders both the reached region and an isolated pocket
    let opened=null;
    for(const c of cells){if(!grid.blocksMove(c))continue;const ns=neighbors(c).filter(nb=>grid.inBounds(nb));
      if(ns.some(nb=>reached.has(hkey(nb)))&&ns.some(nb=>!grid.blocksMove(nb)&&!reached.has(hkey(nb)))){opened=c;break;}}
    if(!opened){const c=unreached[0];opened=neighbors(c).find(nb=>grid.inBounds(nb)&&grid.blocksMove(nb));}
    if(!opened)return;grid.set(opened,"Open");
  }
}

/* ---- exports ---- */
root.AF={BAL,setSeed,rand,mulberry32,setRNG:fn=>{RNG=fn;},
  SIGNS,PLANETS,ELEM,RULER,GLYPH,NAKSHATRA,NAK_ROLE,PADA,
  julianDay,buildChart,chartToLoadout,placement,signOf,nakOf,padaOf,decanOf,sunLon,moonLon,planetLon,ascendantLon,
  Grid,makeArena,hx,hdist,hkey,neighbors,cubeRound,generateTerrain,
  DR,mcurve,moveBudget,bandFor,evalRange,baseDamage,poiseDamage,affinity,aspectBetween,costMult,dmgMult,initWeight,
  KITS,MARTIAL,WEAPONS,EYES,EYE_PLANETS,BLOODLINES,BLOOD_KEYS,SUMMON_STATS,zodiacAbilities,generalArts,buildLoadout,
  ENEMIES,ENEMY_KEYS,enemyLoadout,
  makeFighter,scaleEnemyStats,eff,alive,hasStatus,getStatus,removeStatus,effMaxChakra,isRooted,Battle,resolveRound,planFor,abilityKey,stepCaravan,retargetDefeated,
  /* System 3 — ability clashes */
  peekNextQueued,isDamagingRush,isMobilityRush,isKick,isPunch,matchClashRules,matchWardClashRules,matchGrappleClashRules,applyDamage,applyGrapple,teepAntiPriorityBonus,
  /* positional combat */
  REL,REL_ROLES,MOUNT_ACCESS,REQ,TRANSITION,POSITIONAL_RULES,positionalMetaFor,posMeta,
  relRole,relPartner,isGrappling,isGrappled,isMounting,isMounted,inMount,inStandingGrapple,isEngaged,
  isMountRole,isStandingRole,inRelationship,REL_LABEL,
  positionalLegality,positionalDcModifier,passiveStaminaFactor,isGenericMovementAbility,relationshipRequirement,
  availableSlots,standingGrapplePriority,
  setRelationship,clearRelationship,enterStandingGrapple,enterMount,endRelationship,advanceProjectedRole,
  activeSubmission,setSubmission,clearSubmission,continuedSubmission,submissionCostMult,submissionDamageMult,
  submissionEscapeTurns,submissionEscapeResistance,
  postRoundEffects,relationshipMaintenance,passiveRecovery,endOfRound,relationshipPairs,decideRelease,martialKitFor,
  ABID:()=>ABID,resetIds:()=>{ABID=0;}};
})(typeof globalThis!=="undefined"?globalThis:this);
