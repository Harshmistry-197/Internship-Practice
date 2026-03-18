import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


seperator = f"\n\n{'-' * 100}\n\n"


class LSTMmodel:

    def __init__(self):

        self.data = None
        self.X = None
        self.y = None
        self.model = None
        self.tokenize = Tokenizer()
        self.max_length = 5

    def load_data(self, input_data):
        print(f"Loading Data\n")
        self.data = pd.DataFrame(input_data)
        print(f"Data Loaded successfully\n {self.data}", end=seperator)

    def preprocessing(self, input_data):

        self.load_data(input_data)

        text = self.data["Review"]
        self.y = self.data['Sentiment']

        self.tokenize.fit_on_texts(text)

        sequence = self.tokenize.texts_to_sequences(text)

        self.X = pad_sequences(sequence, maxlen=self.max_length)

        print(f"Data tokenized successfully\n")
        print(self.X, end=seperator)

    def build_model(self, input_data):

        self.preprocessing(input_data)

        vocab_size = len(self.tokenize.word_index) + 1
        self.model = Sequential()
        self.model.add(Embedding(input_dim=vocab_size, output_dim=8,
                                 input_length=self.max_length))
        self.model.add(LSTM(16))
        self.model.add(Dense(1, activation='sigmoid'))

        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        print(f"Model Created successfully")

    def train_model(self, input_data):

        self.build_model(input_data)
        self.model.fit(self.X, self.y, epochs=20, verbose=1)

    def predict(self, input_data):

        self.train_model(input_data)
        test_text = ['I really love this']

        seq = self.tokenize.texts_to_sequences(test_text)

        padded = pad_sequences(seq, maxlen=self.max_length)

        prediction = self.model.predict(padded)

        print("\nPrediction:")
        print(prediction)

        if prediction > 0.5:
            print("Positive Sentiment")
        else:
            print("Negative Sentiment")


def main():
    data = {
        'Review': [
            'I love this product',
            'This is amazing',
            'Very bad experience',
            'I hate this item',
            'Excellent quality',
            'Worst purchase ever',
            'Really happy with this',
            'Not good at all',
            'Superb performance',
            'Terrible service'
        ],
        'Sentiment': [1, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    }

    obj = LSTMmodel()
    obj.predict(data)


if __name__ == '__main__':
    main()