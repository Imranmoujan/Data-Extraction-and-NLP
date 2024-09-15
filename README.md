# Data Extraction and NLP

This project performs text analysis and NLP on web content, extracting key metrics such as average word length, average sentence length, syllable counts, and readability scores. It uses Python libraries like BeautifulSoup for web scraping and NLTK for text processing.

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
- openpyxl

## Usage

1. Install the required packages using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

2. Download NLTK datasets:

    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

3. Prepare the input data:
   
   - Download the `Input Data Structure.xlsx` file place it in the same folder as `main.py`. This file should contain all the web links to be scraped.

4. Run the main script:

    ```bash
    python main.py
    ```

5. The script will scrape the specified web pages, perform text analysis, and output the results.

6. The results will be saved in `Output Data Structure.xlsx`, which contains the analyzed data in a structured format.

## Project Structure

- `main.py`: The main script containing all functions for web scraping, text processing, and analysis.
- `Input Data Structure.xlsx`: Excel file containing all the links to be processed.
- `Output Data Structure.xlsx`: Excel file where the resulting data frame with analysis results is saved.
- `txtfiles/`: Directory where scraped text files are saved.
- `requirements.txt`: Lists all the dependencies required to run the project.
