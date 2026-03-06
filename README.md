# 🚀 JobPilot — Automated Job Discovery & Tracker

> A full-stack application that automates job discovery from Seek, scores listings against your resume, and tracks your entire application pipeline — built with Next.js, Python, and AWS.

---

## 🧩 Features

- **Automated Scraping** — Pulls fresh listings from Seek daily based on your role & location preferences
- **Resume Matching** — Scores each job description against your resume (0–100% match)
- **Application Tracker** — Track every job from discovery through to offer
- **Daily Email Digest** — Top 5 matches delivered to your inbox every morning via AWS SES
- **Clean Dashboard** — Filter, search, and manage all listings in one place

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, Tailwind CSS |
| Backend | Python 3.11, FastAPI |
| Database | AWS DynamoDB |
| File Storage | AWS S3 |
| Email | AWS SES |
| Scheduler | AWS Lambda + EventBridge |
| Frontend Hosting | Vercel |
| Backend Hosting | AWS Lambda |

---

## 📁 Project Structure

```
jobpilot/
├── frontend/               # Next.js application
│   ├── app/                # App router pages
│   ├── components/         # Reusable UI components
│   └── lib/                # API clients, utilities
├── backend/                # Python FastAPI backend
│   ├── api/                # FastAPI route handlers
│   ├── scraper/            # Seek scraper logic
│   ├── database/           # DynamoDB operations
│   ├── matcher/            # Resume-JD scoring engine
│   └── lambda/             # AWS Lambda handlers
├── infrastructure/         # AWS infrastructure config
├── .env.example            # Environment variable template
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS account with configured credentials
- AWS CLI installed

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/jobpilot.git
cd jobpilot
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Fill in your values in .env
```

### 3. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Run the backend
```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

---

## 🗺️ Roadmap

- [x] Phase 1 — Project scaffold & repo setup
- [ ] Phase 2 — Seek scraper (Python + BeautifulSoup)
- [ ] Phase 3 — DynamoDB database layer
- [ ] Phase 4 — Resume matching & scoring engine
- [ ] Phase 5 — Next.js frontend dashboard
- [ ] Phase 6 — AWS Lambda scheduler + SES email digest

---

## 👤 Author

**Sahil** — Master of IT, RMIT University (Dec 2025)  
Built as both a productivity tool and a portfolio project.

---

## 📄 License

MIT
