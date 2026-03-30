# AI Clipper Hub 🚀

Pusat integrasi cerdas untuk pengumpulan data (scraping), analisis cerdas, dan visualisasi data yang responsif. **AI Clipper Hub** dirancang sebagai ekosistem modular yang menggabungkan performa tinggi **Go**, kecerdasan **Python**, dan pengalaman pengguna premium dari **TypeScript/Next.js**.

---

## 🏗️ Struktur Proyek

| Modul | Teknologi | Deskripsi |
| :--- | :--- | :--- |
| **`go-scraper`** | Go | Engine scraping berkecepatan tinggi untuk ekstraksi data masif secara efisien. |
| **`python-engine`** | Python | Otak AI yang menangani analisis, pengelolaan tugas (*tasks*), dan logika *engagement*. |
| **`ts-frontend`** | Next.js / TS | Dashboard modern yang elegan untuk memantau dan mengontrol seluruh ekosistem. |

---

## 🛠️ Stack Teknologi

- **Backend (Scraping):** [Go](https://go.dev/) - Mengutamakan konkurensi dan kecepatan.
- **Engine (AI/Logic):** [Python](https://www.python.org/) - Menggunakan FastAPI/Pydantic untuk orchestrator cerdas.
- **Frontend (UI):** [Next.js](https://nextjs.org/) + [TailwindCSS](https://tailwindcss.com/) - Untuk tampilan yang intuitif dan responsif.
- **Infrastruktur:** [Docker](https://www.docker.com/) & Docker Compose - Untuk kemudahan deployment.

---

## 🚀 Cara Memulai

### 1. Prasyarat
Pastikan Anda sudah menginstal:
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Go 1.21+](https://go.dev/doc/install) (untuk development)
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/en/download/)

### 2. Kloning Repositori
```bash
git clone https://github.com/adhitiad/ai-clipper-hub.git
cd ai-clipper-hub
```

### 3. Jalankan dengan Docker (Rekomendasi)
Ekosistem ini dapat dijalankan sepenuhnya menggunakan Docker Compose:
```bash
docker-compose up --build
```

### 4. Setup Manual (Opsi Development)
Jika ingin menjalankan setiap modul secara terpisah:

- **Go Scraper:**
  ```bash
  cd go-scraper
  go run main.go
  ```
- **Python Engine:**
  ```bash
  cd python-engine
  pip install -r requirements.txt
  python main.py
  ```
- **TS Frontend:**
  ```bash
  cd ts-frontend
  npm install
  npm run dev
  ```

---

## 📂 Struktur Direktori
```text
.
├── go-scraper/       # Solusi ekstraksi data (Go)
├── python-engine/    # Logika bisnis & AI (Python)
├── ts-frontend/      # Dashboard pengguna (Next.js)
├── docker-compose.yml # Konfigurasi orkestrasi
└── LICENSE           # Lisensi proyek
```

---

## 🤝 Kontribusi
Kontribusi selalu terbuka! Silakan buat *pull request* atau buka *issue* untuk mendiskusikan perubahan yang ingin dilakukan.

---

## 📄 Lisensi
Proyek ini dilisensikan di bawah **MIT License**. Lihat file `LICENSE` untuk detail lebih lanjut.

---
**AI Clipper Hub** - *Smart Data. Faster Engine. Better UI.*
