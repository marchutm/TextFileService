import re
from langdetect import detect
from collections import Counter


class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.content = file.read()

    def count_text_statistics(self):
        num_lines = self.content.count('\n')
        num_words = len(self.content.split())
        num_chars = len(self.content)
        return num_lines, num_words, num_chars

    def search_emails(self):
        pattern = r'[\w\.-]+@[\w\.-]+'
        emails = re.findall(pattern, self.content)
        return emails

    def detect_language(self):
        try:
            language = detect(self.content)
            return language
        except Exception as e:
            print("Error while detecting the language: ", e)
            return None

    def count_letter_frequency(self):
        count_lower = self.content.lower()
        letter_count = Counter(c for c in count_lower if c.isalpha())
        total_letters = sum(letter_count.values())
        letter_frequency = {letter: count / total_letters for letter, count in letter_count.items()}
        return letter_frequency

    def get_data_summary(self):
        try:
            text_statistics = self.count_text_statistics()
            emails = self.search_emails()
            language = self.detect_language()
            letter_frequency = self.count_letter_frequency()

            data_summary = {
                'text_statistics': {
                    'num_lines': text_statistics[0],
                    'num_words': text_statistics[1],
                    'num_chars': text_statistics[2]
                },
                'language': language,
                'emails': emails,
                'letter_frequency': letter_frequency,
            }

            return data_summary
        except Exception as e:
            print("Error generating data summary for text file:", e)
            return None
