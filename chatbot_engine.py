import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
import random
import json
import pickle
import os

stemmer = LancasterStemmer()

class ChatbotEngine:
    def __init__(self, intents_path='intents.json', model_path='model.h5', data_path='training_data.pkl'):
        self.intents_path = intents_path
        self.model_path = model_path
        self.data_path = data_path
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?']
        self.model = None
        self.intents = None
        self.context = {}

        # Ensure NLTK data is downloaded
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt')
            nltk.download('punkt_tab')

    def load_intents(self):
        with open(self.intents_path) as file:
            self.intents = json.load(file)

    def prepare_data(self):
        self.load_intents()
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    def train(self):
        self.prepare_data()
        training = []
        output_empty = [0] * len(self.classes)

        for doc in self.documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        # Build Model
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile Model
        sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # Fit & Save
        model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save(self.model_path)
        
        # Save training data
        with open(self.data_path, 'wb') as f:
            pickle.dump({'words': self.words, 'classes': self.classes}, f)
        
        self.model = model

    def load_all(self):
        if not os.path.exists(self.model_path):
            self.train()
        else:
            self.model = load_model(self.model_path)
            with open(self.data_path, 'rb') as f:
                data = pickle.load(f)
                self.words = data['words']
                self.classes = data['classes']
            self.load_intents()

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
        return np.array(bag)

    def classify(self, sentence):
        ERROR_THRESHOLD = 0.25
        p = self.bow(sentence)
        res = self.model.predict(np.array([p]))[0]
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, sentence, userID='123'):
        results = self.classify(sentence)
        if results:
            while results:
                for i in self.intents['intents']:
                    if i['tag'] == results[0]['intent']:
                        # Context handling logic
                        if 'context_set' in i:
                            self.context[userID] = i['context_set']

                        if not 'context_filter' in i or \
                           (userID in self.context and 'context_filter' in i and i['context_filter'] == self.context[userID]):
                            return random.choice(i['responses'])

                results.pop(0)
        return "I'm sorry, I don't quite understand that. Could you rephrase?"

if __name__ == "__main__":
    engine = ChatbotEngine()
    engine.train()
