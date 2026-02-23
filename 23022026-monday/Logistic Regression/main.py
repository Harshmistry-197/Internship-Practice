# import required library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

# Read Data
df = pd.read_csv("healthcare-dataset-stroke-data.csv")
# print(df.head())  # printing first 5 rows
# print(df.shape)
print(df.info())
print(df.describe())
print(df.duplicated().sum())
sns.pairplot(df, hue='stroke')
plt.title('Pair plot of Health care dataset')
plt.show()


# Checking the nul values
print(df.isnull().sum())


# Checking for outliers in 'bmi'
sns.boxplot(df['bmi'])
plt.title('Box plot of BMI')
plt.show()


# Handling null values of 'bmi'
df['bmi'] = df['bmi'].fillna(df['bmi'].median())
print(df.isnull().sum())
print(df.info())


# Splitting the dependent and independent variable
df = df[df['gender'] != 'Other']   # remove the gender = other as there was single row
X = df.drop('stroke', axis=1)
y = df['stroke']
print(X.head())
print(y.head())


# dropping id
X = X.drop('id', axis=1)
print(X.head())


# Checking Outliers

# Checking Outliers in Age
sns.boxplot(X['age'])
plt.title('Box plot of Age')
plt.show()


# Checking and handling Outliers in avg_glucose_level
sns.boxplot(X['avg_glucose_level'])
plt.title('Box plot of abg_glucose_level')
plt.show()

Q1 = X['avg_glucose_level'].quantile(0.25)
Q3 = X['avg_glucose_level'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 1.5 * IQR

X['avg_glucose_level'] = np.where(X['avg_glucose_level'] > upper_limit, upper_limit, X['avg_glucose_level'])


# Checking and handling outlier in bmi
Q1 = X['bmi'].quantile(0.25)
Q3 = X['bmi'].quantile(0.75)
IQR = Q3 -Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR
print(lower_limit, upper_limit)
bmi_median = X['bmi'].median()
X['bmi'] = np.where((X['bmi'] < lower_limit) | (X['bmi'] > upper_limit), bmi_median, X['bmi'])



# Feature Encoding
# Label Encoding on 'gender', 'Residence_type' and 'ever_married'
le = LabelEncoder()
X['gender'] = le.fit_transform(X["gender"])

X['Residence_type'] = le.fit_transform(X["Residence_type"])

X['ever_married'] = le.fit_transform(X["ever_married"])



# One Hot Encoding on 'work_type' and 'smoking_status'
X = pd.get_dummies(X, columns=['work_type', 'smoking_status'], drop_first=True, dtype=int)
print(X.head())

print(X.shape, y.shape)


# Splitting into train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape)


# Scaling the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


smote = SMOTE(random_state=0)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(X_train_res.shape)


# Training the data on logistic regression
classifier = LogisticRegression()
classifier.fit(X_train_res, y_train_res)
y_pred = classifier.predict(X_test)


# Model Evaluation
print(f"The classification report is : \n {classification_report(y_test, y_pred)}")
print(f"The confusion matrix is : \n {confusion_matrix(y_test, y_pred)}")
print(f"The accuracy score is : {accuracy_score(y_test, y_pred)}")


# Sample Data Testing
new_patient = {
    'gender': 'Male',
    'age': 67,
    'hypertension': 0,
    'heart_disease': 1,
    'ever_married': 'Yes',
    'work_type': 'Private',
    'Residence_type': 'Urban',
    'avg_glucose_level': 228.69,
    'bmi': 36.6,
    'smoking_status': 'formerly smoked'
}

sample_df = pd.DataFrame([new_patient])

sample_df['gender'] = le.fit_transform(sample_df['gender'])
sample_df['Residence_type'] = le.fit_transform(sample_df['Residence_type'])
sample_df['ever_married'] = le.fit_transform(sample_df['ever_married'])

new_df_encoded = pd.get_dummies(sample_df, columns=['work_type', 'smoking_status'], drop_first=True, dtype=int)

new_df_encoded = new_df_encoded.reindex(columns=X.columns, fill_value=0)

new_patient_scaled = scaler.transform(new_df_encoded)
prediction = classifier.predict(new_patient_scaled)
if prediction[0] == 1:
    print(f"Stroke")
else:
    print(f"Not Stroke")