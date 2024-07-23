import PyPDF2
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess_text(text):
    # 去除号码和符号
    text = re.sub(r'\d+', '', text)  # 去除数字
    text = re.sub(r'\W', ' ', text)  # 去除非字母数字字符，替换为空格

    # 将文本转换为小写
    text = text.lower()

    return text


def extract_text_from_pdf(pdf_path):
    text_dict = {}
    stop_words = set(stopwords.words('english'))

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_number in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_number)
            text = page.extractText()

            # 预处理文本
            text = preprocess_text(text)

            # 过滤停用词
            words = [word.strip() for word in text.split() if word.strip() and word not in stop_words]

            # 将每个词添加到词典中
            for word in words:
                text_dict[word] = text_dict.get(word, 0) + 1

    return text_dict


# 指定PDF文件路径
pdf_path = 'C:\\Users\\tan04\\Downloads\\Sapiens-A-Brief-History-of-Humankind.pdf'

# 调用函数并获取词典
word_dict = extract_text_from_pdf(pdf_path)

# 打印词典内容
for word, count in word_dict.items():
    print(f'{word}: {count}')
print(len(word_dict))