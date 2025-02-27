import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    # Remove links
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove symbols (except alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove newline characters
    text = text.replace('\n', ' ')
    # Tokenize and remove stopwords
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_text = ' '.join([word for word in words if word.lower() not in stop_words])
    
    return filtered_text

def process_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Assuming JSON file contains a list of dictionaries with a 'text' field
    for entry in data:
        if 'text' in entry:
            entry['text'] = clean_text(entry['text'])
        # Remove 'people_also_viewed' and 'similar_profiles' arrays if they exist
        entry.pop('people_also_viewed', None)
        entry.pop('similar_profiles', None)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Example usage
input_file = 'data\\isatyamks.json'  # Replace with your file
output_file = 'data\\isatyamks.json'
process_json(input_file, output_file)
