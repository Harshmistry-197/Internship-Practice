import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt

seperator = f"\n\n{'-' * 100}\n\n"

class AprioriAlgorithm:


    def __init__(self):
        self.df = None
        self.encoded_df = None
        self.basket = None
        self.transaction = None
        self.encoder = TransactionEncoder()
        self.algorithm = None
        self.rules = None

    def load_data(self):

        try:
            self.df = pd.read_csv("Groceries_Dataset.csv")
            print(f"\nDataset loaded successfully \n{self.df.head()}\n", end=seperator)

        except FileNotFoundError as e:
            print("File not found", e)

    def group_items(self):


        self.load_data()

        try:
            self.basket = self.df.groupby(["Member_number", "Date"])["itemDescription"].apply(list).reset_index()
            self.transaction = self.basket["itemDescription"].tolist()

            print("\nSuccessfully grouped items by transactions", end = seperator)

        except Exception as e:
            print(e)

    def feature_encoding(self):


        self.group_items()

        try:
            encoder_array = self.encoder.fit_transform(self.transaction)
            self.encoded_df = pd.DataFrame(encoder_array, columns = self.encoder.columns_)

            print("Feature encoding successful", end=seperator)

        except Exception as e:
            print(e)

    def run_algorithm(self):


        self.feature_encoding()

        try:
            self.algorithm = apriori(
                self.encoded_df,
                min_support = 0.01,
                use_colnames = True
            )
            print(f"Total Frequent Item-sets = {self.algorithm.shape[0]}\n")

            print("Model Training Completed", end = seperator)

        except Exception as e:
            print(e)

    def generate_association_rules(self):

        self.run_algorithm()

        try:
            # 1. Generate rules
            rules_df = association_rules(
                self.algorithm,
                metric="confidence",
                min_threshold=0.1
            )

            # 2. Guard Clause: Check if rules_df is valid before processing
            if rules_df is None or rules_df.empty:
                print("No association rules were generated.")
                return

            # 3. Filter rules
            self.rules = rules_df[
                rules_df['antecedents'].apply(lambda x: len(x) >= 1) &
                rules_df['consequents'].apply(lambda x: len(x) >= 1)
                ]

            print("Association Rules:", self.rules.shape[0])
            print(self.rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5),end=seperator)

        except Exception as error:
            print(f"Error in generating rules: {error}")

    def visualize(self):

        self.generate_association_rules()
        try:
            print("Visualization Done successfully")
            top_items = self.df['itemDescription'].value_counts().head(10)
            top_items.plot(kind='bar', title='Top 10 Most Purchased Items')
            plt.xlabel("Item")
            plt.ylabel("Count")
            plt.show()

        except Exception as e:
            print(e)

def main():
    algorithm = AprioriAlgorithm()
    algorithm.visualize()

if __name__ == "__main__":
    main()