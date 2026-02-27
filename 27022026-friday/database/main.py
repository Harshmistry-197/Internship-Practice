import pandas as pd
from sklearn.tree import plot_tree
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score,roc_auc_score
import category_encoders as ce

sep = f"\n{'-'*50}\n"

class MSSQLData:
    """
    Handles connections and data retrieval from Microsoft SQL Server.
    """

    def __init__(self,server,database,driver ="ODBC+Driver+17+for+SQL+Server"):
        """
        connecting database
        """

        connection_string = (
            f"mssql+pyodbc://{server}/{database}?driver={driver}"
        )

        try:
            self.engine = create_engine(connection_string)
            print("Engine created successfully!")
        except ConnectionError as e:
            print("Connection Error", e)

    def load_table(self, table_name):
        """
        Loading table from server
        """

        query = f"SELECT * FROM {table_name}"
        dataframe = pd.read_sql(query, self.engine)
        return dataframe

    def load_query(self, query):
        """
        Loading query from server
        """

        dataframe = pd.read_sql(text(query), self.engine)
        return dataframe


class Carevalution:
    """
    ML Pipeline for car evaluation, including EDA, Preprocessing, and Database Export.
    """

    def __init__(self, df, test_size = 0.2, random_state = 42):
        """
        Initializes the model pipeline with a dataframe.
        Args:
        df (pd.DataFrame): The input dataset.
        test_size (float): Proportion of data for testing.
        random_state (int): Seed for reproducibility.
        """

        self.random_state = random_state
        self.test_size = test_size

        self.X = None
        self.y = None
        self.df = df

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None


    def analysis(self):
        """Prints a comprehensive summary of the dataset including nulls and duplicates."""

        print("Analysis of data...")

        print("Concise Summary \n")
        print(f"{self.df.info()}\n")
        print("The Statistical Summary \n")
        print(f"{self.df.describe()}\n", end=sep)

        print(f"Checking for duplicates")
        print(f"{self.df.duplicated().sum()}\n", end=sep)

        print(f"Checking for Null values")
        print(f"{self.df.isnull().sum()}\n", end=sep)


    def split_x_and_y(self):
        """Splits the dataframe into features (X) and target variable (y)."""

        print("Splitting data...", end=sep)

        self.X = self.df[['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']]
        self.y = self.df['class']

    def eda_and_outliers(self):
        """Generates visualizations (Box plots, Pie charts, Histograms) for the features."""

        self.X['doors'] = self.X['doors'].replace('5more', 5).astype(int)
        self.X['persons'] = self.X['persons'].replace('more', 6).astype(int)

        print("Box Plot of ['doors', 'persons'] ")
        columns = ['doors', 'persons']
        for i,col in enumerate(columns):
            plt.subplot(1,2,i+1)
            plt.grid(alpha=0.2)
            plt.title(col)
            sns.boxplot(x=self.X[col], data=self.X)
        plt.tight_layout()
        plt.show()


        print("Pie Chart of ['buying', 'maint','lug_boot', 'safety'] ")
        columns = ['buying', 'maint','lug_boot', 'safety']
        for i,col in enumerate(columns):
            plt.subplot(2,2,i+1)
            plt.grid(alpha=0.2)
            plt.title(col)
            plt.pie(self.df[col].value_counts(), autopct='%1.1f%%', labels=self.df[col].value_counts().index,
                    colors=sns.color_palette())
        plt.tight_layout()
        plt.show()

        print("Histogram of ['doors', 'persons']")
        columns = ['doors', 'persons']
        for i,col in enumerate(columns):
            plt.subplot(1,2,i+1)
            plt.grid(alpha=0.2)
            plt.title(col)
            sns.histplot(self.df[col], kde=True)
        plt.tight_layout()
        plt.show()


    def train_test_split(self):
        """Splits data into Training and Testing sets."""

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                 test_size=self.test_size,
                                                                                 random_state=self.random_state)

    def feature_encoding(self):
        """Encodes categorical strings into ordinal integers."""

        encoder = ce.OrdinalEncoder(cols=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety'])
        self.X_train = encoder.fit_transform(self.X_train)
        self.X_test = encoder.transform(self.X_test)
        self.X = encoder.fit_transform(self.X)


    def model_training(self, tree_index = 0):
        """
        Trains a Random Forest Classifier.
        Returns:
        RandomForestClassifier: Trained model instance.
        """

        rfc = RandomForestClassifier(n_estimators=20,min_samples_split=5, max_depth=20, min_samples_leaf=10,
                                     random_state=42)
        rfc.fit(self.X_train, self.y_train)


        single_tree = rfc.estimators_[tree_index]
        plt.figure(figsize=(20, 10))
        plot_tree(single_tree, filled=True, max_depth=2,
                  feature_names=self.X_train.columns)
        plt.show()

        return rfc

    def model_evaluation(self, rfc):
        """
        Evaluates model performance and prints metrics.
        Args:
        rfc (RandomForestClassifier): The trained classifier.
        Returns:
        np.array: Model predictions on test set.
        """

        y_pred = rfc.predict(self.X_test)
        y_prob = rfc.predict_proba(self.X_test)
        print(f"The classification report is : \n {classification_report(y_pred, self.y_test)}:")
        print(f"The accuracy is :  {accuracy_score(y_pred, self.y_test)}")
        score = roc_auc_score(self.y_test, y_prob, multi_class='ovr')
        print(f"The roc_auc_score is :  {score}")
        print(f"The confusion matrix :\n {confusion_matrix(self.y_test, y_pred)}")
        return y_pred

    def save_predictions(self, engine, table_name, df, model):
        """
        Appends predictions to the dataframe and writes it back to SQL Server.
        Args:
        engine (sqlalchemy.engine): Database engine connection.
        table_name (str): Target table name in SQL.
        df (pd.DataFrame): Original dataframe to update.
        model (RandomForestClassifier): Trained model to generate predictions.
        """

        print("Saving predictions...")
        predictions = model.predict(self.X)
        df["predicted_class"] = predictions
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print("Predictions column added/updated successfully")



def main():
    """Main execution flow: SQL -> ML -> SQL."""

    server = "localhost"
    database = "harsh"

    loader = MSSQLData(server, database)


    df = loader.load_table("car_evaluation")

    print("Original Data:")
    print(df.head())


    model = Carevalution(df)
    model.analysis()
    model.split_x_and_y()
    model.eda_and_outliers()
    model.train_test_split()
    model.feature_encoding()
    classifier = model.model_training()
    model.model_evaluation(classifier)
    model.save_predictions(
        engine=loader.engine,
        table_name='car_evaluation',
        df=df,
        model=classifier
    )


if __name__ == "__main__":
    main()