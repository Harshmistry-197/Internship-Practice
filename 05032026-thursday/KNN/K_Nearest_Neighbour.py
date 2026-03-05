import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier

seperator = f"\n\n{'-'*60}\n\n"

class KNNClassifier:

    def __init__(self,file_path,test_size = 0.3, random_state = 42):

        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.df = None

        self.X = None
        self.Y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def load_data(self):

        print("Loading data...", end=seperator)
        self.df = pd.read_csv(self.file_path)
        print(f"Loaded Data : {self.df.shape}")
        print(f" Dropped the user_id column that is not necessary", end=seperator)
        self.df = self.df.drop(columns="user_id")

    def analyze_data(self):

        self.load_data()

        print("Analyzing data... \n")
        print("The concise analysis of data\n")
        print(self.df.info())

        print("The statistical summary of data\n")
        print(self.df.describe())

        print("Checking for null values\n")
        print(self.df.isnull().sum())

        print("Checking for duplicate values\n")
        print(self.df.duplicated().sum())

    def split_data(self):

        self.analyze_data()

        print("Splitting data...")

        self.X = self.df.drop(columns="purchased")
        self.Y = self.df["purchased"]
        print(f"Split Data : X {self.X.shape}  Y : {self.Y.shape}", end=seperator)

    def eda_outliers(self):

        self.split_data()

        print("Eda Outliers...")
        print("Heatmap of Data", end=seperator)
        corr = self.df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, cmap="YlOrRd")
        plt.show()

        print("Pair plot of Data", end=seperator)
        sns.pairplot(self.df, hue="purchased")
        plt.show()


        columns = ['age', 'estimated_salary']
        for i, col in enumerate(columns):
            q1 = self.X[col].quantile(0.25)
            q3 = self.X[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier = (self.X[col] < lower_bound) | (self.X[col] > upper_bound)
            print(f"Outlier : ")
            print(f"{col} : {outlier.sum()} outliers")
        print(end=seperator)

    def feature_encoding(self):

        self.eda_outliers()

        print("Feature Encoding...", end=seperator)
        le = LabelEncoder()
        self.X['gender'] = le.fit_transform(self.X['gender'])

    def train_test_split(self):

        self.feature_encoding()

        print("Training and Testing Data Splitting...",end=seperator)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y,
                                                                                test_size=self.test_size,
                                                                                random_state = self.random_state)

    def feature_scaling(self):

        self.train_test_split()

        print("Feature Scaling...")
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def perform_grid_search(self):

        self.feature_scaling()

        print("Performing Grid Search...")
        parameter = {
            'n_neighbors': [3, 5, 7, 9, 11],
            'metric': ['euclidean', 'manhattan', 'minkowski'],
            'weights': ['uniform', 'distance']
        }

        grid = GridSearchCV(KNeighborsClassifier(), param_grid=parameter,
                            verbose = 2, cv = 5)

        grid.fit(self.X_train, self.y_train)

        print(f"Best parameters: {grid.best_params_}")
        print(f"Best score: {grid.best_score_}")
        print(f"Best estimator: {grid.best_estimator_}")

        return grid.best_estimator_


    def model_evaluation(self):

        knn = self.perform_grid_search()

        y_pred = knn.predict(self.X_test)
        print("Model Evaluation...")
        print("The Classification Report: \n", classification_report(y_pred, self.y_test))
        print("The Confusion Matrix: \n", confusion_matrix(self.y_test, y_pred))
        print("The Accuracy Score: \n", accuracy_score(self.y_test, y_pred))

        return knn

    def save_model(self):

        knn = self.model_evaluation()
        with open("knn_model.pkl", 'wb') as file:
            pickle.dump(knn, file)
        print("Model saved successfully", end=seperator)

def main():

    model = KNNClassifier(file_path = "customer_purchase_data.csv")

    model.save_model()

if __name__ == "__main__":
    main()
