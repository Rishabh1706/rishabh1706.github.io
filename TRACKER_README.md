# Learning Progress Tracker

A comprehensive web application to track your 12-month learning journey in Data Engineering, MLOps, and Cloud Engineering.

## 🚀 Quick Start

### Windows
1. Double-click `start_tracker.bat`
2. Open http://localhost:5000 in your browser

### Manual Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open http://localhost:5000 in your browser

## 📊 Features

### Real-Time Session Tracking
- **Accurate Time Tracking**: Automatically tracks active learning time
- **Pause/Resume**: Pause sessions when you take breaks
- **Session Notes**: Record what you learned and how you felt
- **Topic Tagging**: Tag sessions with specific topics

### Progress Analysis
- **Weekly Progress**: Compare actual vs expected progress
- **Stage Tracking**: Monitor progress through 8 learning stages
- **Status Indicators**: Know if you're ahead, on track, or behind
- **Streak Tracking**: Maintain learning consistency

### Data Persistence
- **JSON Storage**: All data stored in local JSON files
- **Export Capability**: Download your complete progress data
- **Backup Ready**: Easy to backup and restore your data
- **No Database Required**: Simple file-based storage

### Intelligent Insights
- **Progress Ratios**: Detailed analysis of your learning pace
- **Catch-up Calculations**: Know exactly how much to study daily
- **Achievement System**: Unlock achievements for milestones
- **Detailed Recommendations**: Get specific advice based on your progress

## 🗂️ File Structure

```
learning-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start_tracker.bat     # Windows startup script
├── templates/
│   └── dashboard.html    # Web interface
└── data/                 # Auto-created data directory
    ├── progress.json     # Overall progress data
    ├── sessions.json     # Individual session records
    └── goals.json        # Learning goals and milestones
```

## 📈 How It Works

### 1. Start a Session
Click "Start Session" when you begin studying. The timer starts tracking your active learning time.

### 2. Track Your Time
The application automatically tracks time, pausing when you switch tabs or take breaks.

### 3. End with Notes
When you finish, add notes about what you learned, topics covered, and how you felt.

### 4. Monitor Progress
View your progress against the 12-month learning plan with detailed analytics.

### 5. Stay Motivated
Get real-time feedback on whether you're ahead, on track, or need to catch up.

## 🎯 Learning Plan Integration

The tracker is built specifically for your 12-month learning plan:

- **Week 1-8**: Core Programming + Data Foundations (288 hours)
- **Week 9-16**: Backend Engineering Foundation (288 hours)
- **Week 17-24**: Data Engineering Essentials (288 hours)
- **Week 25-32**: DevOps + Cloud Engineering (288 hours)
- **Week 33-36**: Machine Learning & Data Science (144 hours)
- **Week 37-40**: MLOps (144 hours)
- **Week 41-44**: Generative AI / LLMs (144 hours)
- **Week 45-48**: Cloud Integration & Capstone (144 hours)

**Total Target**: 1,600 hours over 48 weeks

## 🔧 Configuration

The application uses these default targets:
- **Weekdays**: 4 hours per day
- **Weekends**: 8 hours per day
- **Weekly Total**: 36 hours
- **Start Date**: January 1, 2025

You can modify these in `app.py` in the `LEARNING_PLAN` configuration.

## 🎯 Stay Disciplined

This tracker is designed to help you:
- **Be Consistent**: Daily tracking builds habits
- **Stay Accountable**: Visual progress keeps you motivated
- **Measure Progress**: Know exactly where you stand
- **Adjust Course**: Get specific recommendations when behind
- **Celebrate Wins**: Achievements recognize your hard work

Start your journey today and build the discipline to complete your 12-month learning plan! 🚀
