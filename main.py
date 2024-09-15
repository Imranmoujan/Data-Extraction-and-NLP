import pandas as pd
import re
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
import os
import warnings

warnings.filterwarnings("ignore")

nltk.download('punkt')
nltk.download("stopwords")

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Extracting and Saving Scrap Text
def textfile(url, name, r):
    ensure_folder_exists("txtfiles") 

    file_path = f"txtfiles/{name}.txt"
    with open(file_path, "w+", encoding='utf-8') as file:
        soup = BeautifulSoup(r.content, 'html.parser')
        
        content = soup.find_all(class_="td-post-content tagdiv-type")
        headers = soup.find_all("h1", class_="entry-title")
        
        row_text = [header.get_text() for header in headers]
        
        for section in content:
            for link in section.find_all('a', href=True):
                link.decompose() 
            row_text.append(re.sub(r'https?://\S+|www\.\S+', " ", section.get_text()))
        
        row_text = "\n".join(row_text)
        file.write(row_text)

    return row_text

# Average Word Length
def calculate_average_word_length(row_text):
    row_words = word_tokenize(row_text)
    row = []
    char_count = 0
    for word in row_words:
        cleaned_word = re.sub(r"\W|\d|\s", "", word)
        row.append(cleaned_word)
    row_words = list(filter(lambda word: word.strip() != "", row))
    row_words_count = len(row_words)
    for word in row_words:
        char_count += len(word)
    average_word_length = round(char_count / row_words_count) if row_words_count > 0 else 0
    return row_words, row_words_count, average_word_length

# Average Number of Words Per Sentence and Average Sentence Length
def average_number_of_words_per_sentence(row_text, row_words_count):
    sentences = sent_tokenize(row_text)
    sentences_count = len(sentences)
    average_words_per_sentence = round(row_words_count / sentences_count) if sentences_count > 0 else 0
    average_sentence_length = round(average_words_per_sentence)
    return sentences, sentences_count, average_words_per_sentence, average_sentence_length

# Syllable and Complex Word Count
def syllable_and_complex_word_count(words):
    syllable_count = []
    complex_word_count = 0
    vowels = set("aeiou")
    
    for word in words:
        count = sum(1 for char in word.lower() if char in vowels)
        if word.endswith("ed") or word.endswith("es"):
            count = max(count - 1, 1)
        if count > 2:
            complex_word_count += 1
        syllable_count.append(count)
    
    return syllable_count, complex_word_count

# Personal Pronouns
def personal_pronouns(words):
    pp_list = set(["I", "We", "My", "Our", "Us", "i", "we", "my", "ours", "us"])
    return sum(1 for word in words if word in pp_list)

# Analysis of Readability
def analysis_of_readability(average_sentence_length, complex_word_count, row_words_count):
    percentage_of_complex_words = complex_word_count / row_words_count if row_words_count > 0 else 0
    fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words * 100)
    return percentage_of_complex_words, fog_index

# Sentimental Analysis
def sentimental_analysis(words):
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    words_count = len(filtered_words)

    negative_words = pd.read_csv("MasterDictionary/negative-words.txt", encoding='latin1', header=None)[0].tolist()
    positive_words = pd.read_csv("MasterDictionary/positive-words.txt", header=None)[0].tolist()

    negative_score = sum(1 for word in filtered_words if word in negative_words)
    positive_score = sum(1 for word in filtered_words if word in positive_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (words_count + 0.000001)
    
    return words_count, negative_score, positive_score, polarity_score, subjectivity_score

# Main Process
df = pd.read_excel("Input Data Structure.xlsx")

for i in range(len(df.URL)):
    url = df["URL"][i]
    try:
        r = requests.get(url)
        status_code = r.status_code
        
        if status_code == 200:
            row_text = textfile(url, df["URL_ID"][i], r)
            row_words, row_words_count, average_word_length = calculate_average_word_length(row_text)
            sentences, sentence_count, average_words_per_sentence, average_sentence_length = average_number_of_words_per_sentence(row_text, row_words_count)
            syllable_count_per_word, complex_word_count = syllable_and_complex_word_count(row_words)
            pp_count = personal_pronouns(row_words)
            percentage_of_complex_words, fog_index = analysis_of_readability(
                average_sentence_length, complex_word_count, row_words_count)
            words_count, negative_score, positive_score, polarity_score, subjectivity_score = sentimental_analysis(row_words)
            
            # Updating DataFrame
            df.at[i, 'POSITIVE SCORE'] = positive_score
            df.at[i, 'NEGATIVE SCORE'] = negative_score
            df.at[i, 'POLARITY SCORE'] = polarity_score
            df.at[i, 'SUBJECTIVITY SCORE'] = subjectivity_score
            df.at[i, 'AVG SENTENCE LENGTH'] = average_sentence_length
            df.at[i, 'PERCENTAGE OF COMPLEX WORDS'] = percentage_of_complex_words
            df.at[i, 'FOG INDEX'] = fog_index
            df.at[i, 'AVG NUMBER OF WORDS PER SENTENCE'] = average_words_per_sentence
            df.at[i, 'COMPLEX WORD COUNT'] = complex_word_count
            df.at[i, 'WORD COUNT'] = words_count
            df.at[i, 'SYLLABLE PER WORD'] = str(syllable_count_per_word)
            df.at[i, 'PERSONAL PRONOUNS'] = pp_count
            df.at[i, 'AVG WORD LENGTH'] = average_word_length
            
            print(f"Processed URL index: {i}")
    except requests.RequestException as e:
        print(f"Request error for URL {url}: {e}")

df.to_excel("Output Data Structure.xlsx", index=False)
