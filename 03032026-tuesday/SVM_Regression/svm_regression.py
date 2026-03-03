import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import numpy as np

seperator = f"\n\n{'-'*60}\n\n"

class Customer:
    """
    A class to handle the end-to-end pipeline for predicting customer purchases
    using a Support Vector Machine (SVM) classifier.
    """

    def __init__(self,file_path,test_size = 0.2, random_state = 42):
        """Initializes the Customer class with data path and split parameters."""

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
        """Loads the CSV file and removes unnecessary identification columns."""

        print("Loading data...", end=seperator)
        self.df = pd.read_csv(self.file_path)
        print(f"Loaded Data : {self.df.shape}")
        print(f" Dropped the user_id column that is not necessary", end=seperator)
        self.df = self.df.drop(columns="user_id")

        return self.df


    def analyze_data(self):
        """Prints basic statistics, info, null values, and duplicates in the dataset."""

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
        """Separates the features (X) from the target variable (Y)."""

        print("Splitting data...")

        self.X = self.df.drop(columns="purchased")
        self.Y = self.df["purchased"]
        print(f"Split Data : X {self.X.shape}  Y : {self.Y.shape}", end=seperator)


    def eda_outliers(self):
        """Visualizes data relationships and detects outliers using the IQR method."""

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
        """Encodes categorical text data into numerical format."""

        print("Feature Encoding...", end=seperator)
        le = LabelEncoder()
        self.X['gender'] = le.fit_transform(self.X['gender'])


    def train_test_split(self):
        """Splits the dataset into training and testing subsets."""

        print("Training and Testing Data Splitting...",end=seperator)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y,
                                                                                test_size=self.test_size,
                                                                                random_state = self.random_state)


    def feature_scaling(self):
        """Standardizes features by removing the mean and scaling to unit variance."""

        print("Feature Scaling...")
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)


    def perform_grid_search(self):
        """
        Executes a cross-validated grid search to find the optimal SVM hyperparameters.

        This method tests various combinations of 'C', 'kernel', and 'gamma' to
        maximize model accuracy. It uses all available CPU cores (n_jobs=-1)
        and refits the best model on the entire training set.

        Returns:
        sklearn.svm.SVC: The trained model instance with the best discovered parameters.
        """

        print("Performing Grid Search...")
        parameter = {
            'C': [1, 10, 50, 80, 100, 500, 1000],
            'kernel': ['linear','poly','rbf','sigmoid'],
            'gamma': ['scale','auto']

        }

        grid = GridSearchCV(SVC(random_state = self.random_state), param_grid=parameter, n_jobs = -1,
                            verbose = 2, cv = 5, refit=True)

        grid.fit(self.X_train, self.y_train)

        print(f"Best parameters: {grid.best_params_}")
        print(f"Best score: {grid.best_score_}")
        print(f"Best estimator: {grid.best_estimator_}")

        return grid.best_estimator_


    def model_training(self):
        """Trains a Support Vector Machine classifier on the training data."""

        svm = SVC(kernel='linear', random_state = self.random_state)
        svm.fit(self.X_train, self.y_train)
        return svm


    def model_evaluation(self, sv):
        """Evaluates the model and prints accuracy, confusion matrix, and classification report."""

        y_pred = sv.predict(self.X_test)
        print("Model Evaluation...")
        print("The Classification Report: \n", classification_report(y_pred, self.y_test))
        print("The Confusion Matrix: \n", confusion_matrix(self.y_test, y_pred, labels=[0,1]))
        print("The Accuracy Score: \n", accuracy_score(self.y_test, y_pred))


    def plot_decision_boundary(self, kernel='rbf', c=10, gamma = 'scale'):
        """
        X: DataFrame with columns [Age, Estimated Salary]
        y: Target array (Purchased)
        """

        x_subset = self.X.iloc[:, -2:].values if hasattr(self.X, 'iloc') else self.X[:, -2:]
        sc = StandardScaler()
        x_scaled = sc.fit_transform(x_subset)

        model = SVC(kernel=kernel, C=c, gamma= gamma)
        model.fit(x_scaled, self.Y)

        h = .02
        x_min, x_max = x_scaled[:, 0].min() - 1, x_scaled[:, 0].max() + 1
        y_min, y_max = x_scaled[:, 1].min() - 1, x_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        z = z.reshape(xx.shape)

        plt.figure(figsize=(10, 6))
        plt.contourf(xx, yy, z, alpha=0.8)

        plt.scatter(x_scaled[:, 0], x_scaled[:, 1], c=self.Y,
                     edgecolors='k')

        plt.title(f"SVM Decision Boundary (Age vs Salary)\nKernel: {kernel}")
        plt.xlabel('Age (Standardized)')
        plt.ylabel('Estimated Salary (Standardized)')
        plt.show()


def main():
    """Execution entry point."""

    model = Customer(file_path = "customer_purchase_data.csv")
    model.load_data()
    model.analyze_data()
    model.split_data()
    model.eda_outliers()
    model.feature_encoding()
    model.train_test_split()
    model.feature_scaling()
    best_model = model.perform_grid_search()
    model.model_training()
    model.model_evaluation(best_model)
    model.plot_decision_boundary()


if __name__ == "__main__":
    main()
