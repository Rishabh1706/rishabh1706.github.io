#!/usr/bin/env python3
"""
Learning Progress Tracker Application
A Flask-based web application for tracking your 12-month learning journey
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Any
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-learning-tracker'

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Learning Plan Configuration
LEARNING_PLAN = {
    'start_date': '2025-07-15',  # Your actual start date
    'total_weeks': 48,
    'total_hours': 1600,
    'weekly_target': 36,  # hours per week
    'weekday_target': 4,  # hours per weekday
    'weekend_target': 8,  # hours per weekend day
    'stages': {
        1: {
            'name': 'Core Programming + Data Foundations', 
            'weeks': list(range(1, 9)), 
            'hours': 288,
            'description': 'Build strong programming fundamentals and data manipulation skills',
            'topics': [
                'Python Advanced Features (decorators, generators, context managers)',
                'Data Structures & Algorithms (Arrays, Linked Lists, Trees, Graphs)',
                'Object-Oriented Programming (inheritance, polymorphism, design patterns)',
                'Database Fundamentals (SQL, normalization, indexing)',
                'pandas & NumPy for Data Manipulation',
                'Data Cleaning & Preprocessing Techniques',
                'Basic Statistics for Data Analysis',
                'Git Version Control & Collaboration'
            ],
            'projects': [
                'Build a data analysis library',
                'Create a personal finance tracker',
                'Develop a simple web scraper'
            ]
        },
        2: {
            'name': 'Backend Engineering Foundation', 
            'weeks': list(range(9, 17)), 
            'hours': 288,
            'description': 'Master backend development and API design principles',
            'topics': [
                'RESTful API Design & Implementation',
                'Flask/Django Web Framework Mastery',
                'Database Design & ORM (SQLAlchemy)',
                'Authentication & Authorization Systems',
                'Testing (Unit, Integration, API Testing)',
                'Error Handling & Logging',
                'Performance Optimization & Caching',
                'API Documentation (OpenAPI/Swagger)'
            ],
            'projects': [
                'Build a complete REST API with authentication',
                'Create a blog platform with user management',
                'Develop a task management system'
            ]
        },
        3: {
            'name': 'Data Engineering Essentials', 
            'weeks': list(range(17, 25)), 
            'hours': 288,
            'description': 'Learn to build scalable data pipelines and processing systems',
            'topics': [
                'ETL Pipeline Design & Implementation',
                'Apache Airflow for Workflow Management',
                'Data Warehousing Concepts',
                'Big Data Tools (Spark, Kafka)',
                'Data Quality & Validation',
                'Stream Processing & Real-time Data',
                'Data Lake Architecture',
                'SQL Advanced Queries & Optimization'
            ],
            'projects': [
                'Build an automated data pipeline',
                'Create a real-time analytics dashboard',
                'Develop a data validation framework'
            ]
        },
        4: {
            'name': 'DevOps + Cloud Engineering', 
            'weeks': list(range(25, 33)), 
            'hours': 288,
            'description': 'Master cloud infrastructure and deployment automation',
            'topics': [
                'Containerization (Docker, Docker Compose)',
                'Container Orchestration (Kubernetes)',
                'Cloud Platforms (AWS/Azure/GCP)',
                'Infrastructure as Code (Terraform)',
                'CI/CD Pipelines (GitHub Actions, Jenkins)',
                'Monitoring & Logging (Prometheus, Grafana)',
                'Security Best Practices',
                'Microservices Architecture'
            ],
            'projects': [
                'Deploy a multi-container application',
                'Set up a complete CI/CD pipeline',
                'Build a monitoring dashboard'
            ]
        },
        5: {
            'name': 'Machine Learning & Data Science', 
            'weeks': list(range(33, 37)), 
            'hours': 144,
            'description': 'Develop machine learning models and data science skills',
            'topics': [
                'Supervised Learning (Classification, Regression)',
                'Unsupervised Learning (Clustering, Dimensionality Reduction)',
                'Feature Engineering & Selection',
                'Model Evaluation & Validation',
                'scikit-learn & Advanced Libraries',
                'Statistical Analysis & Hypothesis Testing',
                'Data Visualization (matplotlib, seaborn, plotly)',
                'Time Series Analysis'
            ],
            'projects': [
                'Build a predictive model for business metrics',
                'Create a recommendation system',
                'Develop a time series forecasting model'
            ]
        },
        6: {
            'name': 'MLOps (Production ML Systems)', 
            'weeks': list(range(37, 41)), 
            'hours': 144,
            'description': 'Learn to deploy and maintain ML models in production',
            'topics': [
                'Model Deployment Strategies',
                'ML Pipeline Automation',
                'Model Monitoring & Drift Detection',
                'A/B Testing for ML Models',
                'MLflow for Experiment Tracking',
                'Model Versioning & Registry',
                'Scalable ML Infrastructure',
                'Production ML Best Practices'
            ],
            'projects': [
                'Deploy an ML model as a web service',
                'Build an automated ML pipeline',
                'Create a model monitoring system'
            ]
        },
        7: {
            'name': 'Generative AI / LLMs', 
            'weeks': list(range(41, 45)), 
            'hours': 144,
            'description': 'Explore large language models and generative AI applications',
            'topics': [
                'Large Language Model Fundamentals',
                'Prompt Engineering & Fine-tuning',
                'OpenAI API & GPT Integration',
                'Retrieval Augmented Generation (RAG)',
                'Vector Databases & Embeddings',
                'LangChain for LLM Applications',
                'AI Safety & Ethical Considerations',
                'Building AI-Powered Applications'
            ],
            'projects': [
                'Build a chatbot with context awareness',
                'Create a document Q&A system',
                'Develop an AI writing assistant'
            ]
        },
        8: {
            'name': 'Cloud Integration & Capstone', 
            'weeks': list(range(45, 49)), 
            'hours': 144,
            'description': 'Integrate all skills into a comprehensive capstone project',
            'topics': [
                'System Architecture Design',
                'Scalability & Performance Optimization',
                'Security Implementation',
                'Cost Optimization Strategies',
                'Technical Documentation',
                'Project Management & Agile Practices',
                'Code Review & Quality Assurance',
                'Portfolio Development'
            ],
            'projects': [
                'Build a full-stack data platform',
                'Create an AI-powered SaaS application',
                'Develop a comprehensive portfolio showcase'
            ]
        }
    }
}

# Active sessions tracker
active_sessions = {}

class ProgressTracker:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Load all data from JSON files"""
        self.progress_data = self.load_json_file(PROGRESS_FILE, self.get_default_progress())
        self.sessions_data = self.load_json_file(SESSIONS_FILE, [])
        self.goals_data = self.load_json_file(GOALS_FILE, {})
    
    def load_json_file(self, filepath: str, default: Any) -> Any:
        """Load JSON file with default fallback"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
        return default
    
    def save_json_file(self, filepath: str, data: Any):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
    
    def get_default_progress(self) -> Dict:
        """Get default progress data structure"""
        return {
            'total_hours': 0.0,
            'total_sessions': 0,
            'current_streak': 0,
            'longest_streak': 0,
            'last_session_date': None,
            'achievements': [],
            'daily_logs': {},
            'stage_progress': {str(i): 0 for i in range(1, 9)},
            'completed_topics': {},  # {stage_id: [topic_indices]}
            'completed_projects': {},  # {stage_id: [project_indices]}
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    def get_current_week(self) -> int:
        """Calculate current week based on start date"""
        start_date = datetime.strptime(LEARNING_PLAN['start_date'], '%Y-%m-%d')
        current_date = datetime.now()
        days_diff = (current_date - start_date).days
        return max(1, min(48, (days_diff // 7) + 1))
    
    def get_current_stage(self, week: int) -> int:
        """Determine current stage based on week"""
        for stage_num, stage_info in LEARNING_PLAN['stages'].items():
            if week in stage_info['weeks']:
                return stage_num
        return 8  # Final stage
    
    def calculate_expected_hours(self, week: int = None) -> float:
        """Calculate expected hours based on days elapsed since start date"""
        start_date = datetime.strptime(LEARNING_PLAN['start_date'], '%Y-%m-%d')
        current_date = datetime.now()
        days_elapsed = max(0, (current_date - start_date).days)
        
        # If we haven't started yet (future start date), return 0
        if days_elapsed < 0:
            return 0.0
        
        # Calculate expected hours based on daily targets
        total_expected = 0.0
        
        for day in range(days_elapsed + 1):  # Include today
            day_date = start_date + timedelta(days=day)
            day_of_week = day_date.weekday()  # 0=Monday, 6=Sunday
            
            # Weekend days (Saturday=5, Sunday=6) have different targets
            if day_of_week >= 5:  # Weekend
                daily_target = LEARNING_PLAN['weekend_target']
            else:  # Weekday
                daily_target = LEARNING_PLAN['weekday_target']
            
            total_expected += daily_target
        
        # Cap at total program hours
        return min(total_expected, LEARNING_PLAN['total_hours'])
    
    def get_progress_status(self) -> Dict:
        """Calculate detailed progress status"""
        current_week = self.get_current_week()
        current_stage = self.get_current_stage(current_week)
        expected_hours = self.calculate_expected_hours()
        actual_hours = self.progress_data['total_hours']
        
        progress_ratio = actual_hours / expected_hours if expected_hours > 0 else 0
        
        # Calculate daily target for today
        today = datetime.now().weekday()  # 0=Monday, 6=Sunday
        is_weekend = today >= 5
        daily_target = LEARNING_PLAN['weekend_target'] if is_weekend else LEARNING_PLAN['weekday_target']
        
        # Calculate catch-up requirements
        remaining_weeks = max(0, LEARNING_PLAN['total_weeks'] - current_week)
        remaining_hours = max(0, LEARNING_PLAN['total_hours'] - actual_hours)
        hours_per_week_needed = remaining_hours / remaining_weeks if remaining_weeks > 0 else 0
        hours_per_day_needed = hours_per_week_needed / 7
        
        # Determine status
        if progress_ratio >= 1.2:
            status = 'Significantly Ahead 🚀'
            urgency = 'low'
            color = '#10b981'
        elif progress_ratio >= 0.95:
            status = 'On Track 🎯'
            urgency = 'low'
            color = '#3b82f6'
        elif progress_ratio >= 0.8:
            status = 'Slightly Behind ⚠️'
            urgency = 'medium'
            color = '#f59e0b'
        elif progress_ratio >= 0.6:
            status = 'Behind Schedule 🔥'
            urgency = 'high'
            color = '#ef4444'
        else:
            status = 'Critically Behind 🚨'
            urgency = 'critical'
            color = '#dc2626'
        
        return {
            'status': status,
            'urgency': urgency,
            'color': color,
            'current_week': current_week,
            'current_stage': current_stage,
            'expected_hours': expected_hours,
            'actual_hours': actual_hours,
            'progress_ratio': progress_ratio,
            'daily_target': daily_target,
            'hours_per_day_needed': hours_per_day_needed,
            'remaining_weeks': remaining_weeks,
            'remaining_hours': remaining_hours,
            'is_weekend': is_weekend
        }
    
    def start_session(self, user_id: str = 'default') -> str:
        """Start a new learning session"""
        session_id = str(uuid.uuid4())
        session_data = {
            'id': session_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'status': 'active',
            'paused_time': 0.0,
            'topics': [],
            'notes': '',
            'mood': '',
            'difficulty': 3
        }
        
        active_sessions[session_id] = session_data
        return session_id
    
    def end_session(self, session_id: str, notes: str = '', topics: List[str] = None, 
                   mood: str = '', difficulty: int = 3) -> Dict:
        """End a learning session and save data"""
        if session_id not in active_sessions:
            return {'error': 'Session not found'}
        
        session = active_sessions[session_id]
        end_time = datetime.now()
        start_time = datetime.fromisoformat(session['start_time'])
        duration = (end_time - start_time).total_seconds() / 3600  # hours
        
        # Update session data
        session.update({
            'end_time': end_time.isoformat(),
            'duration': duration,
            'notes': notes,
            'topics': topics or [],
            'mood': mood,
            'difficulty': difficulty,
            'status': 'completed'
        })
        
        # Save to sessions file
        self.sessions_data.append(session)
        self.save_json_file(SESSIONS_FILE, self.sessions_data)
        
        # Update progress data
        self.progress_data['total_hours'] += duration
        self.progress_data['total_sessions'] += 1
        self.progress_data['updated_at'] = datetime.now().isoformat()
        
        # Update daily log
        today = datetime.now().date().isoformat()
        if today not in self.progress_data['daily_logs']:
            self.progress_data['daily_logs'][today] = {
                'hours': 0,
                'sessions': 0,
                'topics': [],
                'notes': []
            }
        
        self.progress_data['daily_logs'][today]['hours'] += duration
        self.progress_data['daily_logs'][today]['sessions'] += 1
        if topics:
            self.progress_data['daily_logs'][today]['topics'].extend(topics)
        if notes:
            self.progress_data['daily_logs'][today]['notes'].append(notes)
        
        # Update streak
        self.update_streak()
        
        # Check achievements
        self.check_achievements()
        
        # Save progress data
        self.save_json_file(PROGRESS_FILE, self.progress_data)
        
        # Remove from active sessions
        del active_sessions[session_id]
        
        return {
            'success': True,
            'session': session,
            'new_achievements': self.get_recent_achievements()
        }
    
    def pause_session(self, session_id: str) -> Dict:
        """Pause an active session"""
        if session_id not in active_sessions:
            return {'error': 'Session not found'}
        
        session = active_sessions[session_id]
        if 'pause_start' not in session:
            session['pause_start'] = datetime.now().isoformat()
            return {'success': True, 'message': 'Session paused'}
        else:
            return {'error': 'Session already paused'}
    
    def resume_session(self, session_id: str) -> Dict:
        """Resume a paused session"""
        if session_id not in active_sessions:
            return {'error': 'Session not found'}
        
        session = active_sessions[session_id]
        if 'pause_start' in session:
            pause_start = datetime.fromisoformat(session['pause_start'])
            pause_duration = (datetime.now() - pause_start).total_seconds() / 3600
            session['paused_time'] += pause_duration
            del session['pause_start']
            return {'success': True, 'message': 'Session resumed'}
        else:
            return {'error': 'Session not paused'}
    
    def get_session_status(self, session_id: str) -> Dict:
        """Get current session status and duration"""
        if session_id not in active_sessions:
            return {'error': 'Session not found'}
        
        session = active_sessions[session_id]
        start_time = datetime.fromisoformat(session['start_time'])
        current_time = datetime.now()
        
        if 'pause_start' in session:
            # Session is paused
            pause_start = datetime.fromisoformat(session['pause_start'])
            active_duration = (pause_start - start_time).total_seconds() / 3600
            total_duration = active_duration + session['paused_time']
            status = 'paused'
        else:
            # Session is active
            total_duration = (current_time - start_time).total_seconds() / 3600
            total_duration -= session['paused_time']
            status = 'active'
        
        return {
            'session_id': session_id,
            'status': status,
            'duration': total_duration,
            'start_time': session['start_time'],
            'paused_time': session['paused_time']
        }
    
    def update_streak(self):
        """Update learning streak based on daily logs"""
        dates = sorted(self.progress_data['daily_logs'].keys())
        if not dates:
            self.progress_data['current_streak'] = 0
            return
        
        # Check if logged today or yesterday
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        today_str = today.isoformat()
        yesterday_str = yesterday.isoformat()
        
        if today_str not in dates and yesterday_str not in dates:
            self.progress_data['current_streak'] = 0
            return
        
        # Calculate current streak
        current_streak = 0
        check_date = today
        
        while True:
            date_str = check_date.isoformat()
            if date_str in dates and self.progress_data['daily_logs'][date_str]['hours'] > 0:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        self.progress_data['current_streak'] = current_streak
        self.progress_data['longest_streak'] = max(
            self.progress_data.get('longest_streak', 0), 
            current_streak
        )
    
    def check_achievements(self):
        """Check and award new achievements"""
        new_achievements = []
        current_achievements = set(self.progress_data['achievements'])
        
        # Hour-based achievements
        hours = self.progress_data['total_hours']
        hour_milestones = [10, 25, 50, 100, 200, 500, 1000]
        
        for milestone in hour_milestones:
            achievement_id = f'hours_{milestone}'
            if hours >= milestone and achievement_id not in current_achievements:
                new_achievements.append({
                    'id': achievement_id,
                    'title': f'{milestone} Hours Completed',
                    'description': f'You have completed {milestone} hours of learning!',
                    'earned_at': datetime.now().isoformat()
                })
        
        # Streak-based achievements
        streak = self.progress_data['current_streak']
        streak_milestones = [3, 7, 14, 30, 60, 100]
        
        for milestone in streak_milestones:
            achievement_id = f'streak_{milestone}'
            if streak >= milestone and achievement_id not in current_achievements:
                new_achievements.append({
                    'id': achievement_id,
                    'title': f'{milestone}-Day Streak',
                    'description': f'You have maintained a {milestone}-day learning streak!',
                    'earned_at': datetime.now().isoformat()
                })
        
        # Session-based achievements
        sessions = self.progress_data['total_sessions']
        session_milestones = [5, 25, 50, 100, 250, 500]
        
        for milestone in session_milestones:
            achievement_id = f'sessions_{milestone}'
            if sessions >= milestone and achievement_id not in current_achievements:
                new_achievements.append({
                    'id': achievement_id,
                    'title': f'{milestone} Sessions Completed',
                    'description': f'You have completed {milestone} learning sessions!',
                    'earned_at': datetime.now().isoformat()
                })
        
        # Add new achievements
        for achievement in new_achievements:
            self.progress_data['achievements'].append(achievement['id'])
        
        return new_achievements
    
    def get_recent_achievements(self) -> List[Dict]:
        """Get recently earned achievements"""
        # This would normally track recent achievements
        # For now, return empty list
        return []
    
    def get_dashboard_data(self) -> Dict:
        """Get comprehensive dashboard data"""
        status = self.get_progress_status()
        
        # Calculate stage progress
        stage_progress = {}
        for stage_num, stage_info in LEARNING_PLAN['stages'].items():
            stage_hours = 0
            stage_sessions = 0
            
            # Calculate hours for this stage based on sessions
            for session in self.sessions_data:
                session_date = datetime.fromisoformat(session['start_time'])
                start_date = datetime.strptime(LEARNING_PLAN['start_date'], '%Y-%m-%d')
                session_week = ((session_date - start_date).days // 7) + 1
                
                if session_week in stage_info['weeks']:
                    stage_hours += session.get('duration', 0)
                    stage_sessions += 1
            
            progress_percentage = min(100, (stage_hours / stage_info['hours']) * 100)
            
            stage_progress[stage_num] = {
                'name': stage_info['name'],
                'weeks': stage_info['weeks'],
                'target_hours': stage_info['hours'],
                'actual_hours': stage_hours,
                'sessions': stage_sessions,
                'progress_percentage': progress_percentage,
                'status': self.get_stage_status(stage_num, status['current_week'])
            }
        
        # Get recent sessions
        recent_sessions = sorted(
            self.sessions_data, 
            key=lambda x: x['start_time'], 
            reverse=True
        )[:10]
        
        # Get weekly stats
        weekly_stats = self.get_weekly_stats()
        
        return {
            'status': status,
            'progress_data': self.progress_data,
            'stage_progress': stage_progress,
            'recent_sessions': recent_sessions,
            'weekly_stats': weekly_stats,
            'active_sessions': list(active_sessions.keys()),
            'total_achievements': len(self.progress_data['achievements'])
        }
    
    def get_stage_status(self, stage_num: int, current_week: int) -> str:
        """Get status of a stage (completed, active, upcoming)"""
        stage_info = LEARNING_PLAN['stages'][stage_num]
        stage_weeks = stage_info['weeks']
        
        if current_week > max(stage_weeks):
            return 'completed'
        elif current_week in stage_weeks:
            return 'active'
        else:
            return 'upcoming'
    
    def get_weekly_stats(self) -> List[Dict]:
        """Get weekly statistics"""
        weekly_stats = []
        start_date = datetime.strptime(LEARNING_PLAN['start_date'], '%Y-%m-%d')
        
        for week in range(1, self.get_current_week() + 1):
            week_start = start_date + timedelta(weeks=week - 1)
            week_end = week_start + timedelta(days=6)
            
            week_hours = 0
            week_sessions = 0
            
            for date_str, log in self.progress_data['daily_logs'].items():
                log_date = datetime.strptime(date_str, '%Y-%m-%d')
                if week_start <= log_date <= week_end:
                    week_hours += log['hours']
                    week_sessions += log['sessions']
            
            weekly_stats.append({
                'week': week,
                'start_date': week_start.isoformat(),
                'end_date': week_end.isoformat(),
                'hours': week_hours,
                'sessions': week_sessions,
                'target_hours': LEARNING_PLAN['weekly_target'],
                'percentage': (week_hours / LEARNING_PLAN['weekly_target']) * 100
            })
        
        return weekly_stats
    
    def add_manual_session(self, duration: float, notes: str = '', topics: List[str] = None,
                          mood: str = '', difficulty: int = 3, session_date: str = None) -> Dict:
        """Add a manual session with specified details"""
        try:
            # Parse session date or use current date
            if session_date:
                session_datetime = datetime.fromisoformat(session_date)
            else:
                session_datetime = datetime.now()
            
            # Create session data
            session_data = {
                'id': str(uuid.uuid4()),
                'user_id': 'default',
                'start_time': session_datetime.isoformat(),
                'end_time': session_datetime.isoformat(),
                'duration': duration,
                'notes': notes,
                'topics': topics or [],
                'mood': mood,
                'difficulty': difficulty,
                'status': 'completed',
                'manual_entry': True
            }
            
            # Save to sessions file
            self.sessions_data.append(session_data)
            self.save_json_file(SESSIONS_FILE, self.sessions_data)
            
            # Update progress data
            self.progress_data['total_hours'] += duration
            self.progress_data['total_sessions'] += 1
            self.progress_data['updated_at'] = datetime.now().isoformat()
            
            # Update daily log
            session_date_str = session_datetime.date().isoformat()
            if session_date_str not in self.progress_data['daily_logs']:
                self.progress_data['daily_logs'][session_date_str] = {
                    'hours': 0,
                    'sessions': 0,
                    'topics': [],
                    'notes': []
                }
            
            self.progress_data['daily_logs'][session_date_str]['hours'] += duration
            self.progress_data['daily_logs'][session_date_str]['sessions'] += 1
            if topics:
                self.progress_data['daily_logs'][session_date_str]['topics'].extend(topics)
            if notes:
                self.progress_data['daily_logs'][session_date_str]['notes'].append(notes)
            
            # Update streak
            self.update_streak()
            
            # Check achievements
            self.check_achievements()
            
            # Save progress data
            self.save_json_file(PROGRESS_FILE, self.progress_data)
            
            return {
                'success': True,
                'session': session_data,
                'new_achievements': self.get_recent_achievements()
            }
            
        except Exception as e:
            return {'error': str(e)}

# Initialize tracker
tracker = ProgressTracker()

# Routes
@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('dashboard.html')

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data"""
    try:
        data = tracker.get_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/start', methods=['POST'])
def api_start_session():
    """Start a new learning session"""
    try:
        session_id = tracker.start_session()
        return jsonify({'session_id': session_id, 'message': 'Session started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/end', methods=['POST'])
def api_end_session():
    """End a learning session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        notes = data.get('notes', '')
        topics = data.get('topics', [])
        mood = data.get('mood', '')
        difficulty = data.get('difficulty', 3)
        
        result = tracker.end_session(session_id, notes, topics, mood, difficulty)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/pause', methods=['POST'])
def api_pause_session():
    """Pause a learning session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        result = tracker.pause_session(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/resume', methods=['POST'])
def api_resume_session():
    """Resume a learning session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        result = tracker.resume_session(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/status/<session_id>')
def api_session_status(session_id):
    """Get session status"""
    try:
        result = tracker.get_session_status(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/status')
def api_progress_status():
    """Get detailed progress status"""
    try:
        status = tracker.get_progress_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stage/<int:stage_id>')
def api_stage_details(stage_id):
    """Get detailed information about a specific stage"""
    try:
        if stage_id not in LEARNING_PLAN['stages']:
            return jsonify({'error': 'Stage not found'}), 404
        
        stage_info = LEARNING_PLAN['stages'][stage_id].copy()
        
        # Add current progress for this stage
        dashboard_data = tracker.get_dashboard_data()
        if str(stage_id) in dashboard_data['stage_progress']:
            stage_progress = dashboard_data['stage_progress'][str(stage_id)]
            stage_info.update({
                'actual_hours': stage_progress['actual_hours'],
                'progress_percentage': stage_progress['progress_percentage'],
                'sessions': stage_progress['sessions'],
                'status': stage_progress['status']
            })
        
        # Add completion data
        stage_key = str(stage_id)
        stage_info['completed_topics'] = tracker.progress_data.get('completed_topics', {}).get(stage_key, [])
        stage_info['completed_projects'] = tracker.progress_data.get('completed_projects', {}).get(stage_key, [])
        
        return jsonify(stage_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stage/<int:stage_id>/toggle-topic', methods=['POST'])
def api_toggle_topic(stage_id):
    """Toggle completion status of a topic"""
    try:
        data = request.get_json()
        topic_index = data.get('topic_index')
        
        if topic_index is None:
            return jsonify({'error': 'Topic index required'}), 400
        
        stage_key = str(stage_id)
        if 'completed_topics' not in tracker.progress_data:
            tracker.progress_data['completed_topics'] = {}
        if stage_key not in tracker.progress_data['completed_topics']:
            tracker.progress_data['completed_topics'][stage_key] = []
        
        completed_topics = tracker.progress_data['completed_topics'][stage_key]
        
        if topic_index in completed_topics:
            completed_topics.remove(topic_index)
            action = 'unchecked'
        else:
            completed_topics.append(topic_index)
            action = 'checked'
        
        tracker.progress_data['updated_at'] = datetime.now().isoformat()
        tracker.save_json_file(PROGRESS_FILE, tracker.progress_data)
        
        return jsonify({'success': True, 'action': action, 'completed_topics': completed_topics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stage/<int:stage_id>/toggle-project', methods=['POST'])
def api_toggle_project(stage_id):
    """Toggle completion status of a project"""
    try:
        data = request.get_json()
        project_index = data.get('project_index')
        
        if project_index is None:
            return jsonify({'error': 'Project index required'}), 400
        
        stage_key = str(stage_id)
        if 'completed_projects' not in tracker.progress_data:
            tracker.progress_data['completed_projects'] = {}
        if stage_key not in tracker.progress_data['completed_projects']:
            tracker.progress_data['completed_projects'][stage_key] = []
        
        completed_projects = tracker.progress_data['completed_projects'][stage_key]
        
        if project_index in completed_projects:
            completed_projects.remove(project_index)
            action = 'unchecked'
        else:
            completed_projects.append(project_index)
            action = 'checked'
        
        tracker.progress_data['updated_at'] = datetime.now().isoformat()
        tracker.save_json_file(PROGRESS_FILE, tracker.progress_data)
        
        return jsonify({'success': True, 'action': action, 'completed_projects': completed_projects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def api_export():
    """Export all data as JSON"""
    try:
        export_data = {
            'progress': tracker.progress_data,
            'sessions': tracker.sessions_data,
            'goals': tracker.goals_data,
            'exported_at': datetime.now().isoformat()
        }
        return jsonify(export_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-all', methods=['POST'])
def reset_all_data():
    """Reset all progress data - use with caution!"""
    try:
        # Reset progress data
        default_progress = {
            "total_hours": 0,
            "total_sessions": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_session_date": None,
            "achievements": [],
            "daily_logs": {},
            "stage_progress": {str(i): 0 for i in range(1, 9)},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_topics": {}
        }
        
        # Reset sessions data
        default_sessions = []
        
        # Save reset data
        tracker.save_json_file(PROGRESS_FILE, default_progress)
        tracker.save_json_file(SESSIONS_FILE, default_sessions)
        
        return jsonify({
            'success': True,
            'message': 'All data has been reset successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/set-goal', methods=['POST'])
def set_learning_goal():
    """Set daily/weekly learning goals"""
    try:
        data = request.get_json()
        daily_goal = data.get('daily_goal', 2)  # hours
        weekly_goal = data.get('weekly_goal', 12)  # hours
        
        # Load and update progress data
        progress_data = tracker.progress_data
        
        if 'goals' not in progress_data:
            progress_data['goals'] = {}
            
        progress_data['goals']['daily_hours'] = daily_goal
        progress_data['goals']['weekly_hours'] = weekly_goal
        progress_data['updated_at'] = datetime.now().isoformat()
        
        tracker.save_json_file(PROGRESS_FILE, progress_data)
        
        return jsonify({
            'success': True,
            'goals': progress_data['goals']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productivity-stats', methods=['GET'])
def get_productivity_stats():
    """Get detailed productivity statistics"""
    try:
        progress_data = tracker.progress_data
        
        # Calculate productivity metrics
        daily_logs = progress_data.get('daily_logs', {})
        total_days = len(daily_logs)
        
        # Best day
        best_day = {'date': None, 'hours': 0}
        for date, log in daily_logs.items():
            if log['hours'] > best_day['hours']:
                best_day = {'date': date, 'hours': log['hours']}
        
        # Weekly trends
        weekly_hours = []
        sorted_dates = sorted(daily_logs.keys())
        
        for i in range(0, len(sorted_dates), 7):
            week_dates = sorted_dates[i:i+7]
            week_hours = sum(daily_logs[date]['hours'] for date in week_dates)
            weekly_hours.append(week_hours)
        
        # Learning velocity (hours per week trend)
        velocity_trend = 'stable'
        if len(weekly_hours) >= 2:
            recent_avg = sum(weekly_hours[-2:]) / len(weekly_hours[-2:])
            older_avg = sum(weekly_hours[:-2]) / len(weekly_hours[:-2]) if len(weekly_hours) > 2 else recent_avg
            
            if recent_avg > older_avg * 1.1:
                velocity_trend = 'increasing'
            elif recent_avg < older_avg * 0.9:
                velocity_trend = 'decreasing'
        
        # Most productive time patterns
        session_times = []
        sessions_data = tracker.sessions_data
        for session in sessions_data:
            if session.get('start_time'):
                hour = datetime.fromisoformat(session['start_time']).hour
                session_times.append(hour)
        
        # Find most common hour
        most_productive_hour = None
        if session_times:
            from collections import Counter
            hour_counts = Counter(session_times)
            most_productive_hour = hour_counts.most_common(1)[0][0]
        
        return jsonify({
            'total_days_learned': total_days,
            'best_day': best_day,
            'weekly_hours': weekly_hours,
            'velocity_trend': velocity_trend,
            'most_productive_hour': most_productive_hour,
            'avg_session_length': progress_data['total_hours'] / progress_data['total_sessions'] if progress_data['total_sessions'] > 0 else 0,
            'consistency_score': min(100, (progress_data['current_streak'] / 7) * 100)  # out of 100
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning-insights', methods=['GET'])
def get_learning_insights():
    """Get AI-style learning insights and recommendations"""
    try:
        progress_data = tracker.progress_data
        
        insights = []
        
        # Streak insights
        streak = progress_data.get('current_streak', 0)
        if streak >= 7:
            insights.append({
                'type': 'achievement',
                'icon': '🔥',
                'title': 'Streak Master!',
                'message': f'You\'ve maintained a {streak}-day learning streak! You\'re building solid learning habits.'
            })
        elif streak >= 3:
            insights.append({
                'type': 'progress',
                'icon': '⭐',
                'title': 'Building Momentum',
                'message': f'{streak} days in a row! Keep going to reach your next milestone.'
            })
        
        # Hours insights
        total_hours = progress_data.get('total_hours', 0)
        if total_hours >= 50:
            insights.append({
                'type': 'achievement',
                'icon': '🎯',
                'title': 'Dedicated Learner',
                'message': f'{total_hours:.1f} hours invested in your growth! You\'re making serious progress.'
            })
        
        # Session insights
        total_sessions = progress_data.get('total_sessions', 0)
        if total_sessions >= 20:
            insights.append({
                'type': 'habit',
                'icon': '🏆',
                'title': 'Session Champion',
                'message': f'{total_sessions} learning sessions completed! You\'ve built a strong learning routine.'
            })
        
        # Stage completion insights
        stage_progress = progress_data.get('stage_progress', {})
        completed_stages = sum(1 for progress in stage_progress.values() if progress >= 100)
        if completed_stages > 0:
            insights.append({
                'type': 'achievement',
                'icon': '✅',
                'title': 'Stage Conqueror',
                'message': f'{completed_stages} stage(s) completed! You\'re systematically mastering your learning path.'
            })
        
        # Recent activity insight
        daily_logs = progress_data.get('daily_logs', {})
        recent_dates = sorted(daily_logs.keys())[-7:] if daily_logs else []
        recent_hours = sum(daily_logs[date]['hours'] for date in recent_dates)
        
        if recent_hours > 0:
            insights.append({
                'type': 'trend',
                'icon': '📈',
                'title': 'This Week\'s Progress',
                'message': f'{recent_hours:.1f} hours of learning this week. You\'re staying consistent!'
            })
        
        # Recommendations
        recommendations = []
        
        if streak == 0:
            recommendations.append({
                'type': 'motivation',
                'icon': '🚀',
                'title': 'Start Your Streak',
                'message': 'Begin a learning streak today! Even 15 minutes counts toward building a habit.'
            })
        
        if total_hours > 0 and total_sessions > 0:
            avg_session = total_hours / total_sessions
            if avg_session < 0.5:
                recommendations.append({
                    'type': 'improvement',
                    'icon': '⏰',
                    'title': 'Extend Your Sessions',
                    'message': f'Your average session is {avg_session:.1f}h. Try extending to 1+ hours for deeper learning.'
                })
        
        return jsonify({
            'insights': insights,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("🎯 Learning Progress Tracker Starting...")
    print(f"📊 Data will be stored in: {DATA_DIR}")
    print(f"🌐 Access the tracker at: http://localhost:5000")
    print("📚 Your 12-month learning journey tracking is ready!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
