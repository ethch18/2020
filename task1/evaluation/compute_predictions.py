import argparse

from abydos.distance import Levenshtein, PhoneticEditDistance
from evallib import edit_distance
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--left', type=str)
parser.add_argument('--right', type=str)
parser.add_argument('--out', type=str)
args = parser.parse_args()

PED = PhoneticEditDistance()
PED_IG = PhoneticEditDistance(vowel_ignorance=True)
PED_DOM = PhoneticEditDistance(vowel_dominance=True)
PED_NOF_IG = PhoneticEditDistance(vowel_ignorance=True, no_features=True)
PED_NOF = PhoneticEditDistance(no_features=True)
LEV = Levenshtein()

with open(args.left) as left, open(args.right) as right, open(args.out, 'w') as ouf:
    for left_line, right_line in tqdm(zip(left, right)):
        left_grapheme, left_phoneme = left_line.strip().split('\t')
        right_grapheme, right_phoneme = right_line.strip().split('\t')

        lsplit = left_phoneme.split()
        rsplit = right_phoneme.split()

        gorman_lev = edit_distance(lsplit, rsplit) / len(lsplit)

        left_phon_input = ''.join(lsplit)
        right_phon_input = ''.join(rsplit)

        ped = PED.dist(left_phon_input, right_phon_input)
        ped_ig = PED_IG.dist(left_phon_input, right_phon_input)
        ped_dom = PED_DOM.dist(left_phon_input, right_phon_input)
        ped_nof_ig = PED_NOF_IG.dist(left_phon_input, right_phon_input)
        ped_nof = PED_NOF.dist(left_phon_input, right_phon_input)
        lev = LEV.dist(left_phon_input, right_phon_input)

        ouf.write(f"{left_grapheme}\t{left_phoneme}\t{right_phoneme}\t{right_grapheme}\t"
                  f"{ped}\t{ped_ig}\t{ped_dom}\t{ped_nof_ig}\t{ped_nof}\t{lev}\t{gorman_lev}\n")
