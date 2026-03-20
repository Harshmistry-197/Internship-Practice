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


class TransformerBlock(layers.Layer):
    """
    A standard Transformer decoder block with Multi-Head Attention and Feed-Forward Network.

    Args:
        d_model (int): The dimensionality of the input and output embeddings.
        num_heads (int): Number of attention heads.
        dff (int): Hidden layer size of the feed-forward network.
        rate (float): Dropout rate.
    """

    def __init__(self, d_model, num_heads, dff, rate=0.1):
        """Initializes a single Transformer block (Decoder layer)."""

        super().__init__()

        # Multi-Head Attention mechanism
        self.mha = layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model)

        # Point-wise Feed-Forward Network
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu'),
            layers.Dense(d_model)
        ])

        # Layer normalization and dropout for residual connections
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, x, training=False):
        """
        Forward pass for the Transformer block.
        Applies causal masking to ensure the model only looks at past tokens.
        """

        seq_len = tf.shape(x)[1]

        # Create a causal look-ahead mask (Lower Triangular Matrix)
        i = tf.range(seq_len)[:, tf.newaxis]
        j = tf.range(seq_len)
        mask = i >= j
        mask = tf.reshape(mask, (1, seq_len, seq_len))

        # Multi-head attention over the input sequence
        attn_output = self.mha(query=x, value=x, key=x, attention_mask=mask, training=training)
        attn_output = self.dropout1(attn_output, training=training)

        # Residual connection 1
        out1 = self.layernorm1(x + attn_output)

        # Feed-forward network pass
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)

        # Residual connection 2
        return self.layernorm2(out1 + ffn_output)


class SampleGPT(tf.keras.Model):
    """
    A simplified GPT-style generative model.

    Args:
        vocab_size (int): Size of the vocabulary.
        d_model (int): Embedding dimension.
        num_heads (int): Number of attention heads per block.
        num_layers (int): Number of Transformer blocks to stack.
        max_len (int): Maximum sequence length for positional embeddings.
    """

    def __init__(self, vocab_size, d_model=64, num_heads=4, num_layers=2, max_len=100):
        super().__init__()
        self.d_model = d_model
        self.embedding = layers.Embedding(vocab_size, d_model)
        self.pos_emb = layers.Embedding(max_len, d_model)
        self.blocks = [TransformerBlock(d_model, num_heads, d_model * 4) for _ in range(num_layers)]
        self.dropout = layers.Dropout(0.1)
        self.final_layer = layers.Dense(vocab_size)

    def call(self, x, training=False):
        """Forward pass to predict the next token in a sequence."""

        seq_len = tf.shape(x)[1]
        positions = tf.range(start=0, limit=seq_len, delta=1)

        # Combine token embeddings and positional embeddings
        x = self.embedding(x) + self.pos_emb(positions)
        x = self.dropout(x, training=training)

        # Pass through stacked Transformer blocks
        for block in self.blocks:
            x = block(x, training=training)

        # Map back to vocabulary logits
        return self.final_layer(x)


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

    # Model configuration and compilation
    model = SampleGPT(vocab_size=tokenizer.vocab_size)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    )

    print("--- Training Started ---")
    model.fit(x, y, epochs=80, verbose=1)
    print("--- Training Complete ---\n")

    def generate(prompt, length=4):
        tokens = tokenizer.encode(prompt)
        for _ in range(length):
            input_tokens = np.array([tokens])
            preds = model(input_tokens, training=False)

            # Pick the token with the highest logit for the last position
            next_id = tf.argmax(preds[0, -1, :]).numpy()
            tokens.append(next_id)
        return tokenizer.decode(tokens)

    # Test the model
    print(f"Result: {generate('artificial intelligence')}")


if __name__ == "__main__":
    main()