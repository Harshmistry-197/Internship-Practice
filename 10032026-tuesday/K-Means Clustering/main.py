import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

separator = f"\n\n{'-'*100}\n\n"

class Customer:
    """
    A class to perform customer segmentation using K-Means clustering.
    """

    def __init__(self, file_path):
        """Initializes the Customer class with the dataset path and default values."""

        self.file_path = file_path
        self.random_state = 42
        self.df = None
        self.X = None
        self.within_cluster_sum_of_square = None
        self.model = None

    def load_data(self):
        """Loads the CSV data from the specified file path into a pandas DataFrame."""

        try:
            print("Loading the data\n")
            self.df = pd.read_csv(self.file_path)
            print(f"Data Loaded with rows and columns {self.df.shape}\n")
            print(self.df.head(), end=separator)

        except FileNotFoundError:
            print(f"File not found : {self.file_path}")

    def preprocessing(self):
        """
        Loads data and performs initial cleaning.

        Includes checking for nulls, duplicates, and removing unnecessary columns.
        """

        self.load_data()
        try:
            print("Preprocessing data\n")
            print(f"The concise summary of data :\n ")
            print({self.df.info()})
            print(f"The descriptive summary of data : \n")
            print(self.df.describe())
            print(f"The number of null values in data :\n ")
            print(self.df.isnull().sum())
            print(f"The number of duplicates in data :\n ")
            print(self.df.duplicated().sum())
            print(f"Removing the id column \n ")
            self.df = self.df.drop(columns="CustomerID")
            print(f"Id column is removed \n ")
            print(f"Preprocessing Done", end=separator)

        except Exception as e:
            print("Error in Preprocessing",e)

    def eda(self):
        """
        Performs Exploratory Data Analysis (EDA).

        Generates a correlation heatmap, box plots for outliers, and a scatter plot
        of Income vs. Spending Score.
        """

        self.preprocessing()
        try:
            print(f"EDA summary of data :\n ")

            print(f"Heatmap of the data\n")
            corr = self.df.corr(numeric_only=True)
            sns.heatmap(corr, annot=True)
            plt.show()

            print("Boxplot of the data\n")
            num_cols = self.df.select_dtypes(include="int64").columns

            for i, col in enumerate(num_cols):
                plt.subplot(2, 2, i+1)
                plt.grid(alpha=0.2)
                plt.title(col, weight = "bold", fontsize=10)
                sns.boxplot(x=col, data=self.df)
            plt.tight_layout()
            plt.show()

            print("scatter plot of the data\n")
            plt.scatter(x=self.df["Annual Income (k$)"], y=self.df["Spending Score (1-100)"])
            plt.xlabel("Annual Income (k$)", weight = "bold", fontsize=10)
            plt.ylabel("Spending Score (1-100)", weight = "bold", fontsize=10)
            plt.show()

            print(f"EDA Done",end=separator)

        except Exception as e:
            print("Error in EDA",e)


    def feature_encoding(self):
        """Encodes categorical variables (Gender) into numerical format using LabelEncoder."""

        self.eda()
        try:
            print(f"Encoding feature\n")
            le = LabelEncoder()
            self.df["Gender"] = le.fit_transform(self.df["Gender"])
            print(f"Encoding Done", end=separator)

        except Exception as e:
            print("error in feature encoding",e)

    def feature_scaling(self):
        """Scales numerical features to a standard normal distribution (mean=0, variance=1)."""

        self.feature_encoding()
        try:
            print(f"Scaling feature\n")
            scaler = StandardScaler()
            scaler.set_output(transform="pandas")
            self.X = scaler.fit_transform(self.df)
            print(f"Scaling Done", end=separator)

        except Exception as e:
            print("Error in feature scaling",e)

    def elbow_method(self):
        """
        Executes the Elbow Method to help determine the optimal number of clusters.

        Calculates and plots the Within-Cluster Sum of Square for 1 to 10 clusters.
        """

        self.feature_scaling()
        try:
            self.within_cluster_sum_of_square = []
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, random_state=42)
                kmeans.fit(self.X)
                self.within_cluster_sum_of_square.append(kmeans.inertia_)
            plt.plot(range(1, 11), self.within_cluster_sum_of_square, marker='o')
            plt.title("Elbow Method", fontsize=10, weight='bold')
            plt.xlabel("Number of clusters", fontsize=10, weight='bold')
            plt.ylabel("Within Cluster Sum Of Square", fontsize=10, weight='bold')
            plt.show()
        except Exception as e:
            print("Error in elbow method", e)

    def model_training(self):
        """Fits the K-Means model with a specified number of clusters and labels the data."""

        self.elbow_method()
        try:
            self.model = KMeans(n_clusters=6, random_state=self.random_state)
            self.X["Clusters_formed"] = self.model.fit_predict(self.X)
            print("Training completed and clusters assigned", end=separator)
        except Exception as e:
            print("Error in training the model", e)

    def visualize_clusters(self):
        """
        Visualizes the final clusters and their centroids.

        Displays a scatter plot of segments and prints the Silhouette Score to evaluate quality.
        """

        self.model_training()
        try:
            plt.figure(figsize=(10, 7))
            sns.scatterplot(x=self.X["Annual Income (k$)"], y=self.X["Spending Score (1-100)"],
                            hue=self.X["Clusters_formed"], palette="Set1")
            centers = self.model.cluster_centers_  # Centroids
            plt.scatter(centers[:, 2], centers[:, 3], s=300, marker='*', c='black', label='Centroids')
            plt.title("Customer Segments", color='red', fontsize=20, weight='bold')
            plt.legend()
            plt.show()
            print("Customer Segmentation Visualization Completed", end=separator)
            score = silhouette_score(self.X, self.X["Clusters_formed"])
            print(f'Silhouette Score: {score:.3f}')

        except Exception as e:
            print("Error in visualizing clusters", e)


def main():
    """Entry point to program"""

    path = "Mall_Customers.csv"
    customer = Customer(path)
    customer.visualize_clusters()

if __name__ == "__main__":
    main()
