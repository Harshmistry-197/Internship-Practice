import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler


# Read Data
df = pd.read_csv("insurance.csv")
print(df.head())


# To check shape of dataset
print(f"Shape of dataset {df.shape}\n")
# Feature Name
print(f"Column name : {df.columns}\n")
# data types
print(f"Data type of dataset\n {df.dtypes}\n")
# Unique values
print("Unique values in each feature")
for i in df.columns:
    print(f"{i} : {df[i].nunique()}")

    

# Data Preprocessing
# concise summary
print(f"The concise summary of dataset : \n")
print(df.info())

# statistical summary
print("The statistical summary of the dataset : \n")
print(df.describe(include='all'))

# Finding the missing value
print("Checking missing values in the dataset \n")
print(df.isnull().sum())

# Finding the duplicate values
print("Finding the duplicate values \n")
print(df.duplicated().sum())

# Dropping the duplicate value
df.drop_duplicates(inplace=True)
print(df.duplicated().sum())

# Checking the Outliers
plt.figure(figsize=(8,6))
sns.pairplot(df,hue="smoker", palette="muted")
plt.show()

# Box plot
sns.boxplot(df['age'])
plt.title("Boxplot for Age")

# Scatter plot
plt.scatter(df['bmi'], df['children'])
plt.xlabel("Bmi")
plt.ylabel("Children")
plt.show()

# Barplot
sns.boxplot(df['bmi'])
plt.title("Boxplot for BMI")
plt.show()

Q1 = df['bmi'].quantile(0.25)
Q3 = df['bmi'].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR
outliers = df[(df['bmi'] < lower_limit) | (df['bmi'] > upper_limit)]
print(lower_limit, upper_limit)
print(outliers)

Q1 = df['charges'].quantile(0.25)
Q3 = df['charges'].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR
outliers = df[(df['charges'] < lower_limit) | (df['charges'] > upper_limit)]
print(Q1, Q3)
print(outliers)

# Handling Outlier
import numpy as np
bmi_mean = df['bmi'].mean()
print(bmi_mean)
df['bmi'] = np.where((df['bmi'] < lower_limit) | (df['bmi'] > upper_limit), bmi_mean, df['bmi'])
df.head()

# Handling Categorical Feature
df = pd.get_dummies(df, drop_first = True).astype(int)
print(df.head())



# Train Test Split
X = df.drop('charges', axis = 1)
y = df['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)


# Scaling the Feature
scaler = StandardScaler()
cols_to_scale = ["age", "bmi", "children"]
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)



# Model Training

# Training the Model
model = LinearRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
print(y_pred)



# ## Model Evaluation
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"R2 score : {r2}")
print(f"Mean absolute error : {mae}")
print(f"Mean Squared error : {mse}")
print(f"Root Mean Squared error : {rmse}")



# Actual Price vs Predicted Price
plt.figure(figsize=(8,6))
sns.scatterplot(x=y_test, y=y_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], c='yellow',  linewidth=2)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Predicted vs Actual Price")
plt.show()