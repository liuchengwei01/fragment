import os
import re

def extract_words(file_path, lower=False, encoding='utf-8'):
    try:
        file_size = os.path.getsize(file_path)

        # 如果文件小于 5MB，一次性读取
        if file_size < 5 * 1024 * 1024:  # 5MB
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
                words = re.findall(r"\b(?!\w*\d\w*\d)\w(?:[\w'-]*\w)?\b", text.lower() if lower else text)
                for word in words:
                    yield word
        else:
            # 对于大于 5MB 的文件，逐行读取
            with open(file_path, 'r', encoding=encoding) as file:
                for line in file:
                    words = re.findall(r"\b(?!\w*\d\w*\d)\w(?:[\w'-]*\w)?\b", line.lower() if lower else line)
                    for word in words:
                        yield word

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except (IOError, PermissionError, UnicodeDecodeError) as e:
        print(f"Error when accessing file: {file_path}. Error: {e}")

    
def load_words_and_overwrite_if_changed(file_path, encoding='utf-8'):
    unique_words = set()
    try:
        words = list(extract_words(file_path, encoding=encoding))
        unique_words = set(words)  # 使用集合去重

        # 检查去重是否改变了单词数量
        if len(unique_words) < len(words):
            # 由于数组长度有变化，将去重后的单词写回文件
            with open(file_path, 'w', encoding=encoding) as file:
                for word in sorted(unique_words):
                    file.write(word + '\n')

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return unique_words

def book_new_words(book_file_path, words, new_words, output_file_path, encoding='utf-8'):
    try:
        new_words_set = set(extract_words(book_file_path, lower=True, encoding=encoding))
        new_words = new_words_set - words - new_words

        if new_words:
            with open(output_file_path, 'a', encoding=encoding) as file:
                for word in new_words:
                    file.write(word + '\n')
                    
    except FileNotFoundError:
        print(f"File not found: {book_file_path}")
    except (IOError, PermissionError, UnicodeDecodeError) as e:
        print(f"Error when accessing file: {book_file_path}. Error: {e}")


# 示例使用
words_file_path = r"C:\Users\lenovo\Desktop\words.txt"
output_file_path = r"C:\Users\lenovo\Desktop\new_words.txt" 
book_file_path = r"C:\Users\lenovo\Desktop\book.txt"

words = load_words_and_overwrite_if_changed(words_file_path)
new_words = load_words_and_overwrite_if_changed(output_file_path)

book_new_words(book_file_path, words, new_words, output_file_path)
