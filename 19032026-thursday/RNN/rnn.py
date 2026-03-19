import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

seperator = f"\n\n{'-' * 100}\n\n"

class KNNmodel:
    def __init__(self):

        self.data = [
            "movie was good",
            "movie was bad",
            "i like this film",
            "i hate this film",
            "this movie is amazing",
            "this movie is terrible",
            "film was nice",
            "film was boring",
            "good acting",
            "bad acting"
        ]

        self.labels = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.tokenize = Tokenizer()
        self.model = None
        self.padded_sequence = None

    def data_preparation(self):

        try:
            print("Data Preparation Started ")
            self.tokenize.fit_on_texts(self.data)

            sequence = self.tokenize.texts_to_sequences(self.data)
            self.padded_sequence = pad_sequences(sequence, padding='post')

            print(f"Word Index :\n {self.tokenize.word_index}")
            print(f"Sequence : \n{sequence}")
            print(f"Padded Sequence : \n{self.padded_sequence}")

            print(f"Data Preparation Done", end=seperator)

        except Exception as e:
            print(f"Data Preparation Failed {e}")

    def model_building(self):

        self.data_preparation()
        try:
            print("Building Model")
            vocab_size = len(self.tokenize.word_index) + 1

            self.model = Sequential([
                Embedding(input_dim=vocab_size, output_dim=8),
                SimpleRNN(16),
                Dense(1, activation='sigmoid')
            ])

            self.model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )

            self.model.summary()

            print("Model Building Completed", end=seperator)

        except Exception as e:
            print(f"Model Building Failed {e}")

    def model_training(self):

        self.model_building()
        try:
            print("Model Training Started")
            self.model.fit(
                self.padded_sequence,
                self.labels,
                epochs=20
            )

        except Exception as e:
            print(f"Model Training Failed {e}")

    def predict(self):
        self.model_training()
        try:
            test = ["movie was amazing"]
            sequence = self.tokenize.texts_to_sequences(test)
            padded = pad_sequences(sequence, padding='post',
                                   maxlen=self.padded_sequence.shape[1])
            predict = self.model.predict(padded)
            print("Prediction : ", predict)

            if predict > 0.5:
                print(f"Sentiment: Positive!")
            else:
                print(f"sentiment: Negative!")

        except Exception as e:
            print(f"Prediction Failed {e}")


def main():
    obj = KNNmodel()
    obj.predict()


if __name__ == "__main__":
    main()