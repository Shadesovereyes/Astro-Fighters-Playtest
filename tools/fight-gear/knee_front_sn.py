"""Write kneeFront variants into the wt muayThaiKnee spec (S/N frames 2-4)."""
import json, sys
P = '/tmp/claude-0/s/wt/production/source/characters/anim/male/muayThaiKnee.json'
a = json.load(open(P)); f = a['frontal']; pv = f['partVariants']
B = '000000'
S_SAMPLE = {'o': B, '#': B, '%': B, 'K': [24, 40], 'I': [29, 41], 'G': [25, 41], 'H': [27, 41],
            'L': [25, 46], 'm': [25, 47], 's': [27, 45], 'd': [27, 46], 'D': [27, 47],
            'F': [22, 61], 'N': [25, 61], 'Q': [22, 62]}
N_SAMPLE = {'o': B, '#': B, '%': B, 'K': [33, 41], 'I': [33, 41], 'G': [34, 41], 'H': [35, 41],
            'L': [35, 48], 'm': [35, 46], 's': [34, 46], 'd': [35, 47],
            'F': [37, 60], 'N': [39, 60], 'Q': [37, 62]}
S_PEAK = ["oKIGGHHHHGKo",
          "oKIGHHHHHGKo",
          "oKI#######Ko",
          "oK#mLLLLms#o",
          "oo#mLLLLms#o",
          "..#mmLLmss#.",
          "..#dmmmssd#.",
          "...#dmssd#..",
          "...#dssdd#..",
          "....#dsd#...",
          "....%NFN%...",
          "....%QNQ%...",
          ".....%%%...."]
S_MID = ["oKIGGHHHGKo.",
         "oKIGHHHHGKo.",
         "oKI######Ko.",
         "oK#mLLLms#o.",
         "oo#mLLLms#o.",
         "..#dmmmsd#..",
         "..#dmmssd#..",
         "...#dmsd#...",
         "...#dssd#...",
         "...#dssd#...",
         "...%NFFN%...",
         "...%QNNQ%...",
         "....%%%%...."]
N_PEAK = ["oKGHHHGIKo.",
          "oKGHHHHGIKo",
          "oKGHHHHGIKo",
          "oKoooooooKo",
          "..#sLLLs#..",
          "..#mLLLm#..",
          "..%QNNNQ%..",
          "..%QFFFQ%..",
          "...%QFQ%...",
          "....%%%...."]
N_MID = ["oKGHHHGIKo.",
         "oKGHHHHGIKo",
         "oKoooooooKo",
         "..#sLLLs#..",
         "..#mLLLm#..",
         "..#sLLLs#..",
         "..%QNNNQ%..",
         "..%QFFFQ%..",
         "...%QFQ%...",
         "....%%%...."]
def put(view, name, side, frm, at, rows, sample, frames):
    pv[name] = {'kneeFront': {'side': side, 'from': frm, 'blocks': [{'at': at, 'rows': rows, 'sample': sample}]}}
    for k in frames:
        v = f['views'][view]['variants'][str(k)]
        v[:] = [x for x in v if 'lift' not in x and not x.startswith(view + '-kneeFront')] + [name]
put('S', 'S-kneeFront-peak', 'R', 40, [24, 36], S_PEAK, S_SAMPLE, (3, 4))
put('N', 'N-kneeFront-peak', 'R', 40, [28, 36], N_PEAK, N_SAMPLE, (3, 4))
put('S', 'S-kneeFront-mid', 'R', 40, [22, 38], S_MID, S_SAMPLE, (2, 5))
put('N', 'N-kneeFront-mid', 'R', 40, [29, 38], N_MID, N_SAMPLE, (2, 5))
put('S', 'S-kneeFront-low', 'R', 41, [21, 41], S_MID, S_SAMPLE, (1,))
put('N', 'N-kneeFront-low', 'R', 41, [30, 41], N_MID, N_SAMPLE, (1,))
json.dump(a, open(P, 'w'), indent=2)
print('ok')
