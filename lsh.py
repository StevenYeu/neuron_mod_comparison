import itertools
import numpy as np
import argparse
import pprint
from lsh import cache, minhash
from pathlib import Path
from os import listdir
from os.path import isfile, join


def shingles(text, char_ngram=5):
    return set(
        text[head : head + char_ngram] for head in range(0, len(text) - char_ngram + 1)
    )


def jaccard(set_a, set_b):
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def candidate_duplicates(document_feed, char_ngram=5, seeds=100, bands=5, hashbytes=4):
    hasher = minhash.MinHasher(seeds=seeds, char_ngram=char_ngram, hashbytes=hashbytes)
    if seeds % bands != 0:
        raise ValueError(
            "Seeds has to be a multiple of bands. {} % {} != 0".format(seeds, bands)
        )

    lshcache = cache.Cache(num_bands=bands, hasher=hasher)
    for index, (name, text) in enumerate(document_feed):
        fingerprint = hasher.fingerprint(text.encode("utf8"))
        lshcache.add_fingerprint(fingerprint, doc_id=(index, name))

    candidate_pairs = set()
    for b in lshcache.bins:
        for bucket_id in b:
            if len(b[bucket_id]) > 1:
                pairs_ = set(itertools.combinations(b[bucket_id], r=2))
                candidate_pairs.update(pairs_)

    return candidate_pairs


def main():
    parser = argparse.ArgumentParser(prog="LSH Tester", description="Test LSH")

    parser.add_argument("input")
    parser.add_argument("threshold")

    args = parser.parse_args()

    files = [
        join(args.input, f) for f in listdir(args.input) if isfile(join(args.input, f))
    ]
    print(files)
    docs = [(f, Path(f).read_text()) for f in files]

    candidates = candidate_duplicates(
        docs, char_ngram=5, seeds=100, bands=20, hashbytes=4
    )

    sims_all = np.zeros((4, 4), dtype=np.float64)
    for i, _ in enumerate(docs):
        for j in range(i + 1, len(docs)):
            shingles_a = shingles(docs[i][1])
            shingles_b = shingles(docs[j][1])
            jaccard_sim = jaccard(shingles_a, shingles_b)
            sims_all[i, j] = jaccard_sim

    candidates_dict = {
        (line_a, line_b): (docid_a, docid_b)
        for ((line_a, docid_a), (line_b, docid_b)) in candidates
    }
    found = 0
    pairs_names = set()
    pp = pprint.PrettyPrinter(indent=4)
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            pairs_names.add((docs[i][0], docs[j][0], str(round(sims_all[i, j], 2))))
            if sims_all[i, j] >= round(float(args.threshold), 2):
                found += (i, j) in candidates_dict or (j, i) in candidates_dict
    pairs_ot = (sims_all >= float(args.threshold)).sum()
    pairs_ot = 1 if found == 0 else pairs_ot
    print(
        f"Out of {pairs_ot} pairs with similarity >= {float(args.threshold) * 100}% {found} were found, that's {(found/pairs_ot) * 100}%"
    )
    pp.pprint(pairs_names)


if __name__ == "__main__":
    main()
