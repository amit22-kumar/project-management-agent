# PM Agent - AI-Powered Project Management System

An intelligent project management application that helps teams track projects, manage tasks, and generate insightful reports using AI technology.

## 🚀 Features

- **Project Management**: Create, update, and track multiple projects
- **Task Tracking**: Manage tasks with priorities, status, and assignments
- **AI-Powered Reports**: Generate weekly, monthly, and custom reports with insights
- **Real-time Updates**: Live status updates and progress tracking
- **Interactive Dashboard**: Visual project overview with completion metrics
- **Smart Analytics**: Automatic health scoring and blocker identification

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 14+** (if using React frontend)
- **MongoDB** (local or cloud instance)
- **Git**

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/amit22-kumar/project-management-agent.git
cd project-management-agent
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `backend/.env` with your configuration:

```env
# API Configuration (Optional - using mock data by default)
ANTHROPIC_API_KEY=your_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

### 4. Frontend Setup (if applicable)

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Configure API endpoint
echo "VITE_API_URL=http://localhost:8000" > .env
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The frontend will be available at `http://localhost:3000` or `http://localhost:5173`

## 📁 Project Structure
```
research-agent/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── core.py              # Core AI agent logic
│   │   ├── executor.py          # Task execution engine
│   │   ├── planner.py           # Project planning module
│   │   ├── report_generator.py  # Report generation (mock & AI)
│   │   ├── summarizer.py        # Data summarization
│   │   ├── tools.py             # Utility tools
│   │   └── tracker.py           # Progress tracking
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   └── models/              # Data models
│   ├── .env                     # Environment variables (not in git)
│   ├── .env.example             # Example environment file
│   ├── requirements.txt         # Python dependencies
│   └── main.py                  # Application entry point
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── .gitignore
└── README.md



---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
