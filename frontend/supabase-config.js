// Supabase Configuration
const SUPABASE_URL = 'https://kbmbvuzufkapujadmsld.supabase.co'; // Replace with your actual Supabase URL
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtibWJ2dXp1ZmthcHVqYWRtc2xkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYzMzgzMDMsImV4cCI6MjA3MTkxNDMwM30.4PTOfys2FDDFUjt1CN-AURCCng_ZRs7EXinUCuZhhK4'; // Replace with your actual anon key

// Initialize Supabase client
let supabase;

// Wait for Supabase to be loaded from CDN
document.addEventListener('DOMContentLoaded', () => {
    if (window.supabase) {
        try {
            supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
                auth: {
                    autoRefreshToken: true,
                    persistSession: true,
                    detectSessionInUrl: true
                }
            });
            window.supabaseClient = supabase;
        } catch (error) {
            // Silent fail
        }
    } else {
        setTimeout(() => {
            if (window.supabase) {
                try {
                    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
                        auth: {
                            autoRefreshToken: true,
                            persistSession: true,
                            detectSessionInUrl: true
                        }
                    });
                    window.supabaseClient = supabase;
                } catch (error) {
                    // Silent fail
                }
            }
        }, 2000);
    }
});

// Database Tables Schema:
/*
users:
- id (uuid, primary key)
- email (text, unique)
- full_name (text)
- birthdate (date)
- gender (text)
- created_at (timestamp)
- updated_at (timestamp)

workout_sessions:
- id (uuid, primary key)
- user_id (uuid, foreign key to users.id)
- exercise_type (text)
- start_time (timestamp)
- end_time (timestamp)
- total_reps (integer)
- total_calories (integer)
- form_score (numeric)
- duration_minutes (integer)
- created_at (timestamp)

pose_analysis:
- id (uuid, primary key)
- session_id (uuid, foreign key to workout_sessions.id)
- timestamp (timestamp)
- form_score (numeric)
- arm_position_score (numeric)
- back_alignment_score (numeric)
- range_of_motion_score (numeric)
- feedback_data (jsonb)
- pose_landmarks (jsonb)
*/

// Supabase client is now available globally as window.supabase
