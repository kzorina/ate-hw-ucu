# coding: utf-8

# Implementation of the algorithm described by *Katerina Frantzi, Sophia Ananiadou, Hideki Mima*
# in the **"Automatic Recognition of Multi-Word Terms: the C-value/NC-value Method"**

import ConfigParser
import ate
import csv
import re
import json
import pandas as pd
import numpy as np

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

min_term_length = int(config.get('main', 'min_term_length'))
min_term_words = int(config.get('main', 'min_term_words'))
stopwords = json.loads(config.get('main', 'stopwords'))
term_patterns=json.loads(config.get('main', 'term_patterns'))
doc_file=config.get('main', 'doc_file')
out_file=config.get('main', 'out_file')

reference_file = "hands-on/time-onto-paper/MyTimeOnto-Paper-manually-extracted-terms.csv"

fp = open(doc_file, "r")
doc_txt = fp.read() 
fp.close()
doc_txt = unicode(doc_txt, "utf-8", errors='ignore')
doc_txt = re.sub(r'et +al\.', 'et al', doc_txt)
doc_txt = re.split(r'[\r\n]', doc_txt)

term_extractor = ate.TermExtractor(stopwords=stopwords, term_patterns=term_patterns, min_term_words=min_term_words,
                                       min_term_length=min_term_length)
# terms = term_extractor.extract_terms(doc_txt)



# print(max(map, key=map.get))

def tf(text):
    term_extractor = ate.TermExtractor(stopwords=stopwords, term_patterns=term_patterns, min_term_words=min_term_words,
                                       min_term_length=min_term_length)
    terms = term_extractor.extract_terms(text)
    print len(terms)
    # print type(terms[0])
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
tf_results = tf(doc_txt)
print(tf_results)

# c_values = term_extractor.c_values(terms, trace=True) #replace this line
#my_output = ttf_idf(terms)

# with open(out_file, 'wb') as csvfile:
#     termwriter = csv.writer(csvfile, delimiter=';', quotechar='', quoting=csv.QUOTE_NONE)
#     for cv in c_values:
#         termwriter.writerow(cv)

# with open(out_file,'r') as file_out:
#     terms_c_value = file_out.read()
# print(terms_c_value)
# print(len(terms_c_value))

# with open(reference_file,'r') as golden_standart:
#     terms_gs = golden_standart.read()
terms_gs_df = pd.DataFrame.from_csv(reference_file, sep=';')
# print(type(terms_gs))
# print(len(terms_gs))

print(terms_gs_df.head())
term_gs_agg = terms_gs_df.groupby(['term'])['num'].agg([np.sum])
print(type(term_gs_agg))
# print(term_gs_agg.size())
terms_cvalue_df = pd.DataFrame.from_csv(out_file, sep=';')

t1 = ['a','b','c','d','g']
t2 = ['g','d','y','t']

def precision(test_terms,true_terms):
    num = float(len(set(test_terms).intersection(true_terms)))
    denum = float(len(test_terms))
    #print(num)
    #print(denum)
    return num/denum
def recall(test_terms,true_terms):
    num = float(len(set(test_terms).intersection(true_terms)))
    denum = float(len(true_terms))
    # print(num)
    # print(denum)
    return num / denum
def f_measure(test_terms,true_terms):
    p = precision(test_terms,true_terms)
    r = recall(test_terms,true_terms)
    return 2*p*r/(r+p)
print(precision(t1,t2))
print(precision(terms_cvalue_df.index.values.tolist(),term_gs_agg.index.values.tolist()))
print(precision(tf_results['term'].tolist(),term_gs_agg.index.values.tolist()))

print(recall(t1,t2))
print(recall(terms_cvalue_df.index.values.tolist(),term_gs_agg.index.values.tolist()))
print(recall(tf_results['term'].tolist(),term_gs_agg.index.values.tolist()))

print(f_measure(t1,t2))
print(f_measure(terms_cvalue_df.index.values.tolist(),term_gs_agg.index.values.tolist()))
print(f_measure(tf_results['term'].tolist(),term_gs_agg.index.values.tolist()))

'''
#print terms[:10]
c_values = term_extractor.c_values(terms, trace=True) #replace this line
my_output = ttf_idf(terms)

with open(out_file, 'wb') as csvfile:
    termwriter = csv.writer(csvfile, delimiter=';', quotechar='', quoting=csv.QUOTE_NONE)
    for cv in c_values:
        termwriter.writerow(cv)

def ttf_idf(terms):
    def tfidf(documents):
        tokenized_documents = [tokenize(d) for d in documents]
        idf = inverse_document_frequencies(tokenized_documents)
        tfidf_documents = []
        for document in tokenized_documents:
            doc_tfidf = []
            for term in idf.keys():
                tf = sublinear_term_frequency(term, document)
                doc_tfidf.append(tf * idf[term])
            tfidf_documents.append(doc_tfidf)
        return tfidf_documents

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values


tf = count(word, document) / len(document)
idf = log( len(collection) / count(document_containing_term, collection)
tf-idf = tf * idf'''
