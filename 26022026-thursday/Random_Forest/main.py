import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix

sep = f"\n\n{'-'*50}\n\n"

class Car_evalution:

    def __init__(self, file_path, test_size = 0.2, random_state = 42,):
        self.file_path = file_path
        self.random_state = random_state
        self.test_size = test_size

        self.X = None
        self.y = None
        self.df = None

        self.temp_df = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def load_data(self):
        print("Loading data...", end=sep)
        self.df = pd.read_csv(self.file_path)
        print(f"Data loaded : {self.df.shape}", end=sep)


    def analysis(self):
        print("Analysis of data...")

        print("Concise Summary \n")
        print(f"{self.df.info()}\n")
        print("The Statistical Summary \n")
        print(f"{self.df.describe()}\n", end=sep)

        print(f"Checking for dupliactes")
        print(f"{self.df.duplicated().sum()}\n", end=sep)

        print(f"Checking for Null values")
        print(f"{self.df.isnull().sum()}\n", end=sep)


    def split_x_and_y(self):

        print("Splitting data...", end=sep)

        self.X = self.df.drop(['class'], axis=1)
        self.y = self.df['class']

    def eda_and_outliers(self):

        self.X['doors'] = self.X['doors'].replace('5more', 5).astype(int)
        self.X['persons'] = self.X['persons'].replace('more', 6).astype(int)


        mapping = {"low": 1, "med": 2, "high": 3, "vhigh": 4, "small": 1, "big": 3,"unacc": 1, "acc": 2,
                   "good": 3, "vgood": 4}
        print("Heatmap : ")
        self.temp_df = pd.DataFrame()
        for col in self.X.columns:
            self.temp_df[col] = self.X[col].replace(mapping)
            self.temp_df[col] = pd.to_numeric(self.temp_df[col], errors='coerce')

        corr = self.temp_df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True)
        plt.show()



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


        encoder = ce.OrdinalEncoder(cols=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety'])
        self.X_train = encoder.fit_transform(self.X_train)
        self.X_test = encoder.transform(self.X_test)


    def model_training(self):

        rfc = RandomForestClassifier(n_estimators=20,min_samples_split=5, max_depth=20, min_samples_leaf=10,
                                     random_state=42)
        rfc.fit(self.X_train, self.y_train)

        return rfc

    def model_evaluation(self, rfc):
        y_pred = rfc.predict(self.X_test)
        y_prob = rfc.predict_proba(self.X_test)
        print(f"The classification report is :  {classification_report(y_pred, self.y_test)}:")
        print(f"The accuracy is :  {accuracy_score(y_pred, self.y_test)}")
        score = roc_auc_score(self.y_test, y_prob, multi_class='ovr')
        print(f"The roc_auc_score is :  {score}")
        print(f"The confusion matrix : {confusion_matrix(self.y_test, y_pred)}")







def main():
    path = "car_evaluation.csv"
    model = Car_evalution(path)
    model.load_data()
    model.analysis()
    model.split_x_and_y()
    model.eda_and_outliers()
    model.train_test_split()
    model.feature_encoding()
    classifier = model.model_training()
    model.model_evaluation(classifier)


if __name__ == "__main__":
    main()