# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
# %%
df = pd.read_csv("dataset.csv")

# %%
print(df.head())
print(df.shape)

# %%
X = df.drop("label", axis=1)
y = df["label"]

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# %%
from sklearn.calibration import CalibratedClassifierCV

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)

calibrated_model = CalibratedClassifierCV(model, method='sigmoid')

calibrated_model.fit(X_train, y_train)

model = calibrated_model

# %%
y_pred = model.predict(X_test)
probs = model.predict_proba(X_test)[:,1]
#print(probs)
print(set(probs))
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# %%
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# %%
