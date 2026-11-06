"""Chained Mount preview: plays paired Mount clips back to back (e.g. Kazushi then the submission it sets up), each with
its own clip timing (entry frames at the clip fps, hold loops at the loop fps, repeated). Uses pairpreview.py per pair.
usage: mount_chain_preview.py <animDir> <out> holder:partner[:loops] ..."""
import sys, os, json, subprocess, tempfile
from PIL import Image
anim, out = sys.argv[1:3]; segs = sys.argv[3:]
PP = '/mnt/project-files/hex-sprites/tools/pairpreview.py'; tmp = tempfile.mkdtemp()
frames, durs, strip = [], [], []
for i, sg in enumerate(segs):
    h, p, *lp = sg.split(':'); loops = int(lp[0]) if lp else 2
    subprocess.run(['python3', '-I', PP, anim, h, p, f'{tmp}/s{i}', '--cell', '80', '--x0', '4'], check=True, capture_output=True)
    g = Image.open(f'{tmp}/s{i}-candidate.gif'); fr = []
    for k in range(g.n_frames): g.seek(k); fr.append(g.convert('RGBA').copy())
    clips = json.load(open(os.path.join(anim, h + '.json')))['clips']
    order = [v for k, v in clips.items() if k != 'rule']
    for c in order:
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
