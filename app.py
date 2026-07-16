import streamlit as st
import pickle as pkl
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

# Download required NLTK resources (runs only once)
nltk.download("punkt")
nltk.download("stopwords")

# Initialize stemmer
ps = PorterStemmer()


# Text preprocessing function
def transform_text(text):
    # Convert to lowercase
    text = text.lower()

    # Tokenize
    text = nltk.word_tokenize(text)

    # Keep only alphanumeric words
    y = []
    for word in text:
        if word.isalnum():
            y.append(word)

    text = y[:]
    y.clear()

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words("english"))
    for word in text:
        if word not in stop_words and word not in string.punctuation:
            y.append(word)

    text = y[:]
    y.clear()

    # Stemming
    for word in text:
        y.append(ps.stem(word))

    return " ".join(y)


# Load the trained model and vectorizer
with open("vectorizer.pkl", "rb") as f:
    tfidf = pkl.load(f)

with open("model.pkl", "rb") as f:
    model = pkl.load(f)


# Streamlit UI
st.set_page_config(
    page_title="Spam Classifier",
    page_icon="📧",
    layout="centered"
)

st.title("📧 Email/SMS Spam Classifier")
st.write("Enter an Email or SMS message below to check whether it is **Spam** or **Not Spam**.")

# User input
input_sms = st.text_area("Enter your message")

# Prediction button
if st.button("Predict"):

    if input_sms.strip() == "":
        st.warning("Please enter a message.")
    else:
        # 1. Preprocess
        transformed_sms = transform_text(input_sms)

        # 2. Vectorize
        vector_input = tfidf.transform([transformed_sms])

        # 3. Predict
        prediction = model.predict(vector_input)[0]

        # 4. Display result
        if prediction == 1:
            st.error("🚨 SPAM Message")
        else:
            st.success("✅ NOT SPAM Message")