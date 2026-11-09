"""S/N v1 of the Kyoketsu-Shoge Stance entry (Christopher 2026-11-09 17:43: E/W v3 approved). tanto.py's S/N projection from
the oneHandGuard frontal (as Viper Strike / Machete Slash), then the sickle poses: frame 0 stowed (not drawn); drawn, the
chain hangs free with the ring swinging; the last two frames take the chain into the far hand as the stance idle's S/N
(oneHandGuard itemPoses kyoketsu-shoge-sickle, from the approved kama idle). N: the sickle is hidden in front of the body,
only the chain shows on the guard frames. E/W pixels and weapon rows restored from HEAD.
Run: python3 tools/ks_entry_sn.py"""
import sys, os, json, subprocess, io, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]; sys.argv = sys.argv[:1]
import standin_weapons as SW, tanto as T
from PIL import Image
R, D = T.R, T.D; ST = 'ksStanceEntry'
STAT = 'E/W approved by user 2026-11-09 17:43 (v3 base-tier sickle, chain and ring; W mirrors E); S/N v1 CANDIDATE 2026-11-09'
sh = lambda *c: subprocess.run(c, cwd=R, check=True, capture_output=True)
T.sn(ST)
s = T.load(D + ST + '.json'); w = T.mainw(s); E = w['E']
IDLE = T.load(D + 'oneHandGuard.json')['weapons'][0]['itemPoses']['kyoketsu-shoge-sickle']
for k in range(s['frames']):
    pS, pN = w['S'][k], w['N'][k]
    if k == 0: pS['omit'] = pN['omit'] = True; pS['chain'] = pN['chain'] = {'off': True}; continue
    ch = E[k].get('chain', {})
    if 'via' in ch:   # the guard frames: the idle's S/N pose and chain, on this frame's fist
        iS, iN = IDLE['S'][0], IDLE['N'][0]
        pS.update({kk: copy.deepcopy(v) for kk, v in iS.items() if kk not in ('chain',)})
        pS['chain'] = {**iS['chain'], 'via': [pS['grip'][0] + 12, pS['grip'][1] - 10], 'to': ch['to']}
        pN.update({kk: copy.deepcopy(v) for kk, v in iN.items() if kk not in ('chain',)}); pN.pop('hidden', None); pN['hidden'] = True
        pN['chain'] = {**iN['chain'], 'to': ch['to']}
    else:
        pS['chain'] = {'to': ch.get('to', [0, 12])}
        pN['omit'] = True; pN['chain'] = {'off': True}
s['status'] = STAT
for ww in s['weapons']: ww['status'] = STAT
T.save(s, D + ST + '.json')
sh('node', 'tools/character-posed.mjs', 'male', ST); sh('python3', 'tools/stances.py', '--outline', ST)
T.restore(ST); sh('node', 'tools/character-weapon.mjs', 'male', ST)
d = D + ST + '/'
for f in sorted(os.listdir(d)):
    if not (f.startswith('main-') or f == 'fx.png'): continue
    try: old = Image.open(io.BytesIO(subprocess.check_output(['git', '-C', R, 'show', 'HEAD:' + os.path.relpath(d + f, R)], stderr=subprocess.DEVNULL))).convert('RGBA')
    except subprocess.CalledProcessError: continue
    new = Image.open(d + f).convert('RGBA'); F = old.height // 2
    for o, n in ((0, 1), (1, 3)):
        new.paste(Image.new('RGBA', (new.width, F)), (0, n * F)); new.paste(old.crop((0, o * F, old.width, o * F + F)), (0, n * F))
    new.save(d + f)
print(ST, 'S/N done')
