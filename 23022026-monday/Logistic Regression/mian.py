# import required library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


# Read Data
df = pd.read_csv("weather_forecast_data.csv")
print(df.head())