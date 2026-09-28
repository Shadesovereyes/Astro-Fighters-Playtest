/* Astro Fighters — authored world data.
   All positions are world pixels. Actor x/y is the foot-contact point.
   Collision is authored here, independently of any appearance imagery.
   `backdrop` maps are legacy baked district images kept only as temporary,
   non-reviewable development backdrops (see PHASER_WORLD_REFACTOR_V0.md). */
(() => {
  'use strict';

  const LOOKS = {
    sensei: {skin:'skin05',hair:'locs_short',eyeColor:'#434DA0',hairColor:'#95846C',innerTop:'wrap_top',outerwear:'utility_haori',pants:'fighter_hakama',shoes:'wrapped_boots',innerColor:'#D5BAA0',outerColor:'#29342B',pantsColor:'#141410',shoesColor:'#343427',weapon:'none'},
    guard: {skin:'skin03',hair:'afro_short',eyeColor:'#314B79',hairColor:'#1F0C0B',innerTop:'hoodie_under',outerwear:'short_jacket',pants:'fighter_hakama',shoes:'wrapped_boots',innerColor:'#343427',outerColor:'#2A3B5A',pantsColor:'#1D243C',shoesColor:'#141410',weapon:'katana01'},
    dockworker: {skin:'skin02',hair:'twists',eyeColor:'#4A8998',hairColor:'#3C1B17',innerTop:'hoodie_under',outerwear:'utility_haori',pants:'cuffed_trousers',shoes:'wrapped_boots',innerColor:'#86A07C',outerColor:'#645838',pantsColor:'#3E4F3E',shoesColor:'#464228',weapon:'none'},
    student: {skin:'skin01',hair:'puff_undercut',eyeColor:'#5CA3D4',hairColor:'#291011',innerTop:'wrap_top',outerwear:'short_jacket',pants:'fighter_hakama',shoes:'wrapped_boots',innerColor:'#D5BAA0',outerColor:'#375678',pantsColor:'#1D243C',shoesColor:'#343427',weapon:'none'},
    keeper: {skin:'skin04',hair:'afro_short',eyeColor:'#6D8566',hairColor:'#55503E',innerTop:'wrap_top',outerwear:'patterned_haori',pants:'loose_pants',shoes:'sneaker_hybrid',innerColor:'#B69350',outerColor:'#366F68',pantsColor:'#343427',shoesColor:'#685B47',weapon:'none'},
    thug: {skin:'skin03',hair:'twists',eyeColor:'#9B382D',hairColor:'#14120A',innerTop:'cropped_top',outerwear:'short_jacket',pants:'loose_pants',shoes:'sneaker_hybrid',innerColor:'#2E2516',outerColor:'#7D3524',pantsColor:'#29342B',shoesColor:'#14120A',weapon:'none'},
    thug2: {skin:'skin05',hair:'high_puff',eyeColor:'#945B45',hairColor:'#2E1510',innerTop:'hoodie_under',outerwear:'utility_haori',pants:'cuffed_trousers',shoes:'wrapped_boots',innerColor:'#473522',outerColor:'#5F311D',pantsColor:'#191127',shoesColor:'#2E2516',weapon:'none'}
  };

  const THUG = {name:'Street Thug',hp:75,maxHp:75,poise:60,maxPoise:60,power:8,hostile:true,xp:30,mon:5};

  const MAPS = {
    'Imperial Docks': {
      key:'docks', display:'Imperial Docks · Port District', width:640, height:360,
      backdrop:'assets/runtime/env/imperial-docks.jpg', artState:'legacy',
      spawn:{x:300,y:222},
      objective:'Follow the harbor road north to Civic Ward.',
      colliders:[
        {x:0,y:0,w:168,h:226},{x:0,y:226,w:48,h:134},
        {x:168,y:0,w:184,h:160},{x:352,y:0,w:56,h:104},{x:408,y:0,w:232,h:156},
        {x:48,y:240,w:282,h:120},{x:330,y:266,w:90,h:94},{x:420,y:156,w:220,h:204}
      ],
      exits:[{id:'north-road',x:352,y:104,w:56,h:40,target:'Civic Ward',arrive:'from-docks',label:'Harbor road → Civic Ward',auto:true}],
      arrivals:{'from-civic':{x:380,y:168,facing:'S'},'from-slice0':{x:300,y:222,facing:'S'}},
      npcs:[{id:'dockworker',name:'Dockworker Tomo',x:272,y:214,look:'dockworker',facing:'S',
        lines:['Ships from the outer islands dock here at dawn. Most fighters start the way you did — off a boat, onto these stones.','The Academy is up the harbor road, through the Civic Ward. Sensei Daichi certifies every new fighter.']}],
      enemies:[]
    },
    'Civic Ward': {
      key:'civic', display:'Imperial City · Civic Ward', width:640, height:360,
      backdrop:'assets/runtime/env/civic-ward.png', artState:'legacy',
      spawn:{x:320,y:214},
      objective:'Find the Astro Fighter Academy south of the crossroads.',
      colliders:[
        {x:30,y:35,w:170,h:105},{x:425,y:32,w:175,h:113},
        {x:25,y:250,w:175,h:95},{x:430,y:250,w:180,h:95},{x:194,y:226,w:252,h:114}
      ],
      exits:[
        {id:'academy-gate',x:288,y:212,w:64,h:18,target:'Academy',arrive:'from-civic',label:'Enter Astro Fighter Academy'},
        {id:'west-road',x:0,y:152,w:10,h:78,target:'Imperial Docks',arrive:'from-civic',label:'Return to Imperial Docks',auto:true},
        {id:'east-road',x:630,y:152,w:10,h:78,target:'Fringe Ward',arrive:'from-civic',label:'Enter Fringe Ward',auto:true,requiresAcademy:true}
      ],
      arrivals:{'from-docks':{x:26,y:192,facing:'E'},'from-academy':{x:320,y:206,facing:'N'},'from-fringe':{x:612,y:192,facing:'W'}},
      npcs:[
        {id:'guard-a',name:'Royal Guard',x:250,y:210,look:'guard',facing:'S',lines:['Royal Guard patrols keep the central wards free of street-clan violence.']},
        {id:'guard-b',name:'Royal Guard',x:390,y:210,look:'guard',facing:'S',lines:['The east road leads to the Fringe. Uncertified fighters are turned back at the gate.']}
      ],
      enemies:[]
    },
    'Academy': {
      key:'academy', display:'Astro Fighter Academy · Foundation Hall', width:640, height:360,
      backdrop:'assets/runtime/env/academy-interior.jpg', artState:'legacy',
      spawn:{x:320,y:278},
      objective:'Speak with Sensei Daichi.',
      colliders:[
        {x:0,y:0,w:640,h:136},{x:0,y:136,w:92,h:224},{x:548,y:136,w:92,h:224},
        {x:470,y:136,w:78,h:64},{x:96,y:250,w:96,h:110},{x:446,y:250,w:70,h:110},{x:0,y:312,w:640,h:48}
      ],
      exits:[{id:'hall-door',x:288,y:292,w:64,h:20,target:'Civic Ward',arrive:'from-academy',label:'Exit to Civic Ward'}],
      arrivals:{'from-civic':{x:320,y:278,facing:'N'}},
      npcs:[{id:'sensei-daichi',name:'Sensei Daichi',x:364,y:248,look:'sensei',facing:'W',role:'sensei'}],
      enemies:[{id:'sparring-student',name:'Sparring Student',x:272,y:238,look:'student',hp:80,maxHp:80,poise:100,maxPoise:100,power:0,hostile:false,respawnMs:4000}]
    },
    'Fringe Ward': {
      key:'fringe', display:'Imperial Fringe · Street-Clan Quarter', width:640, height:360,
      backdrop:'assets/runtime/env/fringe-ward.png', artState:'legacy',
      spawn:{x:26,y:192},
      objective:'Hostile district: target, guard, dodge, strike, and use your traps.',
      colliders:[
        {x:10,y:11,w:63,h:119},{x:81,y:41,w:67,h:137},{x:160,y:11,w:63,h:154},{x:231,y:41,w:67,h:119},
        {x:310,y:11,w:63,h:137},{x:381,y:41,w:67,h:154},{x:460,y:11,w:63,h:119},{x:531,y:41,w:67,h:137},{x:610,y:11,w:30,h:154}
      ],
      exits:[{id:'west-road',x:0,y:150,w:10,h:84,target:'Civic Ward',arrive:'from-fringe',label:'Return to Civic Ward',auto:true}],
      arrivals:{'from-civic':{x:26,y:192,facing:'E'}},
      npcs:[],
      enemies:[
        Object.assign({id:'street-thug-1',x:470,y:196,look:'thug'},THUG),
        Object.assign({id:'street-thug-2',x:300,y:262,look:'thug2'},THUG),
        Object.assign({id:'street-thug-3',x:560,y:300,look:'thug'},THUG)
      ]
    },
    'Slice 0': {
      key:'slice0', display:'Slice 0 · Foundation Courtyard (engine test)', width:960, height:540,
      builder:'slice0', artState:'scaffold',
      spawn:{x:480,y:420},
      objective:'Walk the courtyard: pass behind the gate beam, the wall, and the lantern post.',
      colliders:[
        {x:0,y:0,w:960,h:200},{x:288,y:200,w:384,h:40},
        {x:64,y:368,w:192,h:24},
        {x:417,y:376,w:14,h:8},{x:529,y:376,w:14,h:8},
        {x:702,y:236,w:44,h:14},
        {x:352,y:508,w:16,h:12}
      ],
      exits:[{id:'south-lane',x:440,y:522,w:80,h:18,target:'Imperial Docks',arrive:'from-slice0',label:'Return to Imperial Docks'}],
      arrivals:{'from-scale':{x:480,y:500,facing:'N'}},
      npcs:[{id:'courtyard-keeper',name:'Courtyard Keeper',x:600,y:330,look:'keeper',facing:'W',
        lines:['Everything here is loaded as a separate module and sorted by depth each frame. Collision is its own data — the stones do not decide where you can walk.','These textures are procedural scaffolding. Authored source art replaces them file-for-file once it passes review.']}],
      enemies:[],
      // Authored scaffold dimensions (px) checked against AF_SCALE ratios × measured stature.
      proportions:{doorOpeningH:68,doorOpeningW:36,plinthH:22,eaveH:106,windowSill:35,windowH:22,windowW:31,postH:128,beamClearance:112,lanternH:112,crateLarge:28},
      interactables:[{id:'courtyard-door',name:'Courtyard door',x:480,y:252,lines:['The door is barred from inside. Room interiors and authored cutaways arrive with the Academy interior slice.']}],
      // Layer routing follows production/asset-manifest.json canonical.worldLayerOrder.
      ground:{modules:[['stone-clean',6],['stone-cracked',2],['stone-patched',1]],seed:7},
      placements:[
        {tex:'stone-timber-transition',x:704,y:300,layer:'ground'},
        {tex:'stone-timber-transition',x:832,y:300,layer:'ground'},
        {tex:'building-threshold',x:416,y:236,layer:'ground'},
        ...[0,160,320,480,640,800].map(x=>({tex:'drainage-channel',x,y:440,layer:'ground'})),
        {tex:'cracks',x:120,y:250,layer:'decals'},{tex:'cracks',x:620,y:330,layer:'decals'},{tex:'cracks',x:860,y:396,layer:'decals'},
        {tex:'stains',x:330,y:404,layer:'decals'},{tex:'stains',x:700,y:250,layer:'decals'},{tex:'stains',x:70,y:470,layer:'decals'},
        {tex:'cart-wear',x:560,y:292,layer:'decals'},{tex:'cart-wear',x:656,y:300,layer:'decals'},
        {tex:'drainage-grate',x:176,y:448,layer:'architecture-dressing',sortY:-1},
        {tex:'drainage-grate',x:496,y:448,layer:'architecture-dressing',sortY:-1},
        {tex:'drainage-grate',x:816,y:448,layer:'architecture-dressing',sortY:-1},
        {tex:'timber-plaster-wall',x:288,y:58,layer:'architecture',sortY:240},
        {tex:'timber-plaster-wall',x:480,y:58,layer:'architecture',sortY:240},
        {tex:'doorway',x:458,y:146,layer:'architecture-dressing',sortY:240.05},
        {tex:'aged-stone-foundation',x:288,y:176,layer:'architecture',sortY:240.1},
        {tex:'aged-stone-foundation',x:480,y:176,layer:'architecture',sortY:240.1},
        {tex:'noren',x:448,y:146,layer:'architecture-dressing',sortY:240.2},
        {tex:'timber-plaster-wall',x:64,y:210,layer:'architecture',sortY:392,occluder:true},
        {tex:'aged-stone-foundation',x:64,y:328,layer:'architecture',sortY:392.1,occluder:true},
        {tex:'timber-post',x:400,y:256,layer:'architecture',sortY:384,occluder:true},
        {tex:'timber-post',x:512,y:256,layer:'architecture',sortY:384,occluder:true},
        {tex:'horizontal-beam',x:416,y:240,layer:'architecture',sortY:384.1,occluder:true},
        {tex:'crate-stack',x:700,y:196,layer:'props-back',sortY:250},
        {tex:'lantern-post',x:344,y:408,layer:'props-front-occluders',sortY:520,occluder:true}
      ],
      shadows:[
        {x:288,y:240,w:384,h:8,a:.28},{x:64,y:392,w:192,h:7,a:.28},
        {x:410,y:382,w:28,h:5,a:.25},{x:522,y:382,w:28,h:5,a:.25},{x:700,y:250,w:50,h:5,a:.25},{x:348,y:518,w:26,h:4,a:.25}
      ]
    },
    'Scale Reference': {
      key:'scale', display:'Scale Reference · player-relative proportions', width:960, height:540,
      builder:'scale', artState:'scaffold',
      spawn:{x:96,y:470},
      objective:'Walk beside each object and judge it against the player. Every size is a ratio of the player stature S.',
      colliders:[{x:0,y:0,w:960,h:30}],
      exits:[{id:'south-lane',x:440,y:522,w:80,h:18,target:'Slice 0',arrive:'from-scale',label:'Go to Slice 0 · Foundation Courtyard'}],
      arrivals:{},
      npcs:[
        {id:'scale-clerk',name:'Counter Clerk',x:600,y:170,look:'keeper',facing:'S',lines:['The counter top should land near my hip. If it reaches my chest or my knee, the counter is the wrong size, not me.']},
        {id:'scale-passerby',name:'Passer-by',x:520,y:330,look:'dockworker',facing:'W',lines:['Every character shares the player frame scale. Nobody here is scaled to a grid cell.']}
      ],
      enemies:[],
      // Guide items: anchor x and ground line y; sizes come from AF_SCALE ratios × measured stature.
      guideItems:[
        {item:'wall-door',x:250,y:190},{item:'stairs',x:470,y:190},{item:'counter',x:600,y:190,labelDy:58},
        {item:'crate-small',x:700,y:190},{item:'crate-large',x:740,y:190,labelDy:18},{item:'barrel',x:790,y:190,labelDy:32},
        {item:'bench',x:110,y:330},{item:'post',x:200,y:330,labelDy:26},{item:'railing',x:330,y:330},{item:'lantern',x:450,y:330,labelDy:26},
        {item:'bridge-single',x:650,y:402},{item:'bridge-pair',x:820,y:402},{item:'ruler',x:60,y:470}
      ],
      canal:{x:560,y:272,w:390,h:128}
    }
  };

  // Authored shared-foundation runtime PNGs, keyed by manifest dependency id, e.g.
  // 'stone-clean': 'assets/world/shared-foundation/stone-clean.png'. Listed modules replace
  // the procedural scaffold texture of the same id; unlisted ids fall back to scaffold.
  const authoredModules = {};

  window.AF_WORLD = {MAPS, LOOKS, authoredModules};
})();
