-- Supabase Tables Setup for GymJam AI Assistant
-- Run this in your Supabase SQL Editor

-- Enable Row Level Security
ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

-- Create users profile table
CREATE TABLE IF NOT EXISTS public.users (
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

-- Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Users can manage their own profile" ON public.users;

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
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Create workout sessions table
CREATE TABLE IF NOT EXISTS public.workout_sessions (
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

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can manage their own workout sessions" ON public.workout_sessions;

-- Create policy for users to manage their own workout sessions
CREATE POLICY "Users can manage their own workout sessions" ON public.workout_sessions
    FOR ALL USING (auth.uid() = user_id);

-- Create pose analysis table
CREATE TABLE IF NOT EXISTS public.pose_analysis (
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

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can access their pose analysis data" ON public.pose_analysis;

-- Create policy for users to access pose analysis data
CREATE POLICY "Users can access their pose analysis data" ON public.pose_analysis
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions 
            WHERE id = pose_analysis.session_id 
            AND user_id = auth.uid()
        )
    );