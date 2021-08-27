def calc_norm(vec):
    return sum(v ** 2 for v in vec) ** 0.5


def find_inner_product(vec1, vec2):
    return sum([v1 * v2 for v1, v2 in zip(vec1, vec2)])


def calc_similarity(vec1, vec2):
    vec1_norm = calc_norm(vec1)
    vec2_norm = calc_norm(vec2)
    inner_product = find_inner_product(vec1, vec2)
    if inner_product != 0:
        inner_product /= (vec1_norm * vec2_norm)
    return inner_product


def create_user_vectors(user_data_rows):
    user_vectors = []
    for row in user_data_rows:
        user_paper_read_fractions = []
        for read_fraction in row:
            try:
                user_paper_read_fractions.append(float(read_fraction))
            except ValueError:
                user_paper_read_fractions.append(0)
        user_vectors.append(user_paper_read_fractions)
    return user_vectors
