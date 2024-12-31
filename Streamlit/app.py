import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
import pandas as pd

# Fungsi untuk membersihkan teks
def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r'http\S+|www\S+|https\S+', ' ', teks, flags=re.MULTILINE)
    teks = re.sub(r'[^\x00-\x7F]+', ' ', teks)
    teks = re.sub(r'[^a-zA-Z0-9\s]', ' ', teks)
    teks = re.sub(r'\d+', ' ', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks

# Fungsi penggantian kata tidak baku
def replace_taboo_words(text, kamus_tidak_baku):
    words = text.split()
    replaced_words = [kamus_tidak_baku[word] if word in kamus_tidak_baku else word for word in words]
    return ' '.join(replaced_words)

# Menghapus stopwords
def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# Load kamus tidak baku
try:
    kamus_data = pd.read_excel("../kamusslag.xlsx")
    kamus_tidak_baku = dict(zip(kamus_data['kata_tidak_baku'], kamus_data['kata_baku']))
except FileNotFoundError:
    st.error("File kamus tidak ditemukan. Pastikan file 'kamusslag.xlsx' ada di direktori yang sesuai.")
    kamus_tidak_baku = {}

# Load stop words
stop_words = set(stopwords.words('indonesian'))

# Load model dan vectorizer
try:
    with open('RandomForestClassifier.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    st.error("Model file tidak ditemukan. Pastikan 'RandomForestClassifier.pkl' ada di direktori yang sesuai.")

try:
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
except FileNotFoundError:
    st.error("Vectorizer file tidak ditemukan. Pastikan 'vectorizer.pkl' ada di direktori yang sesuai.")

# Streamlit UI
st.title('Sentiment Analysis Instagram Review')
user_input = st.text_area("Input your text here:")

if st.button('Analyze'):
    if user_input:
        # Preprocessing input
        clean_text = bersihkan_teks(user_input)
        normalized_text = replace_taboo_words(clean_text, kamus_tidak_baku)
        final_text = remove_stopwords(normalized_text)

        # Transform user input using the loaded vectorizer
        input_vectorized = vectorizer.transform([final_text])

        # Predict sentiment using the loaded model
        prediction = model.predict(input_vectorized)[0]

        # Display the result
        st.write('Sentiment:', prediction.title())
    else:
        st.warning('Please enter some text for sentiment analysis.')