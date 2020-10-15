# Reads per-checkpoint results files and computes the topk best
# checkpoint-hyperparam combos by {test, dev} WER and PER for each language
import os
import sys

wers = {}
pers = {}

main_path = sys.argv[1]
topk = int(sys.argv[2])
split = sys.argv[3]

for run in os.listdir(main_path):
    run_path = os.path.join(main_path, run)
    run_lang = run[:3]
    if run_lang not in wers:
        wers[run_lang] = []
        pers[run_lang] = []
    for ckpt in os.listdir(run_path):
        if split in ckpt:
            with open(os.path.join(run_path, ckpt)) as f:
                for i, line in enumerate(f):
                    if i == 0:
                        wer = float(line.strip().split('\t')[1])
                    else:
                        per = float(line.strip().split('\t')[1])
            report = f"{run}/{ckpt}: WER {wer}, PER {per}"
            wers[run_lang].append((wer, report))
            pers[run_lang].append((per, report))

def takeTopK(k, lst):
    lst.sort(key=lambda tup: tup[0], reverse=False)
    return lst[:k]

print("======By WER======")
for lang, lst in wers.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)

print("======By PER======")
for lang, lst in pers.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)