# Complete Fake News Detection System with Dataset Creation & Visualization
# Including CSV dataset generation and comprehensive data visualization

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
from collections import Counter

print("🚀 Complete Fake News Detection System with Visualization")
print("="*70)

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_comprehensive_dataset():
    """Create a comprehensive fake news dataset"""
    print("\n📝 CREATING COMPREHENSIVE NEWS DATASET")
    print("-" * 50)
    
    # Real news articles
    real_news = [
        "Scientists at MIT have developed a new renewable energy technology that could revolutionize solar power generation with 40% improved efficiency.",
        "The Federal Reserve announced a quarter-point interest rate increase following the latest economic data showing steady inflation control.",
        "Local authorities report successful completion of the new public transportation project, connecting three major districts in the city.",
        "Climate researchers publish findings in Nature journal showing accelerated ice melting in Antarctic regions over the past decade.",
        "The Supreme Court heard arguments today regarding privacy rights in digital communications, with a decision expected next quarter.",
        "Medical researchers at Johns Hopkins University announce breakthrough in early detection methods for pancreatic cancer through blood tests.",
        "International trade negotiations between allied nations continue as officials work toward mutually beneficial economic agreements.",
        "NASA confirms successful deployment of the James Webb Space Telescope's latest observations revealing new exoplanet discoveries.",
        "Local school district implements new STEM education program with funding from state government and private technology partnerships.",
        "Economic indicators suggest moderate growth in manufacturing sector as supply chain issues show signs of resolution.",
        "University researchers publish peer-reviewed study on sustainable agriculture practices reducing water consumption by 30%.",
        "City council approves budget allocation for infrastructure improvements including road repairs and water system upgrades.",
        "Health officials provide updated vaccination guidelines based on latest clinical trial data and epidemiological studies.",
        "Technology companies announce collaborative effort to improve cybersecurity standards across critical infrastructure sectors.",
        "Environmental protection agency releases annual report showing measurable improvements in air quality in urban areas.",
        "Federal investigators conclude comprehensive review of financial regulations affecting small business lending practices.",
        "Archaeological team uncovers significant historical artifacts providing new insights into ancient Mediterranean civilizations.",
        "Public health authorities confirm seasonal flu vaccination campaign reaches target coverage rates across vulnerable populations.",
        "Transportation department announces completion of highway safety improvements reducing traffic accidents by 25% in pilot areas.",
        "Central bank officials indicate gradual approach to monetary policy adjustments based on employment and inflation metrics."
    ]
    
    # Fake/Spam news articles
    fake_news = [
        "SHOCKING! Secret government experiment turns ordinary people into superhuman beings! Scientists don't want you to know this!",
        "BREAKING: Billionaire reveals one simple trick that made him rich overnight! Banks hate this method!",
        "EXCLUSIVE: Aliens have been living among us for decades! Government finally admits the truth!",
        "MIRACLE CURE: Local grandmother discovers ancient remedy that cures cancer in 3 days! Doctors are furious!",
        "URGENT: New law will take away your savings! Share this before it's too late!",
        "UNBELIEVABLE: Man loses 50 pounds in one week using this weird trick! Nutritionists are speechless!",
        "CONSPIRACY EXPOSED: Major food companies have been poisoning us for years! The truth revealed!",
        "INCREDIBLE: Woman wins lottery 7 times using this secret method! Officials want to ban it!",
        "DANGER: Your smartphone is slowly killing you! This device can save your life!",
        "AMAZING: Scientists discover fountain of youth in remote jungle! Age reversal possible!",
        "TERRIBLE NEWS: Economic collapse predicted for next month! Prepare yourself now!",
        "REVOLUTIONARY: New energy device powers entire house for free! Energy companies are panicking!",
        "HORRIFYING: Deadly chemicals found in popular foods! Your family is at risk!",
        "BREAKING: Celebrity reveals shocking secret about Hollywood elite! You won't believe this!",
        "MIRACLE: Blind woman sees again after taking this natural supplement! Doctors can't explain it!",
        "EXPOSED: Social media giants are controlling your thoughts! Here's how to break free!",
        "INCREDIBLE: Time traveler from 2050 warns about upcoming disaster! Government tries to silence him!",
        "SHOCKING: Popular restaurant chain uses fake meat made from insects! Customers demand answers!",
        "URGENT WARNING: New virus more dangerous than COVID spreading rapidly! Mainstream media ignores it!",
        "AMAZING DISCOVERY: Lost city of Atlantis found! Archaeologists confirm ancient technology!"
    ]
    
    # Additional categories for more diversity
    misleading_health = [
        "Doctors discovered this one weird trick to cure diabetes naturally without medication or diet changes.",
        "Big pharma doesn't want you to know about this miracle plant that cures all diseases instantly.",
        "Shocking study reveals vaccines contain mind control chips implanted by secret organizations worldwide.",
        "Local mom discovers coffee ingredient that melts belly fat overnight while you sleep peacefully.",
        "Ancient Tibetan monks reveal secret breathing technique that adds 20 years to your lifespan."
    ]
    
    clickbait_fake = [
        "You'll never guess what this celebrity looks like now! The transformation will shock you completely!",
        "This simple quiz reveals your exact death date! Take it before it gets banned forever!",
        "Homeless man turns out to be secret millionaire! His story will make you cry tears!",
        "Teachers hate her! Student discovers study method that guarantees perfect grades without effort!",
        "This optical illusion reveals your true personality! Share with friends to compare results!"
    ]
    
    scientific_real = [
        "Peer-reviewed research published in Science journal demonstrates new carbon capture technology efficiency improvements.",
        "Clinical trial results show promising outcomes for new Alzheimer's treatment in phase two testing.",
        "Geological survey reveals previously unknown mineral deposits with potential technological applications in electronics.",
        "Marine biologists document recovery of coral reef ecosystems following conservation intervention programs.",
        "Astrophysicists confirm detection of gravitational waves from neutron star collision using advanced instrumentation."
    ]
    
    # Combine all categories
    all_real_news = real_news + scientific_real
    all_fake_news = fake_news + misleading_health + clickbait_fake
    
    # Create DataFrame
    dataset = pd.DataFrame({
        'text': all_real_news + all_fake_news,
        'label': [0] * len(all_real_news) + [1] * len(all_fake_news),  # 0=Real, 1=Fake
        'category': (
            ['Politics/Economy'] * 20 +
            ['Science/Research'] * 5 +
            ['Sensational/Clickbait'] * 20 +
            ['Health/Medical'] * 5 +
            ['Entertainment/Viral'] * 5
        )
    })
    
    # Add additional features
    dataset['text_length'] = dataset['text'].str.len()
    dataset['word_count'] = dataset['text'].str.split().str.len()
    dataset['exclamation_count'] = dataset['text'].str.count('!')
    dataset['caps_ratio'] = dataset['text'].apply(lambda x: sum(1 for c in x if c.isupper()) / len(x) if len(x) > 0 else 0)
    
    # Save to CSV
    dataset.to_csv('comprehensive_news_dataset.csv', index=False)
    
    print(f"✅ Dataset created successfully!")
    print(f"📊 Total articles: {len(dataset)}")
    print(f"📊 Real news: {sum(dataset['label'] == 0)} articles")
    print(f"📊 Fake news: {sum(dataset['label'] == 1)} articles")
    print(f"💾 Saved as: comprehensive_news_dataset.csv")
    
    return dataset

class FakeNewsVisualizationSystem:
    def __init__(self):
        self.data = None
        self.tokenizer = None
        self.dl_model = None
        self.ml_models = {}
        self.tfidf_vectorizer = None
        self.lemmatizer = WordNetLemmatizer()
        
        # Download NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    
    def load_or_create_dataset(self):
        """Load existing dataset or create new one"""
        print("\n📊 LOADING/CREATING DATASET")
        print("-" * 40)
        
        try:
            # Try to load existing dataset
            self.data = pd.read_csv('comprehensive_news_dataset.csv')
            print("✅ Loaded existing dataset")
        except FileNotFoundError:
            # Create new dataset
            print("📝 Creating new dataset...")
            self.data = create_comprehensive_dataset()
        
        print(f"📋 Dataset shape: {self.data.shape}")
        return self.data
    
    def create_basic_visualizations(self):
        """Create basic data visualizations"""
        print("\n📈 CREATING BASIC VISUALIZATIONS")
        print("-" * 40)
        
        # Set up the plotting area
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Fake News Dataset Analysis', fontsize=16, fontweight='bold')
        
        # 1. Label Distribution
        label_counts = self.data['label'].value_counts()
        labels = ['Real News', 'Fake News']
        colors = ['#2E8B57', '#DC143C']
        
        axes[0, 0].pie(label_counts.values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0, 0].set_title('Distribution of News Labels', fontweight='bold')
        
        # 2. Text Length Distribution
        axes[0, 1].hist(self.data[self.data['label']==0]['text_length'], alpha=0.7, label='Real', color='#2E8B57', bins=20)
        axes[0, 1].hist(self.data[self.data['label']==1]['text_length'], alpha=0.7, label='Fake', color='#DC143C', bins=20)
        axes[0, 1].set_xlabel('Text Length (characters)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Text Length Distribution', fontweight='bold')
        axes[0, 1].legend()
        
        # 3. Word Count Distribution
        axes[0, 2].boxplot([
            self.data[self.data['label']==0]['word_count'].values,
            self.data[self.data['label']==1]['word_count'].values
        ], labels=['Real', 'Fake'])
        axes[0, 2].set_title('Word Count Distribution', fontweight='bold')
        axes[0, 2].set_ylabel('Word Count')
        
        # 4. Exclamation Marks Usage
        axes[1, 0].bar(['Real', 'Fake'], [
            self.data[self.data['label']==0]['exclamation_count'].mean(),
            self.data[self.data['label']==1]['exclamation_count'].mean()
        ], color=['#2E8B57', '#DC143C'])
        axes[1, 0].set_title('Average Exclamation Marks', fontweight='bold')
        axes[1, 0].set_ylabel('Average Count')
        
        # 5. Capital Letters Ratio
        axes[1, 1].bar(['Real', 'Fake'], [
            self.data[self.data['label']==0]['caps_ratio'].mean(),
            self.data[self.data['label']==1]['caps_ratio'].mean()
        ], color=['#2E8B57', '#DC143C'])
        axes[1, 1].set_title('Capital Letters Ratio', fontweight='bold')
        axes[1, 1].set_ylabel('Ratio')
        
        # 6. Category Distribution
        if 'category' in self.data.columns:
            category_label = self.data.groupby(['category', 'label']).size().unstack(fill_value=0)
            category_label.plot(kind='bar', ax=axes[1, 2], color=['#2E8B57', '#DC143C'])
            axes[1, 2].set_title('News by Category', fontweight='bold')
            axes[1, 2].set_xlabel('Category')
            axes[1, 2].set_ylabel('Count')
            axes[1, 2].legend(['Real', 'Fake'])
            axes[1, 2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('news_analysis_basic.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Basic visualizations created and saved as 'news_analysis_basic.png'")
    
    def create_word_clouds(self):
        """Create word clouds for fake and real news"""
        print("\n☁️ CREATING WORD CLOUDS")
        print("-" * 40)
        
        # Prepare text data
        real_text = ' '.join(self.data[self.data['label']==0]['text'].values)
        fake_text = ' '.join(self.data[self.data['label']==1]['text'].values)
        
        # Create word clouds
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        
        # Real news word cloud
        real_wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                  colormap='Greens', max_words=100).generate(real_text)
        axes[0].imshow(real_wordcloud, interpolation='bilinear')
        axes[0].set_title('Real News - Most Common Words', fontsize=16, fontweight='bold')
        axes[0].axis('off')
        
        # Fake news word cloud
        fake_wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                  colormap='Reds', max_words=100).generate(fake_text)
        axes[1].imshow(fake_wordcloud, interpolation='bilinear')
        axes[1].set_title('Fake News - Most Common Words', fontsize=16, fontweight='bold')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig('word_clouds_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Word clouds created and saved as 'word_clouds_comparison.png'")
    
    def analyze_common_words(self):
        """Analyze most common words in fake vs real news"""
        print("\n🔤 ANALYZING COMMON WORDS")
        print("-" * 40)
        
        def get_common_words(texts, n=15):
            all_words = []
            for text in texts:
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                words = [word for word in words if word not in self.stop_words]
                all_words.extend(words)
            return Counter(all_words).most_common(n)
        
        # Get common words for each category
        real_words = get_common_words(self.data[self.data['label']==0]['text'])
        fake_words = get_common_words(self.data[self.data['label']==1]['text'])
        
        # Create comparison plot
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Real news common words
        real_df = pd.DataFrame(real_words, columns=['word', 'count'])
        axes[0].barh(real_df['word'], real_df['count'], color='#2E8B57')
        axes[0].set_title('Most Common Words - Real News', fontweight='bold')
        axes[0].set_xlabel('Frequency')
        
        # Fake news common words
        fake_df = pd.DataFrame(fake_words, columns=['word', 'count'])
        axes[1].barh(fake_df['word'], fake_df['count'], color='#DC143C')
        axes[1].set_title('Most Common Words - Fake News', fontweight='bold')
        axes[1].set_xlabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('common_words_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print top words
        print("📊 Top words in Real News:")
        for word, count in real_words[:10]:
            print(f"   {word}: {count}")
        
        print("\n📊 Top words in Fake News:")
        for word, count in fake_words[:10]:
            print(f"   {word}: {count}")
        
        print("✅ Word analysis completed and saved as 'common_words_comparison.png'")
    
    def create_interactive_visualizations(self):
        """Create interactive visualizations using Plotly"""
        print("\n🎯 CREATING INTERACTIVE VISUALIZATIONS")
        print("-" * 40)
        
        # 1. Interactive scatter plot
        fig1 = px.scatter(self.data, 
                         x='text_length', 
                         y='word_count',
                         color='label',
                         color_discrete_map={0: '#2E8B57', 1: '#DC143C'},
                         labels={'label': 'News Type', 'text_length': 'Text Length', 'word_count': 'Word Count'},
                         title='Text Length vs Word Count Distribution',
                         hover_data=['exclamation_count', 'caps_ratio'])
        
        fig1.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        
        # Update traces to show Real/Fake instead of 0/1
        fig1.for_each_trace(lambda t: t.update(name = 'Real News' if t.name == '0' else 'Fake News'))
        
        fig1.write_html('interactive_scatter_plot.html')
        fig1.show()
        
        # 2. Interactive histogram
        fig2 = make_subplots(rows=2, cols=2, 
                            subplot_titles=('Text Length Distribution', 'Word Count Distribution',
                                          'Exclamation Marks', 'Capital Letters Ratio'))
        
        # Text length histogram
        fig2.add_trace(go.Histogram(x=self.data[self.data['label']==0]['text_length'], 
                                   name='Real News', marker_color='#2E8B57', opacity=0.7), row=1, col=1)
        fig2.add_trace(go.Histogram(x=self.data[self.data['label']==1]['text_length'], 
                                   name='Fake News', marker_color='#DC143C', opacity=0.7), row=1, col=1)
        
        # Word count histogram
        fig2.add_trace(go.Histogram(x=self.data[self.data['label']==0]['word_count'], 
                                   name='Real News', marker_color='#2E8B57', opacity=0.7, showlegend=False), row=1, col=2)
        fig2.add_trace(go.Histogram(x=self.data[self.data['label']==1]['word_count'], 
                                   name='Fake News', marker_color='#DC143C', opacity=0.7, showlegend=False), row=1, col=2)
        
        # Exclamation marks
        excl_real = self.data[self.data['label']==0]['exclamation_count'].mean()
        excl_fake = self.data[self.data['label']==1]['exclamation_count'].mean()
        fig2.add_trace(go.Bar(x=['Real News', 'Fake News'], y=[excl_real, excl_fake],
                             marker_color=['#2E8B57', '#DC143C'], showlegend=False), row=2, col=1)
        
        # Capital letters ratio
        caps_real = self.data[self.data['label']==0]['caps_ratio'].mean()
        caps_fake = self.data[self.data['label']==1]['caps_ratio'].mean()
        fig2.add_trace(go.Bar(x=['Real News', 'Fake News'], y=[caps_real, caps_fake],
                             marker_color=['#2E8B57', '#DC143C'], showlegend=False), row=2, col=2)
        
        fig2.update_layout(height=600, title_text="Comprehensive News Analysis Dashboard")
        fig2.write_html('interactive_dashboard.html')
        fig2.show()
        
        print("✅ Interactive visualizations created:")
        print("   📄 interactive_scatter_plot.html")
        print("   📄 interactive_dashboard.html")
    
    def clean_text(self, text):
        """Clean text for processing"""
        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+|\#\w+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        try:
            tokens = word_tokenize(text)
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                     if word not in self.stop_words and len(word) > 2]
            return ' '.join(tokens)
        except:
            words = text.split()
            return ' '.join([word for word in words if len(word) > 2])
    
    def run_complete_analysis(self):
        """Run complete analysis with visualizations"""
        print("\n🎯 RUNNING COMPLETE ANALYSIS")
        print("="*60)
        
        # Load or create dataset
        self.load_or_create_dataset()
        
        # Display dataset info
        print(f"\n📊 DATASET OVERVIEW:")
        print(f"   Total articles: {len(self.data)}")
        print(f"   Real news: {sum(self.data['label'] == 0)} ({sum(self.data['label'] == 0)/len(self.data)*100:.1f}%)")
        print(f"   Fake news: {sum(self.data['label'] == 1)} ({sum(self.data['label'] == 1)/len(self.data)*100:.1f}%)")
        
        if 'category' in self.data.columns:
            print(f"\n📂 CATEGORIES:")
            category_counts = self.data['category'].value_counts()
            for category, count in category_counts.items():
                print(f"   {category}: {count} articles")
        
        # Create all visualizations
        print("\n🎨 CREATING VISUALIZATIONS...")
        self.create_basic_visualizations()
        self.create_word_clouds()
        self.analyze_common_words()
        self.create_interactive_visualizations()
        
        # Summary statistics
        print("\n📈 SUMMARY STATISTICS:")
        print("-" * 40)
        
        stats_by_label = self.data.groupby('label').agg({
            'text_length': ['mean', 'std'],
            'word_count': ['mean', 'std'],
            'exclamation_count': ['mean', 'sum'],
            'caps_ratio': ['mean', 'std']
        }).round(3)
        
        print("Real News Statistics:")
        real_stats = stats_by_label.loc[0]
        print(f"   Avg text length: {real_stats[('text_length', 'mean')]:.1f} ± {real_stats[('text_length', 'std')]:.1f}")
        print(f"   Avg word count: {real_stats[('word_count', 'mean')]:.1f} ± {real_stats[('word_count', 'std')]:.1f}")
        print(f"   Avg exclamations: {real_stats[('exclamation_count', 'mean')]:.2f}")
        print(f"   Avg caps ratio: {real_stats[('caps_ratio', 'mean')]:.3f}")
        
        print("\nFake News Statistics:")
        fake_stats = stats_by_label.loc[1]
        print(f"   Avg text length: {fake_stats[('text_length', 'mean')]:.1f} ± {fake_stats[('text_length', 'std')]:.1f}")
        print(f"   Avg word count: {fake_stats[('word_count', 'mean')]:.1f} ± {fake_stats[('word_count', 'std')]:.1f}")
        print(f"   Avg exclamations: {fake_stats[('exclamation_count', 'mean')]:.2f}")
        print(f"   Avg caps ratio: {fake_stats[('caps_ratio', 'mean')]:.3f}")
        
        print("\n🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("📁 Files created:")
        print("   📄 comprehensive_news_dataset.csv - Your news dataset")
        print("   🖼️ news_analysis_basic.png - Basic analysis charts")
        print("   🖼️ word_clouds_comparison.png - Word clouds comparison")  
        print("   🖼️ common_words_comparison.png - Common words analysis")
        print("   🌐 interactive_scatter_plot.html - Interactive scatter plot")
        print("   🌐 interactive_dashboard.html - Interactive dashboard")

def main():
    """Main function to run the complete system"""
    print("🚀 FAKE NEWS DETECTION & VISUALIZATION SYSTEM")
    print("="*70)
    
    # Create visualization system
    viz_system = FakeNewsVisualizationSystem()
    
    # Run complete analysis
    viz_system.run_complete_analysis()
    
    print("\n✨ You now have:")
    print("   1️⃣ A comprehensive news dataset (CSV file)")
    print("   2️⃣ Static visualization images (PNG files)")
    print("   3️⃣ Interactive HTML dashboards")
    print("   4️⃣ Complete statistical analysis")
    
    print("\n🎯 Next steps:")
    print("   • Use the CSV file for your machine learning models")
    print("   • Open HTML files in your browser for interactive exploration")
    print("   • Customize the dataset by adding more news articles")
    print("   • Train models using the provided features")

if __name__ == "__main__":
    main()