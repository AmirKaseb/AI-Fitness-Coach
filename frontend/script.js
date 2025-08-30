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
function selectExercise(exerciseType) {
    const exerciseNames = {
        'left': 'Left Arm Curl',
        'right': 'Right Arm Curl',
        'pushup': 'Push-ups',
        'squat': 'Squats'
    };
    
    document.getElementById('exerciseTitle').textContent = exerciseNames[exerciseType];
    
    const videoStream = document.getElementById('videoStream');
    videoStream.src = `http://127.0.0.1:5000/video_feed_${exerciseType}`;
    
    document.getElementById('videoContainer').classList.remove('hidden');
    
    resetWorkout();
    initializeFormFeedback(exerciseType);
    
    ToastNotification.show('info', 'Exercise Selected', `Starting ${exerciseNames[exerciseType]}. Get ready for your workout!`);
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
        
        const workoutInterval = setInterval(async () => {
            const poseData = await getRealTimePoseData();
            
            if (poseData && poseData.rep_detected) {
                reps++;
                calories += calculateCalories(poseData.form_score);
                progress = Math.min((reps / 12) * 100, 100);
                
                document.getElementById('repCount').textContent = reps;
                document.getElementById('calorieCount').textContent = calories;
                document.getElementById('progressValue').textContent = `${Math.round(progress)}%`;
                
                document.getElementById('formScore').textContent = `${Math.round(poseData.form_score)}%`;
                
                await storePoseAnalysis(session.id, poseData);
                
                if (reps >= 12) {
                    clearInterval(workoutInterval);
                    await completeWorkout(session.id, reps, calories, startTime);
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
    
    ToastNotification.show('info', 'Workout Paused', 'Your workout has been paused. Click Start to resume.');
}

function resetWorkout() {
    document.getElementById('repCount').textContent = '0';
    document.getElementById('calorieCount').textContent = '0';
    document.getElementById('progressValue').textContent = '0%';
    
    if (window.currentWorkoutInterval) {
        clearInterval(window.currentWorkoutInterval);
        window.currentWorkoutInterval = null;
    }
    
    if (window.poseAnalysisInterval) {
        clearInterval(window.poseAnalysisInterval);
        window.poseAnalysisInterval = null;
    }
    
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
