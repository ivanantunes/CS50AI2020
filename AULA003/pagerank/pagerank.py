import os
import random
import re
import sys
from copy import deepcopy


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    p_dist = {}
    p_pages = corpus[page]

    if len(p_pages) == 0:
        prob = 1 / len(corpus)

        for c_page in corpus:
            p_dist[c_page] = prob
        return p_dist

    damping_prob = damping_factor / len(p_pages)
    damping_prob_random = (1 - damping_factor) / len(corpus)

    for p_page in p_pages:
        p_dist[p_page] = damping_prob

    for c_page in corpus:
        if c_page in p_pages:
            p_dist[c_page] += damping_prob_random
        else:
            p_dist[c_page] = damping_prob_random

    return p_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {}
    next_page = random.choice(list(corpus))

    for i in range(n - 1):
        model = transition_model(corpus, next_page, damping_factor)
        next_page = random.choices(
            list(model), weights=model.values(), k=1).pop()

        if next_page in page_rank:
            page_rank[next_page] += 1
        else:
            page_rank[next_page] = 1

    for page in page_rank:
        page_rank[page] = page_rank[page] / n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {}

    for page in corpus:
        page_rank[page] = 1 / len(corpus)

    converged = False

    while not converged:
        page_rank_copy = {k: v for k, v in page_rank.items()}
        page_rank_diff = {}

        for page in corpus.keys():
            probability = 0

            for page_i, pages in corpus.items():

                if page in pages:
                    probability += page_rank_copy[page_i] / len(pages)
                elif len(pages) == 0:
                    probability += 1 / len(corpus)

            page_rank[page] = (1 - damping_factor) / \
                len(corpus) + (damping_factor * probability)
            page_rank_diff[page] = abs(page_rank_copy[page] - page_rank[page])

        converged = True

        for page in page_rank_diff:
            if page_rank_diff[page] > 0.001:
                converged = False

    sum_page_rank = 0
    for i in page_rank:
        sum_page_rank += page_rank[i]

    for i in page_rank:
        page_rank[i] = page_rank[i] / sum_page_rank

    return page_rank


if __name__ == "__main__":
    main()
