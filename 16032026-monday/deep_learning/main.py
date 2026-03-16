import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from category_encoders import OneHotEncoder
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

separator = "\n" + "--" * 40 + "\n"


class TitanicDeepLearning:

    def __init__(self, filepath):

        self.filepath = filepath
        self.df = None
        self.model = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.preprocessing = None
        self.history = None

    def load_dataset(self):

        try:
            self.df = pd.read_csv(self.filepath)
            print("Dataset Loaded")
            print(self.df.head(), end=separator)
        except FileNotFoundError:
            print("Dataset Not Found")

    def analysis_data(self):

        try:
            print("Data Info")
            print(self.df.info(), end=separator)
            print(self.df.describe(), end=separator)
            print(self.df.isnull().sum(), end=separator)
            print(self.df.duplicated().sum(), end=separator)
            plt.figure(figsize=(10, 8))
            corr = self.df.corr(numeric_only=True)
            sns.heatmap(corr, annot=True, cmap='coolwarm')
            plt.title("Feature Correlation Heatmap")
            plt.show()
            self.df.drop(columns=["Name", "Ticket", "PassengerId", "Cabin"], inplace=True)
            self.df["Age"] = self.df["Age"].fillna(self.df["Age"].median())
            self.df["Embarked"] = self.df["Embarked"].fillna(self.df["Embarked"].mode()[0])
            self.df["FamilySize"] = self.df["SibSp"] + self.df["Parch"] + 1
            self.df.drop(columns=["SibSp", "Parch"], inplace=True)
            print("Preprocessing Done")
            print(self.df.head(), end=separator)
        except Exception as e:
            print(e)

    def preprocessing_pipeline(self):

        try:
            print("Feature Encoding Started")
            numeric_cols = ["Age", "Fare", "Pclass", "FamilySize"]
            categorical_cols = ["Embarked", "Sex"]

            numeric_pipeline = Pipeline([
                ("scaler", StandardScaler())
            ])

            categorical_pipeline = Pipeline([
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ])

            self.preprocessing = ColumnTransformer([
                ("numeric", numeric_pipeline, numeric_cols),
                ("categorical", categorical_pipeline, categorical_cols)
            ])
            print("feature Encoding Done", end=separator)
        except Exception as e:
            print(e)

    def train_test_split(self):

        try:
            print("Training And Test Data Split", end=separator)
            self.X = self.df.drop("Survived", axis=1)
            self.y = self.df["Survived"]

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=0.3, random_state=42
            )
        except Exception as e:
            print(e)

    def preprocess(self):

        try:
            print("Feature preprocess Started")
            self.X_train = self.preprocessing.fit_transform(self.X_train)
            self.X_test = self.preprocessing.transform(self.X_test)
            print("Feature preprocess Done", end=separator)
        except Exception as e:
            print(e)

    def build_model(self, num_features):

        try:
            print("Model Building Started")
            self.model = Sequential([
                Dense(32, activation='relu', input_dim=num_features),
                Dense(16, activation='relu'),
                Dense(1, activation='sigmoid')
            ])

            self.model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            print("Model Crested successfully")
            print(self.model.summary(), end=separator)
        except Exception as e:
            print(e)

    def train_model(self):

        try:
            early_stopping = EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )
            self.history = self.model.fit(
                self.X_train,
                self.y_train,
                batch_size=16,
                epochs=50,
                validation_data=(self.X_test, self.y_test),
                callbacks=[early_stopping]
            )

        except Exception as e:
            print(e)

    def evaluate_model(self):

        try:
            predictions = self.model.predict(self.X_test)
            predictions = (predictions > 0.5).astype(int)

            print("\nAccuracy Score:")
            print(accuracy_score(self.y_test, predictions))
            print("\nConfusion Matrix:")
            print(confusion_matrix(self.y_test, predictions))
            print("\nClassification Report:")
            print(classification_report(self.y_test, predictions))
        except Exception as e:
            print(e)

    def plot_model(self):

        plt.figure(figsize=(8, 5))
        plt.plot(self.history.history['loss'], label = 'Training Loss')
        plt.plot(self.history.history['val_loss'], label = 'Validation Loss')
        plt.title('Model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend()
        plt.show()

def main():

    obj = TitanicDeepLearning("Titanic_dataset.csv")
    obj.load_dataset()
    obj.analysis_data()
    obj.preprocessing_pipeline()
    obj.train_test_split()
    obj.preprocess()
    obj.build_model(obj.X_train.shape[1])
    obj.train_model()
    obj.evaluate_model()
    obj.plot_model()

if __name__ == "__main__":
    main()