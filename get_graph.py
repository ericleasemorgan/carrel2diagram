import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import json
from itertools import combinations

def get_graph(corpus, pos):
    if not os.path.exists('%s' % corpus):
        os.system("mkdir %s" % corpus)
        os.system("wget http://carrels.distantreader.org/library/%s/study-carrel.zip -O %s.zip" % (corpus, corpus))
        os.system("unzip %s.zip -d ./%s" % (corpus, corpus))

    for path in glob.glob('./%s/*/pos/*.pos' % corpus):
        try:
            df = pd.read_csv(path, sep='\t')
        except:
            continue
        else:
            break
    noun = df[df['pos']==pos]

    punctuation ='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    def remove_puncs(word):
        for i in punctuation:
            if i in word:
                return ''
        return word
    
    number = noun.lemma.value_counts()
    clean_noun = list(set([remove_puncs(i) for i in noun.lemma]))
    try:
        clean_noun.remove('')
    except:
        pass
    noun = noun[noun['lemma'].isin(clean_noun)]

    result = pd.DataFrame(list(combinations(clean_noun, 2)), columns=['token1', 'token2'])
    result['weight'] = np.zeros(result.shape[0])
    result = result.loc[result.index[:10000]]
    # Count
    for i in noun.sid.unique():
        temp = noun[noun['sid']==i]
        temp_lemma = list(set(combinations(temp.lemma.values, 2)))
        for i in temp_lemma:
            value_to_be_add = result[(result['token1']==i[0]) & (result['token2']==i[1])]
            result.loc[value_to_be_add.index, 'weight'] += 1
            value_to_be_add = result[(result['token1']==i[1]) & (result['token2']==i[0])]
            result.loc[value_to_be_add.index, 'weight'] += 1

    clean_result = result[result['weight']>1.0]
    data = {}
    data['nodes'] = []
    data['links'] = []

    for token in clean_noun:
        data['nodes'].append({"id": token, "group": 1, "size": int(number.loc[token])})
    for row in clean_result.iterrows():
        data['links'].append({"source": row[1].token1, "target": row[1].token2, "value": row[1].weight})
    
    print(data)
    import json
    with open('%s-%s.json' % (corpus, pos), 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    get_graph('cooking', 'NNP')
    get_graph('cooking', 'NN')