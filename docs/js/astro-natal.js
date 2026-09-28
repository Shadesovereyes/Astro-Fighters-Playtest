/* Astro Fighters browser natal chart engine.
   Ported from Assets/AstroFighters/Astrology/{AstroTime,SimpleEphemeris,PlanetEphemeris,ChartMath}.cs.
   The analytic planet model is the project's existing fallback (approx. 1800-2050). */
const AF_ASTRO = (()=>{
  const PI=Math.PI,D2R=PI/180,R2D=180/PI,J2000=2451545.0;
  const SIGNS=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"];
  const ELEMENTS={Aries:"Fire",Taurus:"Earth",Gemini:"Air",Cancer:"Water",Leo:"Fire",Virgo:"Earth",Libra:"Air",Scorpio:"Water",Sagittarius:"Fire",Capricorn:"Earth",Aquarius:"Air",Pisces:"Water"};
  const NAKSHATRAS=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"];
  const PADA_NAMES=["Dharma","Artha","Kama","Moksha"];
  const norm360=d=>((d%360)+360)%360;
  const normSigned=d=>{d=norm360(d);return d>180?d-360:d;};
  const centuries=jd=>(jd-J2000)/36525;
  function julianDay(date){
    const u=date instanceof Date?date:new Date(date);let y=u.getUTCFullYear(),m=u.getUTCMonth()+1;
    const day=u.getUTCDate()+(u.getUTCHours()+(u.getUTCMinutes()+(u.getUTCSeconds()+u.getUTCMilliseconds()/1000)/60)/60)/24;
    if(m<=2){y--;m+=12;}const a=Math.floor(y/100),b=2-a+Math.floor(a/4);
    return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+day+b-1524.5;
  }
  function gmstDegrees(jd){const t=centuries(jd);return norm360(280.46061837+360.98564736629*(jd-J2000)+0.000387933*t*t-t*t*t/38710000);}
  function obliquityDegrees(jd){const t=centuries(jd),sec=21.448-t*(46.8150+t*(0.00059-t*0.001813));return 23+26/60+sec/3600;}
  const Earth={a:1.00000261,aDot:.00000562,e:.01671123,eDot:-.00004392,I:-.00001531,IDot:-.01294668,L:100.46457166,LDot:35999.37244981,w:102.93768193,wDot:.32327364,om:0,omDot:0};
  const PE={
    Mercury:{a:.38709927,aDot:.00000037,e:.20563593,eDot:.00001906,I:7.00497902,IDot:-.00594749,L:252.25032350,LDot:149472.67411175,w:77.45779628,wDot:.16047689,om:48.33076593,omDot:-.12534081},
    Venus:{a:.72333566,aDot:.00000390,e:.00677672,eDot:-.00004107,I:3.39467605,IDot:-.00078890,L:181.97909950,LDot:58517.81538729,w:131.60246718,wDot:.00268329,om:76.67984255,omDot:-.27769418},
    Mars:{a:1.52371034,aDot:.00001847,e:.09339410,eDot:.00007882,I:1.84969142,IDot:-.00813131,L:-4.55343205,LDot:19140.30268499,w:-23.94362959,wDot:.44441088,om:49.55953891,omDot:-.29257343},
    Jupiter:{a:5.20288700,aDot:-.00011607,e:.04838624,eDot:-.00013253,I:1.30439695,IDot:-.00183714,L:34.39644051,LDot:3034.74612775,w:14.72847983,wDot:.21252668,om:100.47390909,omDot:.20469106},
    Saturn:{a:9.53667594,aDot:-.00125060,e:.05386179,eDot:-.00050991,I:2.48599187,IDot:.00193609,L:49.95424423,LDot:1222.49362201,w:92.59887831,wDot:-.41897216,om:113.66242448,omDot:-.28867794},
    Uranus:{a:19.18916464,aDot:-.00196176,e:.04725744,eDot:-.00004397,I:.77263783,IDot:-.00242939,L:313.23810451,LDot:428.48202785,w:170.95427630,wDot:.40805281,om:74.01692503,omDot:.04240589},
    Neptune:{a:30.06992276,aDot:.00026291,e:.00859048,eDot:.00005105,I:1.77004347,IDot:.00035372,L:-55.12002969,LDot:218.45945325,w:44.96476227,wDot:-.32241464,om:131.78422574,omDot:-.00508664},
    Pluto:{a:39.48211675,aDot:-.00031596,e:.24882730,eDot:.00005170,I:17.14001206,IDot:.00004818,L:238.92903833,LDot:145.20780515,w:224.06891629,wDot:-.04062942,om:110.30393684,omDot:-.01183482}
  };
  function solveKepler(m,e){let ecc=m+e*Math.sin(m);for(let i=0;i<12;i++){const dM=m-(ecc-e*Math.sin(ecc)),dE=dM/(1-e*Math.cos(ecc));ecc+=dE;if(Math.abs(dE)<1e-9)break;}return ecc;}
  function heliocentric(el,t){
    const a=el.a+el.aDot*t,e=el.e+el.eDot*t,I=(el.I+el.IDot*t)*D2R,L=el.L+el.LDot*t,wbar=el.w+el.wDot*t,om=(el.om+el.omDot*t)*D2R;
    const arg=(wbar-el.om-el.omDot*t)*D2R,m=normSigned(L-wbar)*D2R,E=solveKepler(m,e),xp=a*(Math.cos(E)-e),yp=a*Math.sqrt(1-e*e)*Math.sin(E);
    const cw=Math.cos(arg),sw=Math.sin(arg),co=Math.cos(om),so=Math.sin(om),ci=Math.cos(I),si=Math.sin(I);
    return {x:(cw*co-sw*so*ci)*xp+(-sw*co-cw*so*ci)*yp,y:(cw*so+sw*co*ci)*xp+(-sw*so+cw*co*ci)*yp,z:(sw*si)*xp+(cw*si)*yp};
  }
  function planetLongitude(p,jd){const t=centuries(jd),a=heliocentric(PE[p],t),e=heliocentric(Earth,t);return norm360(Math.atan2(a.y-e.y,a.x-e.x)*R2D);}
  function sunLongitude(jd){const t=centuries(jd),l0=280.46646+36000.76983*t+.0003032*t*t,m=(357.52911+35999.05029*t-.0001537*t*t)*D2R,c=(1.914602-.004817*t-.000014*t*t)*Math.sin(m)+(.019993-.000101*t)*Math.sin(2*m)+.000289*Math.sin(3*m);return norm360(l0+c);}
  const MOON_TERMS=[[0,0,1,0,6288774],[2,0,-1,0,1274027],[2,0,0,0,658314],[0,0,2,0,213618],[0,1,0,0,-185116],[0,0,0,2,-114332],[2,0,-2,0,58793],[2,-1,-1,0,57066],[2,0,1,0,53322],[2,-1,0,0,45758],[0,1,-1,0,-40923],[1,0,0,0,-34720],[0,1,1,0,-30383],[2,0,0,-2,15327],[0,0,1,2,-12528],[0,0,1,-2,10980],[4,0,-1,0,10675],[0,0,3,0,10034],[4,0,-2,0,8548],[2,1,-1,0,-7888],[2,1,0,0,-6766],[1,0,-1,0,-5163],[1,1,0,0,4987],[2,-1,1,0,4036],[2,0,2,0,3994],[4,0,0,0,3861],[2,0,-3,0,3665]];
  function moonLongitude(jd){
    const t=centuries(jd),lp=218.3164477+481267.88123421*t-.0015786*t*t+t*t*t/538841-t*t*t*t/65194000,d=297.8501921+445267.1114034*t-.0018819*t*t+t*t*t/545868-t*t*t*t/113065000,m=357.5291092+35999.0502909*t-.0001536*t*t+t*t*t/24490000,mp=134.9633964+477198.8675055*t+.0087414*t*t+t*t*t/69699-t*t*t*t/14712000,f=93.2720950+483202.0175233*t-.0036539*t*t-t*t*t/3526000+t*t*t*t/863310000,e=1-.002516*t-.0000074*t*t;
    let sum=0;for(const row of MOON_TERMS){const arg=(row[0]*d+row[1]*m+row[2]*mp+row[3]*f)*D2R,mm=Math.abs(row[1]),ef=mm===1?e:mm===2?e*e:1;sum+=row[4]*ef*Math.sin(arg);}return norm360(lp+sum/1e6);
  }
  function ascendant(jd,lat,lon){const ramc=norm360(gmstDegrees(jd)+lon)*D2R,eps=obliquityDegrees(jd)*D2R,phi=lat*D2R,asc=Math.atan2(Math.cos(ramc),-(Math.sin(ramc)*Math.cos(eps)+Math.tan(phi)*Math.sin(eps)));return norm360(asc*R2D);}
  function northNode(jd){const t=centuries(jd);return norm360(125.0445479-1934.1362891*t+.0020754*t*t+t*t*t/467441-t*t*t*t/60616000);}
  function isRetrograde(p,jd){if(p==="Sun"||p==="Moon")return false;return normSigned(planetLongitude(p,jd+1)-planetLongitude(p,jd))<0;}
  function placement(lon){lon=norm360(lon);const sign=SIGNS[Math.floor(lon/30)%12],deg=lon%30,nak=Math.floor(lon/(13+20/60))%27,intoNak=lon%(13+20/60),pada=Math.floor(intoNak/(3+20/60))%4;return {longitude:lon,sign,element:ELEMENTS[sign],degree:deg,decan:Math.floor(deg/10),dwad:Math.floor(deg/2.5),subDwad:Math.floor((deg%2.5)/.2),nakshatraIndex:nak,nakshatra:NAKSHATRAS[nak],pada,padaName:PADA_NAMES[pada]};}
  function buildChart(utcDate,lat,lon,meta={}){
    const jd=julianDay(utcDate),planetNames=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"],planets={};
    for(const p of planetNames){const long=p==="Sun"?sunLongitude(jd):p==="Moon"?moonLongitude(jd):planetLongitude(p,jd);planets[p]={...placement(long),retrograde:isRetrograde(p,jd)};}
    const asc=placement(ascendant(jd,lat,lon)),node=placement(northNode(jd));
    return {birthUtc:new Date(utcDate).toISOString(),latitude:Number(lat),longitude:Number(lon),placeName:meta.placeName||"",timeZone:meta.timeZone||"UTC",planets,Ascendant:asc,NorthNode:node};
  }
  function partsAt(ms,tz){const fmt=new Intl.DateTimeFormat("en-US",{timeZone:tz,year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",hourCycle:"h23"});const out={};for(const p of fmt.formatToParts(new Date(ms)))if(p.type!=="literal")out[p.type]=Number(p.value);return out;}
  function zonedLocalToUtc(dateStr,timeStr,timeZone){
    const [y,m,d]=dateStr.split("-").map(Number),[hh,mm]=timeStr.split(":").map(Number);const desired=Date.UTC(y,m-1,d,hh,mm,0);let guess=desired;
    for(let i=0;i<4;i++){const p=partsAt(guess,timeZone),shown=Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute,p.second||0);guess+=desired-shown;}
    return new Date(guess);
  }
  async function searchPlaces(query){
    const q=String(query||"").trim();if(q.length<2)return[];
    const url=`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(q)}&count=8&language=en&format=json`;
    const res=await fetch(url,{headers:{Accept:"application/json"}});if(!res.ok)throw new Error(`Birthplace search failed (${res.status})`);const d=await res.json();
    return (d.results||[]).map(x=>({name:x.name,admin1:x.admin1||"",country:x.country||"",latitude:x.latitude,longitude:x.longitude,timezone:x.timezone||"UTC",label:[x.name,x.admin1,x.country].filter(Boolean).join(", ")}));
  }
  return {SIGNS,ELEMENTS,NAKSHATRAS,PADA_NAMES,norm360,julianDay,placement,buildChart,zonedLocalToUtc,searchPlaces,sunLongitude,moonLongitude,planetLongitude};
})();

  
