import pandas as pd
import numpy as np
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

# Model list
models = ["Hybrid (Audio + Genre) Model"]

# =======================
# Training Function
# =======================
def train(model_name, params):
    if model_name == models[0]:

        # Load Song data
        try:
            df = pd.read_csv("data/audio_features.csv", on_bad_lines='skip')
        except Exception as e:
             return f"Error loading data: {str(e)}", None
        
        # Select relevant columns
        feature_cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                       'speechiness', 'acousticness', 'instrumentalness', 
                       'liveness', 'valence', 'tempo']
        
        # 1. Deduplication
        df = df.drop_duplicates(subset=['song', 'performer'], keep='first').reset_index(drop=True)

        # 2. Advanced Imputation strategy
        # Strategy A: Impute by Genre Median
        for col in feature_cols:
            df[col] = df[col].fillna(df.groupby('spotify_genre')[col].transform('median'))
            
        # Strategy B: Global Median
        for col in feature_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # 3. Clean Song Titles
        df['song'] = df['song'].astype(str).str.replace(r'^[^\w\s]+', '', regex=True).str.strip()
        df['display_name'] = df['song'] + " - " + df['performer']

        # ==================================================
        # FEATURE ENGINEERING: HYBRID API
        # ==================================================
        
        # A. Audio Features (Scaled)
        features_audio = df[feature_cols]
        scaler = StandardScaler()
        features_audio_scaled = scaler.fit_transform(features_audio)

        # B. Genre Features (TF-IDF)
        # Convert string representation of list "['pop', 'rock']" to clean string "pop rock"
        def clean_genre(genre_str):
            try:
                # Safely evaluate string list to list
                if pd.isna(genre_str): return ""
                genres = ast.literal_eval(genre_str)
                if isinstance(genres, list):
                    return " ".join(genres)
                return str(genre_str)
            except:
                return str(genre_str).replace("[", "").replace("]", "").replace("'", "")
        
        df['genre_clean'] = df['spotify_genre'].apply(clean_genre)
        
        # TF-IDF Vectorization
        # params can be tuned. min_df=2 means ignore unique rare genres.
        tfidf = TfidfVectorizer(stop_words='english', min_df=2)
        features_genre_tfidf = tfidf.fit_transform(df['genre_clean'])

        # C. Combine Features
        # We assume Audio Features are dense and Genre is sparse.
        # We might want to weight genre more heavily if the user wants strict genre matching.
        # Currently 1:1 weight (StandardScaler output is roughly unit variance).
        # To boost genre importance, we can multiply tfidf matrix by a factor.
        genre_weight = 1.5 # Boost genre influence by 50%
        final_features = hstack([features_audio_scaled, features_genre_tfidf * genre_weight]).tocsr()

        # Train NearestNeighbors model on Combined Data
        nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        nn_model.fit(final_features)

        # Simpan ke dict
        model_data = {}
        model_data["df"] = df
        model_data["scaler"] = scaler
        model_data["tfidf"] = tfidf
        model_data["final_features"] = final_features # Keep this for lookup (it's a sparse matrix now)
        model_data["nn_model"] = nn_model
        model_data["top_n"] = params["top_courses"]
        model_data["threshold"] = params["sim_threshold"] / 100
        model_data["genre_weight"] = genre_weight

        return "Model Hybrid (Audio + Genre) berhasil dilatih!", model_data

# =======================
# Prediction Function
# =======================
def predict(model_name, model_data, selected_indexes):
    if model_name == models[0]:

        df = model_data["df"]
        nn_model = model_data["nn_model"]
        final_features = model_data["final_features"]
        top_n = model_data["top_n"]
        threshold = model_data["threshold"]

        recommendations = {}
        search_k = top_n + 10 

        for idx in selected_indexes:
            if idx < final_features.shape[0]:
                # Get feature vector (sparse row)
                # kneighbors accepts sparse matrix input
                query_vector = final_features[idx]
                
                dists, indices = nn_model.kneighbors(query_vector, n_neighbors=search_k)
                
                dists = dists[0]
                indices = indices[0]

                for i, neighbor_idx in enumerate(indices):
                    if neighbor_idx not in selected_indexes:
                        similarity = 1 - dists[i]
                        
                        if similarity >= threshold:
                            if neighbor_idx in recommendations:
                                recommendations[neighbor_idx] = max(recommendations[neighbor_idx], similarity)
                            else:
                                recommendations[neighbor_idx] = similarity

        ranked = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        ranked = ranked[:top_n]

        rec_list = []
        for idx, score in ranked:
            rec_list.append([
                df.iloc[idx]["song"],
                df.iloc[idx]["performer"],
                df.iloc[idx]["spotify_genre"],
                round(score, 3)
            ])

        rec_df = pd.DataFrame(rec_list, columns=[
            "Song", "Performer", "Genre", "Similarity Score"
        ])

        return rec_df
