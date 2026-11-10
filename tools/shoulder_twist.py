"""Shoulder Charge v7 (Christopher 2026-11-10 15:55: "i'd like to see the torso rotate towards the camera as if to be
lowering the shoulder into the impact"). On the twist frames the fighter's upper body turns a quarter toward the viewer
(the lead shoulder, the far one in E, swings round to lead into the target) while the head stays on the target and the
hips and legs keep running side-on. The rig cannot rotate a torso, so the turned torso is the clip's own S-view render
(standins_sn machinery, both fists tucked tight in front of the chest) spliced between the E head and the E hips:
  head layers (hair, helmets, headbands, eyes) and every pixel above the neck row: the E frame
  arms and shoulder pieces: the S frame
  every other layer (body, Gi, armour, stowed gear) between the neck row and the belt: the S frame; below the belt: E
The S rows are sheared row by row onto the E torso's lean line (a straight fit through the E torso centres), so the
turned torso keeps the drive angle. W mirrors E.
Run: python3 tools/shoulder_twist.py   (needs the committed E/W sheets; renders the S view in a scratch copy)"""
import os, sys, json, shutil, subprocess, glob
from PIL import Image
R = '/home/user/astro-fighters-playtest/'; D = R + 'production/source/characters/anim/male/'
ST = 'shoulderCharge'; TWIST = (8, 9, 10, 11); NECK = 26; DROP = 0
TUCK = dict(R=(10, 195, 0.85, 'up'), L=(-30, 175, 0.85, 'up'))   # both fists tucked tight in front of the chest (S view)
HEADL = ('hair', 'afro', 'locs', 'headband', 'headscarf', 'topknot', 'braided', 'bantu', 'ponytail', 'flat-top', 'helmet', 'kabuto', 'cap', 'bascinet', 'eyes')
WHOLE_S = ('arms.png', 'far-arm.png')
SCR = '/tmp/shoulder_twist_sn/'

def render_s():
    sys.path.insert(0, R + 'tools')
    shutil.rmtree(SCR, ignore_errors=True); os.makedirs(SCR)
    for p in (D + ST, D + ST + '.json'):
        (shutil.copytree if os.path.isdir(p) else shutil.copy)(p, SCR + 'ew' + ('' if os.path.isdir(p) else '.json'))
    subprocess.check_call([sys.executable, '-c', 'import sys; sys.path.insert(0, %r); import standins_sn as S, universal_sn as U; '
                           'U.SN[%r] = {k: %r for k in range(1, 15)}; U.BEHIND_N |= {%r}; U.sn(%r)' % (R + 'tools', ST, TUCK, ST, ST)], cwd=R)
    subprocess.check_call(['node', 'tools/character-posed.mjs', 'male', ST], cwd=R, stdout=subprocess.DEVNULL)
    subprocess.check_call([sys.executable, 'tools/stances.py', '--outline', ST], cwd=R, stdout=subprocess.DEVNULL)
    shutil.copytree(D + ST, SCR + 'sn')
    shutil.rmtree(D + ST); shutil.copytree(SCR + 'ew', D + ST); shutil.copy(SCR + 'ew.json', D + ST + '.json')   # the E/W clip back exactly

def ext(img, k, r, y):
    xs = [x for x in range(64) if img.getpixel((k * 64 + x, r * 64 + y))[3]]
    return (min(xs) + max(xs)) / 2 if xs else None

def fit(pts):
    n = len(pts); my = sum(y for y, _ in pts) / n; mx = sum(x for _, x in pts) / n
    b = sum((y - my) * (x - mx) for y, x in pts) / sum((y - my) ** 2 for y, _ in pts)
    return lambda y: mx + b * (y - my)

def splice():
    sn = SCR + 'sn/'; ew = D + ST + '/'
    bE, bS, gS = Image.open(ew + 'body.png').convert('RGBA'), Image.open(sn + 'body.png').convert('RGBA'), Image.open(sn + 'male-gi.png').convert('RGBA')
    plan = {}
    for k in TWIST:
        belt = min(y for y in range(NECK, 64) for x in range(64) if gS.getpixel((k * 64 + x, y))[:3] in ((0x70, 0x24, 0x1d), (0x9e, 0x1c, 0x1c), (0xb3, 0x23, 0x23)) and gS.getpixel((k * 64 + x, y))[3]) if False else None
        rows = range(NECK + 1, NECK + 13)
        fe = fit([(y, ext(bE, k, 0, y)) for y in rows if ext(bE, k, 0, y) is not None])
        fs = fit([(y, ext(bS, k, 0, y)) for y in rows if ext(bS, k, 0, y) is not None])
        hips = [y for y in range(NECK, 64) if ext(bE, k, 0, y) is not None]
        plan[k] = dict(sx=lambda y, fe=fe, fs=fs: round(fe(min(max(y, NECK), NECK + 13)) - fs(min(max(y, NECK), NECK + 13))), belt=NECK + 13)
    for f in sorted(glob.glob(ew + '*.png')):
        n = os.path.basename(f)
        if n == 'fx.png' or not os.path.exists(sn + n): continue
        E = Image.open(f).convert('RGBA'); S = Image.open(sn + n).convert('RGBA')
        head = any(t in n for t in HEADL) and 'shoulders' not in n
        for k in TWIST:
            p = plan[k]; fr = Image.new('RGBA', (64, 64))
            for y in range(64):
                for x in range(64):
                    if head or y < NECK or (y > p['belt'] and n not in WHOLE_S): c = E.getpixel((k * 64 + x, y))
                    else: c = (0, 0, 0, 0)
                    if c[3]: fr.putpixel((x, y), c)
            if not head:
                for y in range(64):
                    if n not in WHOLE_S and not (NECK <= y <= p['belt']): continue
                    if n in WHOLE_S and y < NECK - 4: continue
                    for x in range(64):
                        c = S.getpixel((k * 64 + x, y))
                        X = x + p['sx'](y); Y = y + max(0, round((x - 32) * DROP))   # the lead (viewer's right) shoulder dips into the hit
                        if c[3] and 0 <= X < 64 and Y < 64: fr.putpixel((X, Y), c)
            E.paste(fr, (k * 64, 0)); E.paste(fr.transpose(Image.FLIP_LEFT_RIGHT), (k * 64, 64))
        E.save(f)
    print('spliced', ST, TWIST)

if __name__ == '__main__':
    if '--splice' not in sys.argv: render_s()
    splice()
