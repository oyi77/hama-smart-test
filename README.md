# TodoList Desktop Application

A modern, full-stack desktop application built with **FastAPI** (Python) and **Electron** (React/Vite). This project demonstrates a robust implementation of standard CRUD operations while adhering to **SOLID** and **KISS** principles.

## Features

### Backend (FastAPI)
- **RESTful API**: Complete CRUD endpoints for Todos and Categories.
- **Data Persistence**: SQLite database integration using SQLAlchemy.
- **Validation**: Strict data validation using Pydantic schemas.
- **Search & Filter**: Server-side filtering by category, priority, and completion status.
- **Automation**: Automatic database initialization and migrations.

### Frontend (Electron + React)
- **Desktop Experience**: Native window management with Electron.
- **Modern UI**: Clean, minimalist interface built with React and Tailwind CSS.
- **Real-time Interaction**: Instant updates and responsive state management.
- **Search & Sorting**: Client-side search and advanced filtering options.

## Tech Stack
- **Frontend**: Electron, React, Vite, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Database**: SQLite

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm

### Installation & Startup
We have provided a convenient script to start all stacks:
```bash
./start_all.sh
```
This script will:
1. Initialize the Python virtual environment.
2. Install all backend and frontend dependencies.
3. Start the FastAPI server (Port 8000) and the Electron app concurrently.

## Technical Note: Timing & Setup
This project was completed for a Live Coding Test. Please note that the implementation exceeded the initial 30-minute window due to:
- **Network Failure**: A temporary network disruption during the initial code-setup phase required significant troubleshooting to restore the environment and dependencies.
- **Environment Recovery**: Additional time was spent re-verifying the toolchain and ensuring the integration between the FastAPI backend and Electron frontend was properly established following the outage.

## Architecture Guidelines
- **SOLID Principles**: Focused on Single Responsibility and Open/Closed principles for maintainability.
- **KISS**: Prioritizing simple, readable code over complex abstractions.
- **Testing**: Designed for high testability across both UI and Backend layers.