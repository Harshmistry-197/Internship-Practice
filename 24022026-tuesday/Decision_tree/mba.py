import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix


import warnings
warnings.filterwarnings("ignore")


# Import dataset
def load_data():
    df = pd.read_csv("MBA.csv")
    print(df.head())
    print(df.shape)
    print(df.info())
    print(df.describe())
    return df


# Checking the duplicates
def duplicate(df):
    print(f"\n The duplicate value : {df.duplicated().sum()}")


# Checking for null values
def null_values(df):
    print(f"\n The Null value : {df.isnull().sum()}")


# Handling Missing values
def handle_null_value(df):
    df['race'] = df['race'].fillna(df['race'].mode()[0])
    df['admission'] = df['admission'].fillna("Deny")
    return df


# Spliting X and y
def split(df):
    x = df.drop(["admission", "application_id"], axis = 1)
    y = df['admission']
    print(x.head())
    print(y.head())
    return x, y



# checking outliers
def checking_outliers(x):
    column = ["gpa","gmat", "work_exp"]
    for i, cols in enumerate(column):
        plt.subplot(2, 2, i+1)
        plt.grid(alpha=0.3)
        sns.boxplot(x=cols, data=x, palette="muted")
        plt.title(cols, fontsize = 10, weight = "semibold")
    plt.tight_layout()
    plt.show()

    print(f"The Unique value of Gender : {x['gender'].value_counts()}\n")
    print(f"The Unique value of International : {x['international'].value_counts()}\n")
    print(f"The Unique value of Major : {x['major'].value_counts()}\n")
    print(f"The Unique value of Race : {x['race'].value_counts()}\n")
    print(f"The Unique value of Work_industry : {x['work_industry'].value_counts()}\n")

    cols = ["gpa","gmat", "work_exp"]
    for col in cols:
        q1 = x[col].quantile(0.25)
        q3 = x[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5*iqr
        upper_bound = q3 + 1.5*iqr
        outlier = (x[col] < lower_bound) | (x[col] > upper_bound)
        print(f"{col} : {outlier.sum()} outliers")
        x[col] = x[col].clip(lower_bound, upper_bound)
        print(f"Outliers remove succesfully\n")
    return x


def dependent_data_distribution(y):
    print(y.value_counts())

def encoding_features(X, y):
    le = LabelEncoder()
    X['gender'] = le.fit_transform(X['gender'])
    X['international'] = le.fit_transform(X['international'])

    X = pd.get_dummies(X, columns=["major", 'race', 'work_industry'], drop_first=True, dtype=int)

    y = le.fit_transform(y)
    return X, y


def smote(X_Train, y_Train):
    smote = SMOTE()
    x_rain_res, y_rain_res = smote.fit_resample(X_Train, y_Train)
    return x_rain_res, y_rain_res


def train_model(x_train, ytrain):
    classifier = DecisionTreeClassifier(criterion='log_loss',min_samples_leaf=20, max_depth=20, max_leaf_nodes=15, random_state=42,
                                        ccp_alpha=0.0, max_features='sqrt')
    classifier.fit(x_train, ytrain)
    return classifier



def model_evalution(classifier, x_test, y_est):
    y_pred = classifier.predict(x_test)
    print(f"Classification report : \n{classification_report(y_est, y_pred)}")
    print(f"Confusion Matrix : \n{confusion_matrix(y_est, y_pred)}")
    print(f"Accuracy Score : \n{accuracy_score(y_est, y_pred)}")


def heatmap(df):
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="YlOrRd")
    plt.show()



if __name__ == "__main__":
    data_frame = load_data()
    duplicate(data_frame)
    null_values(data_frame)
    data_frame = handle_null_value(data_frame)
    null_values(data_frame)
    X_, y_ = split(data_frame)
    X_ = checking_outliers(X_)
    heatmap(data_frame)
    dependent_data_distribution(y_)
    X_, y_ = encoding_features(X_, y_)
    X_train, X_test, y_train, y_test = train_test_split(X_, y_, test_size=0.2, random_state=42)
    X_train_res, y_train_res = smote(X_train, y_train)
    classify = train_model(X_train_res, y_train_res)
    model_evalution(classify, X_test, y_test)






