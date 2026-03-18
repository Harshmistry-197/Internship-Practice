import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

seperator = f"\n\n{'-' * 100}\n\n"

class CNN:

    def __init__(self):

        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.history = None

    def load_data(self):

        print("Loading Data")
        (self.X_train, self.y_train), (self.X_test, self.y_test) = tf.keras.datasets.mnist.load_data()
        self.X_train = self.X_train / 255.0
        self.X_test = self.X_test / 255.0

        self.X_train = self.X_train.reshape(-1, 28, 28, 1)
        self.X_test = self.X_test.reshape(-1, 28, 28, 1)

        print("Data Loaded successfully with : ")
        print("Training Data shape : ", self.X_train.shape)
        print("Testing Data shape : ", self.X_test.shape, end=seperator)

    def build_model(self):

        self.load_data()
        self.model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(64, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),

            layers.Flatten(),

            layers.Dense(64, activation="relu"),
            layers.Dense(10, activation="softmax")
        ])

        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        self.model.summary()
        print("Layers Created succesfully", end=seperator)

    def train_model(self):

        self.build_model()
        self.history = self.model.fit(
            self.X_train,
            self.y_train,
            epochs=5,
            validation_data=(self.X_test, self.y_test)
        )

    def evaluate_model(self):

        self.train_model()
        loss, accuracy = self.model.evaluate(self.X_test, self.y_test)
        print(f"Test Loss : {loss}, Test Accuracy : {accuracy}")

    def plot_performance(self):

        self.evaluate_model()
        try:

            plt.figure(figsize=(12, 4))
            # plot for accuracy
            plt.subplot(1, 2, 1)
            plt.plot(self.history.history['accuracy'], label='Train Accuracy')
            plt.plot(self.history.history['val_accuracy'], label='Val Accuracy')
            plt.title('Model Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            # plot for loss
            plt.subplot(1, 2, 2)
            plt.plot(self.history.history['loss'], label='Train Loss')
            plt.plot(self.history.history['val_loss'], label='Val Loss')
            plt.title('Model Loss')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error while plotting: {e}")


def main():

    obj = CNN()
    obj.plot_performance()


if __name__ == "__main__":
    main()