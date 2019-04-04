import pymorphy2
import os

morph = pymorphy2.MorphAnalyzer()
files_dir = '/home/dr/PycharmProjects/inform_retrive/scraper/files'
filenames = os.listdir(files_dir)

lemmed_files_dir = '/home/dr/PycharmProjects/inform_retrive/scraper/lemmedFiles'

for filename in filenames:
    with open(os.path.join(files_dir, filename), 'r') as inp:
        with open(os.path.join(lemmed_files_dir, filename), 'w') as out:
            for line in inp:
                for word in line.split():
                    m = morph.parse(word)[0]
                    lem = m.normal_form
                    out.write("%s " %lem)
        out.close()
    inp.close()
