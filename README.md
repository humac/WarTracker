# WarTracker

Real-time global conflict tracking and analysis platform

## Tech Stack
Next.js 16 + FastAPI + PostgreSQL

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment example
cp .env.example .env.local

# Edit .env.local with your configuration
```

### Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test
```

## Project Structure

```
WarTracker/
├── src/                 # Application source code
│   ├── app/            # Next.js App Router pages & API routes
│   ├── components/     # React components
│   ├── lib/           # Utilities, hooks, types
│   └── styles/        # Global styles
├── docs/              # Project documentation
│   ├── agent-workflow/  # Agent pipeline docs
│   │   ├── REQ.md      # Requirements
│   │   ├── ARCH.md     # Architecture
│   │   ├── TASKS.md    # Implementation tasks
│   │   ├── QA.md       # QA criteria
│   │   ├── CLAUDE.md   # Claude instructions
│   │   ├── GEMINI.md   # Gemini instructions
│   │   └── ISSUES.md   # Issues log
│   ├── DECISIONS.md     # Architecture decisions
│   └── RUN_STATE.md     # Pipeline state
├── public/            # Static assets
├── .env.example       # Environment template
├── .env.local         # Local environment (gitignored)
├── package.json       # Dependencies
└── README.md          # This file
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

- [GitHub Repository](https://github.com/humac/WarTracker)
- [Requirements](docs/agent-workflow/REQ.md)
- [Architecture](docs/agent-workflow/ARCH.md)
- [Tasks](docs/agent-workflow/TASKS.md)
- [QA Plan](docs/agent-workflow/QA.md)
