"""Chained Mount preview: plays paired Mount clips back to back (e.g. Kazushi then the submission it sets up), each with
its own clip timing (entry frames at the clip fps, hold loops at the loop fps, repeated). Uses pairpreview.py per pair.
usage: mount_chain_preview.py <animDir> <out> holder:partner[:loops[:markRole[:markUntil]]] ...
markRole A|B: draw the lingering Kazushi exclamation mark (kzMark) above that fighter's head on every frame of the segment
(for the follow-up submission, up to its clip markUntil, e.g. the entry clip only, where the Kazushi bonus is spent)."""
import sys, os, json, subprocess, tempfile
from PIL import Image
anim, out = sys.argv[1:3]; segs = sys.argv[3:]
PP = '/mnt/project-files/hex-sprites/tools/pairpreview.py'; tmp = tempfile.mkdtemp()
frames, durs, strip = [], [], []
for i, sg in enumerate(segs):
    h, p, *lp = sg.split(':'); loops = int(lp[0]) if lp else 2
    mark = lp[1] if len(lp) > 1 else None; until = lp[2] if len(lp) > 2 else None
    subprocess.run(['python3', '-I', PP, anim, h, p, f'{tmp}/s{i}', '--cell', '80', '--x0', '4'], check=True, capture_output=True)
    g = Image.open(f'{tmp}/s{i}-candidate.gif'); fr = []
    for k in range(g.n_frames): g.seek(k); fr.append(g.convert('RGBA').copy())
    fr_plain = [f.copy() for f in fr]
    if mark:
        hs, ps = json.load(open(os.path.join(anim, h + '.json'))), json.load(open(os.path.join(anim, p + '.json')))
        st, sp_, hair, ox, mot = (h, hs, 'fade-hair', 4, hs['rootMotion']['E']) if mark == 'A' else (p, ps, 'long-hair', 4 + hs['pair'].get('partnerDx', 2), ps['rootMotion']['W'])
        row = sp_['directions'].index('E' if mark == 'A' else 'W'); hp = Image.open(os.path.join(anim, st, hair + '.png')).convert('RGBA')
        KZ = ['###', '#W#', '#W#', '#W#', '#W#', '###', '#W#', '###']; C = {'#': (0, 0, 0, 255), 'W': (255, 255, 255, 255)}
        cut = set(clips[until]['frames']) if False else None
        lim = None
        for k in range(len(fr)):
            px = hp.load(); pts = [(x, y) for y in range(64) for x in range(64) if px[k * 64 + x, row * 64 + y][3]]
            if not pts: continue
            mx = sum(m[0] for m in mot[:k + 1]); my = sum(m[1] for m in mot[:k + 1])
            cx = (min(q[0] for q in pts) + max(q[0] for q in pts)) // 2 + ox + mx; ty = min(q[1] for q in pts) + my - 2 - len(KZ)
            big = fr[k]
            for j, r_ in enumerate(KZ):
                for i2, c in enumerate(r_):
                    for a in range(4):
                        for b in range(4): big.putpixel(((cx - 1 + i2) * 4 + a, (ty + j) * 4 + b), C[c])
    clips = json.load(open(os.path.join(anim, h + '.json')))['clips']
    order = [v for k, v in clips.items() if k != 'rule']
    for c in order:
        if mark and until and c is not order[0] and c.get('loop'): fr = fr_plain
        reps = loops if c.get('loop') else 1
        for _ in range(reps):
            for k in c['frames']: frames.append(fr[k]); durs.append(int(1000 / c.get('fps', 12)))
        if not c.get('loop'): strip += [fr[k] for k in c['frames']]
    if any(c.get('loop') for c in order): strip += [fr[k] for k in next(c for c in order if c.get('loop'))['frames']]
frames[0].save(out + '-candidate.gif', save_all=True, append_images=frames[1:], duration=durs, loop=0, disposal=2)
w, hh = strip[0].size; s2 = [f.resize((w // 2, hh // 2), Image.NEAREST) for f in strip]; n = 10
W = Image.new('RGBA', (n * (w // 2 + 3), ((len(s2) + n - 1) // n) * (hh // 2 + 3)), 'white')
for k, f in enumerate(s2): W.paste(f, ((k % n) * (w // 2 + 3), (k // n) * (hh // 2 + 3)))
W.save(out + '-E-candidate.png'); print('wrote', out, len(frames), 'gif frames,', len(strip), 'strip frames')
