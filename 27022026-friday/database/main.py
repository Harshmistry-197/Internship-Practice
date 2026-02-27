import pandas as pd
from sqlalchemy import create_engine, text


class MSSQLData:
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




def main():

    # Database credentials
    server = "localhost"
    database = "harsh"

    # Initialize loader
    loader = MSSQLData(server, database)


    # Load data from table
    df = loader.load_table("car_evaluation")

    print("Original Data:")
    print(df.head())



if __name__ == "__main__":
    main()