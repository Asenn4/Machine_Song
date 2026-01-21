# 🎧 Teman Musik

**Teman Musik** adalah sistem rekomendasi musik cerdas yang membantu Anda menemukan lagu-lagu baru berdasarkan fitur audio dan genre. Dibangun dengan Python dan Streamlit, aplikasi ini menggunakan pendekatan _Hybrid Filtering_ untuk mencocokkan selera musik Anda dengan presisi.

## ✨ Fitur Utama

- **Rekomendasi Cerdas**: Menggunakan algoritma _K-Nearest Neighbors_ (KNN) yang menggabungkan fitur audio (seperti _danceability_, _energy_, _tempo_) dan kesamaan genre (TF-IDF).
- **Pencarian Interaktif**: Cari lagu favorit Anda dari database Spotify yang luas.
- **Kustomisasi Pencarian**: Atur jumlah rekomendasi yang diinginkan dan filter batas minimum kecocokan (% similarity).
- **Antarmuka Modern**: Desain _Glassmorphism_ yang responsif dan estetis untuk pengalaman pengguna yang menyenangkan.
- **Mobile Friendly**: Tampilan yang menyesuaikan dengan perangkat desktop maupun mobile.

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Framework Web**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (StandardScaler, TfidfVectorizer, NearestNeighbors)
- **Matematika**: SciPy (Sparse Matrix Operations)

## 📋 Prasyarat Instalasi

Pastikan Anda telah menginstal **Python 3.x** di komputer Anda.

## 🚀 Instalasi dan Penggunaan

1.  **Clone Repository**

    ```bash
    git clone https://github.com/username/project-name.git
    cd project-name
    ```

2.  **Buat Virtual Environment (Opsional tapi Disarankan)**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi**
    Pastikan file dataset `audio_features.csv` sudah berada di dalam folder `data/`.

    ```bash
    streamlit run app.py
    ```

5.  **Akses Aplikasi**
    Buka browser dan kunjungi `http://localhost:8501`.

## 📂 Susunan Project

```
├── app.py                # File utama aplikasi Streamlit (Frontend)
├── backend.py            # Logika pemrosesan data dan model ML (Backend)
├── requirements.txt      # Daftar dependensi library Python
├── data/                 # Folder penyimpanan dataset
│   └── audio_features.csv
├── eda_analysis.py       # Script untuk Exploratory Data Analysis
├── eda_results/          # Hasil output analisis data
└── .gitignore            # Daftar file yang diabaikan git
```

## 🤝 Kontribusi

Kontribusi selalu diterima! Jika Anda ingin berkontribusi:

1.  Fork repository ini.
2.  Buat branch fitur baru (`git checkout -b fitur-keren`).
3.  Commit perubahan Anda (`git commit -m 'Menambahkan fitur keren'`).
4.  Push ke branch (`git push origin fitur-keren`).
5.  Buat Pull Request.

## 📝 Lisensi

Project ini dilisensikan di bawah lisensi [MIT](LICENSE).
