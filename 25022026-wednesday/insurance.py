import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

sep = f"\n\n{'-'*70}\n\n"

class Insurance:
    """
    A class to perform end-to-end Machine Learning on Insurance data.
    Includes data loading, EDA, outlier detection, feature engineering
    using pipelines, and model evaluation using Decision Tree Regressor.
    """

    def __init__(self, file_path, test_size=0.2, random_state=42):
        """
        Initializes the Insurance class with data paths and split parameters.
        """

        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.data = None
        self.X = None
        self.y = None
        self.preprocessor = None
        self.X_test = None
        self.y_test = None
        self.X_train = None
        self.y_train = None
        self.pipeline = None


    def load_data(self):
        """Loads the CSV file into a Pandas DataFrame."""

        print("Loading data...", end=sep)
        self.data = pd.read_csv(self.file_path)
        print(f"Dataset loaded with rows and columns = {self.data.shape}",end=sep)
        # print(self.data.head())


    def stats_analysis(self):
        """Performs basic data integrity checks: Info, Describe, Duplicates, and Nulls."""

        print("Performing Statistical analysis\n")
        print(self.data.info())
        print(self.data.describe(), end=sep)

        print("\nChecking for Duplicates")
        duplicated = self.data.duplicated()
        print(duplicated.sum())

        self.data.drop_duplicates(inplace=True)
        print("Dropped Duplicates", end=sep)

        print("Checking for Null Values")
        print(self.data.isnull().sum(), end=sep)


    def data_split_x_and_y(self):
        """Separates the dataset into Features (X) and Target (y)."""

        self.X = self.data.drop(columns="charges")
        self.y = self.data["charges"]


    def outlier_and_eda(self):
        """
        Visualizes data distributions and identifies outliers using IQR.
        Generates Boxplots, Heatmaps, Histograms, and Pie Charts.
        """

        print("Box Plot of ['age', 'bmi', 'children'']", end=sep)
        columns = ["age", "bmi", "children"]
        columns1 = ['sex', 'smoker', 'region']
        for i, col in enumerate(columns):
            plt.subplot(2, 2, i+1)
            plt.title(col, fontsize = 10)
            plt.grid(alpha=0.3)
            sns.boxplot(x=self.X[col], data=self.X)
        plt.tight_layout()
        plt.show()

        corr = self.data.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, cmap="YlOrRd")
        plt.show()

        print("Histgram of ['age', 'bmi', 'children']", end=sep)
        for i, col in enumerate(columns):
            plt.subplot(2, 2, i+1)
            plt.title(col, fontsize = 10)
            plt.grid(alpha=0.2)
            sns.histplot(self.X[col], kde=True, color='green')
        plt.tight_layout()
        plt.show()

        print("Pie Chart of ['sex', 'smoker', 'region']", end=sep)
        for i, col in enumerate(columns1):
            plt.subplot(2, 2, i+1)
            plt.title(col, fontsize = 10)
            plt.grid(alpha=0.3)
            counts = self.X[col].value_counts()
            plt.pie(x=counts, labels=counts.index, colors=['lightblue','red', 'yellow', 'lightgreen'],
                    autopct='%1.1f%%')
        plt.tight_layout()
        plt.show()

        for col in columns:
            q1 = self.X[col].quantile(0.25)
            q3 = self.X[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            print(lower_bound, upper_bound)
            outlier = (self.X[col] < lower_bound) | (self.X[col] > upper_bound)
            print(f"Checking Outlier:")
            print(f"{col} : {outlier.sum()} outliers")


    def feature_encoding(self):
        """
        Sets up the ColumnTransformer for categorical encoding.
        Uses OneHotEncoding for multi-class strings.
        """

        # le = LabelEncoder()
        # column = []
        # for col in column:
        #     self.X[col] = le.fit_transform(self.X[col])
        ohe = OneHotEncoder(drop='first')
        cols = ['region','sex', 'smoker']
        self.preprocessor = ColumnTransformer(transformers=[("ohe",ohe,cols)], remainder='passthrough')
        # self.X['region'] = ohe.fit_transform(self.X[['region']])
        # region_encoded = ohe.fit_transform(self.X[])
        # region_df = pd.DataFrame(region_encoded, columns=ohe.get_feature_names_out(['region']), index=self.X.index)
        # self.X = pd.concat([self.X.drop(columns=['region']), region_df], axis=1)

        # print(self.X.head())


    def train_test_split(self):
        """Splits data into Training and Testing sets."""

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                 test_size=self.test_size,
                                                                                 random_state=self.random_state)


    def model_training(self):
        """
        Creates and trains a Machine Learning Pipeline.
        The pipeline bundles preprocessing and the DecisionTreeRegressor
        to prevent data leakage and simplify deployment.
        """

        regressor = DecisionTreeRegressor(max_depth=10, min_samples_split=5,min_samples_leaf=7, ccp_alpha=0.01,
                                          random_state=self.random_state)
        regressor = Pipeline(steps=[("preprocess", self.preprocessor), ('regressor', regressor)])
        regressor.fit(self.X_train, self.y_train)

        return regressor


    def model_evaluation(self,regressor):
        """
        Evaluates the model performance on the unseen test set.
        Prints MAE, MSE, RMSE, and R2 Score.
        """

        y_pred = regressor.predict(self.X_test)
        print(f"The Mean Absolute Error:{mean_absolute_error(y_pred, self.y_test)}")
        print(f"The Mean Squared Error:{mean_squared_error(y_pred, self.y_test)}")
        print(f"The Root Mean Squared Error:{root_mean_squared_error(self.y_test, y_pred)}")
        print(f"The R2_score :{r2_score(y_pred, self.y_test)}")



def main():
    """Main execution flow."""

    path = "insurance.csv"
    model = Insurance(path)
    model.load_data()
    model.stats_analysis()
    model.data_split_x_and_y()
    model.outlier_and_eda()
    model.feature_encoding()
    model.train_test_split()
    regressor = model.model_training()
    model.model_evaluation(regressor)

if __name__ == "__main__":
    main()