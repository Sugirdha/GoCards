import pandas as pd
from striprtf.striprtf import rtf_to_text
import re


class RTFExtractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_rtf(self):
        """Reads the RTF file and converts it to plain text."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                rtf_content = file.read()
            return rtf_to_text(rtf_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the file: {e}")

    def extract_dataframe(self):
        """Parses the plain text and converts it to a Pandas DataFrame."""
        plain_text = self.read_rtf()
        data = []

        for line in plain_text.splitlines():
            if line.startswith('*{{l|ja|') or line.startswith('*{{l/ja|'):
                parts = line.split('–')
                if len(parts) == 2:
                    japanese, english = parts
                    japanese_parts = japanese.split('}}、')
                    kana = japanese_parts[0].strip('*{{l|ja|').strip('}} ')
                    kanji = ', '.join(part.strip('{{l|ja|').strip('}} ') for part in japanese_parts[1:])\
                        if len(japanese_parts) > 1 else "--"
                    english = english.strip(" ''").strip()
                    data.append({'Kana': kana, 'Kanji': kanji, 'English': english})

        return pd.DataFrame(data)
