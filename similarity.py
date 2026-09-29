def jaro_similarity(a, b):
    a, b = a.lower().strip(), b.lower().strip()
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    distance = max(len(a), len(b)) // 2 - 1
    distance = max(distance, 0)
    am = [False] * len(a)
    bm = [False] * len(b)
    matches = 0
    for i, char in enumerate(a):
        for j in range(max(0, i-distance), min(i+distance+1, len(b))):
            if not bm[j] and char == b[j]:
                am[i] = True
                bm[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0
    k = trans = 0
    for i in range(len(a)):
        if not am[i]:
            continue
        while not bm[k]:
            k += 1
        if a[i] != b[k]:
            trans += 1
        k += 1
    return (matches/len(a) + matches/len(b) + (matches-trans/2)/matches) / 3

def jaro_winkler(a, b):
    score = jaro_similarity(a, b)
    prefix = 0
    for x, y in zip(a.lower(), b.lower()):
        if x != y or prefix == 4:
            break
        prefix += 1
    if score > 0.7:
        score += prefix * 0.1 * (1 - score)
    return score

def closest_option(user_input, options, threshold=0.78):
    best = max(options, key=lambda option: jaro_winkler(user_input, option))
    score = jaro_winkler(user_input, best)
    return (best, score) if score >= threshold else (None, score)