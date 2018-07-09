from math import floor


def jaro_sim(word1, word2):
    s1 = len(word1)
    s2 = len(word2)

    match_window = floor(max(s1, s2)/2) - 1
    m = 0.0
    t = 0.0

    w1m = [0] * s1
    w2m = [0] * s2
    for i, char1 in enumerate(word1):
        start = max(0,i - match_window)
        end = min(len(word2),i+match_window+1)

        for j, char2 in enumerate(word2):
            if ((not w2m[j]) and (char1 == char2)):
                w1m[i] = 1
                w2m[j] = 1
                m += 1
                break

    if m ==0:
        return m
    else:
        mathced1 = []
        mathced2 = []
        for i, el in enumerate(w1m):
            if el:
                mathced1.append(word1[i])
        for i, el in enumerate(w2m):
            if el:
                mathced2.append(word2[i])
        #print(mathced1)
        #print(mathced2)
        for i, char in enumerate(mathced1):
            if char <> mathced2[i]:
                t+=1

        return float((m/s1 + m/s2 + (m-t)/m)/3)


def term_grouping(terms, threshold=0.7):
    terms = terms
    max_sim = 0
    sum = 0
    length = len(terms)
    k = 0
    while k < length:
        term = str(terms.iloc[[k]]["term"].tolist()[0])
        score = float(terms.iloc[[k]]["num"])
        count = 1
        j = k + 1
        while j < length:
            similarity = jaro_sim(term, str(terms.iloc[[j]]["term"].tolist()[0]))
            if similarity > max_sim:
                max_sim = similarity
            if similarity > threshold:
                # print("Similar: {} and {} terms".format(k, j))
                score += float(terms.iloc[[j]]["num"])
                # remove terms[j]
                terms = terms.drop(terms.index[j])
                length = len(terms)
                count += 1
            j += 1

        terms.iloc[[k]]["num"] = score / count
        k += 1
    #print("Max similarity: {}".format(max_sim))
    return terms
