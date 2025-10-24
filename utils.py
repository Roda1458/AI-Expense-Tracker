from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def train_category_model(df):
    df = df.dropna(subset=['Category'])
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Description'])
    y = df['Category']
    model = MultinomialNB()
    model.fit(X, y)
    return model, vectorizer

def predict_missing_categories(df, model, vectorizer):
    missing = df['Category'].isna()
    if missing.any():
        X_pred = vectorizer.transform(df.loc[missing, 'Description'])
        df.loc[missing, 'Category'] = model.predict(X_pred)
    return df
