import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from collections import defaultdict

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('omw-1.4', quiet=True)

def preprocess_text(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # 移除所有非ASCII字符
    text = re.sub(r'\b[A-D]\)\s*', ' ', text)   # 移除形如"A) "的选项
    text = re.sub(r'\d+', ' ', text)            # 移除数字
    text = text.lower()                         # 转换为小写
    return text

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # 默认作为名词处理

def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    pos_tags = pos_tag(tokens)
    lemmatized = []
    for token, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos)
        lemma = lemmatizer.lemmatize(token, wordnet_pos)
        lemmatized.append((lemma, token))
    return lemmatized

def count_word_frequency(lemmatized_tokens):
    frequencies = defaultdict(int)
    for lemma, token in lemmatized_tokens:
        frequencies[lemma] += 1
    return frequencies

def read_word_list(excel_path):
    df = pd.read_excel(excel_path, header=None)
    words = set()
    for col in df.columns:
        for item in df[col]:
            if isinstance(item, str):
                clean_word = item.strip().lower()
                if clean_word:
                    words.add(clean_word)
    return words

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    preprocessed_text = preprocess_text(text)
    return preprocessed_text

def build_word_dict(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = lemmatize_tokens(tokens)
    frequencies = count_word_frequency(lemmatized_tokens)
    return frequencies

def search_word(word, word_dict):
    related_words = {}
    for (lemma, token), freq_list in word_dict.items():
        if lemma == word:
            related_words[token] = sum(freq_list)
    return related_words

def main():
    # 文件路径
    hongbaoshu_path = '红宝书词表1.xls'
    lianlian_path = '恋练有词.xls'
    true_file_paths = [
        '（2005-2023）四级合并（UTF8）.txt',
        '（2005-2023）六级合并（UTF8）.txt',
        '1998-2024合并（英一）（UTF8）.txt',
        '2001-2023英二合并（UTF8）.txt'
    ]

    # 读取词表
    hongbaoshu_words = read_word_list(hongbaoshu_path)
    lianlian_words = read_word_list(lianlian_path)

    # 输入要查找的单词
    search_word_input = input("请输入要查找的单词: ").strip().lower()

    # 读取并预处理文本
    texts = [read_text(path) for path in true_file_paths]
    text_dicts = [build_word_dict(text) for text in texts]

    # 在红宝书词表中查找词频
    hongbaoshu_text = ' '.join(hongbaoshu_words)
    hongbaoshu_dict = build_word_dict(hongbaoshu_text)

    # 在恋练有词词表中查找词频
    lianlian_text = ' '.join(lianlian_words)
    lianlian_dict = build_word_dict(lianlian_text)

    # 在红宝书中查找
    hongbaoshu_result = search_word(search_word_input, hongbaoshu_dict)
    if hongbaoshu_result:
        print(f"红宝书中'{search_word_input}'相关词形变换的出现次数：")
        for w, freq in hongbaoshu_result.items():
            print(f"  {w}: {freq} 次")
    else:
        print(f"红宝书中未收录'{search_word_input}'。")

    # 在恋练有词中查找
    lianlian_result = search_word(search_word_input, lianlian_dict)
    if lianlian_result:
        print(f"恋练有词中'{search_word_input}'相关词形变换的出现次数：")
        for w, freq in lianlian_result.items():
            print(f"  {w}: {freq} 次")
    else:
        print(f"恋练有词中未收录'{search_word_input}'。")

    # 在真题文件中查找
    for i, path in enumerate(true_file_paths):
        result = search_word(search_word_input, text_dicts[i])
        if result:
            print(f"在'{path}'中'{search_word_input}'相关词形变换的出现次数：")
            for w, freq in result.items():
                print(f"  {w}: {freq} 次")
        else:
            print(f"'{path}'中未找到'{search_word_input}'的相关词形变换。")

if __name__ == "__main__":
    main()
