"""
train_model.py
---------------
Trains a Random Forest classifier on the admission dataset and persists
it to admission_model.pkl. This is a genuine, trained machine learning
model — predictions at inference time are computed by the model, not
hardcoded or simulated.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle

df = pd.read_csv('admission_data.csv')

le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])
category_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print("Category encoding:", category_mapping)

features = ['avg_academic_score', 'entrance_score', 'category_encoded', 'score_gap_from_cutoff']
X = df[features]
y = df['admitted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")
print(classification_report(y_test, y_pred))

importance_df = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("Feature Importance:")
print(importance_df.to_string(index=False))

with open('admission_model.pkl', 'wb') as f:
    pickle.dump({
        'model': model,
        'category_mapping': category_mapping,
        'feature_importance': importance_df.to_dict('records'),
        'accuracy': accuracy
    }, f)

print("\nModel saved to 'admission_model.pkl'.")
