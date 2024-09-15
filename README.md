# Data Extraction and NLP

This project performs text analysis and nlp on web content, extracting key metrics such as average word length, average sentence length, syllable counts, and readability scores. It uses Python libraries like BeautifulSoup for web scraping and NLTK for text processing.

## Features

- **Web Scraping**: Extracts text content from web pages using BeautifulSoup.
- **Text Processing**: Tokenizes text and removes stopwords using NLTK.
- **Text Analysis**: Calculates average word length, sentence length, syllable counts, and complex word counts.
- **Readability Analysis**: Analyzes text readability based on sentence length and complexity.

## Requirements

- Python 3.x
- pandas
- requests
- nltk
- BeautifulSoup4

## Usage

1. Download NLTK datasets:

    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

2. Run the main script:

    ```bash
    python main.py
    ```

3. The script will scrape the specified web page, perform text analysis, and output the results.

## Project Structure

- `main.py`: The main script containing all functions for web scraping, text processing, and analysis.
- `txtfiles/`: Directory where scraped text files are saved.
