import os

from .content_based import find_related_papers
from .utils import create_user_vectors, calc_similarity


def find_user_similarities(user_vectors, target_vector):
    similarities = []
    for vector in user_vectors:
        similarities.append((vector, calc_similarity(vector, target_vector)))
    return similarities


def find_most_similar_papers(user_id: int, similar_user_count: int):
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(parent_dir, '../data.csv'), 'r') as f:
        rows = [row.strip().split(',') for row in f.readlines()]
    topics = rows[0]
    user_vectors = create_user_vectors(rows[1:])
    target_user_vector = user_vectors[user_id - 1]
    user_vectors.pop(user_id - 1)
    user_similarities = find_user_similarities(user_vectors, target_user_vector)
    user_similarities.sort(key=lambda x: x[1], reverse=True)
    similar_vectors = [vec[0] for vec in user_similarities[:similar_user_count]]
    new_user_vector = []
    for i in range(len(target_user_vector)):
        new_user_vector.append(sum([vec[i] for vec in similar_vectors]) / similar_user_count)

    return find_related_papers(topics, new_user_vector)
