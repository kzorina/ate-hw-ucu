import pandas as pd
def tf(terms):
    #print len(terms)
    map = {}
    max = 1
    for term in terms:
        if term in map.keys():
            map[term] += 1
            if map[term]>max:
                max = map[term]
        else:
            map[term] = 1
    print(len(map))
    for term in map.keys():
        map[term] = 0.5 + 0.5*map[term]/max
    df = pd.DataFrame({'term': map.keys(), 'num': map.values()})
    return df.sort_values(['num'], ascending=False)