import ConfigParser
from my_suite_helpers.pdf_reader import read_to_clean
from my_suite_helpers.utils import dataset_genreator, precision, recall, f_measure
from my_suite_helpers.ATE_method import tf
from my_suite_helpers.term_grouping import term_grouping, jaro_sim
from my_suite_helpers.thd import thd
import timeit
import json
import ate
from os import listdir
import pandas as pd
import numpy as np

# GLOBAL
pdf_folder = "data/time"
txt_folder = "data/txt"
clean_txt_folder = "data/clean_txt"
golden_st_path = "hands-on/D22.txt"


reference_file_time = "hands-on/time-onto-paper/MyTimeOnto-Paper-manually-extracted-terms.csv"
terms_gs_df_time = pd.DataFrame.from_csv(reference_file_time, sep=';')
term_gs_agg_time= terms_gs_df_time.groupby(['term'])['num'].agg([np.sum])

terms_gs_df = pd.DataFrame.from_csv(golden_st_path, sep=';')
term_gs_agg = terms_gs_df.groupby(['term'])['num'].agg([np.sum])

orders = ['chrono', 'rev-chrono', 'bi-dir', 'random']
order = 'chrono'
num_input = 2
compare_to_c_value = False # c-value is very slow, so I disabled comparing

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
min_term_length = int(config.get('main', 'min_term_length'))
min_term_words = int(config.get('main', 'min_term_words'))
stopwords = json.loads(config.get('main', 'stopwords'))
term_patterns = json.loads(config.get('main', 'term_patterns'))

term_extractor = ate.TermExtractor(stopwords=stopwords, term_patterns=term_patterns, min_term_words=min_term_words,
                                   min_term_length=min_term_length)

print("Stage 1. Reading from PDF and cleaning") # time = 541.463303506 s
start = timeit.default_timer()
read_to_clean(pdf_folder, clean_txt_folder)
stop = timeit.default_timer()
print("Elapsed time: {} s".format(stop-start))

print("Stage 2. Generating dataset")
start = timeit.default_timer()
dataset = dataset_genreator(order, num_input, clean_txt_folder)
stop = timeit.default_timer()
print("Elapsed time: {} s".format(stop-start))

print("Stage 3. ATE Method")
terms = term_extractor.extract_terms(dataset)
print("Starting ATE on extracted terms...")
start_my_ate = timeit.default_timer()
my_ate_terms_df = tf(terms)
stop_my_ate = timeit.default_timer()
print("Elapsed time for my ATE Method: {} s".format(stop_my_ate - start_my_ate))
if num_input == len([f for f in listdir(clean_txt_folder)]):
    print("Metrics with golden standart from {}".format(golden_st_path))
    print("Precision = {}".format(precision(my_ate_terms_df['term'].tolist(), term_gs_agg.index.values.tolist())))
    print("Recall = {}".format(recall(my_ate_terms_df['term'].tolist(), term_gs_agg.index.values.tolist())))
    print("F measure = {}".format(f_measure(my_ate_terms_df['term'].tolist(), term_gs_agg.index.values.tolist())))

else:
    print("Not enough documents to check precision with GS. \n ")
    # print("Precision = {}".format(precision(my_ate_terms_df['term'].tolist(), term_gs_agg_time.index.values.tolist())))
    # print("Recall = {}".format(recall(my_ate_terms_df['term'].tolist(), term_gs_agg_time.index.values.tolist())))
    # print("F measure = {}".format(f_measure(my_ate_terms_df['term'].tolist(), term_gs_agg_time.index.values.tolist())))
print("")
if compare_to_c_value:
    print("Start measurements for comparison")
    start = timeit.default_timer()
    c_value_terms = term_extractor.c_values(terms, trace=True)
    stop = timeit.default_timer()
    print("Elapsed time for reference c-value Method: {} s".format(stop - start))
    terms_cvalue_df = pd.DataFrame(c_value_terms)
    if num_input == len([f for f in listdir(clean_txt_folder)]):

        print("Metrics with golden standart from {}".format(golden_st_path))
        print("Precision = {}".format(precision(terms_cvalue_df[0].tolist(), term_gs_agg.index.values.tolist())))
        print("Recall = {}".format(recall(terms_cvalue_df[0].tolist(), term_gs_agg.index.values.tolist())))
        print("F measure = {}".format(f_measure(terms_cvalue_df[0].tolist(), term_gs_agg.index.values.tolist())))
    else:
        print("Not enough documents to check precision with GS. \n ")



print("Stage 4. Term grouping")
print("Term length before groupint = {}".format(len(my_ate_terms_df)))
start = timeit.default_timer()
my_grouped_terms_df = term_grouping(my_ate_terms_df)
stop = timeit.default_timer()
print("Term length before groupint = {}".format(len(my_grouped_terms_df)))
print("Elapsed time: {} s".format(stop-start))

print("Stage 5. THD Pipeline")
start = timeit.default_timer()

for order in orders:
    #for grouping in (True, False):
    grouping = False
    terms_list = []
    for inc in range(1,21):
        print("processing inc = {}, {} order, with grouping option {}".format(inc,order, grouping))
        dataset = dataset_genreator(order, inc, clean_txt_folder)
        terms = term_extractor.extract_terms(dataset, verbose=False)
        terms = tf(terms)
        # if grouping:
        #     terms = term_grouping(terms)
        terms_list.append(terms)
    for i in range(19):
        print("thd, thdr measures for D{}-D{}".format(i+1, i+2))
        thd(terms_list[i], terms_list[i+1])

stop = timeit.default_timer()
print("Elapsed time: {} s".format(stop-start))

print("Stage 6. Taxonomy generator")
#output_file =
start = timeit.default_timer()
dataset = dataset_genreator("random", 1, clean_txt_folder)
terms = term_extractor.extract_terms(dataset)#, verbose=False)
terms = tf(terms)

threshold_match = 0.9
threshold_combine = 0.6
to_merge = {}
to_combine = {}
for k in range(len(terms)):
    temp = terms.iloc[[k]]["term"]
    temp2 = terms.iloc[[k]]["term"].tolist()[0]
    term = str(terms.iloc[[k]]["term"].tolist()[0])
    merge_list = []
    combine_list = []
    for j in range(k+1,len(terms)):
        if jaro_sim(str(term), str(terms.iloc[[j]]["term"].tolist()[0])) > threshold_match:
            merge_list.append(str(terms.iloc[[j]]["term"].tolist()[0]))
            terms.drop(terms.index[j])
        elif jaro_sim(str(term), str(terms.iloc[[j]]["term"].tolist()[0])) > threshold_combine:
            combine_list.append(str(terms.iloc[[j]]["term"].tolist()[0]))
    if len(merge_list)>0:
        to_merge[term] = merge_list
    if len(combine_list) > 0:
        to_combine[term] = combine_list
stop = timeit.default_timer()
print("Elapsed time: {} s".format(stop-start))

print(to_merge)
print(to_combine)




f= open("output.txt","w+")
f.write("Please think about merging next terms as they are pretty similar\n")
for key in to_merge.keys():
    f.write("{} with {}\n".format(key, to_merge[key]))
f.write("---------------------------------------------------------\n")
f.write("Please think about combining somehow next terms\n")
for key in to_combine.keys():
    f.write("{} with {}\n".format(key, to_combine[key]))