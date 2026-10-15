/* Which rig animation each hex-testbed ability plays, and which abilities still need frames.

   Every ability resolves to an entry:
     play     clips played in order: [state, clip] pairs from web/characters/male.json ([] = no motion)
     weapon   the rig weapon drawn with them ("katana" | "tanto"), if any
     fit      "exact"   the authored motion is this technique
              "standIn" a nearby authored motion plays until the technique's own frames exist
              "missing" nothing authored fits; ranged damage still draws a bolt to the target
     need     the frame set the technique is waiting on (empty for exact)
   Name entries win; otherwise the ability's group and shape decide. The coverage report
   (tools/report-ability-animations.mjs -> docs/ABILITY_ANIMATION_COVERAGE.md) lists every ability. */
(function(root){
"use strict";

const P=(state,clip)=>[state,clip];
const JAB=P("lightAttack","jab"),CROSS=P("lightAttack","cross");
const LOW=P("heavyAttack","lowKick"),SNAP=P("heavyAttack","snapKick"),SPIN=P("heavyAttack","spinRoundhouse");
const CUT_D=P("katanaLight","downCut"),CUT_U=P("katanaLight","upCut"),SIDE_R=P("katanaHeavy","sideCutR");
const SWIPE=P("oneHandHeavy","swipeR");
const WEAVE=P("weave","weave"),BLOCK=P("block","block"),SPRINT=P("sprint",null),WINDED=P("exhausted","exhausted");
const GUARD=P("guard","guard"),KATANA_GUARD=P("twoHandGuard","twoHandGuard"),TANTO_GUARD=P("oneHandGuard","oneHandGuard");

const ex=(play,o)=>({play,fit:"exact",need:"",...o});
const si=(play,need,o)=>({play,fit:"standIn",need,...o});
const no=need=>({play:[],fit:"missing",need});

// frame sets still to author, by the name the coverage report groups them under
const NEED={
  hook:"hook / uppercut",palm:"open-palm strike",elbow:"elbow strike",knee:"knee strike",head:"headbutt",
  sweep:"leg sweep",push:"push kick / side kick",lunge:"dash strike (lunge)",grapple:"clinch, throws and ground grappling",grab:"clinch entry (grab)",
  thrust:"katana thrust",parryK:"katana parry",hilt:"katana hilt strike",machete:"machete chop",sickle:"kusarigama sickle",
  chain:"kusarigama chain throw / snare",bow:"bow draw and release",throw:"thrown weapon",
  seal:"hand seals / ninjutsu cast",gaze:"genjutsu cast",eye:"eye awakening",dojutsu:"eye technique (dojutsu)",charge:"chakra charge / focus",
  heal:"medical healing",trap:"trap placement",summon:"summoning",buff:"power-up / aura",roar:"roar",
  stance:"martial stance entry",bowStance:"bow stance",barrier:"barrier cast",parry:"open-hand parry",recompose:"recompose / reset"
};

const BY_NAME={
  // boxing and general punches
  "Jab-Cross":ex([JAB,CROSS]),"Street Jab":ex([JAB]),"Karate Blitz":ex([JAB,CROSS]),"Dirty Boxing":si([JAB,CROSS],NEED.hook),
  "Iron Fist":ex([CROSS]),"Echo Fist":ex([JAB,CROSS]),"Shatter Punch":ex([CROSS]),"Cheap Shot":si([JAB],NEED.hook),
  "Uppercut":si([CROSS],NEED.hook),"Haymaker":si([CROSS],NEED.hook),"Wild Swing":si([CROSS],NEED.hook),"Body Shot":si([CROSS],NEED.hook),
  "Kidney Shot":si([CROSS],NEED.hook),"Hammer Fist":si([CROSS],NEED.hook),"Numbing Strike":si([JAB],NEED.palm),"Nerve Disruptor":si([JAB],NEED.palm),
  "Iron Mountain":si([CROSS],NEED.elbow),"Viper Strike":si([JAB],NEED.palm),"Rusty Shiv":ex([P("oneHandLight","stab1")],{weapon:"tanto"}),"Silica Strike":si([CROSS],NEED.palm),"Vice Grip":si([CROSS],NEED.grapple),
  // palms and chops
  "Sun Palm":si([CROSS],NEED.palm),"Shock Palm":si([CROSS],NEED.palm),"Aero Palm":si([CROSS],NEED.palm),"Wither Palm":si([CROSS],NEED.palm),
  "Hydro Cannon Palm":si([CROSS],NEED.palm),"Sumo Palm":si([JAB,CROSS],NEED.palm),"Judo Chop":si([CROSS],NEED.palm),"Diamond Cutter":si([CROSS],NEED.palm),
  "Flow Strike":si([CROSS],NEED.palm),"Spectral Touch":si([JAB],NEED.palm),
  // elbows, knees, headbutt
  "Elbow Strike":si([CROSS],NEED.elbow),"Knee Strikes":si([SNAP],NEED.knee),"Headbutt":si([JAB],NEED.head),
  // kicks
  "Calf Kick":ex([LOW]),"Adamantine Shin":ex([LOW]),"Whirlwind Kick":ex([SPIN]),"Roundhouse Kick":ex([SPIN]),"Heavenly Kick":ex([SPIN]),
  "Spinning Top":ex([SPIN]),"Teep Kick":si([SNAP],NEED.push),"Side Kick":si([SNAP],NEED.push),"Leash Kick":si([SNAP],NEED.push),
  "Sweeping Low":si([LOW],NEED.sweep),"Sonic Sweep":si([LOW],NEED.sweep),
  // lunges: the approach already walks; the strike stands in for the dash
  "Mach Lunge":si([SPRINT,CROSS],NEED.lunge),"Bull Rush":si([SPRINT,CROSS],NEED.lunge),"Tidal Slam":si([SPRINT,CROSS],NEED.lunge),
  "Charge":si([SPRINT,CROSS],NEED.lunge),"Battle Roar":no(NEED.roar),
  // grappling: no authored frames
  // clinch: the pair forms on a landed grab (clinchHold / clinchHeld, no grab motion yet); the throws play as paired
  // clips from the hold (af-sprites-v3.js CLINCH_CLIPS), as do Uppercut, Knee Strikes, Elbow Strike and Body Shot
  // when thrown inside a clinch
  "Clinch":si([],NEED.grab),"Grab":no(NEED.grapple),"Hip Toss":ex([P("clinchHipToss","clinchHipToss")]),"Rolling Throw":ex([P("clinchRollingThrow","clinchRollingThrow")]),"Sweeping Shoulder":no(NEED.grapple),
  "Cross Choke":no(NEED.grapple),"Hip Escape":no(NEED.grapple),"Pull Guard":no(NEED.grapple),"Strangle":no(NEED.grapple),"Flying Triangle":no(NEED.grapple),
  "Arm bar":no(NEED.grapple),"Single Leg Shot":no(NEED.grapple),"Suplex":no(NEED.grapple),"Choke Slam":no(NEED.grapple),"Ground and Pound":no(NEED.grapple),
  "Reversal":no(NEED.grapple),"Shadow Possession":no(NEED.seal),"Grasp of the Dead":no(NEED.seal),
  // defence and footwork
  "Bob and Weave":ex([WEAVE]),"Evasive Sway":ex([WEAVE]),"Flow Dodge":ex([WEAVE]),"Defensive Stance":ex([BLOCK]),
  "Flow Parry":si([BLOCK],NEED.parry),"Flowing Sand Parry":si([BLOCK],NEED.parry),
  "Mach Dash":ex([SPRINT]),"Feather Step":ex([SPRINT]),"Slide Counter":ex([SPRINT]),"Shadow Step":si([SPRINT],NEED.seal),
  "Catch Breath":ex([WINDED]),"Recompose":no(NEED.recompose),"Charge Chakra":no(NEED.charge),"Focus":no(NEED.charge),
  // stances
  "Boxing Stance":ex([GUARD]),"Muay Thai Stance":si([GUARD],NEED.stance),"Judo Stance":si([GUARD],NEED.stance),"Jiu-Jitsu Stance":si([GUARD],NEED.stance),
  "Karate Stance":si([GUARD],NEED.stance),"Wrestling Stance":si([GUARD],NEED.stance),"Horse Stance":no(NEED.stance),"Mountain Stance":no(NEED.stance),
  "King's Posture":no(NEED.stance),"Wrestler's Prowess":no(NEED.buff),
  // weapons
  "Kenjutsu Stance":ex([KATANA_GUARD],{weapon:"katana"}),"Kenjutsu Slash":ex([CUT_D],{weapon:"katana"}),
  "Machete Slash":si([CUT_D],NEED.machete,{weapon:"katana"}),"Hilt Bash":si([SIDE_R],NEED.hilt,{weapon:"katana"}),
  "Precision Thrust":si([CUT_U],NEED.thrust,{weapon:"katana"}),"Parry":si([BLOCK],NEED.parryK),
  "Kyoketsu-Shoge Stance":si([TANTO_GUARD],NEED.sickle,{weapon:"tanto"}),"Sickle Strike":si([SWIPE],NEED.sickle,{weapon:"tanto"}),
  "Cord Garrote":no(NEED.chain),"Blade Throw":no(NEED.chain),"Kusari Chain Snare":no(NEED.chain),"Chain Yank":no(NEED.chain),
  "Kyudo Stance":no(NEED.bowStance),"Kyudo Shot":no(NEED.bow),"Arrow Rain":no(NEED.bow),"Thrown Knife":no(NEED.throw),
  // general chakra arts that are barriers or medical
  "Guardian Barrier":no(NEED.barrier),"Warding Sigil":no(NEED.barrier),"Conjure Barrier":no(NEED.barrier),"Earth Wall":no(NEED.barrier)
};

function byShape(ab){
  const g=ab.group,fx=(ab.effects||[]).map(e=>e.k);
  if(g==="Medical")return no(NEED.heal);
  if(g==="Trap")return no(NEED.trap);
  if(g==="Summon"||fx.includes("SpawnSummon"))return no(NEED.summon);
  if(g==="Dojutsu")return no(fx.includes("ActivateEye")?NEED.eye:NEED.dojutsu);
  if(g==="Genjutsu"||ab.atk==="GenVisual")return no(NEED.gaze);
  if(g==="Bloodline"||g==="Ninjutsu")return no(fx.includes("Damage")?NEED.seal:fx.includes("Heal")?NEED.heal:fx.includes("Buff")||(ab.effects||[]).some(e=>e.status==="Fortified"||e.status==="Shield")?NEED.buff:NEED.seal);
  if(g==="General"&&ab.atk!=="Melee")return no(fx.includes("Heal")?NEED.heal:NEED.seal);
  if(ab.atk==="Melee"&&ab.dmg&&ab.dmg!=="None")return si([JAB],NEED.palm);
  if((ab.tags||[]).includes("MartialStance"))return si([GUARD],NEED.stance);
  return no(fx.includes("Buff")?NEED.buff:NEED.seal);
}
function forAbility(ab){return ab?(BY_NAME[ab.name]||byShape(ab)):no("");}

const API={forAbility,NEED,BY_NAME};
root.AFAnimMap=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
})(typeof globalThis!=="undefined"?globalThis:this);
