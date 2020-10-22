import argparse
import hangul_jamo
import re

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, required=True)
parser.add_argument('--output-file', type=str, required=True)
args = parser.parse_args()

do_jamo = 'kor' in args.input_file.lower()
# re_diacritics = re.compile(r"[ːᵝ̆ ͈ ̟ ̠ ̥ ̊ ̃ ̞ˀ˕̹]")
# the above has too many spaces
re_diacritics = re.compile(r"[ːᵝ͈̟̠̥̞̆̊̃ˀ˕̹]")

with open(args.input_file) as inf, open(args.output_file, 'w') as ouf:
    for line in tqdm(inf):
        grapheme, phoneme = line.strip().split('\t')
        phoneme = re_diacritics.sub('', phoneme).replace('w͍', 'w')
        if do_jamo:
            grapheme = hangul_jamo.decompose(grapheme)

        ouf.write(f"{grapheme}\t{phoneme}\n")
