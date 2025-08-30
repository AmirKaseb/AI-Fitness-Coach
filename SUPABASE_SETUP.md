# Supabase Setup Guide for GymJam AI Assistant

## 🚀 Overview
This guide will help you set up Supabase for real user authentication, workout tracking, and pose analysis data storage.

## 📋 Prerequisites
- Supabase account (free tier available)
- Your MediaPipe backend running on port 5000
- Basic knowledge of SQL

## 🔧 Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login and create a new project
3. Choose a project name (e.g., "gymjam-ai")
4. Set a database password (save this!)
5. Choose a region close to your users
6. Wait for project setup (2-3 minutes)

## 🗄️ Step 2: Database Schema Setup

Run these SQL commands in your Supabase SQL Editor:

### Create Users Table
```sql
-- Enable Row Level Security
ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

-- Create users profile table
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    birthdate DATE,
    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on users table
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create policy for users to manage their own profile
CREATE POLICY "Users can manage their own profile" ON public.users
    FOR ALL USING (auth.uid() = id);

-- Create function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### Create Workout Sessions Table
```sql
-- Create workout sessions table
CREATE TABLE public.workout_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    exercise_type TEXT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    total_reps INTEGER DEFAULT 0,
    total_calories INTEGER DEFAULT 0,
    form_score NUMERIC(5,2) DEFAULT 0,
    duration_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on workout_sessions table
ALTER TABLE public.workout_sessions ENABLE ROW LEVEL SECURITY;

-- Create policy for users to manage their own workout sessions
CREATE POLICY "Users can manage their own workout sessions" ON public.workout_sessions
    FOR ALL USING (auth.uid() = user_id);
```

### Create Pose Analysis Table
```sql
-- Create pose analysis table
CREATE TABLE public.pose_analysis (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES public.workout_sessions(id) ON DELETE CASCADE NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    form_score NUMERIC(5,2) NOT NULL,
    arm_position_score NUMERIC(5,2),
    back_alignment_score NUMERIC(5,2),
    range_of_motion_score NUMERIC(5,2),
    feedback_data JSONB,
    pose_landmarks JSONB
);

-- Enable RLS on pose_analysis table
ALTER TABLE public.pose_analysis ENABLE ROW LEVEL SECURITY;

-- Create policy for users to access pose analysis data
CREATE POLICY "Users can access their pose analysis data" ON public.pose_analysis
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions 
            WHERE id = pose_analysis.session_id 
            AND user_id = auth.uid()
        )
    );
```

## 🔑 Step 3: Get API Keys

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the **Project URL** and **anon public** key
3. Update `frontend/supabase-config.js` with your values:

```javascript
const SUPABASE_URL = 'https://your-project-id.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key-here';
```

## 🔒 Step 4: Authentication Settings

1. Go to **Authentication** → **Settings**
2. Configure your site URL (e.g., `http://localhost:3000` for development)
3. Add redirect URLs if needed
4. Enable email confirmations (optional for development)

## 🧪 Step 5: Test the Integration

1. Start your MediaPipe backend: `python backend/app.py`
2. Open `frontend/index.html` in a browser
3. Try signing up with a new account
4. Complete profile setup
5. Start a workout session
6. Check Supabase dashboard for data

## 📊 Step 6: View Your Data

In Supabase dashboard:
- **Table Editor** → View your tables
- **Authentication** → Manage users
- **Logs** → Monitor API calls

## 🔧 Step 7: Backend Integration (Optional)

To get real pose analysis data, add this endpoint to your Flask backend:

```python
@app.route('/pose_analysis/<exercise_type>')
def get_pose_analysis(exercise_type):
    """Get real-time pose analysis data"""
    # This would integrate with your MediaPipe pose detection
    # Return JSON with form scores and rep detection
    
    # Example response:
    return jsonify({
        'rep_detected': True,  # Based on pose analysis
        'form_score': 85.5,    # Overall form score
        'arm_position_score': 90.0,
        'back_alignment_score': 80.0,
        'range_of_motion_score': 85.0,
        'landmarks': {}  # Pose landmarks data
    })
```

## 🚨 Troubleshooting

### Common Issues:

1. **CORS Error**: Ensure your Supabase project allows your domain
2. **RLS Policy Error**: Check if Row Level Security policies are correct
3. **Authentication Error**: Verify API keys and project URL
4. **Table Not Found**: Run the SQL commands in the correct order

### Debug Tips:

1. Check browser console for errors
2. Use Supabase dashboard logs
3. Test SQL queries in Supabase SQL Editor
4. Verify user authentication state

## 📈 Next Steps

1. **Real-time Updates**: Add Supabase real-time subscriptions
2. **Advanced Analytics**: Create custom SQL views for insights
3. **User Progress**: Track long-term fitness goals
4. **Social Features**: Add friend connections and leaderboards
5. **Mobile App**: Use Supabase client for React Native/Flutter

## 🎯 What You've Built

✅ **Real User Authentication** with Supabase Auth  
✅ **User Profile Management** with custom user table  
✅ **Workout Session Tracking** with timestamps and metrics  
✅ **Real-time Pose Analysis** data storage  
✅ **Secure Data Access** with Row Level Security  
✅ **Scalable Database** ready for production  

Your GymJam AI Assistant now has a production-ready backend with real user data, workout history, and pose analysis tracking! 🎉
