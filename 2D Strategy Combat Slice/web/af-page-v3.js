(()=>{
"use strict";
const $=id=>document.getElementById(id);
// Location search data: [display name, lat, lon, standard-time UTC offset]. City-center
// coordinates and STANDARD (non-DST) offsets, matching the existing simplification already
// noted in the setup screen — historical DST is not resolved. ~240 entries: essentially every
// sovereign capital plus major secondary cities for large/populous countries, so the search
// covers real-world geography instead of a fixed 35-city shortlist.
const CITIES=[
// North America
["New York, US",40.7128,-74.0060,-5],["Los Angeles, US",34.0522,-118.2437,-8],["Chicago, US",41.8781,-87.6298,-6],
["Houston, US",29.7604,-95.3698,-6],["Phoenix, US",33.4484,-112.0740,-7],["Philadelphia, US",39.9526,-75.1652,-5],
["San Antonio, US",29.4241,-98.4936,-6],["San Diego, US",32.7157,-117.1611,-8],["Dallas, US",32.7767,-96.7970,-6],
["San Francisco, US",37.7749,-122.4194,-8],["Seattle, US",47.6062,-122.3321,-8],["Denver, US",39.7392,-104.9903,-7],
["Boston, US",42.3601,-71.0589,-5],["Miami, US",25.7617,-80.1918,-5],["Atlanta, US",33.7490,-84.3880,-5],
["Washington, D.C., US",38.9072,-77.0369,-5],["Detroit, US",42.3314,-83.0458,-5],["Minneapolis, US",44.9778,-93.2650,-6],
["Las Vegas, US",36.1699,-115.1398,-8],["Portland, US",45.5152,-122.6784,-8],["Honolulu, US",21.3069,-157.8583,-10],
["Anchorage, US",61.2181,-149.9003,-9],["New Orleans, US",29.9511,-90.0715,-6],["Nashville, US",36.1627,-86.7816,-6],
["Salt Lake City, US",40.7608,-111.8910,-7],["Austin, US",30.2672,-97.7431,-6],
["Toronto, Canada",43.6532,-79.3832,-5],["Vancouver, Canada",49.2827,-123.1207,-8],["Montreal, Canada",45.5019,-73.5674,-5],
["Ottawa, Canada",45.4215,-75.6972,-5],["Calgary, Canada",51.0447,-114.0719,-7],
["Mexico City, Mexico",19.4326,-99.1332,-6],["Guadalajara, Mexico",20.6597,-103.3496,-6],["Monterrey, Mexico",25.6866,-100.3161,-6],
["Guatemala City, Guatemala",14.6349,-90.5069,-6],["San Salvador, El Salvador",13.6929,-89.2182,-6],
["Tegucigalpa, Honduras",14.0723,-87.1921,-6],["Managua, Nicaragua",12.1364,-86.2514,-6],
["San José, Costa Rica",9.9281,-84.0907,-6],["Panama City, Panama",8.9824,-79.5199,-5],
["Havana, Cuba",23.1136,-82.3666,-5],["Kingston, Jamaica",17.9712,-76.7936,-5],["Santo Domingo, Dominican Republic",18.4861,-69.9312,-4],
["San Juan, Puerto Rico",18.4655,-66.1057,-4],["Nassau, Bahamas",25.0480,-77.3554,-5],["Port-au-Prince, Haiti",18.5944,-72.3074,-5],
["Belmopan, Belize",17.2510,-88.7590,-6],
// South America
["São Paulo, Brazil",-23.5505,-46.6333,-3],["Rio de Janeiro, Brazil",-22.9068,-43.1729,-3],["Brasília, Brazil",-15.7975,-47.8919,-3],
["Buenos Aires, Argentina",-34.6037,-58.3816,-3],["Santiago, Chile",-33.4489,-70.6693,-4],["Lima, Peru",-12.0464,-77.0428,-5],
["Bogotá, Colombia",4.7110,-74.0721,-5],["Caracas, Venezuela",10.4806,-66.9036,-4],["Quito, Ecuador",-0.1807,-78.4678,-5],
["La Paz, Bolivia",-16.4897,-68.1193,-4],["Sucre, Bolivia",-19.0333,-65.2627,-4],["Asunción, Paraguay",-25.2637,-57.5759,-4],
["Montevideo, Uruguay",-34.9011,-56.1645,-3],["Georgetown, Guyana",6.8013,-58.1551,-4],["Paramaribo, Suriname",5.8520,-55.2038,-3],
["Medellín, Colombia",6.2442,-75.5812,-5],
// Europe
["London, UK",51.5074,-0.1278,0],["Manchester, UK",53.4808,-2.2426,0],["Edinburgh, UK",55.9533,-3.1883,0],
["Dublin, Ireland",53.3498,-6.2603,0],
["Paris, France",48.8566,2.3522,1],["Marseille, France",43.2965,5.3698,1],["Lyon, France",45.7640,4.8357,1],
["Berlin, Germany",52.5200,13.4050,1],["Munich, Germany",48.1351,11.5820,1],["Hamburg, Germany",53.5511,9.9937,1],
["Frankfurt, Germany",50.1109,8.6821,1],
["Madrid, Spain",40.4168,-3.7038,1],["Barcelona, Spain",41.3851,2.1734,1],
["Rome, Italy",41.9028,12.4964,1],["Milan, Italy",45.4642,9.1900,1],["Naples, Italy",40.8518,14.2681,1],
["Lisbon, Portugal",38.7223,-9.1393,0],["Amsterdam, Netherlands",52.3676,4.9041,1],["Brussels, Belgium",50.8503,4.3517,1],
["Bern, Switzerland",46.9480,7.4474,1],["Zürich, Switzerland",47.3769,8.5417,1],["Vienna, Austria",48.2082,16.3738,1],
["Stockholm, Sweden",59.3293,18.0686,1],["Oslo, Norway",59.9139,10.7522,1],["Copenhagen, Denmark",55.6761,12.5683,1],
["Helsinki, Finland",60.1699,24.9384,2],["Reykjavík, Iceland",64.1466,-21.9426,0],
["Warsaw, Poland",52.2297,21.0122,1],["Prague, Czechia",50.0755,14.4378,1],["Bratislava, Slovakia",48.1486,17.1077,1],
["Budapest, Hungary",47.4979,19.0402,1],["Bucharest, Romania",44.4268,26.1025,2],["Sofia, Bulgaria",42.6977,23.3219,2],
["Zagreb, Croatia",45.8150,15.9819,1],["Ljubljana, Slovenia",46.0569,14.5058,1],["Belgrade, Serbia",44.7866,20.4489,1],
["Sarajevo, Bosnia and Herzegovina",43.8563,18.4131,1],["Podgorica, Montenegro",42.4304,19.2594,1],
["Skopje, North Macedonia",41.9981,21.4254,1],["Tirana, Albania",41.3275,19.8187,1],["Pristina, Kosovo",42.6629,21.1655,1],
["Athens, Greece",37.9838,23.7275,2],["Nicosia, Cyprus",35.1856,33.3823,2],["Valletta, Malta",35.8989,14.5146,1],
["Luxembourg City, Luxembourg",49.6117,6.1319,1],["Monaco",43.7384,7.4246,1],["Andorra la Vella, Andorra",42.5063,1.5218,1],
["Vaduz, Liechtenstein",47.1410,9.5209,1],["San Marino",43.9424,12.4578,1],
["Kyiv, Ukraine",50.4501,30.5234,2],["Minsk, Belarus",53.9006,27.5590,3],["Chisinau, Moldova",47.0105,28.8638,2],
["Vilnius, Lithuania",54.6872,25.2797,2],["Riga, Latvia",56.9496,24.1052,2],["Tallinn, Estonia",59.4370,24.7536,2],
["Moscow, Russia",55.7558,37.6173,3],["Saint Petersburg, Russia",59.9311,30.3609,3],
["Istanbul, Türkiye",41.0082,28.9784,3],["Ankara, Türkiye",39.9334,32.8597,3],
// Africa
["Cairo, Egypt",30.0444,31.2357,2],["Lagos, Nigeria",6.5244,3.3792,1],["Abuja, Nigeria",9.0765,7.3986,1],
["Kinshasa, DR Congo",-4.4419,15.2663,1],["Nairobi, Kenya",-1.2921,36.8219,3],["Johannesburg, South Africa",-26.2041,28.0473,2],
["Cape Town, South Africa",-33.9249,18.4241,2],["Pretoria, South Africa",-25.7479,28.2293,2],
["Accra, Ghana",5.6037,-0.1870,0],["Casablanca, Morocco",33.5731,-7.5898,1],["Rabat, Morocco",34.0209,-6.8416,1],
["Algiers, Algeria",36.7538,3.0588,1],["Tunis, Tunisia",36.8065,10.1815,1],["Tripoli, Libya",32.8872,13.1913,2],
["Khartoum, Sudan",15.5007,32.5599,2],["Addis Ababa, Ethiopia",9.0250,38.7469,3],["Dar es Salaam, Tanzania",-6.7924,39.2083,3],
["Dodoma, Tanzania",-6.1630,35.7516,3],["Kampala, Uganda",0.3476,32.5825,3],["Kigali, Rwanda",-1.9403,29.8739,2],
["Bujumbura, Burundi",-3.3614,29.3599,2],["Mogadishu, Somalia",2.0469,45.3182,3],["Djibouti City, Djibouti",11.8251,42.5903,3],
["Asmara, Eritrea",15.3229,38.9251,3],["Juba, South Sudan",4.8594,31.5713,2],
["Dakar, Senegal",14.7167,-17.4677,0],["Bamako, Mali",12.6392,-8.0029,0],["Ouagadougou, Burkina Faso",12.3714,-1.5197,0],
["Niamey, Niger",13.5127,2.1128,1],["N'Djamena, Chad",12.1348,15.0557,1],["Abidjan, Ivory Coast",5.3600,-4.0083,0],
["Yamoussoukro, Ivory Coast",6.8276,-5.2893,0],["Conakry, Guinea",9.6412,-13.5784,0],["Freetown, Sierra Leone",8.4657,-13.2317,0],
["Monrovia, Liberia",6.2907,-10.7605,0],["Lomé, Togo",6.1319,1.2228,0],["Porto-Novo, Benin",6.4969,2.6289,1],
["Nouakchott, Mauritania",18.0735,-15.9582,0],["Praia, Cape Verde",14.9330,-23.5133,-1],["Bissau, Guinea-Bissau",11.8636,-15.5977,0],
["Banjul, Gambia",13.4549,-16.5790,0],
["Yaoundé, Cameroon",3.8480,11.5021,1],["Libreville, Gabon",0.4162,9.4673,1],["Brazzaville, Republic of the Congo",-4.2634,15.2429,1],
["Bangui, Central African Republic",4.3947,18.5582,1],["Malabo, Equatorial Guinea",3.7500,8.7833,1],
["São Tomé, São Tomé and Príncipe",0.3302,6.7333,0],
["Luanda, Angola",-8.8390,13.2894,1],["Lusaka, Zambia",-15.3875,28.3228,2],["Harare, Zimbabwe",-17.8252,31.0335,2],
["Lilongwe, Malawi",-13.9626,33.7741,2],["Maputo, Mozambique",-25.9692,32.5732,2],["Windhoek, Namibia",-22.5609,17.0658,2],
["Gaborone, Botswana",-24.6282,25.9231,2],["Mbabane, Eswatini",-26.3054,31.1367,2],["Maseru, Lesotho",-29.3151,27.4869,2],
["Antananarivo, Madagascar",-18.8792,47.5079,3],["Port Louis, Mauritius",-20.1609,57.5012,4],["Victoria, Seychelles",-4.6191,55.4513,4],
["Moroni, Comoros",-11.7172,43.2473,3],
["Tripoli, Lebanon",34.4367,35.8497,2],["Tripoli, Libya",32.8872,13.1913,2],
// Middle East
["Dubai, UAE",25.2048,55.2708,4],["Abu Dhabi, UAE",24.4539,54.3773,4],["Riyadh, Saudi Arabia",24.7136,46.6753,3],
["Jeddah, Saudi Arabia",21.4858,39.1925,3],["Doha, Qatar",25.2854,51.5310,3],["Manama, Bahrain",26.2285,50.5860,3],
["Kuwait City, Kuwait",29.3759,47.9774,3],["Muscat, Oman",23.5880,58.3829,4],["Sana'a, Yemen",15.3694,44.1910,3],
["Baghdad, Iraq",33.3152,44.3661,3],["Tehran, Iran",35.6892,51.3890,3.5],["Amman, Jordan",31.9454,35.9284,2],
["Beirut, Lebanon",33.8938,35.5018,2],["Damascus, Syria",33.5138,36.2765,2],["Jerusalem, Israel",31.7683,35.2137,2],
["Tel Aviv, Israel",32.0853,34.7818,2],["Ramallah, Palestine",31.9038,35.2034,2],["Ankara, Türkiye",39.9334,32.8597,3],
["Baku, Azerbaijan",40.4093,49.8671,4],["Tbilisi, Georgia",41.7151,44.8271,4],["Yerevan, Armenia",40.1792,44.4991,4],
// Central & South Asia
["Mumbai, India",19.0760,72.8777,5.5],["Delhi, India",28.6139,77.2090,5.5],["Bengaluru, India",12.9716,77.5946,5.5],
["Kolkata, India",22.5726,88.3639,5.5],["Chennai, India",13.0827,80.2707,5.5],["Hyderabad, India",17.3850,78.4867,5.5],
["Ahmedabad, India",23.0225,72.5714,5.5],["Pune, India",18.5204,73.8567,5.5],["Jaipur, India",26.9124,75.7873,5.5],
["Lucknow, India",26.8467,80.9462,5.5],
["Islamabad, Pakistan",33.6844,73.0479,5],["Karachi, Pakistan",24.8607,67.0011,5],["Lahore, Pakistan",31.5497,74.3436,5],
["Dhaka, Bangladesh",23.8103,90.4125,6],["Kathmandu, Nepal",27.7172,85.3240,5.75],["Thimphu, Bhutan",27.4712,89.6339,6],
["Colombo, Sri Lanka",6.9271,79.8612,5.5],["Malé, Maldives",4.1755,73.5093,5],
["Kabul, Afghanistan",34.5553,69.2075,4.5],
["Tashkent, Uzbekistan",41.2995,69.2401,5],["Almaty, Kazakhstan",43.2220,76.8512,6],["Astana, Kazakhstan",51.1694,71.4491,5],
["Bishkek, Kyrgyzstan",42.8746,74.5698,6],["Dushanbe, Tajikistan",38.5598,68.7870,5],["Ashgabat, Turkmenistan",37.9601,58.3261,5],
["Ulaanbaatar, Mongolia",47.8864,106.9057,8],
// East & Southeast Asia
["Beijing, China",39.9042,116.4074,8],["Shanghai, China",31.2304,121.4737,8],["Guangzhou, China",23.1291,113.2644,8],
["Shenzhen, China",22.5431,114.0579,8],["Chengdu, China",30.5728,104.0668,8],["Xi'an, China",34.3416,108.9398,8],
["Chongqing, China",29.4316,106.9123,8],["Wuhan, China",30.5928,114.3055,8],
["Hong Kong",22.3193,114.1694,8],["Macau",22.1987,113.5439,8],["Taipei, Taiwan",25.0330,121.5654,8],
["Tokyo, Japan",35.6762,139.6503,9],["Osaka, Japan",34.6937,135.5023,9],["Yokohama, Japan",35.4437,139.6380,9],
["Nagoya, Japan",35.1815,136.9066,9],["Sapporo, Japan",43.0621,141.3544,9],["Fukuoka, Japan",33.5904,130.4017,9],
["Seoul, South Korea",37.5665,126.9780,9],["Busan, South Korea",35.1796,129.0756,9],["Pyongyang, North Korea",39.0392,125.7625,9],
["Bangkok, Thailand",13.7563,100.5018,7],["Hanoi, Vietnam",21.0278,105.8342,7],["Ho Chi Minh City, Vietnam",10.8231,106.6297,7],
["Phnom Penh, Cambodia",11.5564,104.9282,7],["Vientiane, Laos",17.9757,102.6331,7],["Naypyidaw, Myanmar",19.7633,96.0785,6.5],
["Yangon, Myanmar",16.8409,96.1735,6.5],
["Singapore",1.3521,103.8198,8],["Kuala Lumpur, Malaysia",3.1390,101.6869,8],["Bandar Seri Begawan, Brunei",4.9031,114.9398,8],
["Manila, Philippines",14.5995,120.9842,8],["Cebu City, Philippines",10.3157,123.8854,8],
["Jakarta, Indonesia",-6.2088,106.8456,7],["Surabaya, Indonesia",-7.2575,112.7521,7],["Bali (Denpasar), Indonesia",-8.6705,115.2126,8],
["Dili, Timor-Leste",-8.5569,125.5603,9],
// Oceania
["Sydney, Australia",-33.8688,151.2093,10],["Melbourne, Australia",-37.8136,144.9631,10],["Brisbane, Australia",-27.4698,153.0251,10],
["Perth, Australia",-31.9505,115.8605,8],["Adelaide, Australia",-34.9285,138.6007,9.5],["Canberra, Australia",-35.2809,149.1300,10],
["Darwin, Australia",-12.4634,130.8456,9.5],["Hobart, Australia",-42.8821,147.3272,10],
["Auckland, New Zealand",-36.8509,174.7645,12],["Wellington, New Zealand",-41.2865,174.7762,12],["Christchurch, New Zealand",-43.5321,172.6362,12],
["Suva, Fiji",-18.1416,178.4419,12],["Port Moresby, Papua New Guinea",-9.4438,147.1803,10],["Nouméa, New Caledonia",-22.2758,166.4581,11],
["Apia, Samoa",-13.8506,-171.7513,13],["Nuku'alofa, Tonga",-21.1789,-175.1982,13],["Honiara, Solomon Islands",-9.4280,159.9498,11],
["Port Vila, Vanuatu",-17.7333,168.3273,11],["Tarawa, Kiribati",1.3291,172.9790,12],["Majuro, Marshall Islands",7.1164,171.1858,12],
["Palikir, Micronesia",6.9147,158.1610,11],["Koror, Palau",7.3419,134.4791,9]
];
const TERRAIN_GLYPH={Tree:"🌲",Rock:"⬡",Bush:"♣",Rubble:"▪",Water:"≈",Smoke:"☁",Wall:"▰",FelledTree:"🪵",Spikes:"▲",Caltrops:"✳",Open:""};
// Small badges drawn above a fighter token: status effects + eye activation.
const STATUS_GLYPH={Burn:"🔥",Bleed:"🩸",Poison:"🧪",Blind:"🌑",Stun:"💫",Sleep:"💤",Slow:"🐌",Root:"🌿",Snare:"🕸️",Prone:"🔻",Stagger:"💢",Silence:"🤐",Disarm:"🗡️",Confusion:"😵",Fear:"😱",Fortified:"🛡️",Shield:"🔷",Regen:"💚",Stealth:"👤",Grappled:"🔗",Grappling:"🤼",Mounting:"🧗",Mounted:"🧎",FocusLock:"🚫"};
const STATUS_BUFF=new Set(["Fortified","Shield","Regen","Stealth","Grappling","Mounting"]);
function fighterIndicators(f,p){
  const badges=[];
  if(f.eyeActive)badges.push({g:"👁️",cls:"eye"});
  const seen=new Set();
  for(const s of f.statuses){if(seen.has(s.kind))continue;seen.add(s.kind);const g=STATUS_GLYPH[s.kind];if(!g)continue;badges.push({g,cls:STATUS_BUFF.has(s.kind)?"buff":"debuff"});}
  if(!badges.length)return"";
  const cap=5;let list=badges,extra=0;
  if(badges.length>cap){list=badges.slice(0,cap-1);extra=badges.length-(cap-1);}
  // above the sprite's head when the rig draws this fighter, else above the glyph token
  const k=ARENA.hexStep/34,step=Math.round(12*k),n=list.length+(extra?1:0),startX=p.x-(n-1)*step/2,y=SPR&&SPR.handles(f)?p.y-Math.round(ARENA.hexStep*0.4)-60:p.y-Math.round(23*k);
  let out="";
  list.forEach((b,i)=>{const x=startX+i*step;out+=`<g class="statind ${b.cls}"><rect class="statind-bar" x="${x-5.5*k}" y="${y+7*k}" width="${11*k}" height="${2.3*k}" rx="${k}"></rect><text class="statind-g" x="${x}" y="${y}">${b.g}</text></g>`;});
  if(extra){const x=startX+list.length*step;out+=`<text class="statind-more" x="${x}" y="${y}">+${extra}</text>`;}
  return out;
}
const ELEMENT_SIGN={Fire:"Aries",Earth:"Taurus",Air:"Gemini",Water:"Cancer"};
const S={chart:null,profile:null,B:null,player:null,queue:[],moveTo:null,category:"Ready",source:"All",query:"",showLocked:false,selectedMartials:new Set(["Boxing"]),aiNoise:.12,god:false,mainTarget:null,targeting:null,lastKnown:null,hoverCell:null,caravan:null,scenario:"duel",roster:{allies:[],opponents:[]},rosterScenario:null};
// Scalability testbed cap (2026-08-17): the roster-based scenarios (1vX gang battle, N-way
// team battle, N-way free-for-all) can seat this many combatants total, player included.
const ROSTER_CAP=10;
// --- Targeting model (Slice B) ---
// S.queue holds wrapper entries {ab, target, point}. These helpers keep the
// view-model (which expects a flat ability list) and the resolver in sync.
const qAbils=()=>S.queue.map(e=>e.ab);
function perceivedEnemies(){if(!S.B)return[];return S.B.all.filter(f=>AF.alive(f)&&f.faction!==S.player.faction&&S.B.perceives(S.player,f));}
function wantsPoint(ab){return ab.targeting==="PointRadius"||(ab.effects||[]).some(e=>e.k==="Terrain"||e.k==="SpawnSummon");}
// A throw destination is aimed relative to the grapple PARTNER's current cell, not the
// caster's — distinct from the generic "point" mode above, which places an AoE relative to
// the caster. An unaimed throw (no point set) falls back to the engine's straight-line-away
// default, so aiming is optional, never required.
function hasThrow(ab){return (ab.effects||[]).some(e=>e.k==="GrappleTech"&&e.throw>0);}
function throwRange(ab){const e=(ab.effects||[]).find(x=>x.k==="GrappleTech"&&x.throw>0);return e?e.throw:0;}
function throwOrigin(){const partner=AF.relPartner(S.player);return partner?{...partner.cell}:null;}
function validThrowPick(ab,cell){const from=throwOrigin();if(!from)return false;return AF.hdist(from,cell)<=throwRange(ab)&&S.B.grid.inBounds(cell);}
function isSummonAb(ab){return (ab.effects||[]).some(e=>e.k==="SpawnSummon");}
function placesTerrain(ab){return ab.targeting==="PointRadius"||(ab.effects||[]).some(e=>e.k==="Terrain");}
function targetMode(ab){if(hasThrow(ab))return"throw";if(ab.targeting==="SingleEnemy")return"enemy";if(ab.targeting==="SingleAlly")return"ally";if(wantsPoint(ab))return"point";return null;}
function canTarget(ab){return !!targetMode(ab);}
function enemyAt(cell){return perceivedEnemies().find(f=>f.cell.q===cell.q&&f.cell.r===cell.r)||null;}
function allyAt(cell){return S.B.all.find(f=>AF.alive(f)&&f.faction===S.player.faction&&f.cell.q===cell.q&&f.cell.r===cell.r)||null;}
function updateLastKnown(){if(!S.lastKnown)S.lastKnown=new Map();for(const f of S.B.all)if(f.faction!==S.player.faction&&AF.alive(f)&&S.B.perceives(S.player,f))S.lastKnown.set(f,{...f.cell});}
function ensureMainTarget(){const seen=perceivedEnemies();if(S.mainTarget&&(!AF.alive(S.mainTarget)||!seen.includes(S.mainTarget)))S.mainTarget=null;if(!S.mainTarget&&seen.length)S.mainTarget=S.B.nearestPerceivedEnemy(S.player)||seen[0];}
function cycleMainTarget(dir=1){const seen=perceivedEnemies();if(!seen.length){S.mainTarget=null;return;}const i=seen.indexOf(S.mainTarget);S.mainTarget=seen[((i<0?0:i)+dir+seen.length)%seen.length];}
function enterTargeting(index){const e=S.queue[index];const m=e&&targetMode(e.ab);if(!m){S.targeting=null;return;}S.targeting={index,mode:m};}
function exitTargeting(){S.targeting=null;S.hoverCell=null;}
function targetLabelFor(e){const ab=e.ab;
  if(hasThrow(ab))return e.point?`🎯 land at ${e.point.q},${e.point.r}`:"↳ default (straight back)";
  if(ab.targeting==="SingleEnemy"){if(e.target)return`🎯 ${e.target.name}`;return S.mainTarget?`↳ main (${S.mainTarget.name})`:"↳ nearest";}
  if(ab.targeting==="SingleAlly")return e.target?`🎯 ${e.target.name}`:"↳ auto (most hurt in range)";
  if(isSummonAb(ab))return e.point?`🎯 place ${e.point.q},${e.point.r}`:"↳ beside you";
  if(wantsPoint(ab)){if(e.point)return`🎯 ${e.point.q},${e.point.r}`;const c=mainTargetCell();return c?`↳ main area (${c.q},${c.r})`:"↳ auto";}
  return"self";}
function mainTargetCell(){if(S.mainTarget){if(AF.alive(S.mainTarget)&&S.B.perceives(S.player,S.mainTarget))return{...S.mainTarget.cell};const lk=S.lastKnown&&S.lastKnown.get(S.mainTarget);if(lk)return{...lk};}return null;}
function planActions(){return S.queue.map(e=>{const ab=e.ab;let target=e.target,point=e.point;
  if(!target&&!point){
    if(ab.targeting==="SingleEnemy"){if(S.mainTarget&&AF.alive(S.mainTarget)&&S.B.perceives(S.player,S.mainTarget))target=S.mainTarget;}
    else if(placesTerrain(ab))point=mainTargetCell();
    // SingleAlly and summons fall through — engine auto-picks the most-hurt ally / a cell beside the caster
  }
  if(target&&ab.targeting==="SingleEnemy"&&!(AF.alive(target)&&S.B.perceives(S.player,target)))target=null;
  if(target&&ab.targeting==="SingleAlly"&&!AF.alive(target))target=null;
  return(target||point)?{ability:ab,target,point}:ab;});}
// Arena pixel geometry is per-battle, not fixed: a larger map-size choice needs a bigger
// viewBox so hexes stay the same visual size instead of shrinking to cram more cells into the
// old fixed canvas (which would defeat the point of a "less cramped" bigger map). ARENA is
// (re)computed by computeArenaGeometry() at battle start and applied to the SVG element there;
// pointy() just reads whatever is current.
// Hex step 20 (was 34; user, 2026-10-15: adjacent fighters stood too far apart for melee to read as connecting). At
// step 20 adjacent cells are ~35 px apart, so a jab (23 px past the pivot) meets an adjacent opponent's guard. The
// arena is drawn at an integer 2x when it fits (fitArena), so the pixel-art sprites stay crisp.
let ARENA={cx:380,cy:305,hexStep:20,zoom:2};
const pointy=(q,r,s=ARENA.hexStep)=>({x:ARENA.cx+s*Math.sqrt(3)*(q+r/2),y:ARENA.cy+s*1.5*r});
const poly=(x,y,s=ARENA.hexStep-1)=>Array.from({length:6},(_,i)=>{const a=(60*i-30)*Math.PI/180;return`${x+s*Math.cos(a)},${y+s*Math.sin(a)}`}).join(" ");
// Sprite layer (af-sprites-v3.js): playtest rig drawn over the arena; rounds replay from B.events.
const SPR=window.AFSprites||null;
AFUI.arenaHexStep=()=>ARENA.hexStep;
if(SPR)SPR.attach({cellPx:c=>pointy(c.q,c.r),hexStep:()=>ARENA.hexStep,focusOf:f=>f===S.player&&S.mainTarget&&AF.alive(S.mainTarget)?S.mainTarget:null,board:boardForRecording,rerender:()=>{if(S.B&&!$("battle").classList.contains("hidden"))renderArena();},onRecap:showRecapProgress});
const hexCorners=(x,y,s=ARENA.hexStep-1)=>Array.from({length:6},(_,i)=>{const a=(60*i-30)*Math.PI/180;return{x:x+s*Math.cos(a),y:y+s*Math.sin(a)};});
// Exact half-extents of a radius-R hex grid at the current hex step, so the viewBox fits every
// cell with a fixed margin — computed directly rather than approximated, so it's exact at any
// radius instead of needing a per-tier magic number.
function computeArenaGeometry(radius){
  const s=ARENA.hexStep,pad=Math.round(s*1.4);
  let maxX=0,maxY=0;
  for(let q=-radius;q<=radius;q++)for(let r=Math.max(-radius,-q-radius);r<=Math.min(radius,-q+radius);r++){
    maxX=Math.max(maxX,Math.abs(s*Math.sqrt(3)*(q+r/2)));maxY=Math.max(maxY,Math.abs(s*1.5*r));
  }
  const cx=Math.round(maxX+pad),cy=Math.round(maxY+pad);
  return{cx,cy,hexStep:s,vbW:cx*2,vbH:cy*2};
}
// Display size: an integer 2x when the arena fits its panel at 2x, otherwise scaled to fit the panel width.
function fitArena(){
  const svg=$("arena"),wrap=svg&&svg.parentElement;if(!svg||!ARENA.vbW)return;
  const avail=(wrap&&wrap.clientWidth)||ARENA.vbW*2;
  const z=avail>=ARENA.vbW*2?2:Math.max(0.5,avail/ARENA.vbW);ARENA.zoom=z;
  svg.style.width=Math.floor(ARENA.vbW*z)+"px";svg.style.height=Math.floor(ARENA.vbH*z)+"px";svg.style.margin="0 auto";
}
window.addEventListener("resize",()=>{if(S.B)fitArena();});
// what the recap recorder redraws: every hex centre with its terrain kind and glyph
const TERRAIN_KIND={Tree:"hard",Rock:"hard",Wall:"hard",Bush:"soft",Rubble:"soft",Smoke:"soft",FelledTree:"fell",Spikes:"hazard",Caltrops:"hazard"};
function boardForRecording(){
  if(!S.B)return null;
  return{vbW:ARENA.vbW,vbH:ARENA.vbH,hexStep:ARENA.hexStep,cells:[...S.B.grid.cells()].map(c=>{const p=pointy(c.q,c.r),t=S.B.grid.terrainAt(c);return{x:p.x,y:p.y,kind:TERRAIN_KIND[t]||"open",glyph:TERRAIN_GLYPH[t]||""};})};
}
// Map-size tiers (owner request, 2026-08-18): a small 1v1/2v2 stays on the original radius-5
// arena; larger rosters get genuinely more room instead of feeling cramped. "Auto" sizes off the
// scenario's actual combatant count; the player can always override via the Map size selector.
const MAP_SIZES={small:5,medium:7,large:10};
function estimateCombatantCount(scenario){
  if(scenario==="duel")return 2;
  if(scenario==="escort"||scenario==="ambush")return 4;
  if(usesRoster(scenario))return rosterTotal();
  return 2;
}
function mapRadiusFor(sizeChoice,combatantCount){
  if(sizeChoice&&sizeChoice!=="auto")return MAP_SIZES[sizeChoice]||MAP_SIZES.small;
  if(combatantCount<=4)return MAP_SIZES.small;
  if(combatantCount<=7)return MAP_SIZES.medium;
  return MAP_SIZES.large;
}
// Trace only the connected outer perimeter of the reach disc: for each in-range tile, draw the
// hex edges it shares with a tile that is NOT in range (interior edges are shared and skipped).
function reachPerimeter(center,R){
  const cells=[...S.B.grid.cells()].filter(c=>AF.hdist(center,c)<=R);
  const inSet=new Set(cells.map(c=>AF.hkey(c)));
  const segs=[];
  for(const c of cells){
    const ctr=pointy(c.q,c.r),corners=hexCorners(ctr.x,ctr.y);
    for(const n of AF.neighbors(c)){
      if(inSet.has(AF.hkey(n)))continue; // shared interior edge — not on the perimeter
      const nc=pointy(n.q,n.r),dx=nc.x-ctr.x,dy=nc.y-ctr.y;
      let bi=0,bd=-1e9;
      for(let i=0;i<6;i++){const a=corners[i],b=corners[(i+1)%6],mx=(a.x+b.x)/2-ctr.x,my=(a.y+b.y)/2-ctr.y,dot=mx*dx+my*dy;if(dot>bd){bd=dot;bi=i;}}
      const a=corners[bi],b=corners[(bi+1)%6];
      segs.push(`M${a.x.toFixed(1)} ${a.y.toFixed(1)}L${b.x.toFixed(1)} ${b.y.toFixed(1)}`);
    }
  }
  return segs.join("");
}

// --- Searchable birth location (replaces the old fixed 35-city <select>) ---
// #city stays a hidden input holding JSON {name,lat,lon} so captureBirth/restoreBirth and
// previewChart's lat/lon lookup keep working off "$(\"city\").value" like before — it's just
// no longer an index into CITIES, so the list can grow/reorder freely without corrupting any
// previously saved career profile's stored value.
let cityHighlight=-1,cityMatches=[];
function citySnapToOffset(raw){
  const step=Math.round(raw*2)/2; // nearest half-hour, matching the manual UTC-offset dropdown's granularity
  return Math.max(-12,Math.min(14,step));
}
function selectCity(entry,fireChange=true){
  $("city").value=JSON.stringify({name:entry[0],lat:entry[1],lon:entry[2]});
  $("citySearch").value=entry[0];
  $("offset").value=String(citySnapToOffset(entry[3]));
  closeCityResults();
  if(fireChange)$("city").dispatchEvent(new Event("change",{bubbles:true}));
}
function renderCityResults(){
  const q=$("citySearch").value.trim().toLowerCase();
  const box=$("cityResults");
  if(!q){cityMatches=[];box.classList.add("hidden");box.innerHTML="";return;}
  cityMatches=CITIES.filter(c=>c[0].toLowerCase().includes(q)).slice(0,8);
  cityHighlight=cityMatches.length?0:-1;
  if(!cityMatches.length){box.classList.add("hidden");box.innerHTML="";return;}
  box.innerHTML=cityMatches.map((c,i)=>`<div class="city-result${i===cityHighlight?" hl":""}" data-i="${i}">${c[0]}</div>`).join("");
  box.classList.remove("hidden");
}
function closeCityResults(){$("cityResults").classList.add("hidden");$("cityResults").innerHTML="";cityMatches=[];cityHighlight=-1;}
// Reads #city's stored value as [name,lat,lon] regardless of whether it's the new JSON form
// or a legacy CITIES-array-index string from a save made before this change, falling back to
// the same default (CITIES[0]) the field starts with.
function parseCityValue(raw){
  try{const parsed=JSON.parse(raw);if(parsed&&typeof parsed==="object"&&parsed.lat!=null)return[parsed.name,parsed.lat,parsed.lon];}catch(e){}
  return CITIES[+raw||0]||CITIES[0];
}
function paintCityHighlight(){$("cityResults").querySelectorAll(".city-result").forEach((el,i)=>el.classList.toggle("hl",i===cityHighlight));}
function initCitySearch(){
  selectCity(CITIES[0],false); // sensible non-empty default, same city the old <select> defaulted to
  $("citySearch").addEventListener("input",renderCityResults);
  $("citySearch").addEventListener("focus",()=>{if($("citySearch").value.trim())renderCityResults();});
  $("citySearch").addEventListener("keydown",e=>{
    if(!cityMatches.length){if(e.key==="Enter")e.preventDefault();return;}
    if(e.key==="ArrowDown"){e.preventDefault();cityHighlight=Math.min(cityMatches.length-1,cityHighlight+1);paintCityHighlight();}
    else if(e.key==="ArrowUp"){e.preventDefault();cityHighlight=Math.max(0,cityHighlight-1);paintCityHighlight();}
    else if(e.key==="Enter"){e.preventDefault();if(cityHighlight>=0)selectCity(cityMatches[cityHighlight]);}
    else if(e.key==="Escape"){closeCityResults();}
  });
  $("citySearch").addEventListener("blur",()=>setTimeout(closeCityResults,150));
  $("cityResults").addEventListener("mousedown",e=>{
    const row=e.target.closest(".city-result");if(!row)return;
    e.preventDefault(); // keep focus/selection order sane: fire before the input's blur
    selectCity(cityMatches[+row.dataset.i]);
  });
}

function init(){
  if(!window.AF||!window.AFUI){$("engineState").textContent="Engine/UI module failed to load";return;}
  $("engineState").textContent=`AF ${AF.VERSION} · UI ${AFUI.VERSION}`;
  for(let x=-12;x<=14;x+=.5){const label=`UTC${x>=0?"+":""}${Number.isInteger(x)?x:x.toFixed(1)}`;$("offset").add(new Option(label,x));}
  $("offset").value="-5";
  initCitySearch();
  for(const id of["enemy1","enemy2","ally"])AF.ENEMY_KEYS.forEach(k=>$(id).add(new Option(`${AF.ENEMIES[k].glyph} ${AF.ENEMIES[k].name} · ${AF.ENEMIES[k].persona}`,k)));
  $("enemy1").value="StreetThug";$("enemy2").value="Sorcerer";$("ally").value="MuayThaiFighter";
  Object.keys(AF.MARTIAL).forEach(k=>{$("martials").insertAdjacentHTML("beforeend",`<button type="button" class="style-toggle ${S.selectedMartials.has(k)?"selected":""}" data-style="${k}">${labelStyle(k)}</button>`);});
  $("martials").querySelectorAll("button").forEach(b=>b.onclick=()=>{const k=b.dataset.style;S.selectedMartials.has(k)?S.selectedMartials.delete(k):S.selectedMartials.add(k);b.classList.toggle("selected",S.selectedMartials.has(k));if(S.career){S.progress.martials=[...S.selectedMartials];saveCareer();renderCareerPanel();}});
  Object.keys(AF.WEAPONS).forEach(k=>$("weapon").add(new Option(labelStyle(k),k)));
  $("weapon").onchange=()=>{if(S.career&&S.progress.birth){S.progress.birth.weapon=$("weapon").value;saveCareer();}};
  AF.BLOOD_KEYS.forEach(k=>$("bloodline").add(new Option(k,k)));
  ["STR","AGI","FORT","INT","CHA"].forEach((s,i)=>{$("stats").insertAdjacentHTML("beforeend",`<div class="field"><label>${s}</label><input id="s${s}" type="number" min="1" max="30" value="${[9,10,9,8,8][i]}"></div>`);$("s"+s).addEventListener("input",updateStatTotal);});
  $("milestones").innerHTML=AFUI.LEVEL_MILESTONES.map(m=>`<button type="button" class="milestone" data-level="${m.level}">L${m.level}</button>`).join("");
  $("milestones").querySelectorAll("button").forEach(b=>b.onclick=()=>setLevel(+b.dataset.level));
  $("level").oninput=()=>setLevel($("level").value,false);$("levelRange").oninput=()=>setLevel($("levelRange").value,true);
  ["city","offset","birthDate","birthTime","forceAll"].forEach(id=>$(id).addEventListener("change",previewChart));
  $("scenario").onchange=renderScenarioFields;$("preview").onclick=previewChart;$("start").onclick=startBattle;
  $("addAlly").onclick=()=>{if(rosterTotal()<ROSTER_CAP){S.roster.allies.push({key:"MuayThaiFighter",level:playerLevel(),auto:true});renderRoster();}};
  $("addOpponent").onclick=()=>{if(rosterTotal()<ROSTER_CAP){S.roster.opponents.push({key:"StreetThug",level:playerLevel(),auto:true});renderRoster();}};
  for(const id of["enemy1Level","enemy2Level","allyLevel"])$(id).addEventListener("input",()=>{$(id).dataset.autoLevel="0";});
  $("clearQueue").onclick=()=>{S.queue=[];exitTargeting();renderQueue();renderAbilityBrowser();renderArena();};
  $("resolve").onclick=resolveRound;$("recapSkip").onclick=()=>SPR&&SPR.skip();$("watchRecap").onclick=watchRecap;$("recordRecap").onclick=recordRecap;$("rematch").onclick=()=>location.reload();$("newBtn").onclick=()=>location.reload();
  $("abilitySearch").oninput=e=>{S.query=e.target.value;renderAbilityBrowser();};
  $("sourceFilter").onchange=e=>{S.source=e.target.value;renderAbilityBrowser(false);};
  $("showLocked").onchange=e=>{S.showLocked=e.target.checked;renderAbilityBrowser();};
  $("godBtn").onclick=()=>{S.god=!S.god;if(S.B)S.B.god=S.god;$("godBtn").textContent=`God mode: ${S.god?"on":"off"}`;};
  $("healBtn").onclick=restoreRoster;$("terrainBtn").onclick=regenerateTerrain;$("seedBtn").onclick=()=>{AF.setSeed(+$("seed").value||42);log(`RNG seed set to ${+$("seed").value||42}.`,"sys");};
  $("copyLog").onclick=copyLog;
  S.progress=loadCareer();
  $("mode").onchange=()=>{S.career=$("mode").value==="career";applyCareerMode();};
  $("start").addEventListener("click",()=>{if(S.career)S.progress.stats=stats();},true);
  bindBalance();
  updateStatTotal();renderScenarioFields();setLevel(20);previewChart();renderCareerPanel();
}
function labelStyle(k){return k.replace(/([a-z])([A-Z])/g,"$1 $2").replace("Jiu Jitsu","Jiu-Jitsu").replace("Kyoketsu Shoge","Kyoketsu-Shoge");}
// --- Career progression (Slice 2): persisted XP profile in localStorage ---
const CAREER_KEY="af-career-v1";
function loadCareer(){try{const j=JSON.parse(localStorage.getItem(CAREER_KEY));if(j&&j.abilityXp)return j;}catch(e){}const p=AFUI.newProgress();p.stats=null;return p;}
function saveCareer(){try{localStorage.setItem(CAREER_KEY,JSON.stringify(S.progress));}catch(e){}}
// "weapon" is deliberately NOT in this list: unlike birth date/city/eye/bloodline (immutable
// facts about the fighter), weapon is a trained discipline — same as martials, it should stay
// swappable between fights in career mode instead of getting locked forever after fight 1.
const BIRTH_FIELDS=["name","birthDate","birthTime","city","offset","eye","bloodline"];
function captureBirth(){return{name:$("name").value,birthDate:$("birthDate").value,birthTime:$("birthTime").value,city:$("city").value,offset:$("offset").value,weapon:$("weapon").value,eye:$("eye").value,bloodline:$("bloodline").value};}
function restoreBirth(b){
  if(b.name!=null)$("name").value=b.name;if(b.birthDate)$("birthDate").value=b.birthDate;if(b.birthTime)$("birthTime").value=b.birthTime;
  if(b.city!=null){$("city").value=b.city;
    // Old saves stored a CITIES array index; new ones store {name,lat,lon} JSON. Both are
    // handled so a career profile from before the searchable-location change still loads.
    try{const parsed=JSON.parse(b.city);if(parsed&&parsed.name)$("citySearch").value=parsed.name;
      else if(CITIES[+b.city])$("citySearch").value=CITIES[+b.city][0];}
    catch(e){if(CITIES[+b.city])$("citySearch").value=CITIES[+b.city][0];}}
  if(b.offset!=null)$("offset").value=b.offset;$("weapon").value=b.weapon||"";$("bloodline").value=b.bloodline||"";
  previewChart();
  if(b.eye!=null&&[...$("eye").options].some(o=>o.value===b.eye))$("eye").value=b.eye;}
function restoreMartials(list){
  S.selectedMartials=new Set(list&&list.length?list:["Boxing"]);
  $("martials").querySelectorAll("button").forEach(btn=>btn.classList.toggle("selected",S.selectedMartials.has(btn.dataset.style)));
  previewChart();}
function lockBirth(on){for(const id of BIRTH_FIELDS){const el=$(id);if(el)el.disabled=on;}$("citySearch").disabled=on;$("forceAll").disabled=on;if(on)$("forceAll").checked=false;}
function applyCareerMode(){const lvl=$("level"),rng=$("levelRange");
  if(S.career){
    if(S.progress.birth)restoreBirth(S.progress.birth);
    restoreMartials(S.progress.martials&&S.progress.martials.length?S.progress.martials:(S.progress.birth&&S.progress.birth.martials));
    lvl.value=String(S.progress.level);if(S.progress.stats){for(const s of["STR","AGI","FORT","INT","CHA"])if(S.progress.stats[s]!=null){const el=$("s"+s);if(el)el.value=S.progress.stats[s];}}
    lvl.readOnly=true;rng.disabled=true;lvl.dispatchEvent(new Event("input",{bubbles:true}));
    lockBirth(!!S.progress.birth);}
  else{lvl.readOnly=false;rng.disabled=false;lockBirth(false);}
  renderCareerPanel();previewChart();}
function renderCareerPanel(){const el=$("careerPanel");if(!el)return;
  if(!S.career){el.innerHTML='<span class="note">Quick battle — nothing is saved. Switch to Career to earn and keep XP.</span>';return;}
  const p=S.progress,cur=AFUI.charXpToReach(p.level),next=AFUI.charXpToReach(p.level+1),into=Math.max(0,(p.charXp||0)-cur),span=Math.max(1,next-cur);
  const abs=Object.entries(p.abilityXp||{}).map(([k,xp])=>({n:k.split("|")[1],lv:AFUI.abilityLevelFromXp(xp)})).filter(a=>a.lv>0).sort((a,b)=>b.lv-a.lv);
  el.innerHTML=`${p.birth?`<div class="note" style="margin-bottom:5px">Fighter: <b>${p.birth.name||"Starfighter"}</b> · born ${p.birth.birthDate} ${p.birth.birthTime} · birth locked</div>`:'<div class="note" style="margin-bottom:5px">New career — set birth data + build, then Enter arena to lock this fighter in.</div>'}<div class="tags"><span class="tag good">Career Level ${p.level}</span><span class="tag">${p.charXp||0} char XP</span></div>
  <div class="bar" style="margin:7px 0"><div class="fill" style="width:${Math.min(100,into/span*100)}%"></div></div>
  <div class="note">${next>cur?`${into} / ${span} XP to Level ${p.level+1}`:"maximum level"}</div>
  <div class="note" style="margin-top:6px">Leveled abilities: ${abs.length?abs.map(a=>`${a.n} <b>L${a.lv}</b>`).join(" · "):"none yet — use abilities in battle to level them"}</div>
  <div class="actions"><button class="secondary" id="resetCareer" type="button">Reset career</button></div>`;
  const r=$("resetCareer");if(r)r.onclick=()=>{
    if(r.dataset.armed){S.progress=AFUI.newProgress();S.progress.stats=null;saveCareer();applyCareerMode();return;}
    r.dataset.armed="1";r.textContent="Confirm reset — click again";r.classList.add("danger");
    clearTimeout(r._t);r._t=setTimeout(()=>{delete r.dataset.armed;r.textContent="Reset career";r.classList.remove("danger");},4000);
  };}
function setLevel(v,fromRange=false){if(S.career)v=S.progress.level;const n=AFUI.normLevel(v);$("level").value=n;$("levelRange").value=n;$("milestones").querySelectorAll("button").forEach(b=>b.classList.toggle("on",+b.dataset.level<=n));syncOpponentLevels(n);previewChart();}
// Opponent/ally levels default to the player's own level (owner request, 2026-08-17) rather
// than a fixed 20, and keep following it as the player's level changes — but only for a field
// the player hasn't manually overridden. Manual edits mark themselves via a "touched" flag
// (dataset on the three fixed inputs, an `auto` flag per roster entry) and stop following.
function syncOpponentLevels(n){
  for(const id of["enemy1Level","enemy2Level","allyLevel"]){const el=$(id);if(el&&el.dataset.autoLevel!=="0")el.value=n;}
  let touched=false;
  for(const e of[...S.roster.allies,...S.roster.opponents])if(e.auto!==false){e.level=n;touched=true;}
  if(touched&&!$("rosterField").classList.contains("hidden"))renderRoster();
}
function isCaravanScenario(v=S.scenario){return v==="escort"||v==="ambush";}
function usesRoster(v=S.scenario){return v==="onevx"||v==="team"||v==="ffa";}
function renderScenarioFields(){
  const v=$("scenario").value,roster=usesRoster(v);
  $("enemy1Field").classList.toggle("hidden",roster);
  $("enemy2Field").classList.toggle("hidden",v==="duel"||roster);
  $("allyField").classList.toggle("hidden",(v!=="team"&&!isCaravanScenario(v))||roster);
  const cf=$("caravanField");if(cf)cf.classList.toggle("hidden",!isCaravanScenario(v));
  $("rosterField").classList.toggle("hidden",!roster);
  if(roster){ensureRosterDefaults(v);renderRoster();}
}
// Roster-based scenarios reseed sensible defaults the first time the setup form switches TO
// them (or between them), but never stomp edits the player is mid-way through making while
// staying on the same scenario.
function ensureRosterDefaults(v){
  if(S.rosterScenario===v)return;
  S.rosterScenario=v;
  const lvl=playerLevel(),e=()=>({level:lvl,auto:true});
  if(v==="onevx")S.roster={allies:[],opponents:[{key:"StreetThug",...e()},{key:"StreetThug",...e()},{key:"Sorcerer",...e()}]};
  else if(v==="team")S.roster={allies:[{key:"MuayThaiFighter",...e()}],opponents:[{key:"StreetThug",...e()},{key:"Sorcerer",...e()}]};
  else if(v==="ffa")S.roster={allies:[],opponents:[{key:"StreetThug",...e()},{key:"Sorcerer",...e()}]};
}
function rosterTotal(){return 1+S.roster.allies.length+S.roster.opponents.length;}
function rosterOptionsHtml(sel){return AF.ENEMY_KEYS.map(k=>`<option value="${k}" ${k===sel?"selected":""}>${AF.ENEMIES[k].glyph} ${AF.ENEMIES[k].name} · ${AF.ENEMIES[k].persona}</option>`).join("");}
function rosterRowHtml(entry,idx,group){
  return`<div class="roster-row" data-group="${group}" data-idx="${idx}"><select class="rosterType">${rosterOptionsHtml(entry.key)}</select><input class="rosterLevel" max="100" min="1" title="Level — scales stats; 20 is the canonical baseline" type="number" value="${entry.level}"><button class="secondary rosterRemove" title="Remove" type="button">×</button></div>`;
}
function renderRoster(){
  const v=$("scenario").value,showAllies=v==="team";
  $("alliesGroup").classList.toggle("hidden",!showAllies);
  $("alliesRoster").innerHTML=S.roster.allies.map((e,i)=>rosterRowHtml(e,i,"allies")).join("")||'<div class="note">No allies</div>';
  $("opponentsRoster").innerHTML=S.roster.opponents.map((e,i)=>rosterRowHtml(e,i,"opponents")).join("");
  $("rosterField").querySelectorAll(".roster-row").forEach(row=>{
    const group=row.dataset.group,idx=+row.dataset.idx;
    row.querySelector(".rosterType").onchange=e=>{S.roster[group][idx].key=e.target.value;};
    row.querySelector(".rosterLevel").oninput=e=>{const entry=S.roster[group][idx];entry.level=Math.max(1,Math.min(100,+e.target.value||20));entry.auto=false;};
    row.querySelector(".rosterRemove").onclick=()=>{
      if(group==="opponents"&&S.roster.opponents.length<=1)return; // a scenario needs at least one opponent
      S.roster[group].splice(idx,1);renderRoster();
    };
  });
  const total=rosterTotal();
  $("rosterCount").textContent=`${total} / ${ROSTER_CAP}`;
  $("addAlly").disabled=total>=ROSTER_CAP;
  $("addOpponent").disabled=total>=ROSTER_CAP;
}
function updateStatTotal(){const t=["STR","AGI","FORT","INT","CHA"].reduce((n,s)=>n+(+$("s"+s).value||0),0);$("statTotal").textContent=t;$("statTotal").style.color=t===44?"var(--green)":"var(--red)";}
function birthUtc(){const [y,m,d]=$("birthDate").value.split("-").map(Number),[hh,mm]=$("birthTime").value.split(":").map(Number);return Date.UTC(y,m-1,d,hh,mm)-Number($("offset").value)*3600000;}
function previewChart(){
  try{
    const city=parseCityValue($("city").value);S.chart=AF.buildChart(birthUtc(),city[1],city[2]);S.profile=AFUI.levelProfile(S.chart,+$("level").value,$("forceAll").checked);
    const placements=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"];
    $("chartSummary").innerHTML=`<div class="summary-grid">${placements.map(p=>{const x=S.chart.placements[p];return`<div class="chipbox"><b>${p}</b>${AF.GLYPH[x.sign]} ${x.sign} ${x.deg.toFixed(1)}°<small class="note" style="display:block">Decan ${x.decan+1} · Dwad ${x.dwad+1}</small></div>`}).join("")}<div class="chipbox"><b>Ascendant</b>${AF.GLYPH[S.chart.asc.sign]} ${S.chart.asc.sign} ${S.chart.asc.deg.toFixed(1)}°<small class="note" style="display:block">Decan ${S.chart.asc.decan+1} · Dwad ${S.chart.asc.dwad+1}</small></div></div>`;
    updateEyeOptions();
    const p=S.profile;
    $("unlockSummary").innerHTML=`<div class="tags"><span class="tag good">L${p.level} · ${p.phase}</span>${p.signs.map(s=>`<span class="tag">${AF.GLYPH[s]} ${s}</span>`).join("")||'<span class="tag warn">No zodiac kit yet</span>'}</div><p class="note">Eyes: ${p.eyes.length?p.eyes.join(", "):"none"} · Summon: ${p.summon?AF.chartToLoadout(S.chart).summonSpecies.name+" ("+AF.chartToLoadout(S.chart).summonSpecies.role+")":"locked until L15"} · Ultimates: ${p.ultimates?"unlocked":"locked until L20"}</p>${p.northNode?'<p class="error">L100 reached: the North Node Karmic Ultimate is not authored in the current core.</p>':p.nextUnlock?`<p class="note">Next: L${p.nextUnlock.level} ${p.nextUnlock.label} — ${p.nextUnlock.detail}</p>`:""}`;
    $("progression").innerHTML=AFUI.LEVEL_MILESTONES.map(m=>`<div class="progress-row ${p.level>=m.level?"on":p.nextUnlock&&p.nextUnlock.level===m.level?"next":""}"><b>L${m.level}</b><span>${m.label}</span><span>${m.detail}</span></div>`).join("");
    $("setupError").textContent="";
  }catch(e){$("setupError").textContent=e.message||String(e);S.chart=null;}
}
function updateEyeOptions(){const old=$("eye").value;$("eye").innerHTML='<option value="">None</option>';for(const p of S.profile.eyes)$("eye").add(new Option(`${p} · ${AF.EYES[p].deity}`,p));if(S.profile.eyes.includes(old))$("eye").value=old;else if(S.profile.eyes.includes("Sun"))$("eye").value="Sun";}
function learnedMedical(){const v=$("learnedMedical")?.value||"";return v?v.split("|"):[];}
function stats(){return Object.fromEntries(["STR","AGI","FORT","INT","CHA"].map(s=>[s,+$("s"+s).value]));}
function makeEnemy(key,faction,cell,labelSuffix="",level=20){
  const E=AF.ENEMIES[key];return AF.makeFighter({name:E.name+labelSuffix,sign:ELEMENT_SIGN[E.element]||"Leo",stats:AF.scaleEnemyStats(E.stats,level),faction,cell,abilities:AF.enemyLoadout(key),glyph:E.glyph,focus:E.focus,persona:E.persona,summonSpecies:E.summon});
}
function enemyLevel(id){const el=$(id);const v=el?+el.value:20;return Number.isFinite(v)&&v>0?v:20;}
function playerLevel(){const v=+$("level").value;return Number.isFinite(v)&&v>0?v:20;}
const CARAVANS={
  standard:{name:"Caravan",hp:1000,speed:1,glyph:"🛒",attack:null},
  light:{name:"Light Caravan",hp:850,speed:2,glyph:"🛺",attack:null},
  heavy:{name:"Heavy Caravan",hp:1500,speed:1,glyph:"🚚",attack:{power:18,radius:2}}
};
function linePath(a,b){const n=AF.hdist(a,b),out=[{...a}];for(let i=1;i<=n;i++){const t=i/n;out.push(AF.cubeRound(a.q+(b.q-a.q)*t,a.r+(b.r-a.r)*t));}return out;}
function makeCaravan(typeKey,path,faction=0){
  const t=CARAVANS[typeKey]||CARAVANS.standard;
  const car=AF.makeFighter({name:t.name,sign:"Taurus",stats:{STR:8,AGI:2,FORT:20,INT:6,CHA:6},faction,cell:{...path[0]},glyph:t.glyph});
  car.isCaravan=true;car.maxHp=t.hp;car.hp=t.hp;car.path=path;car.pathIndex=0;car.speed=t.speed;car.caravanAttack=t.attack;
  return car;
}
/* Picks a random cell within `spread` tiles of an anchor, keeping each battle's opening
   layout fresh while preserving each scenario's overall shape (which side each faction opens
   on, caravan-relative positioning). Falls back to the anchor itself if the zone is somehow
   fully blocked, so a spawn never silently fails. */
function randomNear(grid,anchor,spread,taken,minSep=2){
  const candidates=[];
  for(let dq=-spread;dq<=spread;dq++)for(let dr=-spread;dr<=spread;dr++){
    const c=AF.hx(anchor.q+dq,anchor.r+dr);
    if(AF.hdist(anchor,c)>spread||!grid.inBounds(c))continue;
    if(AF.hdist(c,grid.center)===0)continue;
    if(taken.some(t=>AF.hdist(t,c)<minSep))continue;
    candidates.push(c);
  }
  const pick=candidates.length?candidates[Math.floor(AF.rand()*candidates.length)]:anchor;
  taken.push(pick);return pick;
}
// Spreads N spawn anchors along an arc of the arena so a roster of up to ROSTER_CAP
// combatants doesn't all pile into one corner. Purely a starting-anchor layout — each
// combatant's actual cell is still scattered around its anchor by randomNear.
function arcAnchors(n,startDeg,endDeg,radius){
  const out=[];
  for(let i=0;i<n;i++){
    const t=n<=1?0.5:i/(n-1);
    const rad=(startDeg+(endDeg-startDeg)*t)*Math.PI/180;
    out.push(AF.hx(Math.round(radius*Math.cos(rad)),Math.round(radius*Math.sin(rad))));
  }
  return out;
}
const ROMAN=["","I","II","III","IV","V","VI","VII","VIII","IX","X"];
// Matches the original fixed-scenario naming (first combatant of a group unsuffixed, then
// " II", " III", ...), generalized to an arbitrary group size.
function ordinalSuffix(i){return i===0?"":` ${ROMAN[i+1]||i+1}`;}
function startBattle(){
  previewChart();if(!S.chart)return;
  const st=stats(),total=Object.values(st).reduce((a,b)=>a+b,0);if(total!==44){$("setupError").textContent="Attributes must total exactly 44.";return;}
  if(S.career&&!S.progress.birth){S.progress.birth=captureBirth();lockBirth(true);}
  if(S.career){S.progress.martials=[...S.selectedMartials];saveCareer();}
  const prog=S.career?S.progress:null,plvl=S.career?S.progress.level:+$("level").value;
  const built=AFUI.buildPlayerAbilities(S.chart,plvl,{forceAllKits:$("forceAll").checked,martials:[...S.selectedMartials],weapon:$("weapon").value||null,eye:$("eye").value||null,bloodline:$("bloodline").value||null,learnedMedical:learnedMedical(),progress:prog});
  S.profile=built.profile;
  // Every fresh battle gets genuinely fresh entropy for spawn placement, terrain, and AI
  // behavior. The debug seed field / Apply Seed button remain a separate manual tool for
  // reproducing a specific state mid-session — they no longer pin every NEW battle's opening
  // layout to the same fixed default.
  AF.setSeed((Date.now()^Math.floor(Math.random()*0xFFFFFFFF))>>>0);AF.resetIds();
  const runtime=AFUI.buildPlayerAbilities(S.chart,plvl,{forceAllKits:$("forceAll").checked,martials:[...S.selectedMartials],weapon:$("weapon").value||null,eye:$("eye").value||null,bloodline:$("bloodline").value||null,learnedMedical:learnedMedical(),progress:prog});
  const scenario=$("scenario").value;
  const mapRadius=mapRadiusFor($("mapSize").value,estimateCombatantCount(scenario));
  S.mapRadius=mapRadius;
  const grid=AF.makeArena(mapRadius);
  // Every hardcoded anchor/spread below was tuned for the original radius-5 arena; scale them
  // by how much bigger the chosen map is so combatants actually spread across the extra room
  // instead of clustering near the center of a much larger, mostly-empty map.
  const spawnScale=mapRadius/MAP_SIZES.small;
  const sc=h=>AF.hx(Math.round(h.q*spawnScale),Math.round(h.r*spawnScale));
  const spawnSpread=Math.max(2,Math.round(2*spawnScale));
  ARENA=Object.assign(ARENA,computeArenaGeometry(mapRadius));
  const arenaSvg=$("arena");
  arenaSvg.setAttribute("viewBox",`0 0 ${ARENA.vbW} ${ARENA.vbH}`);
  fitArena();
  const taken=[];
  S.player=AF.makeFighter({name:$("name").value.trim()||"Starfighter",sign:S.chart.placements.Sun.sign,stats:st,faction:0,cell:randomNear(grid,sc(AF.hx(-4,2)),spawnSpread,taken),isPlayer:true,summonSpecies:AF.chartToLoadout(S.chart).summonSpecies,abilities:runtime.abilities,glyph:AF.GLYPH[S.chart.placements.Sun.sign]});
  S.player.level=runtime.profile.level;
  const all=[S.player];S.scenario=scenario;S.caravan=null;
  const lv1=enemyLevel("enemy1Level"),lv2=enemyLevel("enemy2Level"),lvAlly=enemyLevel("allyLevel");
  if(scenario==="duel")all.push(makeEnemy($("enemy1").value,1,randomNear(grid,sc(AF.hx(4,-2)),spawnSpread,taken),"",lv1));
  if(scenario==="onevx"){
    // 1 vs X: player alone against a gang of same-faction opponents, up to ROSTER_CAP-1 of them.
    const opps=S.roster.opponents.slice(0,ROSTER_CAP-1);
    const anchors=arcAnchors(opps.length,-70,160,4*spawnScale);
    opps.forEach((o,i)=>all.push(makeEnemy(o.key,1,randomNear(grid,anchors[i],spawnSpread,taken,1),ordinalSuffix(i),o.level)));
  }
  if(scenario==="team"){
    // N allies (faction 0, with the player) vs M opponents (faction 1), up to ROSTER_CAP total.
    const allies=S.roster.allies.slice(0,ROSTER_CAP-2),opps=S.roster.opponents.slice(0,ROSTER_CAP-1-allies.length);
    const allyAnchors=arcAnchors(allies.length,130,230,3*spawnScale);
    allies.forEach((a,i)=>all.push(makeEnemy(a.key,0,randomNear(grid,allyAnchors[i],spawnSpread,taken,1),` Ally${ordinalSuffix(i)}`,a.level)));
    const oppAnchors=arcAnchors(opps.length,-70,160,4*spawnScale);
    opps.forEach((o,i)=>all.push(makeEnemy(o.key,1,randomNear(grid,oppAnchors[i],spawnSpread,taken,1),ordinalSuffix(i),o.level)));
  }
  if(scenario==="ffa"){
    // True free-for-all: every opponent gets its own faction id, spread wide around the arena.
    const opps=S.roster.opponents.slice(0,ROSTER_CAP-1);
    const anchors=arcAnchors(opps.length,-150,140,4*spawnScale);
    opps.forEach((o,i)=>all.push(makeEnemy(o.key,i+1,randomNear(grid,anchors[i],spawnSpread,taken,1),ordinalSuffix(i),o.level)));
  }
  if(scenario==="escort"){
    S.player.cell=randomNear(grid,sc(AF.hx(-4,1)),Math.max(1,Math.round(spawnScale)),taken);
    const car=makeCaravan($("caravanType").value,linePath(sc(AF.hx(-5,0)),sc(AF.hx(5,0))),0);S.caravan=car;
    all.push(makeEnemy($("ally").value,0,randomNear(grid,sc(AF.hx(-4,-1)),Math.max(1,Math.round(spawnScale)),taken)," Escort",lvAlly),car,makeEnemy($("enemy1").value,1,randomNear(grid,sc(AF.hx(4,1)),spawnSpread,taken),"",lv1),makeEnemy($("enemy2").value,1,randomNear(grid,sc(AF.hx(4,-1)),spawnSpread,taken)," II",lv2));
  }
  if(scenario==="ambush"){
    // player is the attacker; an enemy caravan (faction 1) + its guards run A -> B.
    S.player.cell=randomNear(grid,sc(AF.hx(4,1)),Math.max(1,Math.round(spawnScale)),taken);
    const car=makeCaravan($("caravanType").value,linePath(sc(AF.hx(-5,0)),sc(AF.hx(5,0))),1);S.caravan=car;
    all.push(makeEnemy($("ally").value,0,randomNear(grid,sc(AF.hx(4,-1)),Math.max(1,Math.round(spawnScale)),taken)," Raider",lvAlly),car,makeEnemy($("enemy1").value,1,randomNear(grid,sc(AF.hx(-4,1)),spawnSpread,taken)," Guard",lv1),makeEnemy($("enemy2").value,1,randomNear(grid,sc(AF.hx(-4,-1)),spawnSpread,taken)," Guard II",lv2));
  }
  const avoid=all.map(f=>f.cell);if(S.caravan)avoid.push(...S.caravan.path);
  AF.generateTerrain(grid,avoid);S.B=new AF.Battle(all,grid);S.B.god=S.god;S.aiNoise=+$("difficulty").value;
  S.queue=[];S.moveTo=null;S.category="Ready";S.source="All";S.query="";S.mainTarget=null;S.targeting=null;S.lastKnown=new Map();$("abilitySearch").value="";
  const mapSizeName=Object.keys(MAP_SIZES).find(k=>MAP_SIZES[k]===mapRadius)||`radius ${mapRadius}`;
  log(`Scenario started: ${scenarioLabel(scenario)}. Level ${S.player.level} ${runtime.profile.phase}. ${mapSizeName} map.`,"sys");
  $("setup").classList.add("hidden");$("battle").classList.remove("hidden");fitArena();renderAll();
}
function scenarioLabel(v){
  if(v==="duel")return"1v1 duel";
  if(v==="onevx")return`1v${S.roster.opponents.length} gang battle`;
  if(v==="team")return`${1+S.roster.allies.length}v${S.roster.opponents.length} team battle`;
  if(v==="ffa")return`${1+S.roster.opponents.length}-way free-for-all`;
  if(v==="escort")return"caravan escort";
  return"caravan ambush";
}
function meter(label,v,max,cls=""){return`<div class="meter ${cls}"><span>${label}</span><div class="bar"><div class="fill" style="width:${Math.max(0,Math.min(100,v/Math.max(1,max)*100))}%"></div></div><b>${Math.round(v)} / ${Math.round(max)}</b></div>`;}
function fighterHud(f){
  if(f.isCaravan){const goal=Math.max(1,f.path.length-1),role=f.faction===S.player.faction?"escort":"target";return`<div class="fighter caravan ${role}"><h3><span>${f.glyph} ${f.name}</span><small>${role} · ${f.pathIndex}/${goal} to B${f.caravanAttack?" · armed":""}</small></h3><div class="meters">${meter("HP",f.hp,f.maxHp,"hp")}${meter("A → B",f.pathIndex,goal,"prog")}</div></div>`;}
  const stance=f.activeMartial?.styleKey||f.activeWeapon?.weaponKey||null;
  return`<div class="fighter ${f===S.player?"player":f.faction===S.player.faction?"ally":"enemy"}"><h3><span>${f.glyph} ${f.name}</span><small>${f===S.player?`L${f.level} · `:""}${f.sign}</small></h3><div class="meters">${meter("HP",f.hp,f.maxHp,"hp")}${meter("Stamina",f.stam,f.maxStam,"stam")}${meter("Chakra",f.chakra,f.maxChakra)}${meter("Poise",f.poise,f.maxPoise,"poise")}</div><div class="tags" style="margin-top:6px">${stance?`<span class="tag good">${stance} stance</span>`:""}${f.statuses.map(s=>`<span class="tag bad">${s.kind} ${s.rounds}</span>`).join("")}${f.eyeActive?`<span class="tag warn">${f.activeEye} eye · strain ${f.strain}</span>`:""}</div></div>`;
}
function renderHud(){$("hud").innerHTML=S.B.all.filter(AF.alive).map(fighterHud).join("");}
function reachable(){if(!S.B||AF.isRooted(S.player))return new Map();const mc=AF.moveBudget(S.player);return S.B.grid.reachable(S.player.cell,mc,c=>S.B.occupied(c,S.player)).cells;}
function aoeRadius(ab){return ab.tags.includes("Ultimate")?AF.BAL.ultimateAoeRadius:((ab.effects||[]).some(e=>e.k==="Terrain")?Math.max(1,Math.round(ab.radius)):AF.BAL.normalAoeRadiusCap);}
function projCell(){return S.moveTo?{...S.moveTo}:{...S.player.cell};}
function validPointPick(ab,cell){const from=projCell(),dist=AF.hdist(from,cell);if(ab.needsLoS&&!S.B.grid.los(from,cell))return false;return AF.evalRange(ab,dist).outcome!=="Impossible";}
function renderTargetBar(){const bar=$("targetBar");if(!bar)return;const seen=perceivedEnemies();
  if(!seen.length){bar.innerHTML='<span class="note">No visible enemies</span>';return;}
  bar.innerHTML=`<span class="note">Main target:</span> <b>${S.mainTarget?S.mainTarget.name:"—"}</b> <button class="secondary tgt-cycle" id="cycleTgt" title="Cycle main target through visible enemies">⟳</button>${S.targeting?' <button class="secondary tgt-cycle" id="cancelTgt" title="Cancel targeting">✕ aiming</button>':""}`;
  const cyc=$("cycleTgt");if(cyc)cyc.onclick=()=>{cycleMainTarget(1);renderAll();};
  const can=$("cancelTgt");if(can)can.onclick=()=>{exitTargeting();renderAll();};
}
function onCellClick(c,k,reach,pickable){
  if(S.targeting){const e=S.queue[S.targeting.index];if(!e){exitTargeting();renderAll();return;}
    if(S.targeting.mode==="enemy"){const foe=enemyAt(c);if(foe){e.target=foe;e.point=null;exitTargeting();renderAll();}}
    else if(S.targeting.mode==="ally"){const al=allyAt(c);if(al&&pickable){e.target=al;e.point=null;exitTargeting();renderAll();}}
    else if(pickable){e.point={...c};e.target=null;exitTargeting();renderAll();}
    return;}
  const foe=enemyAt(c);if(foe){S.mainTarget=foe;renderAll();return;}
  if(reach.has(k)){S.moveTo={...c};renderArena();renderQueue();}
}
function renderArena(){
  updateLastKnown();ensureMainTarget();
  const svg=$("arena"),reach=reachable(),aware=AF.DR.awareness(AF.eff(S.player));svg.innerHTML="";
  const tgt=S.targeting?S.queue[S.targeting.index]:null,tgtAb=tgt?tgt.ab:null;
  const radius=tgtAb&&wantsPoint(tgtAb)?aoeRadius(tgtAb):0;
  const previewCenter=(S.targeting&&S.targeting.mode==="point"&&S.hoverCell)?S.hoverCell:null;
  const mainCellK=(S.mainTarget&&AF.alive(S.mainTarget)&&S.B.perceives(S.player,S.mainTarget))?AF.hkey(S.mainTarget.cell):null;
  // Reach extent: outline the tiles a queued/aiming reach move can lunge into, from the player's current cell.
  const reachAbs=[];if(tgtAb&&tgtAb.reach>0)reachAbs.push(tgtAb);for(const e of S.queue)if(e.ab&&e.ab.reach>0)reachAbs.push(e.ab);
  const reachR=reachAbs.length?Math.max(...reachAbs.map(a=>a.reach||0)):0;
  for(const c of S.B.grid.cells()){
    const p=pointy(c.q,c.r),k=AF.hkey(c),t=S.B.grid.terrainAt(c),classes=["hex"];
    if(AF.hdist(S.player.cell,c)<=aware)classes.push("aware");
    if(reach.has(k)&&k!==AF.hkey(S.player.cell))classes.push("reachable");
    if(S.moveTo&&k===AF.hkey(S.moveTo))classes.push("selected");
    if(mainCellK===k)classes.push("main-target");
    let pickable=false;
    if(S.targeting){if(S.targeting.mode==="enemy"){if(enemyAt(c)){classes.push("target-pick");pickable=true;}}
      else if(S.targeting.mode==="ally"){const al=allyAt(c),from=S.moveTo||S.player.cell;if(al&&tgtAb&&AF.hdist(from,c)<=Math.max(1,tgtAb.maxR||1)){classes.push("ally-pick");pickable=true;}}
      else if(S.targeting.mode==="throw"){if(tgtAb&&validThrowPick(tgtAb,c)){classes.push("place-pick");pickable=true;}}
      else if(validPointPick(tgtAb,c)){classes.push("place-pick");pickable=true;}}
    if(previewCenter&&AF.hdist(previewCenter,c)<=radius)classes.push("aoe-preview");
    const g=document.createElementNS("http://www.w3.org/2000/svg","g");g.innerHTML=`<polygon class="${classes.join(" ")}" points="${poly(p.x,p.y)}"></polygon><text class="terrain" x="${p.x}" y="${p.y}">${TERRAIN_GLYPH[t]||""}</text>`;
    const pg=g.querySelector("polygon");
    g.addEventListener("mouseenter",()=>{if(S.targeting&&S.targeting.mode==="point"){if(!S.hoverCell||S.hoverCell.q!==c.q||S.hoverCell.r!==c.r){S.hoverCell={...c};renderArena();}}else showHover(c,pg);});
    g.addEventListener("mouseleave",()=>{if(!S.targeting)clearHover();});
    g.addEventListener("click",()=>onCellClick(c,k,reach,pickable));svg.appendChild(g);
  }
  if(reachR>0){const rc=S.moveTo?S.moveTo:S.player.cell,d=reachPerimeter(rc,reachR);if(d)svg.insertAdjacentHTML("beforeend",`<path class="reach-outline" d="${d}"></path>`);}
  const line=document.createElementNS("http://www.w3.org/2000/svg","line");line.id="hoverLine";line.classList.add("hoverline");line.style.display="none";svg.appendChild(line);
  if(S.moveTo){const a=pointy(S.player.cell.q,S.player.cell.r),m=pointy(S.moveTo.q,S.moveTo.r);svg.insertAdjacentHTML("beforeend",`<line class="moveline" x1="${a.x}" y1="${a.y}" x2="${m.x}" y2="${m.y}"></line><text class="token player move-preview" x="${m.x}" y="${m.y}">${S.player.glyph}</text>`);}
  if(S.lastKnown)for(const[f,cell]of S.lastKnown){if(f.faction===S.player.faction||!AF.alive(f)||S.B.perceives(S.player,f))continue;const gp=pointy(cell.q,cell.r);svg.insertAdjacentHTML("beforeend",`<text class="ghost-mark" x="${gp.x}" y="${gp.y}">?</text>`);}
  const viewer=AF.alive(S.player)?S.player:null;
  S.B.all.filter(AF.alive).forEach(f=>{const p=pointy(f.cell.q,f.cell.r),cls=f===S.player?"player":f.faction===S.player.faction?"ally":"enemy";svg.insertAdjacentHTML("beforeend",`<text class="token ${cls}${SPR&&SPR.handles(f)?" sprited":""}" x="${p.x}" y="${p.y}">${f.glyph}</text>`);if(!viewer||AFUI.canRenderFighter(S.B,viewer,f))svg.insertAdjacentHTML("beforeend",fighterIndicators(f,p));});
  if(mainCellK){const mc=pointy(S.mainTarget.cell.q,S.mainTarget.cell.r);svg.insertAdjacentHTML("beforeend",`<circle class="main-ring" cx="${mc.x}" cy="${mc.y}" r="${Math.round(ARENA.hexStep*0.65)}"></circle>`);}
  if(SPR)SPR.sync(S.B,S.player);
  renderTargetBar();
  $("moveReadout").textContent=S.targeting?`Aiming ${tgtAb.name} — click ${S.targeting.mode==="enemy"?"a visible enemy":S.targeting.mode==="ally"?"a friendly fighter":S.targeting.mode==="throw"?"a landing tile for the throw":"a highlighted tile"} (✕ in the target bar to cancel)`:(S.moveTo?`Planned ${AF.hdist(S.player.cell,S.moveTo)} hex move to ${S.moveTo.q},${S.moveTo.r}`:`Movement ${AF.moveBudget(S.player)} · Awareness ${aware}`);
}
let hoverPolygon=null;
function showHover(c,polygon){clearHover();hoverPolygon=polygon;polygon.classList.add("hover");const a=pointy(S.player.cell.q,S.player.cell.r),b=pointy(c.q,c.r),los=S.B.grid.los(S.player.cell,c),line=$("hoverLine");line.setAttribute("x1",a.x);line.setAttribute("y1",a.y);line.setAttribute("x2",b.x);line.setAttribute("y2",b.y);line.style.stroke=los?"var(--gold)":"var(--red)";line.style.display="block";$("moveReadout").textContent=`${c.q},${c.r} · ${AF.hdist(S.player.cell,c)} hex · ${S.B.grid.terrainAt(c)} · ${los?"clear LoS":"blocked LoS"}`;}
function clearHover(){if(hoverPolygon)hoverPolygon.classList.remove("hover");hoverPolygon=null;const line=$("hoverLine");if(line)line.style.display="none";}
function renderFocus(){
  $("focusAbilities").innerHTML=AFUI.focusAbilities(S.player.abilities).map(a=>abilityCard(a,true)).join("");
  bindAbilityButtons($("focusAbilities"));
}
function renderCategoryTabs(){
  const counts=AFUI.categoryCounts(S.player.abilities,S.player,qAbils());
  $("categoryTabs").innerHTML=AFUI.CATEGORIES.map(c=>`<button class="tab ${S.category===c?"active":""}" data-cat="${c}">${c}<span class="count">${counts[c]}</span></button>`).join("");
  $("categoryTabs").querySelectorAll("button").forEach(b=>b.onclick=()=>{S.category=b.dataset.cat;S.source="All";renderAbilityBrowser();});
}
function contextTags(){
  const c=AFUI.queueContext(S.player,qAbils()),tags=[];
  if(c.martial.size)tags.push(...[...c.martial].map(x=>`${x} martial ready`));
  if(c.weapon.size)tags.push(...[...c.weapon].map(x=>`${x} weapon ready`));
  if(c.eye)tags.push("eye ready");if(c.grapple)tags.push("grapple chain ready");if(c.mounted)tags.push("mount chain ready");
  $("abilityContext").innerHTML=tags.map(t=>`<span class="tag good">${t}</span>`).join("")||'<span class="note">Contextual children remain hidden until their parent state is active or earlier in the queue.</span>';
}
function renderAbilityBrowser(resetSource=true){
  renderFocus();renderCategoryTabs();contextTags();
  const sources=AFUI.sourcesFor(S.player.abilities,S.player,qAbils(),S.category);
  if(resetSource&& !sources.includes(S.source))S.source="All";
  $("sourceFilter").innerHTML=sources.map(s=>`<option ${s===S.source?"selected":""}>${s}</option>`).join("");
  const box=$("abilities");
  if(S.category==="Martial"){box.innerHTML=renderStylePanels("martial");bindAbilityButtons(box);return;}
  if(S.category==="Weapon"){box.innerHTML=renderStylePanels("weapon");bindAbilityButtons(box);return;}
  const rows=AFUI.visibleAbilities(S.player.abilities,S.player,qAbils(),{category:S.category,source:S.source,query:S.query,showLockedChildren:S.showLocked});
  const groups=AFUI.groupRows(rows,S.category);
  box.innerHTML=groups.length?groups.map(([name,list])=>`<section class="ability-section"><h4>${name}</h4><div class="ability-grid">${list.map(a=>abilityCard(a)).join("")}</div></section>`).join(""):'<div class="dependency-note">No abilities match this filter in the current context.</div>';
  bindAbilityButtons(box);
}
function renderStylePanels(type){
  const keys=type==="martial"?[...S.selectedMartials]:[$("weapon").value].filter(Boolean),isMartial=type==="martial";
  if(!keys.length)return`<div class="dependency-note">No ${type} training selected for this fighter.</div>`;
  const ctx=AFUI.queueContext(S.player,qAbils());
  return keys.filter(k=>S.source==="All"||S.source===k).map(k=>{
    const stance=S.player.abilities.find(a=>isMartial?a.isStyleStance&&a.styleKey===k:a.isWeaponStance&&a.weaponKey===k);
    if(!stance)return"";
    const children=S.player.abilities.filter(a=>isMartial?a.isStyleTechnique&&a.parentStyles?.includes(k):a.isWeaponTechnique&&a.parentWeapons?.includes(k));
    const ready=isMartial?ctx.martial.has(k):ctx.weapon.has(k),active=isMartial?S.player.activeMartial?.styleKey===k:S.player.activeWeapon?.weaponKey===k;
    const filteredChildren=children.filter(a=>AFUI.matches(a,S.query)&&(S.showLocked||AFUI.dependencyVisible(a,S.player,qAbils(),false)));
    const queryMatches=AFUI.matches(stance,S.query)||children.some(a=>AFUI.matches(a,S.query));
    if(S.query&&!queryMatches)return"";
    return`<div class="style-panel"><div class="style-head"><b>${k}</b><span class="style-state">${active?"ACTIVE":ready?"QUEUED / READY":"LOCKED BEHIND STANCE"}</span></div><div class="ability-grid">${abilityCard(stance)}${ready||S.showLocked?filteredChildren.map(a=>abilityCard(a)).join(""):""}</div>${!ready&&!S.showLocked?`<div class="dependency-note">Queue ${stance.name} to reveal ${children.length} ${type} techniques.</div>`:""}</div>`;
  }).join("")||'<div class="dependency-note">No styles match the current search.</div>';
}
// Compact positional badge: what this ability's relationship metadata allows.
function positionalBadge(a){
  const m=AF.posMeta(a);if(!m.audited&&!m.req)return"";
  const parts=[];
  if(m.req===AF.REQ.MOUNTING)parts.push("Mounting only");
  else if(m.req===AF.REQ.MOUNTED)parts.push("Mounted only");
  else if(m.req===AF.REQ.MOUNT)parts.push("Mounting or Mounted");
  else if(m.req===AF.REQ.GRAPPLING)parts.push("Grappling only");
  else if(m.req===AF.REQ.GRAPPLED)parts.push("Grappled only");
  else if(m.req===AF.REQ.STANDING)parts.push("Standing Grapple");
  else if(m.access===AF.MOUNT_ACCESS.BOTH)parts.push("Mount: both");
  else if(m.access===AF.MOUNT_ACCESS.MOUNTING_ONLY)parts.push("Mount: top only");
  else if(m.access===AF.MOUNT_ACCESS.MOUNTED_ONLY)parts.push("Mount: bottom only");
  else if(m.access===AF.MOUNT_ACCESS.NEITHER)parts.push("Not in Mount");
  if(m.submission)parts.push("Maintained Submission");
  if(m.escape){const t=AF.submissionEscapeTurns(S.player);parts.push(t>0?`Escape DC −${AF.submissionEscapeResistance(S.player)} (held ${t}rd)`:"Contested escape");}
  if(m.positionalDc)parts.push("Positional DC");
  if(!parts.length)return"";
  return`<span class="cost" title="Positional Rules (canonical)">${parts.join(" · ")}</span>`;
}
function abilityCard(a,compact=false){
  const reason=AFUI.lockReason(a,S.player,qAbils());
  // A submission being continued is quoted at its escalated price, not its face cost.
  const subMult=AF.submissionCostMult(AF.continuedSubmission(S.player,a));
  const pctS=a.stamPct?Math.round(a.stamPct*S.player.maxStam):0,pctC=a.chakraPct?Math.round(a.chakraPct*AF.effMaxChakra(S.player)):0;
  const costS=Math.round((a.stam+pctS)*AF.costMult(a)*subMult),costC=Math.round((a.chakra+pctC)*AF.costMult(a)*subMult);
  const elem=a.kitSign?(AF.ELEM[a.kitSign]||"").toLowerCase():"";
  const alvl=(S.career&&S.progress)?AFUI.abilityLevelFromXp(S.progress.abilityXp[AF.abilityKey(a)]||0):0;
  return`<button class="ability" data-id="${a.id}" ${reason?"disabled":""}><span class="name">${a.name}${alvl>0?` <span class="lvl">L${alvl}</span>`:""}</span><span class="source${elem?" elem-"+elem:""}">${AFUI.sourceLabel(a)}</span><span class="desc">${AFUI.abilitySummary(a)}</span><span class="costs"><span class="cost">${a.slots}◆</span>${costS?`<span class="cost stam" title="Stamina">${costS}</span>`:""}${costC?`<span class="cost chakra" title="Chakra">${costC}</span>`:""}${a.supply?`<span class="cost">Supply ${a.supply}</span>`:""}${a.reach?`<span class="cost reach" title="Gap-closer: lunges to melee if the target is within ${a.reach} tiles">↝${a.reach}</span>`:""}${a.tags.slice(0,2).map(t=>`<span class="cost">${t}</span>`).join("")}${a.poiseMult>1?`<span class="cost guard" title="Guard break — deals ${a.poiseMult}× poise damage">⛊ ${a.poiseMult}x Poise Dmg</span>`:""}${positionalBadge(a)}</span>${reason?`<span class="locked">${reason}</span>`:""}</button>`;
}
function bindAbilityButtons(root){root.querySelectorAll("button.ability").forEach(b=>b.onclick=()=>{const a=S.player.abilities.find(x=>x.id===b.dataset.id);if(a)queueAbility(a);});}
function queueAbility(a){const reason=AFUI.lockReason(a,S.player,qAbils());if(reason){showBattleError(reason);return;}S.queue.push({ab:a,target:null,point:null});if(canTarget(a))enterTargeting(S.queue.length-1);else exitTargeting();renderQueue();renderAbilityBrowser();renderArena();}
function sanitizeWrappers(){const kept=[],keptAb=[],dropped=[];for(const e of S.queue){if(AFUI.dependencyReason(e.ab,S.player,keptAb))dropped.push(e.ab);else{kept.push(e);keptAb.push(e.ab);}}S.queue=kept;return dropped;}
/* Relationship readout: the player must be able to tell Grappling / Grappled /
   Mounting / Mounted apart, see any Maintained Submission, and release explicitly. */
function renderRelationship(){
  const el=$("relationshipPanel");if(!el||!S.player)return;
  const info=AFUI.relationshipLabel(S.player);
  if(info.role===AF.REL.FREE){el.className="relationship";el.innerHTML="";return;}
  const notes=[];
  if(AF.isMountRole(info.role))notes.push(`Mount upkeep ${AF.BAL.mountUpkeepStamina} Stamina at Relationship Maintenance.`);
  else notes.push(`Standing hold upkeep ${AF.BAL.grappleHoldUpkeepStamina} Stamina at Relationship Maintenance.`);
  if(info.role===AF.REL.GRAPPLING)notes.push(`+1 positional Priority against ${info.partner.name}.`);
  notes.push(`Passive Stamina recovery ${Math.round(AF.passiveStaminaFactor(info.role)*100)}%.`);
  notes.push("No voluntary movement or teleport while engaged.");
  const sub=info.submission;
  const mounting=AF.isMountRole(info.role);
  const controlling=info.role===AF.REL.GRAPPLING||info.role===AF.REL.MOUNTING;
  const mountLocked=mounting&&!!sub;
  el.className="relationship on";
  el.innerHTML=`<span class="rel-role rel-${info.role}">${info.role}</span> — ${info.partner.name}`+
    (sub?`<span class="rel-sub">Maintained Submission: ${sub.name} (held by ${sub.holder})`+
        (sub.holding
          ? ` · <b>queue ${sub.name} again this round or the hold is released</b>`+
            (sub.consecutive?` · round ${sub.consecutive+1} of the hold`:"")+
            ` · next application ×${sub.costMult.toFixed(1)} cost, ×${sub.damageMult.toFixed(1)} damage`
          : ` · ${sub.holder} must keep working it or it lapses`)+
        (sub.escapeTurns>0?`<span class="rel-note">Locked in ${sub.escapeTurns} turn${sub.escapeTurns>1?"s":""} — contested escapes are at −${sub.escapeResistance} DC and get harder every turn it holds.</span>`:"")+
        `</span>`:"")+
    `<span class="rel-note">${notes.join(" ")}</span>`+
    (controlling
      ? (mountLocked
          ? `<span class="rel-note">Mount cannot be given up while a submission is actively held.</span>`
          : `<button type="button" class="secondary rel-release" id="relRelease">${S.player.releaseIntent?"Releasing at maintenance ✓":`Release ${mounting?"mount":"hold"} at maintenance`}</button>`)
      : "");
  const btn=$("relRelease");
  if(btn)btn.onclick=()=>{S.player.releaseIntent=!S.player.releaseIntent;renderRelationship();};
}
function renderQueue(){
  $("queue").innerHTML=S.queue.length?S.queue.map((e,i)=>{const a=e.ab,aiming=S.targeting&&S.targeting.index===i;const tctrl=canTarget(a)?`<button class="tgt-btn${e.target||e.point?" set":""}" data-tgt="${i}" title="Set / change target">${targetLabelFor(e)}</button>`:`<small class="note" style="display:block">${targetLabelFor(e)}</small>`;return`<div class="queued${aiming?" aiming":""}"><b>${i+1}</b><span><b>${a.name}</b><small class="note" style="display:block">${AFUI.sourceLabel(a)} · ${a.slots} slot${a.slots===1?"":"s"}</small>${tctrl}</span><span class="queue-tools"><button data-up="${i}" title="Move up">↑</button><button data-down="${i}" title="Move down">↓</button><button data-remove="${i}" title="Remove">×</button></span></div>`;}).join(""):'<div class="note">Queue actions, or select a movement cell and resolve a movement-only round.</div>';
  $("queue").querySelectorAll("[data-remove]").forEach(b=>b.onclick=()=>removeQueue(+b.dataset.remove));
  $("queue").querySelectorAll("[data-up]").forEach(b=>b.onclick=()=>moveQueue(+b.dataset.up,-1));
  $("queue").querySelectorAll("[data-down]").forEach(b=>b.onclick=()=>moveQueue(+b.dataset.down,1));
  $("queue").querySelectorAll("[data-tgt]").forEach(b=>b.onclick=()=>{enterTargeting(+b.dataset.tgt);renderQueue();renderArena();});
  renderRelationship();
  const cap=AF.availableSlots(S.player);
  const p=AFUI.projectedCosts(qAbils(),S.player);
  $("slots").textContent=`${p.slots} / ${cap}`;$("queueCosts").textContent=`S ${p.stam} · C ${p.chakra} · Supplies ${p.supplies}`;
  $("resolve").disabled=!S.queue.length&&!S.moveTo;
}
function removeQueue(i){S.queue.splice(i,1);const dropped=sanitizeWrappers();if(dropped.length)showBattleError(`Removed dependent actions: ${dropped.map(x=>x.name).join(", ")}`);if(S.targeting&&S.targeting.index>=S.queue.length)exitTargeting();renderQueue();renderAbilityBrowser();renderArena();}
function moveQueue(i,d){const j=i+d;if(j<0||j>=S.queue.length)return;[S.queue[i],S.queue[j]]=[S.queue[j],S.queue[i]];const invalid=AFUI.validateQueue(S.player,qAbils());if(invalid.length){[S.queue[i],S.queue[j]]=[S.queue[j],S.queue[i]];showBattleError(`${invalid[0].ability.name}: ${invalid[0].reason}`);}exitTargeting();renderQueue();renderAbilityBrowser();renderArena();}
function showBattleError(t){$("battleError").textContent=t;setTimeout(()=>{if($("battleError").textContent===t)$("battleError").textContent="";},3500);}
function renderLog(){$("log").innerHTML=S.B.log.map(x=>x.calc?`<details class="calc ${x.cls||""}"><summary>${x.text}</summary><div class="calc-detail">${x.calc}</div></details>`:`<div class="${x.cls||""}">${x.text}</div>`).join("");$("log").scrollTop=$("log").scrollHeight;}
function log(t,cls){if(S.B)S.B.line(t,cls);}
function copyLog(){
  if(!S.B)return;
  const text=S.B.log.map(x=>x.text.replace(/<[^>]*>/g,"")).join("\n");
  const btn=$("copyLog"),label=btn.textContent,flash=ok=>{btn.textContent=ok?"Copied!":"Press Ctrl+C";setTimeout(()=>{btn.textContent=label;},1600);};
  const fallback=()=>{try{const ta=document.createElement("textarea");ta.value=text;ta.setAttribute("readonly","");ta.style.position="fixed";ta.style.top="-1000px";ta.style.opacity="0";document.body.appendChild(ta);ta.focus();ta.select();const ok=document.execCommand("copy");document.body.removeChild(ta);flash(ok);}catch(e){flash(false);}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(()=>flash(true)).catch(fallback);else fallback();
}
function renderResultXp(sum){
  const el=$("resultXp");if(!el)return;
  if(!S.career||!sum){el.classList.add("hidden");el.innerHTML="";return;}
  el.classList.remove("hidden");
  if(!sum.committed){el.innerHTML='<div class="note">No XP earned — god mode / force-unlock battle.</div>';return;}
  const rows=Object.entries(sum.abilityGains).map(([k,g])=>({n:k.split("|")[1],xp:g.xp,lv:g.levelAfter,up:g.levelAfter>g.levelBefore})).sort((a,b)=>b.xp-a.xp);
  el.innerHTML=`<div class="note" style="text-align:left"><b>Character XP +${sum.charGain}</b> — usage +${sum.charFromOutput}, participation +${sum.charFromParticipation}${sum.charFromWin?`, victory +${sum.charFromWin}`:` (no victory bonus)`}${sum.levelAfter>sum.levelBefore?` · <b class="hl">Character Level ${sum.levelBefore} → ${sum.levelAfter}!</b>`:""}</div>
  <div class="note" style="text-align:left;margin-top:6px">Ability XP from use this battle:</div>
  <div class="xp-list">${rows.length?rows.map(r=>`<div class="xp-row"><span>${r.n}${r.up?' <span class="hl">▲ leveled</span>':""}</span><span>+${r.xp} XP · L${r.lv}</span></div>`).join(""):'<div class="note">No abilities were used offensively this battle.</div>'}</div>`;
}
function renderAll(){renderHud();renderArena();renderQueue();renderAbilityBrowser();renderLog();$("round").textContent=S.B.round;}
function resolveRound(){
  $("battleError").textContent="";if(!S.queue.length&&!S.moveTo){showBattleError("Queue an action or select a movement cell.");return;}
  const invalid=AFUI.validateQueue(S.player,qAbils());if(invalid.length){showBattleError(`${invalid[0].ability.name}: ${invalid[0].reason}`);return;}
  try{
    const plans=[{owner:S.player,actions:planActions(),moveTo:S.moveTo?{...S.moveTo}:null}];
    for(const f of S.B.all)if(f!==S.player&&AF.alive(f)&&!f.isCaravan)plans.push(AF.planFor(S.B,f,S.aiNoise));
    if(SPR)SPR.beginRound();
    AF.resolveRound(S.B,plans);S.B.round++;
    if(isCaravanScenario()&&S.caravan&&AF.alive(S.caravan))AF.stepCaravan(S.B,S.caravan);
    S.queue=[];S.moveTo=null;exitTargeting();
    let o=currentOutcome();
    let replay=null;
    if(!o&&!AF.alive(S.player)){log("You were downed — auto-resolving the remaining battle…","sys");if(SPR)SPR.cancel();autoResolveDowned();o=currentOutcome()||fallbackOutcome();}
    renderAll();
    if(SPR)replay=SPR.playRound(S.B);
    // the result card waits for the replay, so the deciding blow is seen before it covers the arena
    // then the whole fight plays back round by round before the result card
    if(o)Promise.resolve(replay).then(()=>SPR&&SPR.animateOn()?playRecap():null).then(()=>finishBattle(o.won,o.title,o.text));
  }catch(e){console.error(e);showBattleError(e.message||String(e));}
}
// Outcome, unified across scenarios. Returns {won,title,text} or null if undecided.
function currentOutcome(){
  if(isCaravanScenario()){const o=escortOutcome();if(!o)return null;const amb=S.scenario==="ambush";
    return{won:o.won,title:o.won?(amb?"Ambush Success":"Escort Success"):(amb?"Ambush Failed":"Escort Failed"),text:o.reason};}
  if(S.B.decided()){const alive=S.B.all.filter(AF.alive),won=alive.some(f=>f.faction===S.player.faction);return{won,title:won?"Victory":"Defeat",text:`${alive.map(f=>f.name).join(", ")||"No one"} survived after ${S.B.round-1} rounds.`};}
  return null;
}
function fallbackOutcome(){const won=S.B.all.some(f=>f.faction===S.player.faction&&!f.isCaravan&&AF.alive(f));return{won,title:won?"Victory":"Defeat",text:`Battle auto-resolved after ${S.B.round-1} rounds.`};}
// Player is down: hand every remaining fighter to the AI and play out the fight until it's decided.
function autoResolveDowned(){
  while(!currentOutcome()){
    const plans=[];
    for(const f of S.B.all)if(AF.alive(f)&&!f.isCaravan)plans.push(AF.planFor(S.B,f,S.aiNoise));
    AF.resolveRound(S.B,plans);S.B.round++;
    if(isCaravanScenario()&&S.caravan&&AF.alive(S.caravan))AF.stepCaravan(S.B,S.caravan);
  }
}
function escortOutcome(){
  const car=S.caravan;if(!car)return null;
  const def=car.faction; // the side protecting the caravan (escort=player's 0, ambush=enemy's 1)
  const playerDefends=S.player.faction===def;
  const defend=r=>({won:playerDefends,reason:r}),attack=r=>({won:!playerDefends,reason:r});
  if(!AF.alive(car))return attack(`${car.name} was destroyed.`);
  if(car.pathIndex>=car.path.length-1)return defend(`${car.name} reached the destination.`);
  if(!S.B.all.some(f=>f.faction!==def&&!f.isCaravan&&AF.alive(f)))return defend("All attackers eliminated — the caravan is safe.");
  if(!S.B.all.some(f=>f.faction===def&&!f.isCaravan&&AF.alive(f)))return attack("All guards fell — the caravan is overrun.");
  return null;
}
// post-fight recap: every round replayed in order on the sprite layer; the SVG tokens (which show the end of the fight) are hidden meanwhile
function playRecap(){
  if(!SPR||!S.B)return Promise.resolve(false);
  $("resolve").disabled=true;
  return SPR.playRecap(S.B,S.player).finally(()=>{$("resolve").disabled=false;});
}
function showRecapProgress(p){
  const wrap=document.querySelector(".arena-wrap");if(wrap)wrap.classList.toggle("recapping",!!p);
  $("recapBar").classList.toggle("hidden",!p);
  if(p)$("recapRound").textContent=`${p.recording?"Recording · ":""}Round ${p.round} · ${p.index} of ${p.total}`;
}
function watchRecap(){$("resultOverlay").classList.add("hidden");playRecap().then(()=>$("resultOverlay").classList.remove("hidden"));}
// Recap export (user, 2026-10-15): the recap plays while it is recorded, then the result card offers the files.
function recordRecap(){
  if(!SPR||!S.B)return;
  $("resultOverlay").classList.add("hidden");$("resolve").disabled=true;
  SPR.recordRecap(S.B,S.player).then(out=>{S.recording=out;renderRecording();}).finally(()=>{$("resolve").disabled=false;$("resultOverlay").classList.remove("hidden");});
}
const kb=b=>b.size>=1048576?`${(b.size/1048576).toFixed(1)} MB`:`${Math.max(1,Math.round(b.size/1024))} KB`;
function renderRecording(){
  const el=$("recordOut"),o=S.recording;if(!el)return;
  if(!o||(!o.video&&!o.gif)){el.className="record-out note";el.textContent=o?"Nothing was recorded.":"";return;}
  el.className="record-out";
  el.innerHTML=`${o.complete?"":'<div class="note">Recording stopped early; the files hold what played.</div>'}<div class="actions" style="justify-content:center">`
    +(o.video?`<button class="secondary" id="saveVideo" type="button">Save video (.${o.video.ext}, ${kb(o.video.blob)})</button>`:"")
    +(o.gif?`<button class="secondary" id="saveGif" type="button">Save GIF (${kb(o.gif)})</button>`:"")+`</div><div class="note" id="saveNote"></div>`;
  const stamp=new Date().toISOString().slice(0,16).replace(/[:T]/g,"-");
  const bind=(id,name,blob)=>{const b=$(id);if(b)b.onclick=()=>saveBlob(name,blob).then(msg=>{$("saveNote").textContent=msg;});};
  if(o.video)bind("saveVideo",`astro-fighters-recap-${stamp}.${o.video.ext}`,o.video.blob);
  if(o.gif)bind("saveGif",`astro-fighters-recap-${stamp}.gif`,o.gif);
}
// saves through the Artifact host's downloads capability when it is there, else a plain browser download
async function saveBlob(name,blob){
  const host=window.claude&&typeof window.claude.use==="function"?await window.claude.use("downloads").catch(()=>null):null;
  if(host){
    try{await host.save({filename:name,data:blob});return`Saved ${name}.`;}
    catch(e){if(e&&e.code==="declined")return"Save cancelled.";if(e&&e.code==="rate_limited")return"A save prompt is already open.";if(e&&e.code&&!["unavailable","not_granted","capability_disabled","capability_removed"].includes(e.code))return`Could not save: ${e.message||e.code}`;}
  }
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},5000);return`Downloading ${name}.`;
}
function finishBattle(won,title,text){
  $("resultTitle").textContent=title;
  let sum=null;
  if(S.career){sum=AFUI.commitProgress(S.B,S.progress,{god:S.god,won});saveCareer();renderCareerPanel();}
  $("resultText").textContent=text;renderResultXp(sum);const canRecap=!!(SPR&&SPR.ready&&S.B.history&&S.B.history.length);$("watchRecap").classList.toggle("hidden",!canRecap);$("recordRecap").classList.toggle("hidden",!canRecap);S.recording=null;renderRecording();$("resultOverlay").classList.remove("hidden");
}
function restoreRoster(){for(const f of S.B.all){f.hp=f.maxHp;f.stam=f.maxStam;f.chakra=AF.effMaxChakra(f);f.poise=f.maxPoise;}log("Roster restored by debug console.","sys");renderAll();}
function regenerateTerrain(){AF.generateTerrain(S.B.grid,S.B.all.filter(AF.alive).map(f=>f.cell));S.moveTo=null;log("Terrain regenerated.","sys");renderAll();}
function bindBalance(){
  const rows=[["bHit","vHit","baseHitChance",0],["bDmg","vDmg","damageScale",2],["bECost","vECost","elementalCostMult",2],["bEDmg","vEDmg","elementalDamageMult",2],["bFF","vFF","aoeFriendlyFireMultiplier",2]];
  for(const [id,val,key,d] of rows){$(id).value=AF.BAL[key];const apply=()=>{AF.BAL[key]=+$(id).value;$(val).textContent=Number(AF.BAL[key]).toFixed(d);};$(id).oninput=apply;apply();}
}
window.addEventListener("DOMContentLoaded",init);
})();