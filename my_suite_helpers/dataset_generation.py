from os import listdir
from os.path import join
import random
import re



def dataset_genreator(order, num_input, clean_txt_dir):
    print("Getting {} docs in {} order".format(num_input, order))
    text_files = [f for f in listdir(clean_txt_dir)]
    if (order == 'chrono'):
        to_process = text_files[:num_input]
    elif (order == 'rev-chrono'):
        to_process = text_files[-num_input:]
    elif (order == 'bi-dir'):
        to_process = text_files[:int(num_input/2)]
        to_process += text_files[-(num_input-int(num_input/2)):]
    elif (order == 'random'):
        indexes = random.sample(range(0, len(text_files)), num_input)
        to_process = []
        for ind in indexes:
            to_process.append(text_files[ind])

    else:
        print("Unknown order option")
    # print(to_process)
    large_text = ""
    for file in to_process:

        with open(join(clean_txt_dir, file)) as txt_file:
            #print("File {}".format(file))
            text = txt_file.read()
            large_text += text
    large_text = unicode(large_text, "utf-8", errors='ignore')
    large_text = re.sub(r'et +al\.', 'et al', large_text)
    large_text = re.split(r'[\r\n]', large_text)
    return large_text