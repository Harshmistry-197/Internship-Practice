import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


seperator = f"\n\n{'-'*60}\n\n"

class Customer:

    def __init__(self,file_path,test_size = 0.2, random_state = 42):

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

        return self.df


    def analyze_data(self):

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

        print("Splitting data...")

        self.X = self.df.drop(columns="purchased")
        self.Y = self.df["purchased"]
        print(f"Split Data : X {self.X.shape}  Y : {self.Y.shape}", end=seperator)


    def eda_outliers(self):

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



def main():

    model = Customer(file_path = "customer_purchase_data.csv")
    model.load_data()
    model.analyze_data()
    model.split_data()
    model.eda_outliers()



if __name__ == "__main__":
    main()
