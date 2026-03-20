import tensorflow as tf
from tensorflow.keras.layers import Dense

class DataLoader:

      def __init__(self, sentences):
        self.sentence = sentences
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer('')

      def load_data(self):

        self.tokenizer.fit_on_texts(self.sentence)
        sequence = self.tokenizer.texts_to_sequences(self.sentence)

        padded_data = tf.keras.preprocessing.sequence.pad_sequences(
              sequence,
              padding='post'
        )

        return padded_data

      def get_vocab_size(self):
        return len(self.tokenizer.word_index) + 1



def main():
      sentences = [
            "i love ai",
            "transformer learns context",
            "attention improves translation"
        ]

      loader = DataLoader(sentences)
      data = loader.load_data()
      vocab_size = loader.get_vocab_size()
      print("success")

if __name__ == "__main__":
      main()