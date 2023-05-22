from flask import Flask, request, jsonify, render_template
import pickle
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import string
import numpy as np

app = Flask(__name__)


with open('./output.pkl', 'rb') as file:
    headlineData = pickle.load(file)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts=headlineData)
# print(tokenizer.word_index)
loaded_model = tf.keras.saving.load_model("nepali_news_headline_model.hdf5")


print(headlineData[1])
print(headlineData[2])

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
    for word, index in tokenizer.word_index.items():
      if index == predictedIndex:
        seed_text += " " + word

  return seed_text


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = request.form.get('headline')
        headline = generate_headline(data, loaded_model)
        return render_template('index.html', result=headline)
    
    if request.method == 'GET':
       return render_template('index.html')
    
    return "Believe in Yourself!"




if __name__ == "__main__":
    app.run()