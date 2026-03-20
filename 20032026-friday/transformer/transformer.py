import tensorflow as tf
from tensorflow.keras import layers
import numpy as np


class Tokenizer:
    """Handles basic word-level tokenization and vocabulary mapping.

    Attributes:
        word2idx (dict): Maps words to unique integer IDs.
        idx 2 word (dict): Maps integer IDs back to words.
        vocab_size (int): Total number of unique words in the vocabulary.
    """

    def __init__(self, texts):
        """Initializes the tokenizer by building a vocabulary from provided texts."""

        all_text = " ".join(texts)
        self.words = sorted(set(all_text.split()))
        self.word2idx = {w: i for i, w in enumerate(self.words)}
        self.idx2word = {i: w for w, i in self.word2idx.items()}
        self.vocab_size = len(self.words)

    def encode(self, text):
        """Converts a string of text into a list of integer tokens."""

        return [self.word2idx[w] for w in text.split() if w in self.word2idx]

    def decode(self, tokens):
        """Converts a list of integer tokens back into a space-separated string."""

        return " ".join([self.idx2word[int(t)] for t in tokens])



def main():
    """Main execution script to train the model and generate text."""

    # Dataset: Short sentences about AI/ML
    training_samples = [
        "the neural network learns patterns",
        "deep learning models need data",
        "artificial intelligence is changing technology",
        "transformers process sequences in parallel",
        "large language models generate text",
        "machine learning improves with experience",
        "python is great for data science"
    ]

    # Initialize tokenizer and process text
    tokenizer = Tokenizer(training_samples)
    all_encoded = []
    for s in training_samples:
        all_encoded.extend(tokenizer.encode(s))

    # Create sliding window training data
    xs, ys = [], []
    seq_len = 4
    for i in range(len(all_encoded) - seq_len):
        xs.append(all_encoded[i: i + seq_len])

        # The target (y) is the next token in the sequence (x shifted by 1)
        ys.append(all_encoded[i + 1: i + seq_len + 1])

    x, y = np.array(xs), np.array(ys)

if __name__ == "__main__":
    main()