import json

from .utils import calc_similarity


def get_paper_vectors(topics, papers_file_path):
    with open(papers_file_path, 'r') as f:
        papers = json.load(f)
    paper_vectors = {paper['id']: [] for paper in papers}
    for paper in papers:
        for topic in topics:
            if topic in paper['related_topics']:
                paper_vectors[paper['id']].append(1)
            else:
                paper_vectors[paper['id']].append(0)
    return paper_vectors


def find_related_papers(topics, user_vector):
    relevant_count = 10
    paper_vectors = get_paper_vectors(topics, 'CrawledPapers.json')
    papers_relevance = []
    for paper_id, paper_vector in paper_vectors.items():
        papers_relevance.append((paper_id, calc_similarity(user_vector, paper_vector)))
    papers_relevance.sort(key=lambda x: x[1], reverse=True)
    return [paper[0] for paper in papers_relevance[:relevant_count]]
