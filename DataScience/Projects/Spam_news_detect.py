# Advanced Fake News Detection System
# Using AI, ML, and Deep Learning Techniques

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Deep Learning Libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Natural Language Processing
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

print("🚀 Starting Advanced Fake News Detection System")
print("="*60)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    print("✅ NLTK data downloaded successfully")
except:
    print("⚠️ NLTK download failed, using basic preprocessing")

class FakeNewsDetector:
    def __init__(self):
        self.tokenizer = None
        self.dl_model = None
        self.ml_models = {}
        self.tfidf_vectorizer = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def load_dataset(self, file_path="news_dataset.csv"):
        """Load and display dataset information"""
        print("\n📊 LOADING DATASET")
        print("-" * 30)
        
        try:
            # For demonstration, creating a sample dataset if file doesn't exist
            # In real use, replace with your actual dataset
            if not pd.io.common.file_exists(file_path):
                print("📝 Creating sample dataset for demonstration...")
                sample_data = {
                    'text': [
                        "Scientists discover new planet in solar system with potential for life",
                        "SHOCKING: Celebrity reveals secret that will change everything!",
                        "Local government announces new infrastructure project funding",
                        "You won't believe what happened next! Doctors hate this simple trick!",
                        "Research shows climate change effects accelerating globally",
                        "BREAKING: Miracle cure found! Big pharma doesn't want you to know!",
                        "Economic indicators suggest market stability in next quarter",
                        "This one simple trick will make you rich overnight guaranteed!",
                        "University study reveals new insights into human behavior",
                        "EXCLUSIVE: Secret government documents leaked! Truth revealed!"
                    ],
                    'label': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 0=Real, 1=Fake
                }
                self.data = pd.DataFrame(sample_data)
                print("✅ Sample dataset created successfully")
            else:
                self.data = pd.read_csv(file_path)
                print(f"✅ Dataset loaded from {file_path}")
            
            # Display dataset info
            print(f"📋 Dataset Shape: {self.data.shape}")
            print(f"📋 Columns: {list(self.data.columns)}")
            print(f"📋 Missing Values: {self.data.isnull().sum().sum()}")
            
            # Label distribution
            label_counts = self.data['label'].value_counts()
            print(f"📊 Label Distribution:")
            print(f"   Real News (0): {label_counts.get(0, 0)} articles")
            print(f"   Fake News (1): {label_counts.get(1, 0)} articles")
            
            return self.data
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None
    
    def clean_text(self, text):
        """Advanced text cleaning and preprocessing"""
        if pd.isna(text):
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+|\#\w+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and remove stopwords
        try:
            tokens = word_tokenize(text)
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                     if word not in self.stop_words and len(word) > 2]
            return ' '.join(tokens)
        except:
            # Fallback if NLTK fails
            words = text.split()
            return ' '.join([word for word in words if len(word) > 2])
    
    def preprocess_data(self):
        """Preprocess the text data"""
        print("\n🧹 PREPROCESSING DATA")
        print("-" * 30)
        
        print("🔄 Cleaning text data...")
        self.data['cleaned_text'] = self.data['text'].apply(self.clean_text)
        
        # Remove empty texts
        initial_size = len(self.data)
        self.data = self.data[self.data['cleaned_text'].str.len() > 0]
        final_size = len(self.data)
        
        print(f"✅ Text cleaning completed")
        print(f"📊 Removed {initial_size - final_size} empty texts")
        print(f"📊 Final dataset size: {final_size}")
        
        # Display sample cleaned texts
        print("\n📝 Sample cleaned texts:")
        for i in range(min(3, len(self.data))):
            print(f"   Original: {self.data.iloc[i]['text'][:100]}...")
            print(f"   Cleaned:  {self.data.iloc[i]['cleaned_text'][:100]}...")
            print()
    
    def exploratory_data_analysis(self):
        """Perform EDA on the dataset"""
        print("\n📈 EXPLORATORY DATA ANALYSIS")
        print("-" * 30)
        
        # Text length analysis
        self.data['text_length'] = self.data['cleaned_text'].str.len()
        self.data['word_count'] = self.data['cleaned_text'].str.split().str.len()
        
        print("📊 Text Statistics:")
        print(f"   Average text length: {self.data['text_length'].mean():.1f} characters")
        print(f"   Average word count: {self.data['word_count'].mean():.1f} words")
        
        # Statistics by label
        stats_by_label = self.data.groupby('label')[['text_length', 'word_count']].mean()
        print(f"\n📊 Statistics by Label:")
        for label in [0, 1]:
            label_name = "Real" if label == 0 else "Fake"
            if label in stats_by_label.index:
                print(f"   {label_name} News - Avg Length: {stats_by_label.loc[label, 'text_length']:.1f}, "
                      f"Avg Words: {stats_by_label.loc[label, 'word_count']:.1f}")
        
        print("✅ EDA completed")
    
    def prepare_features(self):
        """Prepare features for ML and DL models"""
        print("\n🔧 PREPARING FEATURES")
        print("-" * 30)
        
        # Features and labels
        X = self.data['cleaned_text'].values
        y = self.data['label'].values
        
        print(f"📊 Features shape: {X.shape}")
        print(f"📊 Labels shape: {y.shape}")
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📊 Training set: {len(self.X_train)} samples")
        print(f"📊 Test set: {len(self.X_test)} samples")
        print("✅ Features prepared successfully")
    
    def prepare_dl_features(self):
        """Prepare features specifically for deep learning"""
        print("\n🤖 PREPARING DEEP LEARNING FEATURES")
        print("-" * 30)
        
        # Tokenization for DL
        self.tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(self.X_train)
        
        # Convert texts to sequences
        X_train_seq = self.tokenizer.texts_to_sequences(self.X_train)
        X_test_seq = self.tokenizer.texts_to_sequences(self.X_test)
        
        # Padding sequences
        max_length = 200
        self.X_train_pad = pad_sequences(X_train_seq, maxlen=max_length)
        self.X_test_pad = pad_sequences(X_test_seq, maxlen=max_length)
        
        vocab_size = len(self.tokenizer.word_index) + 1
        
        print(f"📊 Vocabulary size: {vocab_size}")
        print(f"📊 Sequence max length: {max_length}")
        print(f"📊 Training sequences shape: {self.X_train_pad.shape}")
        print(f"📊 Test sequences shape: {self.X_test_pad.shape}")
        print("✅ DL features prepared successfully")
    
    def prepare_ml_features(self):
        """Prepare features for traditional ML models"""
        print("\n🔬 PREPARING MACHINE LEARNING FEATURES")
        print("-" * 30)
        
        # TF-IDF Vectorization
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        self.X_train_tfidf = self.tfidf_vectorizer.fit_transform(self.X_train)
        self.X_test_tfidf = self.tfidf_vectorizer.transform(self.X_test)
        
        print(f"📊 TF-IDF features shape: {self.X_train_tfidf.shape}")
        print("✅ ML features prepared successfully")
    
    def build_dl_model(self):
        """Build and train deep learning model"""
        print("\n🧠 BUILDING DEEP LEARNING MODEL")
        print("-" * 30)
        
        vocab_size = len(self.tokenizer.word_index) + 1
        embedding_dim = 128
        max_length = 200
        
        # Build LSTM model
        self.dl_model = Sequential([
            Embedding(vocab_size, embedding_dim, input_length=max_length),
            Bidirectional(LSTM(64, return_sequences=True, dropout=0.5, recurrent_dropout=0.5)),
            Bidirectional(LSTM(32, dropout=0.5, recurrent_dropout=0.5)),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        # Compile model
        self.dl_model.compile(
            loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        
        print("🏗️ Model Architecture:")
        self.dl_model.summary()
        
        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.0001)
        
        print("\n🔄 Training Deep Learning Model...")
        
        # Train model
        history = self.dl_model.fit(
            self.X_train_pad, self.y_train,
            epochs=10,
            batch_size=32,
            validation_split=0.2,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        print("✅ Deep Learning model trained successfully")
        return history
    
    def train_ml_models(self):
        """Train traditional ML models"""
        print("\n🎯 TRAINING MACHINE LEARNING MODELS")
        print("-" * 30)
        
        # Define models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'SVM': SVC(kernel='linear', random_state=42, probability=True)
        }
        
        # Train each model
        for name, model in models.items():
            print(f"🔄 Training {name}...")
            model.fit(self.X_train_tfidf, self.y_train)
            self.ml_models[name] = model
            print(f"✅ {name} trained successfully")
        
        print("✅ All ML models trained successfully")
    
    def evaluate_models(self):
        """Evaluate all models"""
        print("\n📊 EVALUATING MODELS")
        print("=" * 50)
        
        results = {}
        
        # Evaluate Deep Learning Model
        print("\n🧠 DEEP LEARNING MODEL RESULTS:")
        print("-" * 40)
        dl_loss, dl_accuracy = self.dl_model.evaluate(self.X_test_pad, self.y_test, verbose=0)
        dl_predictions = (self.dl_model.predict(self.X_test_pad, verbose=0) > 0.5).astype(int)
        
        print(f"📈 Accuracy: {dl_accuracy:.4f}")
        print(f"📉 Loss: {dl_loss:.4f}")
        print("\n📋 Classification Report:")
        print(classification_report(self.y_test, dl_predictions))
        
        results['Deep Learning'] = dl_accuracy
        
        # Evaluate ML Models
        print("\n🔬 MACHINE LEARNING MODELS RESULTS:")
        print("-" * 40)
        
        for name, model in self.ml_models.items():
            ml_predictions = model.predict(self.X_test_tfidf)
            ml_accuracy = accuracy_score(self.y_test, ml_predictions)
            
            print(f"\n📊 {name}:")
            print(f"   Accuracy: {ml_accuracy:.4f}")
            
            results[name] = ml_accuracy
        
        # Best model
        best_model = max(results, key=results.get)
        best_accuracy = results[best_model]
        
        print(f"\n🏆 BEST PERFORMING MODEL:")
        print(f"   Model: {best_model}")
        print(f"   Accuracy: {best_accuracy:.4f}")
        
        return results
    
    def predict_single_text(self, text):
        """Predict if a single text is fake or real"""
        print("\n🔍 MAKING PREDICTION")
        print("-" * 30)
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        print(f"📝 Original text: {text[:100]}...")
        print(f"🧹 Cleaned text: {cleaned_text[:100]}...")
        
        predictions = {}
        
        # Deep Learning Prediction
        if self.dl_model and self.tokenizer:
            text_seq = self.tokenizer.texts_to_sequences([cleaned_text])
            text_pad = pad_sequences(text_seq, maxlen=200)
            dl_pred = self.dl_model.predict(text_pad, verbose=0)[0][0]
            dl_label = "FAKE" if dl_pred > 0.5 else "REAL"
            predictions['Deep Learning'] = {'confidence': dl_pred, 'label': dl_label}
            print(f"🧠 Deep Learning: {dl_label} (confidence: {dl_pred:.4f})")
        
        # ML Predictions
        if self.tfidf_vectorizer:
            text_tfidf = self.tfidf_vectorizer.transform([cleaned_text])
            
            for name, model in self.ml_models.items():
                ml_pred_proba = model.predict_proba(text_tfidf)[0]
                ml_confidence = ml_pred_proba[1]  # Probability of being fake
                ml_label = "FAKE" if ml_confidence > 0.5 else "REAL"
                predictions[name] = {'confidence': ml_confidence, 'label': ml_label}
                print(f"🎯 {name}: {ml_label} (confidence: {ml_confidence:.4f})")
        
        # Ensemble prediction
        if predictions:
            confidences = [pred['confidence'] for pred in predictions.values()]
            avg_confidence = np.mean(confidences)
            ensemble_label = "FAKE" if avg_confidence > 0.5 else "REAL"
            
            print(f"\n🎭 ENSEMBLE PREDICTION:")
            print(f"   Label: {ensemble_label}")
            print(f"   Confidence: {avg_confidence:.4f}")
        
        return predictions
    
    def interactive_prediction(self):
        """Interactive prediction interface"""
        print("\n🎯 INTERACTIVE PREDICTION MODE")
        print("=" * 50)
        print("Enter news text to check if it's real or fake")
        print("Type 'exit' to quit")
        
        while True:
            print("\n" + "-" * 50)
            user_input = input("📰 Enter news text: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Thank you for using Fake News Detector!")
                break
            
            if not user_input:
                print("⚠️ Please enter some text")
                continue
            
            try:
                predictions = self.predict_single_text(user_input)
                print("\n" + "="*50)
            except Exception as e:
                print(f"❌ Error making prediction: {e}")

# Main execution
def main():
    print("🎯 INITIALIZING FAKE NEWS DETECTOR")
    print("="*60)
    
    # Create detector instance
    detector = FakeNewsDetector()
    
    # Step 1: Load Dataset
    data = detector.load_dataset()
    if data is None:
        print("❌ Failed to load dataset. Exiting...")
        return
    
    # Step 2: Preprocess Data
    detector.preprocess_data()
    
    # Step 3: Exploratory Data Analysis
    detector.exploratory_data_analysis()
    
    # Step 4: Prepare Features
    detector.prepare_features()
    
    # Step 5: Prepare DL Features
    detector.prepare_dl_features()
    
    # Step 6: Prepare ML Features
    detector.prepare_ml_features()
    
    # Step 7: Build and Train DL Model
    dl_history = detector.build_dl_model()
    
    # Step 8: Train ML Models
    detector.train_ml_models()
    
    # Step 9: Evaluate Models
    results = detector.evaluate_models()
    
    print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    # Step 10: Interactive Prediction
    detector.interactive_prediction()

if __name__ == "__main__":
    main()