import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

# Load dataset
df = pd.read_csv('properties.csv', low_memory=False)

# ✅ Select useful numeric and categorical features
selected_columns = [
    'Carpet Area', 'bedroom', 'Bathroom', 'Parking',
    'City', 'furnished Type', 'Ownership Type', 'Type of Property',
    'Price'  # Target variable
]

df = df[selected_columns].copy()

# 🧹 Clean Parking (e.g., "1 Covered" → 1)
df['Parking'] = df['Parking'].astype(str).str.extract(r'(\d+)')
df['Parking'] = pd.to_numeric(df['Parking'], errors='coerce')

# Drop rows with any missing values
df = df.dropna()

# ✅ Split features and target
X = df.drop('Price', axis=1)
y = df['Price']

# Identify column types
numeric_features = ['Carpet Area', 'bedroom', 'Bathroom', 'Parking']
categorical_features = ['City', 'furnished Type', 'Ownership Type', 'Type of Property']

# ⚙️ Preprocessing pipelines
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# 🔧 Create full pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# 📊 Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🧠 Train the model
model_pipeline.fit(X_train, y_train)

# 💾 Save model
joblib.dump(model_pipeline, 'house_price_model.pkl')
print("✅ Model trained and saved as 'house_price_model.pkl'")
