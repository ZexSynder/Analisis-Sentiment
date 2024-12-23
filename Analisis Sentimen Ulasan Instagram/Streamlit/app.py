import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load the RandomForest model
with open('RandomForestClassifier.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the TfidfVectorizer
with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

st.title('Sentiment Analysis Instagram Review')
user_input = st.text_area("Input your text here:")

if st.button('Analyze'):
    if user_input:
        # Transform user input using the loaded vectorizer
        input_vectorized = vectorizer.transform([user_input])

        # Convert the sparse matrix to dense
        input_vectorized_dense = input_vectorized.todense()

        # Convert to numpy array
        input_array = np.asarray(input_vectorized_dense)

        # Predict sentiment using the loaded SVM model
        prediction = model.predict(input_array)[0]

        # Display the result
        st.write('Sentiment:', prediction.title())
    else:
        st.warning('Please enter some text for sentiment analysis.')