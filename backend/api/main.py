"""
Project Management Agent API - MOCK MODE
FastAPI backend with mock responses
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Import only what you need from models
from api.models import ProjectCreate, TaskUpdate

load_dotenv()

app = FastAPI(title="Project Management Agent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
projects_db = {}
active_connections: Dict[str, WebSocket] = {}

# Helper Functions
def generate_id():
    return f"proj_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

def generate_mock_plan(project_name: str, goals: List[str]) -> dict:
    """Generate a mock project plan without calling AI"""
    return {
        "project_name": project_name,
        "total_estimated_weeks": 12,
        "phases": [
            {
                "phase_number": 1,
                "name": "Planning & Research",
                "description": "Initial planning and requirement gathering",
                "duration_weeks": 2,
                "milestones": [{"name": "Requirements Complete", "target_week": 2}],
                "tasks": [
                    {"task_id": "task_001", "title": "Define project scope", "priority": "high", "estimated_hours": 8},
                    {"task_id": "task_002", "title": "Research technologies", "priority": "medium", "estimated_hours": 16}
                ]
            },
            {
                "phase_number": 2,
                "name": "Development",
                "description": "Main development work",
                "duration_weeks": 8,
                "milestones": [{"name": "MVP Complete", "target_week": 6}],
                "tasks": [
                    {"task_id": "task_003", "title": "Build core features", "priority": "high", "estimated_hours": 80},
                    {"task_id": "task_004", "title": "Create user interface", "priority": "high", "estimated_hours": 60}
                ]
            },
            {
                "phase_number": 3,
                "name": "Testing & Deployment",
                "description": "Testing and production deployment",
                "duration_weeks": 2,
                "milestones": [{"name": "Production Launch", "target_week": 12}],
                "tasks": [
                    {"task_id": "task_005", "title": "Run integration tests", "priority": "high", "estimated_hours": 20},
                    {"task_id": "task_006", "title": "Deploy to production", "priority": "high", "estimated_hours": 8}
                ]
            }
        ]
    }

def generate_mock_report(project_data: dict) -> str:
    """Generate a mock status report"""
    goals_text = "\n".join([f"- {goal}" for goal in project_data.get('goals', [])])
    
    return f"""# Project Status Report: {project_data['name']}

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}

## Executive Summary

The project "{project_data['name']}" is currently in {project_data['status']} status with {project_data['completion_percentage']}% completion. Overall health is {project_data['health_indicator'].upper()}.

## Project Overview

**Description:** {project_data.get('description', 'N/A')}

**Goals:**
{goals_text}

## Current Status

- **Overall Completion:** {project_data['completion_percentage']}%
- **Health Indicator:** {project_data['health_indicator'].upper()}
- **Project Status:** {project_data['status'].upper()}
- **Start Date:** {project_data.get('start_date', 'Not set')}
- **Deadline:** {project_data.get('deadline', 'Not set')}

## Progress Highlights

✅ **Completed Milestones:**
- Initial project setup complete
- Planning phase finished

🔄 **In Progress:**
- Development phase ongoing
- Feature implementation in progress

📋 **Upcoming:**
- Testing phase
- Final deployment

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Phases | {len(project_data.get('phases', []))} |
| Team Members | {len(project_data.get('team_members', []))} |
| Budget | ${project_data.get('budget', 0)} |

## Risks & Issues

**Current Risks:**
- No major blockers identified
- Timeline on track

**Recommendations:**
1. Continue current development pace
2. Monitor deadlines closely
3. Regular team check-ins recommended

## Next Steps

1. Complete current development tasks
2. Schedule testing phase
3. Prepare deployment checklist
4. Update stakeholders on progress

---

*This is a mock report. For AI-powered intelligent reports with real insights, add credits at https://console.anthropic.com/settings/billing*

**Report ID:** RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}
"""

# REST API Endpoints

@app.get("/")
async def root():
    return {
        "message": "Project Management Agent API", 
        "status": "running",
        "mode": "MOCK (Add AI credits for intelligent features)"
    }

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    """Create a new project with mock plan"""
    try:
        project_id = generate_id()
        plan = generate_mock_plan(project.name, project.goals)
        
        project_dict = {
            "id": project_id,
            "project_id": project_id,
            "name": project.name,
            "description": project.description,
            "goals": project.goals,
            "start_date": project.start_date,
            "deadline": project.deadline,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            "completion_percentage": 0,
            "health_indicator": "green",
            "team_members": project.team_members if project.team_members else [],
            "budget": project.budget,
            "phases": plan.get("phases", []),
            "plan": plan
        }
        
        projects_db[project_id] = project_dict
        
        return {"project_id": project_id, "project": projects_db[project_id]}
    except Exception as e:
        print(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[project_id]

@app.get("/api/projects")
async def list_projects():
    return {"projects": list(projects_db.values())}

@app.get("/api/projects/{project_id}/report")
async def generate_report(project_id: str, report_type: str = "weekly"):
    """Generate mock status report"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        project_data = projects_db[project_id]
        report = generate_mock_report(project_data)
        
        # Save report to file for PDF export
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_filename = f"report_{project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        report_path = reports_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            "project_id": project_id,
            "generated_at": datetime.now().isoformat(),
            "report": report,
            "report_file": report_filename,
            "completion_percentage": project_data.get("completion_percentage", 0),
            "status": project_data.get("status", "active"),
            "health_indicator": project_data.get("health_indicator", "green")
        }
    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/download/{filename}")
async def download_report(filename: str):
    """Download report file"""
    report_path = Path("reports") / filename
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        path=report_path,
        filename=filename,
        media_type='text/markdown'
    )

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects_db[project_id]
    return {"message": "Project deleted successfully"}

# WebSocket Endpoint with Smart Responses
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to PM Agent (Mock Mode)"
        })
        
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "").lower()
            
            # Smart responses based on keywords
            if "report" in message or "status" in message:
                response = """📊 I can help you generate reports!

**To Generate a Report:**
1. Go to the **Reports** section in sidebar
2. Select your project from dropdown
3. Choose report type (Weekly/Monthly/Executive)
4. Click "Generate Report"
5. Use "Export PDF" to download

**Available Report Types:**
- Weekly Status Report
- Monthly Summary  
- Executive Brief
- Detailed Analysis

Try it now! 🚀"""
            
            elif "project" in message and ("create" in message or "new" in message):
                response = """✨ Let's create a project!

**Steps:**
1. Click **Projects** in sidebar
2. Click "New Project" button
3. Fill in details:
   - Project name
   - Description
   - Goals (can add multiple)
   - Dates
4. Click "Create Project"

I'll generate a complete plan with phases and tasks automatically!"""
            
            elif "task" in message:
                response = """📋 Task Management Features:

**Available Views:**
- Kanban Board (drag & drop)
- List View (filterable)
- Task Details (click any task)

**Go to Tasks section to:**
- Create new tasks
- Update status
- Set priorities
- Assign team members
- Track deadlines"""
            
            elif "help" in message or "what" in message:
                response = """👋 I'm your PM AI Assistant!

**Quick Navigation:**
📊 Dashboard - Project overview
📁 Projects - Manage projects  
✅ Tasks - Task boards
📅 Timeline - Gantt charts
📈 Reports - Status reports
💬 AI Assistant - That's me!

**What I Can Do:**
- Guide you through features
- Answer questions
- Provide instructions
- Help with navigation

Ask me anything! Type:
- "create project"
- "generate report"
- "task management"
- "timeline view"

💡 Note: I'm in mock mode. Add AI credits for intelligent context-aware responses!"""
            
            else:
                response = f"""I see you asked: "{message}"

I'm here to help! Try asking:
- "How do I create a project?"
- "Generate a report"
- "Task management"
- "Help"

**Quick Tip:** All features work in the app! Navigate using the sidebar on the left.

For AI-powered intelligent responses, add credits at:
https://console.anthropic.com/settings/billing"""
            
            await websocket.send_json({
                "type": "message",
                "response": response,
                "usage": {"input_tokens": 0, "output_tokens": 0}
            })
            
    except WebSocketDisconnect:
        if session_id in active_connections:
            del active_connections[session_id]
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🚀 PM Agent API - Mock Mode")
    print("="*60)
    print("✅ All features functional")
    print("💡 Add AI credits for intelligent responses")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000)