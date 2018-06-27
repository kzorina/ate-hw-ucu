import ate

from os import listdir, remove
from os.path import isfile, join
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def read_to_clean(pdf_folder, clean_txt_folder):
    pdf_files = sorted(
        [(pdf_folder, f) for f in listdir(pdf_folder) if isfile(join(pdf_folder, f)) and f.lower().endswith(".pdf")])

    for f in pdf_files:

        try:
            # removing only hyphens in the end of line
            text = ate.pdf_to_text_textract(join(f[0], f[1])).replace("-\n","").replace("\n", " ")
            text = unicode(text, "utf-8", errors='ignore')
            text = re.sub(r'et +al\.', 'et al', text)
            text = re.split(r'[\r\n]', text)
            sent_tokenize_list = filter(lambda x: len(x) > 0, map(lambda s: nltk.tokenize.sent_tokenize(s), text))
            sentences = []
            _ = [sentences.extend(lst) for lst in sent_tokenize_list]
            fpath_out = join(clean_txt_folder, f[1][:-4] + '.txt')
            ftxt = open(fpath_out, 'w')
            for sentence in sentences:
                ftxt.write(sentence.encode('utf-8') + " ")
        except TypeError:
            print ("error reading file {}. Skipping it".format(f))
            #remove(fpath_out)

def read_from_pdf(pdf_dir, txt_dir):
    pdf_files = sorted(
        [(pdf_dir, f) for f in listdir(pdf_dir) if isfile(join(pdf_dir, f)) and f.lower().endswith(".pdf")])
    # print pdf_files
    for f in pdf_files:

        fpath_out = join(txt_dir, f[1][:-4] + '.txt')
        #print pdf_dir, '/', f[1], "=>", fpath_out
        ftxt = open(fpath_out, 'w')
        try:
            ftxt.write(ate.pdf_to_text_textract(join(f[0], f[1])).replace("\n", " "))
        except TypeError:
            print ("error reading file {}. Skipping it".format(fpath_out))

        ftxt.close()


def dehypn_and_sent_per_line(txt_dir, clean_txt_dir):
    text_files = [f for f in listdir(txt_dir)]
    for file in text_files:
        with open(join(txt_dir, file)) as txt_file:
            with open(join(clean_txt_dir,file), 'w') as out_file:
                text = txt_file.read().replace("-\n","")
                text = unicode(text, "utf-8", errors='ignore')
                text = re.sub(r'et +al\.', 'et al', text)
                text = re.split(r'[\r\n]', text)
                sent_tokenize_list = filter(lambda x: len(x) > 0, map(lambda s: nltk.tokenize.sent_tokenize(s), text))
                sentences = []
                _ = [sentences.extend(lst) for lst in sent_tokenize_list]
                for sentence in sentences:
                    out_file.write(sentence.encode('utf-8') + " ")

def check_legatures(txt_dir):
    text_files = [f for f in listdir(txt_dir)]
    for file in text_files:
        with open(join(txt_dir, file)) as txt_file:
            for line in txt_file:
                for char in line:
                    if char in gliph_list:
                        print(char)
gliph_list = [
u'\uA732',
u'\u00C6',
u'\uA734',
u'\uA736',
u'\uA738',
u'\uA73A',
u'\uA73C',
u'\u1F670',
u'\uFB00',
u'\uFB03',
u'\uFB04',
u'\uFB01',
u'\uFB02',
u'\u0152',
u'\uA74E',
u'\u1E9E',
u'\uFB06',
u'\uFB05',
u'\uA728',
u'\u1D6B',
u'\uA760',
 u'\uA733',
 u'\u00E6',
 u'\uA735',
 u'\uA737',
 u'\uA739',
 u'\uA73B',
 u'\uA73D',
 u'\u0153',
 u'\uA74F',
 u'\u00DF',
 u'\uA729',
 u'\uA761'
]