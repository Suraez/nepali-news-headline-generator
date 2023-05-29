import tensorflow as tf
import pickle
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import string
import numpy as np
import streamlit as st

with open('./output.pkl', 'rb') as file:
    headlineData = pickle.load(file)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts=headlineData)
# print(tokenizer.word_index)
loaded_model = tf.keras.saving.load_model("nepali_news_headline_model.hdf5")

def get_padded_sequence(seed_text):
  # cleaning the sentence
  sentence = seed_text.translate(str.maketrans('', '', string.punctuation))
  sentence = ' '.join(sentence.split())
  #generate sequence of known words in the vocabulary
  sentence_sequence = tokenizer.texts_to_sequences([sentence])[0]
  maxLengthDataSequence = 13 # hard-coded needs to be changed later
  padding_size = maxLengthDataSequence - len(sentence_sequence) - 1
  padding = [0] * padding_size
  sentence_sequence[:0] = padding
  return sentence_sequence

def generate_headline(seed_text, model):
  while len(seed_text.split(' ')) < 10:
    textPaddedSequence = get_padded_sequence(seed_text)
    predictedIndex = np.argmax(model.predict([textPaddedSequence], verbose=0))
    if predictedIndex > len(tokenizer.word_index):
       seed_text += ' विषय'
    else: 
      for word, index in tokenizer.word_index.items():
        if index == predictedIndex:
          seed_text += " " + word
          break

  return seed_text


# Create a text input field
st.title("Nepali Text Generator")
user_input = st.text_input("Please provide some context as given in the examples below: ")
st.text("Examples: काम नगर्ने ठेकेदारलाई, सर्पदंशका बिरामीलाई, दलित र सीमान्त")
if st.button("Generate"):
  generated = generate_headline(user_input, loaded_model)
  st.subheader("Generated Headline: " + generated)