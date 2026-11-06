"""S/N (front/back) views of the approved stand-in replacement clips (Christopher 2026-11-06: E/W approved; S/N after
approval). Same machinery as universal_sn.py: the base is the approved boxing guard's S/N view, the ability frames override
the frontal arms (R = near/rear arm, the viewer's left in S; L = far/lead arm; (angle, forearm angle or None, scale, fist)),
the target is toward the viewer in S and away in N; impact splashes in front of the fighter only show outside the figure in N.
Run: python3 tools/standins_sn.py [state..] ; node tools/character-posed.mjs male <state> ; python3 tools/standins_sn.py --restore [state..] ;
     python3 tools/stances.py --outline <state> ; preview: python3 /mnt/project-files/hex-sprites/tools/dir4.py <animDir> <state> <out>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standins, astro   # registers the stand-in clips and their fx patterns
import universal_sn as U
G = U.stances.GA
AIM = (70, None, 0.45, 'front')            # lead hand reaching out at the target (toward the viewer), measuring
COCK = (155, 178, 1, 'up')                 # rear fist cocked high behind the head
SN = {
 'boxUppercut': {1: dict(R=(25, 150, 1, 'up')),                  # rear fist dropped to the hip, palm up
                 2: dict(R=(-5, 185, 1, 'up')),                   # driving up close to the body
                 3: dict(R=(-30, 192, 0.9, 'up')), 4: dict(R=(-30, 192, 0.9, 'up')),   # under the chin of the target, toward the viewer
                 5: dict(R=(-5, 195, 1, 'up'))},
 'boxHaymaker': {1: dict(R=COCK, L=AIM), 2: dict(R=(165, 185, 1, 'up'), L=AIM),              # loaded behind the head, lead hand measuring
                 3: dict(R=(130, 110, 0.8, 'up'), L=(-30, 175, 1, 'up')),                  # the loop comes over the top
                 4: dict(R=(-55, -70, 0.8, 'up'), L=(-30, 175, 1, 'up')),                  # lands at the jaw, fist across in front
                 5: dict(R=(-35, -20, 1, 'up'), L=(-30, 175, 1, 'up')),                    # carries on through and down across the body
                 6: dict(R=(20, 190, 1, 'up'))},
 'boxBodyShot': {1: dict(R=(25, 200, 1, 'up'), L=(-25, 165, 1, 'up')),                     # level change, rear glove covering the ducked head
                 2: dict(R=(25, 200, 1, 'up'), L=(-75, -30, 1, 'up')),                     # lead elbow swings out wide
                 3: dict(R=(25, 200, 1, 'up'), L=(-70, 40, 0.8, 'up')), 4: dict(R=(25, 200, 1, 'up'), L=(-70, 40, 0.8, 'up')),   # hooks in at belly height
                 5: dict(L=(-30, 160, 1, 'up'))},
 'wildSwing': {1: dict(R=(160, 175, 1, 'up'), L=(-45, -70, 1, 'up')),                      # rears way back, guard thrown open
               2: dict(R=(110, 75, 1, 'up'), L=(-35, -40, 1, 'up')),                       # flinging round flat
               3: dict(R=(-65, -85, 0.85, 'up'), L=(-25, -30, 1, 'up')),                   # lands at the head
               4: dict(R=(-45, -25, 1, 'up'), L=(-15, -20, 1, 'up')),                      # overswings across the body
               5: dict(R=(-25, -15, 1, 'up'), L=(-10, -30, 1, 'up')),
               6: dict(R=(20, 190, 1, 'up'), L=(-20, 170, 1, 'up'))},
 'clinchEntry': {1: dict(R=(-35, None, 0.45, 'front'), L=(35, None, 0.45, 'front')),      # both open hands shooting out at the neck, toward the viewer
                 2: dict(R=(-50, None, 0.3, 'front'), L=(50, None, 0.3, 'front')),
                 3: dict(R=(-140, None, 0.4, 'up'), L=(140, None, 0.4, 'up')),             # closed behind the target's head (in front of the face): collar tie
                 4: dict(R=(-110, None, 0.4, 'up'), L=(110, None, 0.4, 'up')),             # pulled down
                 5: dict(R=(15, 185, 1, 'up'), L=(-15, 175, 1, 'up'))},
}
FX_SN = {
 'boxUppercut': [(3, 'star6', 'hand', 'hand'), (4, 'star3', 'hand', 'hand')],
 'boxHaymaker': [(4, 'star9', 'hand', 'hand')],
 'boxBodyShot': [(3, 'star6', [36, 42], [22, 42]), (4, 'star3', [37, 41], [23, 41])],
 'wildSwing': [(3, 'star9', 'hand', 'hand'), (4, 'dust', [24, 63], [24, 63]), (5, 'dust', [20, 63], [20, 63])],
}
U.SN.update(SN); U.FX_SN.update(FX_SN); U.BEHIND_N |= set(SN)
U.SNAP = '/tmp/standins_sn_ew/'
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SN)
    for s in args:
        if '--restore' in sys.argv: U.restore(s); U.fx(s)
        else: U.sn(s)
