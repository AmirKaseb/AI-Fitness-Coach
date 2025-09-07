// AI Powered Coach - Complete Application JavaScript with Supabase Integration

// Toast Notification System
class ToastNotification {
    static show(type, title, message, duration = 4000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icons[type]}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Rate limiting utility
const rateLimiter = {
    lastRequest: 0,
    minInterval: 1000, // 1 second between requests
    
    async throttle() {
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequest;
        
        if (timeSinceLastRequest < this.minInterval) {
            await new Promise(resolve => 
                setTimeout(resolve, this.minInterval - timeSinceLastRequest)
            );
        }
        
        this.lastRequest = Date.now();
    }
};

// Function to get Supabase client
function getSupabaseClient() {
    // First check if we already have a client
    if (window.supabaseClient) {
        return window.supabaseClient;
    }
    
    // Check if Supabase is loaded
    if (window.supabase) {
        try {
            // Create a new client with proper configuration
            const supabaseClient = window.supabase.createClient(
                'https://kbmbvuzufkapujadmsld.supabase.co',
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtibWJ2dXp1ZmthcHVqYWRtc2xkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYzMzgzMDMsImV4cCI6MjA3MTkxNDMwM30.4PTOfys2FDDFUjt1CN-AURCCng_ZRs7EXinUCuZhhK4',
                {
                    auth: {
                        autoRefreshToken: true,
                        persistSession: true,
                        detectSessionInUrl: true
                    }
                }
            );
            
            // Store the client globally
            window.supabaseClient = supabaseClient;
            return supabaseClient;
        } catch (error) {
            // If creation fails, return null
            return null;
        }
    }
    
    return null;
}

class AIPoweredCoach {
    constructor() {
        this.currentUser = null;
        this.currentSection = 'home';
        this.workoutFlow = {
            step: 0,
            goal: null,
            plan: null,
            type: null,
            session: null
        };
        this.currentWorkoutSession = null;
        this.poseAnalysisInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        
        // Initialize Supabase client
        this.initializeSupabase();
        
        setTimeout(() => {
            this.checkAuthStatus();
        }, 1000);
    }
    
    initializeSupabase() {
        if (window.supabase && !window.supabaseClient) {
            try {
                const supabaseClient = window.supabase.createClient(
                    'https://kbmbvuzufkapujadmsld.supabase.co',
                    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtibWJ2dXp1ZmthcHVqYWRtc2xkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYzMzgzMDMsImV4cCI6MjA3MTkxNDMwM30.4PTOfys2FDDFUjt1CN-AURCCng_ZRs7EXinUCuZhhK4',
                    {
                        auth: {
                            autoRefreshToken: true,
                            persistSession: true,
                            detectSessionInUrl: true
                        }
                    }
                );
                window.supabaseClient = supabaseClient;
            } catch (error) {
                // Silent fail
            }
        }
    }

    setupEventListeners() {
        const signupForm = document.getElementById('signup-form');
        const loginForm = document.getElementById('login-form');
        const profileForm = document.getElementById('profile-form');
        
        signupForm?.addEventListener('submit', (e) => this.handleSignUp(e));
        loginForm?.addEventListener('submit', (e) => this.handleLogIn(e));
        profileForm?.addEventListener('submit', (e) => this.handleProfileSetup(e));
    }

    // Authentication Functions
    showSignUp() {
        const landingPage = document.getElementById('landing-page');
        const signupModal = document.getElementById('signup-modal');
        
        if (landingPage && signupModal) {
            landingPage.classList.add('hidden');
            signupModal.classList.remove('hidden');
        }
    }

    showLogIn() {
        const landingPage = document.getElementById('landing-page');
        const loginModal = document.getElementById('login-modal');
        
        if (landingPage && loginModal) {
            landingPage.classList.add('hidden');
            loginModal.classList.remove('hidden');
        }
    }

    hideModals() {
        const landingPage = document.getElementById('landing-page');
        const signupModal = document.getElementById('signup-modal');
        const loginModal = document.getElementById('login-modal');
        const profileModal = document.getElementById('profile-modal');
        const mainApp = document.getElementById('main-app');
        
        if (landingPage) landingPage.classList.remove('hidden');
        if (signupModal) signupModal.classList.add('hidden');
        if (loginModal) loginModal.classList.add('hidden');
        if (profileModal) profileModal.classList.add('hidden');
        if (mainApp) mainApp.classList.add('hidden');
    }

    switchTab(tab) {
        this.hideModals();
        
        if (tab === 'signup') {
            this.showSignUp();
        } else if (tab === 'login') {
            this.showLogIn();
        }
    }

    async handleSignUp(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        if (formData.get('password') !== formData.get('confirm-password')) {
            ToastNotification.show('error', 'Password Mismatch', 'Passwords do not match. Please try again.');
            return;
        }

        if (formData.get('password').length < 8) {
            ToastNotification.show('error', 'Password Too Short', 'Password must be at least 8 characters long.');
            return;
        }

        try {
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) {
                ToastNotification.show('error', 'Connection Error', 'Unable to connect to our servers. Please try again.');
                return;
            }
            
            const { data, error } = await supabaseClient.auth.signUp({
                email: formData.get('email'),
                password: formData.get('password'),
                options: {
                    data: {
                        full_name: formData.get('fullname')
                    }
                }
            });
            
            if (error) {
                if (error.message.includes('already registered')) {
                    ToastNotification.show('warning', 'Account Exists', 'This email is already registered. Please log in instead.');
                } else if (error.message.includes('Invalid email')) {
                    ToastNotification.show('error', 'Invalid Email', 'Please enter a valid email address.');
                } else {
                    ToastNotification.show('error', 'Signup Failed', 'Unable to create account. Please try again.');
                }
                return;
            }
            
            if (data.user) {
                ToastNotification.show('success', 'Account Created', 'Welcome! Please check your email to verify your account.');
                
                this.currentUser = {
                    id: data.user.id,
                    email: data.user.email,
                    full_name: formData.get('fullname')
                };
                
                this.authenticateUser();
            }
        } catch (error) {
            ToastNotification.show('error', 'Signup Failed', 'Something went wrong. Please try again.');
        }
    }

    async handleLogIn(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) {
                ToastNotification.show('error', 'Connection Error', 'Unable to connect to our servers. Please try again.');
                return;
            }
            
            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email: formData.get('email'),
                password: formData.get('password')
            });
            
            if (error) {
                if (error.message.includes('Invalid login credentials')) {
                    ToastNotification.show('error', 'Invalid Credentials', 'Email or password is incorrect. Please try again.');
                } else if (error.message.includes('Email not confirmed')) {
                    ToastNotification.show('warning', 'Email Verification Required', 'Please check your email and verify your account before logging in.');
                } else {
                    ToastNotification.show('error', 'Login Failed', 'Unable to log in. Please try again.');
                }
                return;
            }
            
            if (data.user) {
                ToastNotification.show('success', 'Welcome Back!', 'Successfully logged in to your account.');
                
                this.currentUser = {
                    id: data.user.id,
                    email: data.user.email,
                    full_name: data.user.user_metadata?.full_name || 'User',
                    birthdate: null,
                    gender: null
                };
                
                this.authenticateUser();
            }
        } catch (error) {
            ToastNotification.show('error', 'Login Failed', 'Something went wrong. Please try again.');
        }
    }

    async handleProfileSetup(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            // Apply rate limiting
            await rateLimiter.throttle();
            
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) {
                return;
            }
            const { data, error } = await supabaseClient
                .from('users')
                .insert([
                    {
                        id: this.currentUser.id,
                        email: this.currentUser.email,
                        full_name: formData.get('name'),
                        birthdate: formData.get('birthdate'),
                        gender: formData.get('gender')
                    }
                ])
                .select()
                .single();
            
            if (error) {
                if (error.code === '23505') {
                    const { data: updateData, error: updateError } = await supabaseClient
                        .from('users')
                        .update({
                            full_name: formData.get('name'),
                            birthdate: formData.get('birthdate'),
                            gender: formData.get('gender')
                        })
                        .eq('id', this.currentUser.id)
                        .select()
                        .single();
                    
                    if (updateError) {
                        return;
                    }
                    data = updateData;
                } else {
                    return;
                }
            }
            
            this.currentUser = {
                ...this.currentUser,
                full_name: data.full_name,
                birthdate: data.birthdate,
                gender: data.gender
            };
            
            this.authenticateUser();
        } catch (error) {
            // Handle error silently
        }
    }

    authenticateUser() {
        this.hideModals();
        
        document.getElementById('landing-page').classList.add('hidden');
        document.getElementById('main-app').classList.remove('hidden');
        
        this.updateUserInterface();
    }

    async checkAuthStatus() {
        try {
            // Apply rate limiting
            await rateLimiter.throttle();
            
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) {
                return;
            }
            
            const { data: { session }, error } = await supabaseClient.auth.getSession();
            
            if (error) {
                return;
            }
            
            if (session?.user) {
                // Apply rate limiting for profile fetch
                await rateLimiter.throttle();
                
                const { data: profile, error: profileError } = await supabaseClient
                    .from('users')
                    .select('*')
                    .eq('id', session.user.id)
                    .single();
                
                this.currentUser = {
                    id: session.user.id,
                    email: session.user.email,
                    full_name: profile?.full_name || session.user.user_metadata?.full_name || 'User',
                    birthdate: profile?.birthdate,
                    gender: profile?.gender
                };
                
                this.authenticateUser();
            } else {
                const savedUser = localStorage.getItem('aiCoachUser');
                if (savedUser) {
                    this.currentUser = JSON.parse(savedUser);
                    this.authenticateUser();
                }
            }
        } catch (error) {
            // Silent fail
        }
    }

    async updateUserInterface() {
        const greeting = document.querySelector('.greeting');
        if (greeting && this.currentUser) {
            const hour = new Date().getHours();
            let timeGreeting = 'Good morning!';
            if (hour >= 12 && hour < 17) timeGreeting = 'Good afternoon!';
            else if (hour >= 17) timeGreeting = 'Good evening!';
            
            greeting.textContent = `${timeGreeting}, ${this.currentUser.full_name}!`;
        }

        await this.loadWorkoutHistory();
        await this.loadProfileData();
        localStorage.setItem('aiCoachUser', JSON.stringify(this.currentUser));
    }
    
    async loadWorkoutHistory() {
        try {
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) {
                return;
            }
            const { data: sessions, error } = await supabaseClient
                .from('workout_sessions')
                .select('*')
                .eq('user_id', this.currentUser.id)
                .order('created_at', { ascending: false })
                .limit(7);
            
            if (error) {
                return;
            }
            
            this.updateChartsWithRealData(sessions);
            
        } catch (error) {
            // Silent fail
        }
    }
    
    updateChartsWithRealData(sessions) {
        const poseChart = document.querySelector('.chart:has(h3:contains("Score")) .chart-bars');
        if (poseChart) {
            this.updateChartBars(poseChart, sessions, 'form_score', 100);
        }
        
        const caloriesChart = document.querySelector('.chart:has(h3:contains("Calories")) .chart-bars');
        if (caloriesChart) {
            this.updateChartBars(caloriesChart, sessions, 'total_calories', 100);
        }
        
        const timeChart = document.querySelector('.chart:has(h3:contains("Time")) .chart-bars');
        if (timeChart) {
            this.updateChartBars(timeChart, sessions, 'duration_minutes', 60);
        }
    }
    
    updateChartBars(chartElement, sessions, field, maxValue) {
        const barGroups = chartElement.querySelectorAll('.bar-group');
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        
        barGroups.forEach((barGroup, index) => {
            const bar = barGroup.querySelector('.bar');
            const dayLabel = barGroup.querySelector('span');
            
            const session = sessions.find(s => {
                const sessionDate = new Date(s.created_at);
                return sessionDate.getDay() === index;
            });
            
            if (session) {
                const value = session[field] || 0;
                const height = Math.min((value / maxValue) * 100, 100);
                bar.style.height = `${height}%`;
                
                if (height >= 80) {
                    bar.className = 'bar dark-green';
                } else if (height >= 50) {
                    bar.className = 'bar light-green';
                } else {
                    bar.className = 'bar light-green';
                }
            } else {
                bar.style.height = '0%';
            }
        });
    }

    // Profile Section Functions
    async loadProfileData() {
        if (!this.currentUser) return;
        
        try {
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) return;
            
            // Load user profile data
            const { data: profile, error: profileError } = await supabaseClient
                .from('users')
                .select('*')
                .eq('id', this.currentUser.id)
                .single();
            
            if (profile) {
                this.updateProfileDisplay(profile);
            }
            
            // Load workout statistics
            const { data: sessions, error: sessionsError } = await supabaseClient
                .from('workout_sessions')
                .select('*')
                .eq('user_id', this.currentUser.id);
            
            if (sessions) {
                this.updateWorkoutStatistics(sessions);
                this.updateRecentWorkouts(sessions);
            }
            
        } catch (error) {
            console.error('Error loading profile data:', error);
        }
    }

    updateProfileDisplay(profile) {
        document.getElementById('displayName').textContent = profile.full_name || 'Not set';
        document.getElementById('displayEmail').textContent = profile.email || 'Not set';
        document.getElementById('displayBirthdate').textContent = profile.birthdate || 'Not set';
        document.getElementById('displayGender').textContent = profile.gender || 'Not set';
        
        // Update form fields
        document.getElementById('updateName').value = profile.full_name || '';
        document.getElementById('updateBirthdate').value = profile.birthdate || '';
        document.getElementById('updateGender').value = profile.gender || '';
    }

    updateWorkoutStatistics(sessions) {
        const totalWorkouts = sessions.length;
        const totalCalories = sessions.reduce((sum, session) => sum + (session.total_calories || 0), 0);
        const totalTime = sessions.reduce((sum, session) => sum + (session.duration_minutes || 0), 0);
        const avgScore = sessions.length > 0 ? 
            Math.round(sessions.reduce((sum, session) => sum + (session.form_score || 0), 0) / sessions.length) : 0;
        
        document.getElementById('totalWorkouts').textContent = totalWorkouts;
        document.getElementById('totalCalories').textContent = totalCalories;
        document.getElementById('totalTime').textContent = totalTime;
        document.getElementById('avgScore').textContent = `${avgScore}%`;
    }

    updateRecentWorkouts(sessions) {
        const recentWorkouts = sessions
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .slice(0, 5);
        
        const container = document.getElementById('recentWorkouts');
        container.innerHTML = '';
        
        if (recentWorkouts.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #7f8c8d; padding: 2rem;">No workouts yet. Start your first workout!</p>';
            return;
        }
        
        recentWorkouts.forEach(session => {
            const workoutItem = document.createElement('div');
            workoutItem.className = 'workout-item';
            
            const exerciseType = this.formatExerciseType(session.exercise_type);
            const date = new Date(session.created_at).toLocaleDateString();
            
            workoutItem.innerHTML = `
                <div class="workout-info">
                    <span class="workout-type">${exerciseType}</span>
                    <span class="workout-date">${date}</span>
                </div>
                <div class="workout-stats">
                    <span class="workout-reps">${session.total_reps || 0} reps</span>
                    <span class="workout-score">${session.form_score || 0}%</span>
                </div>
            `;
            
            container.appendChild(workoutItem);
        });
    }

    formatExerciseType(type) {
        const typeMap = {
            'left_arm_curl': 'Left Arm Curl',
            'right_arm_curl': 'Right Arm Curl',
            'pushup': 'Push-ups',
            'squat': 'Squats'
        };
        return typeMap[type] || type;
    }

    async updatePersonalInfo(formData) {
        try {
            const supabaseClient = getSupabaseClient();
            if (!supabaseClient) return false;
            
            const { data, error } = await supabaseClient
                .from('users')
                .update({
                    full_name: formData.get('name'),
                    birthdate: formData.get('birthdate'),
                    gender: formData.get('gender')
                })
                .eq('id', this.currentUser.id)
                .select()
                .single();
            
            if (error) {
                console.error('Error updating profile:', error);
                return false;
            }
            
            // Update current user object
            this.currentUser = {
                ...this.currentUser,
                full_name: data.full_name,
                birthdate: data.birthdate,
                gender: data.gender
            };
            
            // Update display
            this.updateProfileDisplay(data);
            
            return true;
        } catch (error) {
            console.error('Error updating profile:', error);
            return false;
        }
    }

    // Navigation Functions
    showSection(sectionName) {
        const sections = document.querySelectorAll('.app-section');
        sections.forEach(section => section.classList.add('hidden'));
        
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }

        const navLinks = document.querySelectorAll('.app-nav .nav-link');
        navLinks.forEach(link => link.classList.remove('active'));
        
        const activeLink = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        this.currentSection = sectionName;
    }

    // Workout Flow Functions
    startWorkoutFlow() {
        this.workoutFlow.step = 1;
        this.showGoalsSection();
    }

    showGoalsSection() {
        if (!document.getElementById('goals-section')) {
            this.createGoalsSection();
        }
        
        this.showSection('goals');
    }

    createGoalsSection() {
        const mainApp = document.getElementById('main-app');
        
        const goalsSection = document.createElement('section');
        goalsSection.id = 'goals-section';
        goalsSection.className = 'app-section';
        goalsSection.innerHTML = `
            <div class="goals-content">
                <h2>Set Your Goal</h2>
                <p class="goals-subtitle">What would you like to focus on?</p>
                
                <div class="goal-options">
                    <div class="goal-option" onclick="aiCoach.selectGoal('lose-weight')">
                        <div class="goal-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="goal-info">
                            <h3>Lose weight</h3>
                            <p>Burn calories and increase stamina</p>
                        </div>
                    </div>
                    
                    <div class="goal-option" onclick="aiCoach.selectGoal('build-strength')">
                        <div class="goal-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="goal-info">
                            <h3>Build strength</h3>
                            <p>Tone muscles and get stronger</p>
                        </div>
                    </div>
                    
                    <div class="goal-option" onclick="aiCoach.selectGoal('improve-flexibility')">
                        <div class="goal-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="goal-info">
                            <h3>Improve flexibility</h3>
                            <p>Stretch deeper and move better</p>
                        </div>
                    </div>
                </div>
                
                <button class="continue-btn" onclick="aiCoach.continueToPlan()">Continue</button>
            </div>
        `;
        
        mainApp.appendChild(goalsSection);
    }

    selectGoal(goal) {
        this.workoutFlow.goal = goal;
        
        const goalOptions = document.querySelectorAll('.goal-option');
        goalOptions.forEach(option => {
            option.classList.remove('selected');
        });
        
        const selectedOption = document.querySelector(`[onclick="aiCoach.selectGoal('${goal}')"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        const continueBtn = document.querySelector('.continue-btn');
        if (continueBtn) {
            continueBtn.disabled = false;
            continueBtn.classList.add('active');
            continueBtn.classList.remove('disabled');
        }
    }

    continueToPlan() {
        if (!this.workoutFlow.goal) return;
        
        this.workoutFlow.step = 2;
        this.showPlanSection();
    }

    showPlanSection() {
        if (!document.getElementById('plan-section')) {
            this.createPlanSection();
        }
        
        this.showSection('plan');
    }

    createPlanSection() {
        const mainApp = document.getElementById('main-app');
        
        const planSection = document.createElement('section');
        planSection.id = 'plan-section';
        planSection.className = 'app-section';
        planSection.innerHTML = `
            <div class="plan-content">
                <h2>Choose your workout plan</h2>
                <p class="plan-subtitle">Based on your goal</p>
                
                <div class="plan-options">
                    <div class="plan-option" onclick="aiCoach.selectPlan('beginner')">
                        <div class="plan-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="plan-info">
                            <h3>Beginner Plan</h3>
                            <p>Perfect for those just starting their fitness journey</p>
                        </div>
                    </div>
                    
                    <div class="plan-option" onclick="aiCoach.selectPlan('intermediate')">
                        <div class="plan-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="plan-info">
                            <h3>Intermediate Plan</h3>
                            <p>For those with some fitness experience</p>
                        </div>
                    </div>
                    
                    <div class="plan-option" onclick="aiCoach.selectPlan('advanced')">
                        <div class="plan-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="plan-info">
                            <h3>Advanced Plan</h3>
                            <p>Challenging workouts for fitness enthusiasts</p>
                        </div>
                    </div>
                </div>
                
                <button class="continue-btn" onclick="aiCoach.continueToType()">Continue</button>
            </div>
        `;
        
        mainApp.appendChild(planSection);
    }

    selectPlan(plan) {
        this.workoutFlow.plan = plan;
        
        const planOptions = document.querySelectorAll('.plan-option');
        planOptions.forEach(option => {
            option.classList.remove('selected');
        });
        
        const selectedOption = document.querySelector(`[onclick="aiCoach.selectPlan('${plan}')"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        const continueBtn = document.querySelector('.continue-btn');
        if (continueBtn) {
            continueBtn.disabled = false;
            continueBtn.classList.add('active');
            continueBtn.classList.remove('disabled');
        }
    }

    continueToType() {
        if (!this.workoutFlow.plan) return;
        
        this.workoutFlow.step = 3;
        this.showTypeSection();
    }

    showTypeSection() {
        if (!document.getElementById('type-section')) {
            this.createTypeSection();
        }
        
        this.showSection('type');
    }

    createTypeSection() {
        const mainApp = document.getElementById('main-app');
        
        const typeSection = document.createElement('section');
        typeSection.id = 'type-section';
        typeSection.className = 'app-section';
        typeSection.innerHTML = `
            <div class="type-content">
                <h2>Choose your workout type</h2>
                
                <div class="workout-grid">
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('yoga')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>Yoga</h3>
                        <p>Beginner - 45 min</p>
                    </div>
                    
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('pilates')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>Pilates</h3>
                        <p>Beginner - 30 min</p>
                    </div>
                    
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('hiit')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>HIIT</h3>
                        <p>Intermediate - 25 min</p>
                    </div>
                    
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('cardio')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>Cardio</h3>
                        <p>Intermediate - 35 min</p>
                    </div>
                    
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('strength')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>Strength Training</h3>
                        <p>Advanced - 40 min</p>
                    </div>
                    
                    <div class="workout-card" onclick="aiCoach.selectWorkoutType('flexibility')">
                        <div class="workout-image">
                            <i class="fas fa-user"></i>
                        </div>
                        <h3>Flexibility</h3>
                        <p>Beginner - 20 min</p>
                    </div>
                </div>
            </div>
        `;
        
        mainApp.appendChild(typeSection);
    }

    selectWorkoutType(type) {
        this.workoutFlow.type = type;
        
        const workoutCards = document.querySelectorAll('.workout-card');
        workoutCards.forEach(card => {
            card.classList.remove('selected');
        });
        
        const selectedCard = document.querySelector(`[onclick="aiCoach.selectWorkoutType('${type}')"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        setTimeout(() => {
            this.showSessionSection();
        }, 500);
    }

    showSessionSection() {
        if (!document.getElementById('session-section')) {
            this.createSessionSection();
        }
        
        this.showSection('session');
    }

    createSessionSection() {
        const mainApp = document.getElementById('main-app');
        
        const sessionSection = document.createElement('section');
        sessionSection.id = 'session-section';
        sessionSection.className = 'app-section';
        sessionSection.innerHTML = `
            <div class="session-content">
                <h2>Choose session</h2>
                
                <div class="session-options">
                    <div class="session-option" onclick="aiCoach.selectSession('morning-flow')">
                        <div class="session-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="session-info">
                            <h3>Morning Flow - 15 min</h3>
                            <p>Start your day with gentle movement</p>
                        </div>
                    </div>
                    
                    <div class="session-option" onclick="aiCoach.selectSession('stress-relief')">
                        <div class="session-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="session-info">
                            <h3>Stress Relief - 15 min</h3>
                            <p>Relax and unwind</p>
                        </div>
                    </div>
                    
                    <div class="session-option" onclick="aiCoach.selectSession('full-body')">
                        <div class="session-radio">
                            <div class="radio-dot"></div>
                        </div>
                        <div class="session-info">
                            <h3>Full Body Yoga - 15 min</h3>
                            <p>Complete body workout</p>
                        </div>
                    </div>
                </div>
                
                <button class="continue-btn" onclick="aiCoach.continueToWorkout()">Continue</button>
            </div>
        `;
        
        mainApp.appendChild(sessionSection);
    }

    selectSession(session) {
        this.workoutFlow.session = session;
        
        const sessionOptions = document.querySelectorAll('.session-option');
        sessionOptions.forEach(option => {
            option.classList.remove('selected');
        });
        
        const selectedOption = document.querySelector(`[onclick="aiCoach.selectSession('${session}')"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        const continueBtn = document.querySelector('.continue-btn');
        if (continueBtn) {
            continueBtn.disabled = false;
            continueBtn.classList.add('active');
            continueBtn.classList.remove('disabled');
        }
    }

    continueToWorkout() {
        if (!this.workoutFlow.session) return;
        
        this.startWorkoutSession();
    }

    startWorkoutSession() {
        this.createWorkoutSession();
        this.showSection('workout');
    }

    createWorkoutSession() {
        const mainApp = document.getElementById('main-app');
        
        const workoutSection = document.createElement('section');
        workoutSection.id = 'workout-section';
        workoutSection.className = 'app-section';
        workoutSection.innerHTML = `
            <div class="workout-session">
                <h2>${this.workoutFlow.type.toUpperCase()}</h2>
                <p>Try a session preview to see how the coaching feature works</p>
                
                <div class="session-preview">
                    <div class="preview-placeholder">
                        <i class="fas fa-play-circle"></i>
                        <p>Session Preview</p>
                    </div>
                </div>
                
                <div class="session-actions">
                    <button class="demo-btn" onclick="aiCoach.startDemo()">Start Demo</button>
                    <button class="start-btn" onclick="aiCoach.startRealWorkout()">Start Now</button>
                </div>
            </div>
        `;
        
        mainApp.appendChild(workoutSection);
    }

    startDemo() {
        this.showSection('workout');
    }

    startRealWorkout() {
        this.showSection('workout');
    }

    // Utility Functions
    async logOut() {
        try {
            const supabaseClient = getSupabaseClient();
            if (supabaseClient) {
                await supabaseClient.auth.signOut();
            }
        } catch (error) {
            // Silent fail
        }
        
        this.currentUser = null;
        localStorage.removeItem('aiCoachUser');
        
        document.getElementById('main-app').classList.add('hidden');
        document.getElementById('landing-page').classList.remove('hidden');
        
        this.workoutFlow = {
            step: 0,
            goal: null,
            plan: null,
            type: null,
            session: null
        };
        
        ToastNotification.show('info', 'Logged Out', 'You have been successfully logged out. Come back soon!');
    }


}

// Initialize the app when DOM is ready
let aiCoach;

document.addEventListener('DOMContentLoaded', () => {
    aiCoach = new AIPoweredCoach();
    initializeVoiceSynthesis();
});

// Global functions for onclick handlers - work immediately without aiCoach
function showSignUp() {
    const landingPage = document.getElementById('landing-page');
    const signupModal = document.getElementById('signup-modal');
    
    if (landingPage && signupModal) {
        landingPage.classList.add('hidden');
        signupModal.classList.remove('hidden');
    }
}

function showLogIn() {
    const landingPage = document.getElementById('landing-page');
    const loginModal = document.getElementById('login-modal');
    
    if (landingPage && loginModal) {
        landingPage.classList.add('hidden');
        loginModal.classList.remove('hidden');
    }
}

function hideModals() {
    const landingPage = document.getElementById('landing-page');
    const signupModal = document.getElementById('signup-modal');
    const loginModal = document.getElementById('login-modal');
    const profileModal = document.getElementById('profile-modal');
    const mainApp = document.getElementById('main-app');
    
    if (landingPage) landingPage.classList.remove('hidden');
    if (signupModal) signupModal.classList.add('hidden');
    if (loginModal) loginModal.classList.add('hidden');
    if (profileModal) profileModal.classList.add('hidden');
    if (mainApp) mainApp.classList.add('hidden');
}

function switchTab(tab) {
    const signupModal = document.getElementById('signup-modal');
    const loginModal = document.getElementById('login-modal');
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');
    
    if (tab === 'signup') {
        if (signupModal) signupModal.classList.remove('hidden');
        if (loginModal) loginModal.classList.add('hidden');
        if (signupForm) signupForm.style.display = 'block';
        if (loginForm) loginForm.style.display = 'none';
    } else if (tab === 'login') {
        if (signupModal) signupModal.classList.add('hidden');
        if (loginModal) loginModal.classList.remove('hidden');
        if (signupForm) signupForm.style.display = 'none';
        if (loginForm) loginForm.style.display = 'block';
    }
}

function showSection(sectionName) {
    if (aiCoach) {
        aiCoach.showSection(sectionName);
    }
}

function startWorkoutFlow() {
    if (aiCoach) {
        aiCoach.startWorkoutFlow();
    }
}





// Workout Functions
let currentExerciseType = null;
let voiceSynthesis = null;

// Initialize voice synthesis
function initializeVoiceSynthesis() {
    if ('speechSynthesis' in window) {
        voiceSynthesis = window.speechSynthesis;
        
        // Wait for voices to load
        if (voiceSynthesis.getVoices().length === 0) {
            voiceSynthesis.addEventListener('voiceschanged', () => {
                console.log('Voices loaded:', voiceSynthesis.getVoices().length);
            });
        }
    }
}

// Speak feedback with female voice
function speakFeedback(text) {
    if (!voiceSynthesis) return;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.8;
    utterance.pitch = 1.3;
    utterance.volume = 0.9;
    
    // Get all available voices
    const voices = voiceSynthesis.getVoices();
    
    // Comprehensive list of female voice names across different systems
    const femaleVoiceNames = [
        'Samantha', 'Karen', 'Victoria', 'Susan', 'Alex', 'Fiona',
        'Female', 'Woman', 'Girl', 'Samantha (Enhanced)', 'Karen (Enhanced)',
        'Microsoft Zira Desktop', 'Microsoft Hazel Desktop', 'Microsoft Susan Desktop',
        'Google UK English Female', 'Google US English Female', 'Google Australian English Female',
        'Google Canadian English Female', 'Google Indian English Female',
        'Microsoft Zira - English (United States)', 'Microsoft Hazel - English (Great Britain)',
        'Microsoft Susan - English (Australia)', 'Microsoft Catherine - English (Canada)',
        'Microsoft Linda - English (United States)', 'Microsoft Ravi - English (India)',
        'Samantha (Premium)', 'Karen (Premium)', 'Victoria (Premium)',
        'Female Voice', 'Woman Voice', 'Girl Voice'
    ];
    
    // Find the best female voice
    let femaleVoice = voices.find(voice => 
        femaleVoiceNames.some(name => 
            voice.name.toLowerCase().includes(name.toLowerCase())
        )
    );
    
    // If no specific female voice found, try to find any voice that sounds female
    if (!femaleVoice) {
        femaleVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') ||
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('girl') ||
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('karen') ||
            voice.name.toLowerCase().includes('victoria') ||
            voice.name.toLowerCase().includes('susan') ||
            voice.name.toLowerCase().includes('fiona') ||
            voice.name.toLowerCase().includes('alex') ||
            voice.name.toLowerCase().includes('zira') ||
            voice.name.toLowerCase().includes('hazel')
        );
    }
    
    // If still no female voice, use a higher pitch to simulate female voice
    if (femaleVoice) {
        utterance.voice = femaleVoice;
        utterance.pitch = 1.2; // Slightly lower pitch for natural female voice
    } else {
        utterance.pitch = 1.4; // Higher pitch to simulate female voice
        utterance.rate = 0.85; // Slightly slower for more feminine sound
    }
    
    // Add some personality to the voice
    utterance.volume = 0.9;
    
    voiceSynthesis.speak(utterance);
}

// Update voice feedback display
function updateVoiceFeedback(text) {
    const feedbackElement = document.getElementById('feedbackText');
    if (feedbackElement) {
        feedbackElement.textContent = text;
    }
    speakFeedback(text);
}

function selectExercise(exerciseType) {
    currentExerciseType = exerciseType;
    const exerciseNames = {
        'left': 'Left Arm Curl',
        'right': 'Right Arm Curl',
        'pushup': 'Push-ups',
        'squat': 'Squats'
    };
    
    // Show demo video first
    showDemoVideo(exerciseType, exerciseNames[exerciseType]);
}

function showDemoVideo(exerciseType, exerciseName) {
    const demoModal = document.getElementById('demo-video-modal');
    const demoTitle = document.getElementById('demo-title');
    const demoVideo = document.getElementById('demo-video');
    
    demoTitle.textContent = `${exerciseName} Demo`;
    
    // Set video source based on exercise type
    const videoSources = {
        'left': '../videos/left curl.mp4',
        'right': '../videos/right curl.mp4',
        'pushup': '../videos/pushup.mp4',
        'squat': '../videos/squat.mp4'
    };
    
    demoVideo.src = videoSources[exerciseType];
    demoModal.classList.remove('hidden');
    
    // Speak welcome message
    updateVoiceFeedback(`Welcome to ${exerciseName}! Watch the demo to learn proper form.`);
}

function closeDemoVideo() {
    const demoModal = document.getElementById('demo-video-modal');
    const demoVideo = document.getElementById('demo-video');
    
    demoModal.classList.add('hidden');
    demoVideo.pause();
    demoVideo.currentTime = 0;
}

function startExerciseAfterDemo() {
    closeDemoVideo();
    startActualExercise();
}

function skipDemo() {
    closeDemoVideo();
    startActualExercise();
}

function startActualExercise() {
    const exerciseNames = {
        'left': 'Left Arm Curl',
        'right': 'Right Arm Curl',
        'pushup': 'Push-ups',
        'squat': 'Squats'
    };
    
    document.getElementById('exerciseTitle').textContent = exerciseNames[currentExerciseType];
    
    const videoStream = document.getElementById('videoStream');
    videoStream.src = `http://127.0.0.1:5000/video_feed_${currentExerciseType}`;
    
    document.getElementById('videoContainer').classList.remove('hidden');
    
    resetWorkout();
    initializeFormFeedback(currentExerciseType);
    
    updateVoiceFeedback(`Great! Now let's start your ${exerciseNames[currentExerciseType]} workout. Get in position and click start when ready!`);
    
    ToastNotification.show('info', 'Exercise Selected', `Starting ${exerciseNames[currentExerciseType]}. Get ready for your workout!`);
}

function closeVideo() {
    const videoStream = document.getElementById('videoStream');
    videoStream.src = '';
    
    document.getElementById('videoContainer').classList.add('hidden');
    
    resetWorkout();
}

async function startWorkout() {
    try {
        const supabaseClient = getSupabaseClient();
        if (!supabaseClient) {
            ToastNotification.show('error', 'Connection Error', 'Unable to start workout. Please try again.');
            return;
        }
        const { data: session, error } = await supabaseClient
            .from('workout_sessions')
            .insert([
                {
                    user_id: aiCoach.currentUser.id,
                    exercise_type: getCurrentExerciseType(),
                    start_time: new Date().toISOString(),
                    total_reps: 0,
                    total_calories: 0,
                    form_score: 0,
                    duration_minutes: 0
                }
            ])
            .select()
            .single();
        
        if (error) {
            ToastNotification.show('error', 'Workout Error', 'Unable to start workout session. Please try again.');
            return;
        }
        
        aiCoach.currentWorkoutSession = session;
        
        startRealTimePoseAnalysis();
        
        let reps = 0;
        let calories = 0;
        let progress = 0;
        const startTime = Date.now();
        
        // Voice feedback for workout start
        updateVoiceFeedback("Workout started! Let's do this! Remember to maintain proper form.");
        
        const workoutInterval = setInterval(async () => {
            const poseData = await getRealTimePoseData();
            
            if (poseData && poseData.rep_detected) {
                reps++;
                calories += calculateCalories(poseData.form_score);
                progress = Math.min((reps / 12) * 100, 100);
                
                document.getElementById('repCount').textContent = reps;
                document.getElementById('calorieCount').textContent = calories;
                
                document.getElementById('formScore').textContent = `${Math.round(poseData.form_score)}%`;
                
                // Voice feedback for reps
                if (reps % 3 === 0) {
                    updateVoiceFeedback(`Great job! You've completed ${reps} reps. Keep going!`);
                }
                
                // Voice feedback for form
                if (poseData.form_score < 70) {
                    updateVoiceFeedback("Focus on your form. Keep your back straight and control the movement.");
                } else if (poseData.form_score > 90) {
                    updateVoiceFeedback("Excellent form! You're doing great!");
                }
                
                await storePoseAnalysis(session.id, poseData);
                
                if (reps >= 12) {
                    clearInterval(workoutInterval);
                    await completeWorkout(session.id, reps, calories, startTime);
                    updateVoiceFeedback(`Amazing work! You completed ${reps} reps and burned ${calories} calories. Great job!`);
                    ToastNotification.show('success', 'Workout Complete!', `Great job! You completed ${reps} reps and burned ${calories} calories.`);
                }
            }
        }, 1000);
        
        window.currentWorkoutInterval = workoutInterval;
        
        ToastNotification.show('success', 'Workout Started', 'Your AI-powered workout session has begun! Keep up the great form.');
        
    } catch (error) {
        ToastNotification.show('error', 'Workout Error', 'Something went wrong. Please try again.');
    }
}

function stopWorkout() {
    if (window.currentWorkoutInterval) {
        clearInterval(window.currentWorkoutInterval);
        window.currentWorkoutInterval = null;
    }
    
    if (window.poseAnalysisInterval) {
        clearInterval(window.poseAnalysisInterval);
        window.poseAnalysisInterval = null;
    }
    
    updateVoiceFeedback("Workout paused. Take a break and click start when you're ready to continue.");
    ToastNotification.show('info', 'Workout Paused', 'Your workout has been paused. Click Start to resume.');
}

function resetWorkout() {
    document.getElementById('repCount').textContent = '0';
    document.getElementById('calorieCount').textContent = '0';
    document.getElementById('formScore').textContent = '85%';
    
    if (window.currentWorkoutInterval) {
        clearInterval(window.currentWorkoutInterval);
        window.currentWorkoutInterval = null;
    }
    
    if (window.poseAnalysisInterval) {
        clearInterval(window.poseAnalysisInterval);
        window.poseAnalysisInterval = null;
    }
    
    updateVoiceFeedback("Workout reset. Ready for a fresh start!");
    ToastNotification.show('info', 'Workout Reset', 'Workout stats have been reset. Ready for a fresh start!');
}

// Form Feedback Functions
function initializeFormFeedback(exerciseType) {
    const tips = getExerciseTips(exerciseType);
    updateFormTips(tips);
    startFormAnalysis(exerciseType);
}

function getExerciseTips(exerciseType) {
    const tips = {
        'left': [
            'Keep your back straight throughout the movement',
            'Control the descent for better muscle engagement',
            'Breathe steadily during the exercise',
            'Keep your elbow close to your body'
        ],
        'right': [
            'Maintain proper shoulder alignment',
            'Focus on controlled movement',
            'Avoid swinging the weight',
            'Keep your core engaged'
        ],
        'pushup': [
            'Maintain a straight line from head to heels',
            'Lower your body as a single unit',
            'Keep your core tight throughout',
            'Breathe steadily during the movement'
        ],
        'squat': [
            'Keep your knees in line with your toes',
            'Lower until thighs are parallel to ground',
            'Keep your chest up and back straight',
            'Push through your heels when rising'
        ]
    };
    
    return tips[exerciseType] || tips['left'];
}

function updateFormTips(tips) {
    const tipsList = document.getElementById('formTips');
    tipsList.innerHTML = '';
    
    tips.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        tipsList.appendChild(li);
    });
}

function startFormAnalysis(exerciseType) {
    // Real-time form analysis will come from MediaPipe backend
    // This function is called when exercise starts
}

function updateFeedbackItems(score, exerciseType) {
    const feedbackItems = document.querySelectorAll('.feedback-item');
    
    feedbackItems.forEach((item, index) => {
        const icon = item.querySelector('.feedback-icon');
        const status = item.querySelector('.feedback-status');
        
        if (index === 0) {
            if (score > 85) {
                icon.className = 'feedback-icon good';
                icon.innerHTML = '<i class="fas fa-check"></i>';
                status.textContent = 'Good form';
            } else if (score > 70) {
                icon.className = 'feedback-icon warning';
                icon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
                status.textContent = 'Minor adjustment needed';
            } else {
                icon.className = 'feedback-icon bad';
                icon.innerHTML = '<i class="fas fa-times"></i>';
                status.textContent = 'Needs correction';
            }
        } else if (index === 1) {
            if (score > 80) {
                icon.className = 'feedback-icon good';
                icon.innerHTML = '<i class="fas fa-check"></i>';
                status.textContent = 'Proper alignment';
            } else {
                icon.className = 'feedback-icon warning';
                icon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
                status.textContent = 'Keep straight';
            }
        } else if (index === 2) {
            if (score > 90) {
                icon.className = 'feedback-icon good';
                icon.innerHTML = '<i class="fas fa-check"></i>';
                status.textContent = 'Perfect range';
            } else if (score > 75) {
                icon.className = 'feedback-icon warning';
                icon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
                status.textContent = 'Extend further';
            } else {
                icon.className = 'feedback-icon bad';
                icon.innerHTML = '<i class="fas fa-times"></i>';
                status.textContent = 'Limited range';
            }
        }
    });
}

// Helper functions for real-time workout tracking
function getCurrentExerciseType() {
    if (currentExerciseType) {
        const typeMap = {
            'left': 'left_arm_curl',
            'right': 'right_arm_curl',
            'pushup': 'pushup',
            'squat': 'squat'
        };
        return typeMap[currentExerciseType] || 'unknown';
    }
    
    const exerciseTitle = document.getElementById('exerciseTitle').textContent;
    if (exerciseTitle.includes('Left')) return 'left_arm_curl';
    if (exerciseTitle.includes('Right')) return 'right_arm_curl';
    if (exerciseTitle.includes('Push-up')) return 'pushup';
    if (exerciseTitle.includes('Squat')) return 'squat';
    return 'unknown';
}

async function getRealTimePoseData() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/pose_analysis/${getCurrentExerciseType()}`);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        return null;
    }
}

async function storePoseAnalysis(sessionId, poseData) {
    try {
        const supabaseClient = getSupabaseClient();
        if (!supabaseClient) {
            return;
        }
        await supabaseClient
            .from('pose_analysis')
            .insert([
                {
                    session_id: sessionId,
                    timestamp: new Date().toISOString(),
                    form_score: poseData.form_score,
                    arm_position_score: poseData.arm_position_score,
                    back_alignment_score: poseData.back_alignment_score,
                    range_of_motion_score: poseData.range_of_motion_score,
                    feedback_data: {
                        arm_position: poseData.arm_position_score > 80 ? 'good' : 'needs_improvement',
                        back_alignment: poseData.back_alignment_score > 80 ? 'good' : 'needs_improvement',
                        range_of_motion: poseData.range_of_motion_score > 80 ? 'good' : 'needs_improvement'
                    },
                    pose_landmarks: poseData.landmarks || {}
                }
            ]);
    } catch (error) {
        // Silent fail
    }
}

async function completeWorkout(sessionId, reps, calories, startTime) {
    try {
        const duration = Math.round((Date.now() - startTime) / 60000);
        
        const supabaseClient = getSupabaseClient();
        if (!supabaseClient) {
            return;
        }
        
        await supabaseClient
            .from('workout_sessions')
            .update({
                end_time: new Date().toISOString(),
                total_reps: reps,
                total_calories: calories,
                duration_minutes: duration,
                form_score: calculateAverageFormScore(sessionId)
            })
            .eq('id', sessionId);
        
    } catch (error) {
        // Silent fail
    }
}

async function calculateAverageFormScore(sessionId) {
    try {
        const supabaseClient = getSupabaseClient();
        if (!supabaseClient) {
            return 0;
        }
        const { data, error } = await supabaseClient
            .from('pose_analysis')
            .select('form_score')
            .eq('session_id', sessionId);
        
        if (error || !data.length) return 0;
        
        const totalScore = data.reduce((sum, record) => sum + record.form_score, 0);
        return Math.round(totalScore / data.length);
    } catch (error) {
        return 0;
    }
}

function calculateCalories(formScore) {
    const baseCalories = 2;
    const formMultiplier = formScore / 100;
    return Math.round(baseCalories * formMultiplier);
}

function startRealTimePoseAnalysis() {
    // Start real-time pose analysis from MediaPipe backend
    const poseAnalysisInterval = setInterval(async () => {
        try {
            const poseData = await getRealTimePoseData();
            if (poseData) {
                // Update form score in real-time
                document.getElementById('formScore').textContent = `${Math.round(poseData.form_score)}%`;
                
                // Update feedback items based on real pose data
                updateFeedbackItems(poseData.form_score, getCurrentExerciseType());
                
                // Update form tips based on real-time analysis
                updateFormTipsBasedOnPose(poseData);
            }
        } catch (error) {
            // Silent error handling
        }
    }, 500); // Update every 500ms for real-time feedback
    
    window.poseAnalysisInterval = poseAnalysisInterval;
}

function updateFormTipsBasedOnPose(poseData) {
    const tipsList = document.getElementById('formTips');
    if (!tipsList) return;
    
    let tips = [];
    
    // Generate tips based on actual pose analysis
    if (poseData.arm_position_score < 80) {
        tips.push('Focus on proper arm positioning');
    }
    if (poseData.back_alignment_score < 80) {
        tips.push('Keep your back straight and aligned');
    }
    if (poseData.range_of_motion_score < 80) {
        tips.push('Extend your range of motion further');
    }
    
    // Add general tips if no specific issues
    if (tips.length === 0) {
        tips = getExerciseTips(getCurrentExerciseType());
    }
    
    updateFormTips(tips);
}

// Profile Section Functions
function toggleEditMode(section) {
    const infoElement = document.getElementById(`${section}Info`);
    const formElement = document.getElementById(`${section}Form`);
    
    if (infoElement && formElement) {
        infoElement.classList.toggle('hidden');
        formElement.classList.toggle('hidden');
    }
}

// Handle personal information form submission
document.addEventListener('DOMContentLoaded', () => {
    const updatePersonalForm = document.getElementById('updatePersonalForm');
    if (updatePersonalForm) {
        updatePersonalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            if (aiCoach) {
                const success = await aiCoach.updatePersonalInfo(formData);
                if (success) {
                    toggleEditMode('personal');
                    ToastNotification.show('success', 'Profile Updated', 'Your personal information has been updated successfully!');
                    updateVoiceFeedback("Profile updated successfully!");
                } else {
                    ToastNotification.show('error', 'Update Failed', 'Failed to update profile. Please try again.');
                }
            }
        });
    }
    
    // Handle preferences form submission
    const updatePreferencesForm = document.getElementById('updatePreferencesForm');
    if (updatePreferencesForm) {
        updatePreferencesForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            // Update preferences (you can extend this to save to database)
            const voiceFeedback = formData.get('voice_feedback');
            const workoutReminders = formData.get('workout_reminders');
            const fitnessGoal = formData.get('fitness_goal');
            
            // Update display
            document.getElementById('displayVoiceFeedback').textContent = voiceFeedback === 'enabled' ? 'Enabled' : 'Disabled';
            document.getElementById('displayReminders').textContent = workoutReminders === 'enabled' ? 'Enabled' : 'Disabled';
            document.getElementById('displayGoal').textContent = fitnessGoal || 'Not Set';
            
            toggleEditMode('preferences');
            ToastNotification.show('success', 'Preferences Updated', 'Your preferences have been updated successfully!');
            updateVoiceFeedback("Preferences updated successfully!");
        });
    }
});

function confirmDeleteAccount() {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        if (confirm('This will permanently delete all your data. Are you absolutely sure?')) {
            deleteAccount();
        }
    }
}

async function deleteAccount() {
    try {
        const supabaseClient = getSupabaseClient();
        if (!supabaseClient) {
            ToastNotification.show('error', 'Error', 'Unable to connect to server.');
            return;
        }
        
        // Delete user data from database
        await supabaseClient
            .from('workout_sessions')
            .delete()
            .eq('user_id', aiCoach.currentUser.id);
        
        await supabaseClient
            .from('pose_analysis')
            .delete()
            .eq('user_id', aiCoach.currentUser.id);
        
        await supabaseClient
            .from('users')
            .delete()
            .eq('id', aiCoach.currentUser.id);
        
        // Sign out and redirect
        await supabaseClient.auth.signOut();
        
        ToastNotification.show('info', 'Account Deleted', 'Your account has been permanently deleted.');
        updateVoiceFeedback("Account deleted. Thank you for using our service.");
        
        // Redirect to landing page
        setTimeout(() => {
            window.location.reload();
        }, 2000);
        
    } catch (error) {
        console.error('Error deleting account:', error);
        ToastNotification.show('error', 'Error', 'Failed to delete account. Please try again.');
    }
}

function exportData() {
    if (!aiCoach || !aiCoach.currentUser) {
        ToastNotification.show('error', 'Error', 'No user data available to export.');
        return;
    }
    
    try {
        const userData = {
            user: aiCoach.currentUser,
            exportDate: new Date().toISOString(),
            appVersion: '1.0.0'
        };
        
        const dataStr = JSON.stringify(userData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `gymjam-data-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        ToastNotification.show('success', 'Data Exported', 'Your data has been exported successfully!');
        updateVoiceFeedback("Data exported successfully!");
        
    } catch (error) {
        console.error('Error exporting data:', error);
        ToastNotification.show('error', 'Export Failed', 'Failed to export data. Please try again.');
    }
}
