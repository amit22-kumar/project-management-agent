
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Import only what you need from models
from api.models import ProjectCreate, TaskUpdate

# NO AGENT IMPORT! This is the key difference

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
                "tasks": [
                    {"task_id": "task_003", "title": "Build core features", "priority": "high", "estimated_hours": 80}
                ]
            }
        ]
    }

def generate_mock_report(project_data: dict) -> str:
    """Generate a mock status report"""
    return f"""# Project Status Report: {project_data['name']}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Executive Summary
The project is currently in active development. Overall progress is on track with {project_data['completion_percentage']}% completion.

## Key Highlights
- ✅ Planning phase completed
- 🔄 Development in progress
- 📊 All major milestones on schedule

## Current Status
- **Completion:** {project_data['completion_percentage']}%
- **Health:** {project_data['health_indicator'].upper()}
- **Status:** {project_data['status'].upper()}

## Next Steps
1. Continue development on core features
2. Schedule testing phase
3. Prepare for deployment

---
*Mock report - Add AI credits for AI-powered reports*
"""

# REST API Endpoints

@app.get("/")
async def root():
    return {"message": "Project Management Agent API - MOCK MODE", "status": "running"}

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
        
        return {
            "project_id": project_id,
            "generated_at": datetime.now().isoformat(),
            "report": report,
            "completion_percentage": project_data.get("completion_percentage", 0),
            "status": project_data.get("status", "active"),
            "health_indicator": project_data.get("health_indicator", "green")
        }
    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects_db[project_id]
    return {"message": "Project deleted successfully"}

# WebSocket Endpoint (Mock Mode)
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Connected (Mock Mode - No AI)"
        })
        
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            mock_response = f"Mock response to: '{message}'\n\nAdd credits at: https://console.anthropic.com/settings/billing"
            
            await websocket.send_json({
                "type": "message",
                "response": mock_response,
                "usage": {"input_tokens": 0, "output_tokens": 0}
            })
            
    except WebSocketDisconnect:
        if session_id in active_connections:
            del active_connections[session_id]

if __name__ == "__main__":
    import uvicorn
    print("🚀 MOCK MODE - No AI credits needed!")
    uvicorn.run(app, host="0.0.0.0", port=8000)