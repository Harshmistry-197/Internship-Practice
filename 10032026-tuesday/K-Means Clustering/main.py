import pandas as pd
import numpy as np

separator = f"\n\n{'-'*60}\n\n"

class Customer:
    def __init__(self, file_path):

        self.file_path = file_path
        self.random_state = 42

        self.df = None

    def load_data(self):
        print("Loading the data\n")
        self.df = pd.read_csv(self.file_path)
        print(f"Data Loaded with rows and columns {self.df.shape}\n")
        print(self.df.head(), end=separator)


def main():
    path = "Mall_Customers.csv"
    customer = Customer(path)
    customer.load_data()

if __name__ == "__main__":
    main()
