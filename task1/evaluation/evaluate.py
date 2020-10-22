#!/usr/bin/env python
"""Evaluates sequence model.

This script assumes the gold and hypothesis data is stored in a two-column TSV
file, one example per line."""

__author__ = "Kyle Gorman"

import argparse
import logging
import multiprocessing

import evallib


def main(args: argparse.Namespace) -> None:
    # Word-level measures.
    correct = 0
    incorrect = 0
    # Label-level measures.
    total_edits = 0
    total_length = 0
    # Aux measures
    ignorance_edits = 0.
    dominance_edits = 0.
    no_feature_edits = 0.
    ped_edits = 0.
    # Since the edit distance algorithm is quadratic, let's do this with
    # multiprocessing.
    with multiprocessing.Pool(args.cores) as pool:
        gen = pool.starmap(evallib.score, evallib.tsv_reader(args.tsv_path))
        for (edits, length, (ig, dom, nof, ped)) in gen:
            if edits == 0:
                correct += 1
            else:
                incorrect += 1
            total_edits += edits
            total_length += length
            ignorance_edits += ig
            dominance_edits += dom
            no_feature_edits += nof
            ped_edits += ped
    print(f"WER:\t{100 * incorrect / (correct + incorrect):.2f}")
    print(f"LER:\t{100 * total_edits / total_length:.2f}")
    print(f"PED_IG:\t{100 * ignorance_edits / total_length:.2f}")
    print(f"PED_DOM:\t{100 * dominance_edits / total_length:.2f}")
    print(f"PED_NOF:\t{100 * no_feature_edits / total_length:.2f}")
    print(f"PED:\t{100 * ped_edits / total_length:.2f}")


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Evaluates sequence model")
    parser.add_argument("tsv_path", help="path to gold/hypo TSV file")
    parser.add_argument(
        "--cores",
        default=multiprocessing.cpu_count(),
        help="number of cores (default: %(default)s)",
    )
    main(parser.parse_args())
