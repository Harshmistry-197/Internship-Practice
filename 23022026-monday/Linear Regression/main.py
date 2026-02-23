from sklearn.datasets import load_diabetes
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

df = load_diabetes()

X = df.data
y = df.target

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=10)

scaling = StandardScaler()
X_train = scaling.fit_transform(X_train)
X_test = scaling.transform(X_test)

regression = LinearRegression()
regression.fit(X_train,y_train)

y_pred = regression.predict(X_test)

r2 = r2_score(y_test,y_pred)
print(r2)