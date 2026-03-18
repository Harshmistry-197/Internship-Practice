import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


seperator = f"\n\n{'-' * 100}\n\n"


class LSTMmodel:
    """
    A class to perform sentiment analysis using an LSTM neural network.

    Attributes:
        data (pd.DataFrame): The input text and labels.
        X (numpy.ndarray): Padded numerical sequences of text.
        y (pd.Series): Sentiment labels.
        model (Sequential): The Keras LSTM model.
        tokenize (Tokenizer): Keras Tokenizer instance for text-to-number mapping.
        max_length (int): Maximum length of input sequences.
    """

    def __init__(self):
        """Initializes the LSTMmodel with default parameters."""

        self.data = None
        self.X = None
        self.y = None
        self.model = None
        self.tokenize = Tokenizer()
        self.max_length = 5

    def load_data(self, input_data):
        """Converts raw dictionary data into a pandas DataFrame."""

        print(f"Loading Data\n")
        self.data = pd.DataFrame(input_data)
        print(f"Data Loaded successfully\n {self.data}", end=seperator)

    def preprocessing(self, input_data):
        """
        Tokenizes text data and pads sequences to a fixed length.

        Args:
            input_data (dict): Dictionary containing 'Review' and 'Sentiment' keys.
        """

        self.load_data(input_data)

        text = self.data["Review"]
        self.y = self.data['Sentiment']

        # Update the internal vocabulary based on the text
        self.tokenize.fit_on_texts(text)

        # Convert text strings to lists of integer IDs
        sequence = self.tokenize.texts_to_sequences(text)

        self.X = pad_sequences(sequence, maxlen=self.max_length)

        print(f"Data tokenized successfully\n")
        print(self.X, end=seperator)

    def build_model(self, input_data):
        """
        Defines the LSTM architecture and compiles the model.

        Args:
            input_data (dict): Training data used to trigger preprocessing.
        """

        self.preprocessing(input_data)

        # Calculate vocab size (word count + 1 for padding)
        vocab_size = len(self.tokenize.word_index) + 1
        self.model = Sequential()

        # Embedding: Turns word IDs into dense vectors of fixed size (8)
        self.model.add(Embedding(input_dim=vocab_size, output_dim=8,
                                 input_length=self.max_length))

        # LSTM: Learns the relationship between words in a sequence
        self.model.add(LSTM(16))

        # Dense: Output layer with Sigmoid to get a probability between 0 and 1
        self.model.add(Dense(1, activation='sigmoid'))

        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        print(f"Model Created successfully")

    def train_model(self, input_data):
        """Trains the compiled LSTM model on the provided data."""

        self.build_model(input_data)

        # Train for 20 iterations through the dataset
        self.model.fit(self.X, self.y, epochs=20, verbose=1)

    def predict(self, input_data):
        """
        Trains the model and performs a prediction on a sample string.

        Args:
            input_data (dict): Data used for training before prediction.
        """

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
    """Main execution point: defines dataset and runs the model pipeline."""

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