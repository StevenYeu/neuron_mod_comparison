import itertools
import pprint
from typing import List, Tuple, Set

import numpy as np
from lsh import cache, minhash


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

def apply_lsh(data: List[str, str], threshold: float) -> Tuple[str,Set[str]]:
    candidates = candidate_duplicates(
        data, char_ngram=5, seeds=100, bands=20, hashbytes=4
    )

    n = len(data)
    sims_all = np.zeros((n, n), dtype=np.float64)
    for i, _ in enumerate(data):
        for j in range(i + 1, len(data)):
            shingles_a = shingles(data[i][1])
            shingles_b = shingles(data[j][1])
            jaccard_sim = jaccard(shingles_a, shingles_b)
            sims_all[i, j] = jaccard_sim

    candidates_dict = {
        (line_a, line_b): (docid_a, docid_b)
        for ((line_a, docid_a), (line_b, docid_b)) in candidates
    }
    found = 0
    pairs_names = set()
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            pairs_names.add((data[i][0], data[j][0], str(round(sims_all[i, j], 2))))
            if sims_all[i, j] >= round(float(threshold), 2):
                found += (i, j) in candidates_dict or (j, i) in candidates_dict
    pairs_ot = (sims_all >= float(threshold)).sum()
    pairs_ot = 1 if found == 0 else pairs_ot
    results = f"{pairs_ot} pairs with similarity >= {float(threshold) * 100}% were found."
    return (results, pairs_names)

