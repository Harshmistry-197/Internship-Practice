import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

seperator = f"\n\n{'-' * 100}\n\n"

class RNNmodel:
    """
    Initializes the dataset.
    1 is Positive Sentiment, 0 is Negative Sentiment.
    """

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

        # Initialize Tokenizer and placeholders for data and model
        self.tokenize = Tokenizer()
        self.model = None
        self.padded_sequence = None

    def data_preparation(self):
        """
        Converts raw text into numeric sequences and pads them to a uniform length.
        """

        try:
            print("Data Preparation Started ")

            # Create a vocabulary index based on word frequency
            self.tokenize.fit_on_texts(self.data)

            # Convert sentences into lists of integers (sequences)
            sequence = self.tokenize.texts_to_sequences(self.data)

            # Pad sequences with zeros at the end so all inputs have the same length
            self.padded_sequence = pad_sequences(sequence, padding='post')

            print(f"Word Index :\n {self.tokenize.word_index}")
            print(f"Sequence : \n{sequence}")
            print(f"Padded Sequence : \n{self.padded_sequence}")

            print(f"Data Preparation Done", end=seperator)

        except Exception as e:
            print(f"Data Preparation Failed {e}")

    def model_building(self):
        """
        Created the Neural Network architecture: Embedding -> RNN -> Dense.
        """

        self.data_preparation()
        try:
            print("Building Model")

            # vocab_size is total words + 1 (to account for the 0-padding index)
            vocab_size = len(self.tokenize.word_index) + 1

            self.model = Sequential([
                # Turns integers into dense vectors of fixed size (8)
                Embedding(input_dim=vocab_size, output_dim=8, input_shape=(4,)),

                # Simple Recurrent layer to process sequence data with 16 units
                SimpleRNN(16),

                # Output layer with Sigmoid for binary classification (0 to 1)
                Dense(1, activation='sigmoid')
            ])

            # Compile with Adam optimizer and Binary Cross-entropy loss
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
        """
        Trains the model on the prepared padded sequences Data.
        """

        self.model_building()
        try:
            # Training the model for 20 iterations over the dataset
            print("Model Training Started")
            self.model.fit(
                self.padded_sequence,
                self.labels,
                epochs=20
            )

        except Exception as e:
            print(f"Model Training Failed {e}")

    def predict(self):
        """
        Preprocesses a new test string and predicts its sentiment.
        """

        self.model_training()
        try:
            test = ["movie was amazing"]

            # Transform test text using the SAME tokenizer used for training
            sequence = self.tokenize.texts_to_sequences(test)

            # Pad to match the exact input length the model expects
            padded = pad_sequences(sequence, padding='post',
                                   maxlen=self.padded_sequence.shape[1])

            # Generate prediction (a value between 0 and 1)
            predict = self.model.predict(padded)
            print("Prediction : ", predict)

            if predict > 0.5:
                print(f"Sentiment: Positive!")
            else:
                print(f"sentiment: Negative!")

        except Exception as e:
            print(f"Prediction Failed {e}")


def main():
    """
    Entry point of code.
    """

    obj = RNNmodel()
    obj.predict()


if __name__ == "__main__":
    main()