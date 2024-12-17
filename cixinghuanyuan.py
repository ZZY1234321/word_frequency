import nltk
from nltk.corpus import wordnet

# 下载 WordNet 数据
nltk.download('wordnet')

def find_lemmas(word):
    synsets = wordnet.synsets(word)
    lemmas = set()
    for synset in synsets:
        for lemma in synset.lemmas():
            lemmas.add(lemma.name())
    return lemmas

# 示例单词
word = "suitable"
lemmas = find_lemmas(word)
print("Lemmas:", lemmas)
