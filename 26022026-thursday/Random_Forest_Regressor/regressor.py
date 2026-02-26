import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(filename="flight.log",filemode='w',level=logging.INFO, format='%(asctime)s : %(message)s')

seprator = f"\n\n{'-'*60}\n\n"

class Flight:
    def __init__(self, file_path, test_size=0.2, random_state=42):

        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.df = None
        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = RandomForestRegressor(n_estimators = 3, max_depth=2, min_samples_leaf=5, ccp_alpha=0.001)

        self.preprocessing = None
        self.regressor = None
        self.encoder = OneHotEncoder(handle_unknown='ignore', drop="first")

    def load(self):
        logging.info("Loading data...")
        self.df = pd.read_csv(self.file_path)
        self.df.drop(['Unnamed: 0','flight'], axis=1, inplace=True)
        print(self.df.head())
        logging.info(f"Loaded Successfully with rows and columns : {self.df.shape}")

    def stats(self):

        logging.info(f"COncise Analysis")
        print(self.df.info(), end= seprator)
        logging.info("Statistical Analysis")
        print(self.df.describe(), end= seprator)

        logging.info("Checking for duplicates")
        print(self.df.duplicated().sum(), end= seprator)

        logging.info("Checking for null values")
        print(self.df.isnull().sum(), end= seprator)


    def x_and_y_split(self):

        self.X = self.df.drop(['price'], axis=1)
        self.y = self.df['price']


    def eda_and_outliers(self):

        logging.info("EDA Started")
        logging.info("Heatmap of Data")
        corr = self.df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True)
        plt.title("Correlation Matrix", fontsize=15, color="red", fontweight="bold")
        plt.show()

        numeric_cols = self.df.select_dtypes(include=["int64", "float64"]).columns.drop("price")
        for i, cols in enumerate(numeric_cols):
            plt.subplot(2, 2, i + 1)
            sns.boxplot(self.df[cols])
            plt.title(cols, fontsize=15, color="red", fontweight="bold")
            q1 = self.df[cols].quantile(0.25)
            q3 = self.df[cols].quantile(0.75)
            iqr = q3 - q1
            lb = q1 - 1.5 * iqr
            ub = q3 + 1.5 * iqr
            outliers = self.df[(self.df[cols] < lb) | (self.df[cols] > ub)]
            print(f"{cols} :- {len(outliers)}")
            self.df[cols] = self.df[cols].clip(lower=lb, upper=ub)
        plt.tight_layout()
        plt.show()
        print("\nOutlier Removed Successfully", end=seprator)
        logging.info("EDA Completed")

    def encoding(self):
        logging.info("Encoder Pipline Started")
        cat_cols = self.df.select_dtypes(include=["str"]).columns
        self.preprocessing = ColumnTransformer(transformers=[("categorical", self.encoder, cat_cols)],
                                                   remainder="passthrough")
        print("Encoding Pipeline Created", end=seprator)
        logging.info("Encoder Pipline Completed")

    def train_test_split(self):
        logging.info("train_test_split Started")
        self.X = self.df.drop(columns="price")
        self.y = self.df["price"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                test_size=self.test_size,
                                                                                random_state=self.random_state)
        print("Train Test Split Completed", end=seprator)
        logging.info("Train Test Split Completed")

    def model_training(self):
        logging.info("Model Training Started")
        self.regressor = Pipeline(steps=[("preprocessor", self.preprocessing), ("model", self.model)])
        self.regressor.fit(self.X_train, self.y_train)
        print("Model Training Completed", end=seprator)
        logging.info("Model Training Completed")

    def model_evaluation(self):
        logging.info("Model Evaluation Started")
        y_pred = self.regressor.predict(self.X_test)
        print(f"The R2_Score is :- {r2_score(self.y_test,y_pred) * 100:.2f}%")
        print(f"The Mean Absolute Error is :- {mean_absolute_error(self.y_test, y_pred)}")
        print(f"The Mean Squared Error is :- {mean_squared_error(self.y_test, y_pred)}")
        print("Model Evaluation Completed", end=seprator)
        logging.info("Model Evaluation Completed")


def main():
    path = "flght_price_prediction.csv"
    model = Flight(path)
    model.load()
    model.stats()
    model.eda_and_outliers()
    model.encoding()
    model.train_test_split()
    model.model_training()
    model.model_evaluation()


if __name__ == "__main__":
    main()