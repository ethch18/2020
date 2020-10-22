# Reads per-checkpoint results files and computes the topk best
# checkpoint-hyperparam combos by {test, dev} WER and PER for each language
import os
import sys

wers = {}
pers = {}
ped_ig = {}
ped_dom = {}
ped_nof = {}
ped = {}

main_path = sys.argv[1]
topk = int(sys.argv[2])
split = sys.argv[3]

for run in os.listdir(main_path):
    run_path = os.path.join(main_path, run)
    run_lang = run[:3]
    if run_lang not in wers:
        wers[run_lang] = []
        pers[run_lang] = []
        ped_ig[run_lang] = []
        ped_dom[run_lang] = []
        ped_nof[run_lang] = []
        ped[run_lang] = []
    for ckpt in os.listdir(run_path):
        if split in ckpt:
            with open(os.path.join(run_path, ckpt)) as f:
                for i, line in enumerate(f):
                    if i == 0:
                        wer = float(line.strip().split('\t')[1])
                    elif i == 1:
                        per = float(line.strip().split('\t')[1])
                    elif i == 2:
                        ped_ig = float(line.strip().split('\t')[1])
                    elif i == 3:
                        ped_dom = float(line.strip().split('\t')[1])
                    elif i == 4:
                        ped_nof = float(line.strip().split('\t')[1])
                    else:
                        ped = float(line.strip().split('\t')[1])
            report = f"{run}/{ckpt}: WER {wer}, PER {per}, PED_IG: {ped_ig}, " \
                     f"PED_DOM: {ped_dom}, PED_NOF: {ped_nof}, PED: {ped}"
            wers[run_lang].append((wer, report))
            pers[run_lang].append((per, report))
            ped_ig[run_lang].append((ped_ig, report))
            ped_dom[run_lang].append((ped_dom, report))
            ped_nof[run_lang].append((ped_nof, report))
            ped[run_lang].append((ped, report))


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

print("======By PED_IG======")
for lang, lst in ped_ig.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)

print("======By PED_DOM======")
for lang, lst in ped_dom.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)

print("======By PED_NOF======")
for lang, lst in ped_nof.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)

print("======By PED======")
for lang, lst in ped.items():
    print(lang)
    for _, report in takeTopK(topk, lst):
        print("    ", report)