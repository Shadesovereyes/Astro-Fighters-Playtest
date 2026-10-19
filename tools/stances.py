"""Martial stance idles (Christopher 2026-10-19): one looping combat idle per martial stance; Boxing keeps the approved
guard. Built on the approved guard spec (E/W first, W mirrors E; S/N to author after approval).
Run: python3 tools/stances.py ; node tools/character-posed.mjs male <state> (each)"""
import sys, copy, json
sys.path.insert(0, '/mnt/project-files/hex-sprites/tools')
from gen import load, build, save
R = '/home/claude/astro-fighters-playtest/'
D = R + 'production/source/characters/anim/male/'
GUARD = load(D + 'guard.json')
PALM = {k: v for k, v in load(D + 'mountPalm.json')['arms']['band'].items() if k in ('palmUp', 'palmDown')}
def band(a, e, **k): return {'construction': 'band', 'angle': a, 'elbow': {'at': 8, 'angle': e}, **k}
def leg(name, hip, knee, foot, wrap=56, kind='flat', hipX=None):
    return {'name': name, 'construction': 'band', 'hipX': hip[0], 'hipRow': hip[1], 'kneeX': knee[0], 'kneeRow': knee[1],
            'footX': foot, 'wrapRow': wrap, 'foot': kind}
STAT = 'CANDIDATE 2026-10-19 (E/W; W mirrors E; S/N to author after approval)'
APPROVED = {s: 'E/W approved by user 2026-10-19 (W mirrors E); S/N to author' for s in ('karateGuard', 'judoGuard', 'muayThaiGuard')}

STANCES = {}
def stance(state, ability, fps, intent, frames, poses):
    STANCES[state] = (ability, fps, intent, frames, poses)

# Muay Thai: tall and square, weight on the rear leg, lead heel up and the lead knee tapping, long high guard
MT = [leg('mt-lead', (32, 41), (36, 48), 38, 54, 'toe60'), {'name': 'mt-lead-up', 'construction': 'band', 'hipX': 33, 'hipRow': 41, 'kneeX': 40, 'kneeRow': 42, 'ankle': [39, 50], 'foot': 'toe30k'},
      leg('mt-rear', (31, 41), (29, 49), 25)]
mt_n, mt_f = band(-20, 212), band(-45, 222)   # the boxing guard's hands-up arms (Christopher 2026-10-19)
stance('muayThaiGuard', 'Muay Thai Stance', 6,
       'Muay Thai stance idle: tall and square, weight sitting on the rear leg, the lead heel off the ground and the lead knee lifting high once per loop; the boxing hands-up guard rocking on its own half-length rhythm, out of sync with the leg (Christopher 2026-10-19).',
       [dict(an=band(-20 + dn, 212 + dn), af=band(-45 + df, 222 + df), bob=(dy, dy, ab), lean=(0, 2), root=(0, 0), ln='mt-rear', lf=lf)
        for (dn, df, ab), (dy, lf) in zip([(0, 0, 2), (2, -3, 1), (4, -5, 1), (2, -3, 2)] * 2,
                                          [(1, 'mt-lead'), (1, 'mt-lead'), (1, 'mt-lead'), (1, 'mt-lead-up'), (1, 'mt-lead-up'), (2, 'mt-lead'), (2, 'mt-lead'), (1, 'mt-lead')])], MT)

# Karate: long front stance, lead hand out at chest height, rear fist chambered at the hip (hikite)
KA = [leg('ka-lead', (33, 43), (38, 49), 40), leg('ka-rear', (31, 43), (27, 50), 21)]
stance('karateGuard', 'Karate Stance', 6,
       'Karate stance idle: long front stance, lead knee bent over the foot and the rear leg long behind; the lead arm extended at chest height toward the opponent, the rear fist chambered at the hip; slow breathing settle.',
       [dict(an=band(55, -60), af=band(-75, -95), bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-75, -95), bob=(2, 2, 2), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-73, -93), bob=(3, 3, 3), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead'),
        dict(an=band(55, -60), af=band(-73, -93), bob=(3, 3, 4), lean=(0, 1), root=(0, 0), ln='ka-rear', lf='ka-lead')], KA)

# Horse Stance: deep straddle, back upright, both fists chambered at the hips
HS = [leg('hs-near', (32, 47), (38, 51), 35), leg('hs-far', (31, 47), (36, 51), 30)]
stance('horseStance', 'Horse Stance', 4,
       'Horse Stance idle: deep straddle with the knees bent out over the feet and the back upright; both fists chambered at the hips; slow, rooted breathing.',
       [dict(an=band(55, -60), af=band(55, -60), bob=(6, 6, 6), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 6, 6), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 7, 7), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far'),
        dict(an=band(55, -60), af=band(55, -60), bob=(6, 7, 7), lean=(0, 0), root=(0, 0), ln='hs-near', lf='hs-far')], HS)

# Judo: upright natural stance, both open hands out at chest height hunting for the lapel and sleeve grip
JU = [leg('ju-lead', (32, 42), (34, 50), 36), leg('ju-rear', (31, 42), (30, 50), 27)]
P = dict(fistKind='palm')
stance('judoGuard', 'Judo Stance', 6,
       'Judo stance idle: upright natural stance, knees soft; both hands open and out at chest height, the lead hand reaching for the sleeve and the rear hand for the lapel, pawing in and out.',
       [dict(an=band(-55, -88, **P), af=band(-72, -96, **P), bob=(1, 1, 2), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-55, -88, **P), af=band(-78, -100, **P), bob=(1, 1, 1), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-60, -92, **P), af=band(-72, -96, **P), bob=(2, 2, 2), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead'),
        dict(an=band(-55, -88, **P), af=band(-72, -96, **P), bob=(2, 2, 3), lean=(0, 2), root=(0, 0), ln='ju-rear', lf='ju-lead')], JU)

# Jiu-Jitsu: crouched and leaning in, elbows tight to the ribs, open hands forward to frame and grab
JJ = [leg('jj-lead', (33, 46), (38, 51), 38), leg('jj-rear', (31, 46), (30, 52), 24)]
stance('jiuJitsuGuard', 'Jiu-Jitsu Stance', 6,
       'Jiu-Jitsu stance idle: crouched with the hips back and the head forward, elbows tight to the ribs and both open hands out in front to frame and grab; small weight shifts.',
       [dict(an=band(-40, -85, **P), af=band(-35, -70, **P), bob=(5, 5, 5), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-40, -85, **P), af=band(-35, -70, **P), bob=(5, 5, 6), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-45, -90, **P), af=band(-38, -74, **P), bob=(6, 6, 6), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead'),
        dict(an=band(-45, -90, **P), af=band(-38, -74, **P), bob=(6, 6, 7), lean=(1, 7), root=(0, 0), ln='jj-rear', lf='jj-lead')], JJ)

# Wrestling: deep sprawl-ready crouch, chest over the lead knee, hands low and forward hand-fighting
WR = [leg('wr-lead', (33, 47), (39, 51), 38), leg('wr-rear', (31, 47), (31, 52), 23)]
stance('wrestlingGuard', 'Wrestling Stance', 6,
       'Wrestling stance idle: deep crouch with the chest over the lead knee and the rear leg driving behind; the off hand forward and away from the body with the elbow bent, the lead hand lower, both open hands leaning forward (redone like Jiu-Jitsu, Christopher 2026-10-19).',
       [dict(an=band(-45, -105, **P), af=band(-35, -70, **P), bob=(6, 6, 6), lean=(2, 10), root=(0, 0), ln='wr-rear', lf='wr-lead'),
        dict(an=band(-45, -105, **P), af=band(-35, -70, **P), bob=(6, 6, 6), lean=(2, 10), root=(0, 0), ln='wr-rear', lf='wr-lead'),
        dict(an=band(-50, -110, **P), af=band(-38, -74, **P), bob=(6, 6, 7), lean=(2, 10), root=(0, 0), ln='wr-rear', lf='wr-lead'),
        dict(an=band(-50, -110, **P), af=band(-38, -74, **P), bob=(6, 6, 7), lean=(2, 10), root=(0, 0), ln='wr-rear', lf='wr-lead')], WR)

def specs(only=None):
    base = copy.deepcopy(GUARD)
    base.pop('frontal', None); base['directions'] = ['E', 'W']
    base['arms']['band'].update(copy.deepcopy(PALM))
    for f, v in load(D + 'clinchKnee.json')['legs']['feet'].items(): base['legs']['feet'].setdefault(f, copy.deepcopy(v))   # toe30k etc. for a lifted lead leg
    for st, (ab, fps, intent, frames, poses) in STANCES.items():
        if only and st not in only: continue
        s = build(base, st, [dict(src=0, **f) for f in frames], status=APPROVED.get(st, STAT), intent=intent, newPoses=poses,
                  clips={'rule': 'martial stance idle: loops while that stance is active; attacks of the style start and end in the guard', st: {'frames': list(range(len(frames))), 'fps': fps, 'loop': True}},
                  rmRule='in place', extra={'stance': ab})
        s['fps'] = fps; s.pop('approved', None); s.pop('keyPoses', None)
        if st in ('judoGuard', 'jiuJitsuGuard', 'wrestlingGuard'):   # Christopher 2026-10-19: open hands angled forward, fingers leaning toward the opponent
            s['arms']['band']['palmUp'] = {'use': 'open hand angled forward, fingers leaning toward the opponent (judo grip hunt)', 'anchor': [0, 4],
                                           'rows': ['...Lm', '..LLm', '.LLLm', 'LLLLm', 'LLLms', 'mLLs.', '.sDs.']}
        save(s, D + st + '.json')
    print(' '.join(STANCES))


def outline(states=None):
    """after render: close the outline where an open hand's fingertips or a joint meet empty space (renderer QC
    'unoutlinedEdges'); the black pixel goes on the arms layer, or the body layer when the edge pixel is body"""
    from PIL import Image
    for st in states or STANCES:
        b = Image.open(D + st + '/body.png').convert('RGBA'); a = Image.open(D + st + '/arms.png').convert('RGBA')
        W, H = b.size; n = 0
        for oy in range(0, H, 64):
            for ox in range(0, W, 64):
                fig = {}
                for lay, im in (('body', b), ('arms', a)):
                    for y in range(64):
                        for x in range(64):
                            p = im.getpixel((ox + x, oy + y))
                            if p[3] == 255: fig[(x, y)] = (lay, p[:3])
                for (x, y), (lay, c) in list(fig.items()):
                    if c == (0, 0, 0): continue
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (x + dx, y + dy)
                        if q not in fig and 0 <= q[0] < 64 and 0 <= q[1] < 64:
                            (a if lay == 'arms' else b).putpixel((ox + q[0], oy + q[1]), (0, 0, 0, 255)); fig[q] = (lay, (0, 0, 0)); n += 1
        b.save(D + st + '/body.png'); a.save(D + st + '/arms.png'); print(st, 'outline +', n)

if __name__ == '__main__':
    if '--outline' in sys.argv: outline([a for a in sys.argv[1:] if a != '--outline'] or None)
    else: specs(sys.argv[1:] or None)
