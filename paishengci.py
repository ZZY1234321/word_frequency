import pandas as pd
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

# 初始化词干提取工具
lemmatizer = WordNetLemmatizer()

def process_word(word):
    """对单词进行词干提取"""
    return lemmatizer.lemmatize(word.lower())

def create_word_groups(excel_paths):
    """读取Excel文件并为相同词源的单词分组"""
    word_groups = defaultdict(list)
    processed_words = set()

    # 读取Excel文件
    for path in excel_paths:
        df = pd.read_excel(path, sheet_name=None)  # 读取所有工作表
        for sheet_name, sheet_data in df.items():
            for col in sheet_data.columns:  # 遍历每一列
                for word in sheet_data[col].dropna():  # 遍历每个单词，忽略NaN值
                    if isinstance(word, str):  # 确保只处理字符串类型的数据
                        root_word = process_word(word)
                        if root_word not in processed_words:
                            word_groups[root_word].append(word)
                            processed_words.add(root_word)
                        else:
                            word_groups[root_word].append(word)

    return word_groups

def export_to_excel(word_groups, output_path):
    """将分组后的结果导出为Excel文件"""
    # 创建 DataFrame，用来存储分组后的单词
    max_group_size = max(len(words) for words in word_groups.values())  # 找到最大组的大小
    data = []
    
    for root_word, words in word_groups.items():
        row = [root_word] + words  # 每行以词源为起点，后跟属于该词源的单词
        data.append(row + [''] * (max_group_size - len(words)))  # 补齐空白单元格
    
    # 创建 DataFrame
    df = pd.DataFrame(data, columns=['Root Word'] + [f"Word {i+1}" for i in range(max_group_size)])
    
    # 导出到Excel文件
    df.to_excel(output_path, index=False)

# 定义文件路径
excel_paths = ["红宝书词表1.xls", "恋练有词.xls"]
output_path = "词源分组结果.xlsx"

# 创建词组
word_groups = create_word_groups(excel_paths)

# 导出到Excel
export_to_excel(word_groups, output_path)

print(f"分组结果已导出到文件: {output_path}")
