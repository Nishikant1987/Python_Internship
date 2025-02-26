import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the dataset
file_path = r"C:\Users\Administrator\Downloads\spam_dataset.csv"  # Update this with the correct path if needed
data = pd.read_csv(file_path)

# Display basic dataset info
print("Dataset Head:")
print(data.head())
print("\nDataset Info:")
print(data.info())

# Check class distribution
sns.countplot(x='Label', data=data)
plt.title("Distribution of Spam and Non-Spam Emails")
plt.show()

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['Email'], data['Label'], test_size=0.2, random_state=42)

# Creating a pipeline for text processing and model training
model_pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('classifier', MultinomialNB())
])

# Train the model
model_pipeline.fit(X_train, y_train)

# Make predictions
y_pred = model_pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Spam', 'Spam'], yticklabels=['Not Spam', 'Spam'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()
