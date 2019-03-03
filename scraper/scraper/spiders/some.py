import pymorphy2
import os

morph = pymorphy2.MorphAnalyzer()
filesDir = '/home/dr/PycharmProjects/inform_retrive/scraper/files'
names = os.listdir(filesDir)

lemmedFilesDir = '/home/dr/PycharmProjects/inform_retrive/scraper/lemmedFiles'

for name in names:
    with open(os.path.join(filesDir, name), 'r') as inp:
        with open(os.path.join(lemmedFilesDir, name), 'w') as out:
            for line in inp:
                for word in line.split():
                    m = morph.parse(word)[0]
                    lem = m.normal_form
                    out.write("%s " %lem)
        out.close()
    inp.close()
