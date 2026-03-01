# WarTracker 🌍

**Real-time Global Conflict Tracking & Analysis Platform**

## Mission

WarTracker searches the internet continuously to provide users with **real-time, verified information on conflicts around the world**. Our goal is to cut through noise and deliver accurate, actionable intelligence on global conflicts, humanitarian crises, and geopolitical tensions.

## Core Features

- 🔍 **Real-time Monitoring** - Continuous web scraping and API integration for live conflict data
- 🗺️ **Interactive Map** - Visual representation of global conflicts with severity indicators
- 📊 **Trend Analysis** - AI-powered pattern detection and escalation warnings
- 📰 **Source Verification** - Multi-source cross-referencing to combat misinformation
- 🔔 **Alerts** - Customizable notifications for specific regions or conflict types
- 📈 **Historical Data** - Track conflict evolution over time with analytics

## Tech Stack

- **Frontend:** Next.js 16, TypeScript, Tailwind CSS, MapLibre/Leaflet
- **Backend:** FastAPI, Python, PostgreSQL, Redis (caching)
- **AI/ML:** Ollama Cloud models (analysis, summarization, trend detection)
- **Data Sources:** News APIs, social media, government reports, NGO feeds
- **Infrastructure:** Docker, PostgreSQL with PostGIS (geospatial queries)

## Status

🚧 **Phase:** Requirements Gathering (Pepper)  
📋 **Next:** Architecture Design (Tony) → Implementation (Peter) → QA (Heimdall)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/humac/WarTracker.git
cd WarTracker

# Install dependencies (after setup)
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Start development servers
# (Detailed instructions in ADMIN_GUIDE.md)
```

## Project Structure

```
WarTracker/
├── frontend/            # Next.js frontend application
├── backend/             # FastAPI backend + data collectors
├── docs/                # Project documentation
│   ├── agent-workflow/  # Agent pipeline docs
│   ├── DECISIONS.md     # Architecture decisions
│   └── RUN_STATE.md     # Pipeline state
├── agents/              # Agent personas (tony, peter, heimdall, pepper)
└── README.md            # This file
```

## Development Workflow

This project follows the Jarvis agent workflow:

1. **Pepper (Analyst)** - Requirements gathering
2. **Tony (Architect)** - System design & architecture
3. **Peter (Developer)** - Implementation & unit tests
4. **Heimdall (QA)** - Security audit & validation
5. **Pepper (Closeout)** - Documentation & final report

Agent workflow documents are in `docs/agent-workflow/`.

## Links

- **GitHub:** https://github.com/humac/WarTracker
- **Issues:** https://github.com/humac/WarTracker/issues
- **Requirements:** docs/agent-workflow/REQ.md
- **Architecture:** docs/agent-workflow/ARCH.md

---

**Built with ❤️ for global awareness and transparency**

*WarTracker provides information only and does not take political positions. All data is sourced from publicly available information.*
