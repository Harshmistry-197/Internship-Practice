import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
        print(f"Loaded Data : {self.df.shape}", end=seperator)


        return self.df


def main():
    model = Customer(file_path = "customer_purchase_data.csv")
    model.load_data()


if __name__ == "__main__":
    main()
