import streamlit as st
import pandas as pd
import backend

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Teman Musik",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS & DESIGN SYSTEM
# ==========================================
st.markdown("""
<style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700&display=swap');

    /* GLOBAL STYLES */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* REMOVE DEFAULT STREAMLIT PADDING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* HEADER STYLES */
    .hero-section {
        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
        padding: 40px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }

    /* CARD STYLES (Glassmorphism) */
    .song-card {
        background: rgba(255, 255, 255, 0.05); /* Very transparent white */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        text-align: left;
        transition: all 0.3s ease;
        height: 100%;
        color: white; /* Assume dark mode or handle text color */
    }
    
    /* Handle Light/Dark mode text visibility for cards */
    @media (prefers-color-scheme: light) {
        .song-card {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(0,0,0,0.05);
            color: #191414;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }
    }

    .song-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-color: #1DB954;
    }

    .match-badge {
        background-color: #1DB954;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    .song-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 4px;
        white-space: nowrap; 
        overflow: hidden; 
        text-overflow: ellipsis; 
    }
    
    .artist-name {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-bottom: 15px;
    }

    /* BUTTON STYLES */
    .stButton > button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(29, 185, 84, 0.4);
    }

    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem; /* Smaller font on mobile */
        }
        .hero-section {
            padding: 20px 10px; /* Less padding */
        }
        .song-card {
            padding: 15px; /* Compact card */
            margin-bottom: 10px;
        }
        .block-container {
            padding-top: 1rem; /* Less top space */
        }
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# APP LOGIC
# ==========================================

# 1. HERO SECTION
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎧 Teman Musik</div>
    <div class="hero-subtitle">Jelajahi dunia musik baru yang seirama dengan jiwamu.</div>
</div>
""", unsafe_allow_html=True)

# 2. SIDEBAR (MINIMAL)
with st.sidebar:
    st.header("� Teman Musik")
    st.caption("Dibuat dengan ❤️ dan Streamlit")
    st.markdown("---")
    
    # Just the destructive/reset actions here
    if 'model_data' in st.session_state:
        if st.button("🔄 Reset / Muat Ulang DB"):
            del st.session_state['model_data']
            st.rerun()

# 3. STATE MANAGEMENT & INITIALIZATION
if 'model_data' not in st.session_state:
    # Empty State - Call to Action
    st.info("👋 Halo! Untuk memulai, kita perlu memuat database lagu spotify dulu ya.")
    
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        # Default params for initial load
        params = {"top_courses": 10, "sim_threshold": 40}
        model_selection = backend.models[0]

        if st.button("🚀 Mulai Jelajahi Musik", use_container_width=True):
            with st.spinner("Sedang menghubungkan ke Spotify Database..."):
                msg, model_data = backend.train(model_selection, params)
            
            if model_data:
                st.session_state['model_data'] = model_data
                st.rerun()
            else:
                st.error("Gagal memuat data. Pastikan file ada.")

else:
    # 4. MAIN INTERFACE
    df = st.session_state['model_data']['df']
    
    # Ensure display column exists
    if 'display_name' not in df.columns:
         df['display_name'] = df['song'] + " - " + df['performer']
    
    # SEARCH BAR (Floated Center)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("##### 🔍 Cari lagu favoritmu sekarang:")
        song_options = df['display_name'].tolist()
        
        # Multiselect with custom placeholder handled by label
        selected_songs = st.multiselect(
            "Ketik judul lagu...",
            options=song_options,
            label_visibility="collapsed",
            placeholder="Ketik judul lagu (contoh: Bohemian Rhapsody)..."
        )
        
        # Controls Section (Moved from Sidebar)
        with st.expander("⚙️ Atur Jumlah & Filter Kecocokan"):
            c1, c2, c3 = st.columns(3)
            with c1:
                top_n = st.slider("Mau berapa lagu?", 4, 20, 8)
            with c2:
                sim_threshold = st.slider("Min. Kecocokan (%)", 0, 100, 40)
            with c3:
                model_selection = st.selectbox("Algoritma AI", backend.models)
        
        params = {"top_courses": top_n, "sim_threshold": sim_threshold}

        # Action Button
        find_btn = st.button("✨ Temukan Lagu Mirip", use_container_width=True, type="primary")

    # 5. RESULTS GRID
    if find_btn and selected_songs:
        st.markdown("<br><h3 style='text-align:center;'>� Hasil Rekomendasi</h3><br>", unsafe_allow_html=True)
        
        # Get Data
        selected_indexes = df[df['display_name'].isin(selected_songs)].index.tolist()
        
        # Update dynamic params
        st.session_state['model_data']['threshold'] = params['sim_threshold'] / 100
        st.session_state['model_data']['top_n'] = params['top_courses']

        # Predict
        res_df = backend.predict(model_selection, st.session_state['model_data'], selected_indexes)

        if not res_df.empty:
            # Grid Layout Calculation
            cols_per_row = 4
            rows = len(res_df) // cols_per_row + 1
            
            # Iterate and display
            for i in range(0, len(res_df), cols_per_row):
                cols = st.columns(cols_per_row)
                batch = res_df.iloc[i:i+cols_per_row]
                
                for idx, (col, row) in enumerate(zip(cols, batch.iterrows())):
                    row_data = row[1] # iterrows returns (index, series)
                    
                    with col:
                        st.markdown(f"""
                        <div class="song-card">
                            <div class="match-badge">{int(row_data['Similarity Score']*100)}% Match</div>
                            <div class="song-title" title="{row_data['Song']}">{row_data['Song']}</div>
                            <div class="artist-name">{row_data['Performer']}</div>
                            <div style="font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px;">
                                {row_data['Genre'].split(',')[0][:20] if isinstance(row_data['Genre'], str) else 'Pop'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Belum ada yang cocok banget nih. Coba turunkan 'Min. Kecocokan' di menu samping atau pilih lagu lain.")

    elif find_btn:
        st.toast("⚠️ Ops! Pilih minimal satu lagu dulu ya.", icon="👆")
