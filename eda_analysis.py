import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Create directory for plots
if not os.path.exists("eda_results"):
    os.makedirs("eda_results")

def run_eda():
    print("=========================================")
    print("      EXPLORATORY DATA ANALYSIS (EDA)    ")
    print("=========================================")
    
    # 1. Load Data
    try:
        df = pd.read_csv("data/audio_features.csv", on_bad_lines='skip')
        print(f"Dataset Loaded. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 3. Struktur Data & Tipe Kolom (Step 3 in Request)
    print("\n[3] Data Structure & Types:")
    print(df.info())

    # 4. Cek Missing Values (Step 4 in Request)
    print("\n[4] Missing Values Check:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # Plot missing values
    plt.figure(figsize=(10, 6))
    missing.plot(kind='bar')
    plt.title("Missing Values per Column")
    plt.tight_layout()
    plt.savefig("eda_results/missing_values.png")
    print("-> Plot saved to eda_results/missing_values.png")

    # 5. Cek Data Duplikat (Step 5 in Request)
    print("\n[5] Duplicate Check (Song + Performer):")
    dups = df.duplicated(subset=['song', 'performer']).sum()
    print(f"Count of duplicates: {dups}")

    # 6. Statistik Deskriptif (Step 6 in Request)
    print("\n[6] Descriptive Statistics:")
    print(df.describe())

    # 7. Visualisasikan Distribusi Data Numerik (Step 7 in Request)
    print("\n[7] Visualizing Distributions...")
    feature_cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                   'speechiness', 'acousticness', 'instrumentalness', 
                   'liveness', 'valence', 'tempo']
    
    for col in feature_cols:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, color='skyblue')
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(f"eda_results/dist_{col}.png")
        plt.close() # Close to save memory
    print(f"-> Distribution plots saved to eda_results/dist_*.png")

    # 8. Heatmap Korelasi (Step 8 in Request)
    print("\n[8] Correlation Heatmap...")
    plt.figure(figsize=(12, 10))
    corr = df[feature_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Audio Features")
    plt.tight_layout()
    plt.savefig("eda_results/correlation_heatmap.png")
    print("-> Heatmap saved to eda_results/correlation_heatmap.png")

    # Explanation for Steps 9-12
    print("\n=========================================")
    print("      PRE-MODELING STEPS (9-12)          ")
    print("=========================================")
    print("[9] Encoding: Categorical features (Genre) are not encoded for distance calculations (using pure audio features).")
    print("    However, Genre is used for Smart Imputation of missing values in backend.py.")
    print("[10] Normalization: Implemented in backend.py using StandardScaler.")
    print("[11-12] Split Data: SKIPPED. This is Unsupervised Learning (Clustering/Similarity).")
    print("        We do not have target labels (y) to split into Train/Test.")
    print("=========================================")
    print("EDA Complete. Check 'eda_results' folder for visualizations.")

if __name__ == "__main__":
    run_eda()
