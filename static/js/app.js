/**
 * FairPayCheck - Main Application JavaScript
 * Handles form wizard, API calls, results display, dark mode, and skill suggestions
 */
(function () {
    'use strict';

    // Configuration
    const API_ENDPOINT = '/api/calculate/';
    const LOADING_DELAY = 5000;
    const CURRENCIES = window.COUNTRY_CURRENCIES || {
        'USA': { symbol: '$', code: 'USD' },
        'UK': { symbol: '£', code: 'GBP' },
        'Germany': { symbol: '€', code: 'EUR' },
        'Canada': { symbol: 'C$', code: 'CAD' },
        'Australia': { symbol: 'A$', code: 'AUD' },
        'India': { symbol: '₹', code: 'INR' }
    };
    const ROLE_SKILL_SUGGESTIONS = window.ROLE_SKILL_SUGGESTIONS || {};
    const ROLE_KEYWORDS = window.ROLE_KEYWORDS || {};

    const VERDICT_CLASSES = {
        'likely_underpaid': 'underpaid',
        'possibly_underpaid': 'possibly-underpaid',
        'fairly_paid': 'fairly-paid',
        'fairly_overpaid': 'fairly-paid'
    };

    const VERDICT_COLORS = {
        'likely_underpaid': '#E53E3E',
        'possibly_underpaid': '#D69E2E',
        'fairly_paid': '#38A169',
        'fairly_overpaid': '#38A169'
    };


    const JOB_SUGGESTIONS = [
        // Technology & Engineering
        'Software Engineer', 'Senior Software Engineer', 'Staff Software Engineer', 'Principal Engineer',
        'Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'DevOps Engineer',
        'Site Reliability Engineer', 'Cloud Engineer', 'Platform Engineer', 'Data Engineer',
        'Data Scientist', 'Data Analyst', 'Machine Learning Engineer', 'AI Engineer',
        'QA Engineer', 'Test Engineer', 'Security Engineer', 'Network Engineer',
        'Systems Administrator', 'Database Administrator', 'IT Manager', 'IT Support Specialist',
        'Technical Lead', 'Engineering Manager', 'Solutions Architect', 'Enterprise Architect',
        'CTO', 'VP of Engineering', 'Director of Engineering',

        // Product & Design
        'Product Manager', 'Senior Product Manager', 'Product Owner', 'Program Manager',
        'Project Manager', 'Scrum Master', 'Agile Coach', 'Technical Product Manager',
        'UX Designer', 'UI Designer', 'Product Designer', 'Visual Designer',
        'Graphic Designer', 'Motion Designer', 'Creative Director', 'Art Director',
        'UX Researcher', 'Content Designer', 'Brand Designer',
        'Head of Product', 'Head of Design', 'VP of Product',

        // Marketing & Communications
        'Marketing Manager', 'Digital Marketing Manager', 'Marketing Director',
        'Growth Manager', 'Growth Hacker', 'Content Manager', 'Content Strategist',
        'SEO Specialist', 'SEM Specialist', 'Social Media Manager', 'Community Manager',
        'Brand Manager', 'PR Manager', 'Communications Manager', 'Copywriter',
        'Email Marketing Specialist', 'Marketing Analyst', 'CMO',

        // Sales & Business Development
        'Sales Manager', 'Sales Director', 'VP of Sales', 'Account Executive',
        'Business Development Manager', 'Business Development Representative',
        'Account Manager', 'Key Account Manager', 'Customer Success Manager',
        'Sales Engineer', 'Inside Sales Representative', 'Outside Sales Representative',
        'Regional Sales Manager', 'Territory Manager', 'Sales Operations Manager',

        // Finance & Accounting
        'Financial Analyst', 'Senior Financial Analyst', 'Finance Manager',
        'Accountant', 'Senior Accountant', 'Staff Accountant', 'Tax Accountant',
        'Controller', 'Assistant Controller', 'FP&A Manager', 'FP&A Analyst',
        'CFO', 'Treasurer', 'Auditor', 'Internal Auditor',
        'Bookkeeper', 'Accounts Payable Specialist', 'Accounts Receivable Specialist',
        'Payroll Specialist', 'Credit Analyst', 'Investment Analyst',

        // Human Resources
        'HR Manager', 'HR Director', 'VP of HR', 'CHRO',
        'Recruiter', 'Senior Recruiter', 'Technical Recruiter', 'Talent Acquisition Manager',
        'HR Generalist', 'HR Business Partner', 'People Operations Manager',
        'Compensation Analyst', 'Benefits Administrator', 'Training Manager',
        'Learning & Development Specialist', 'Employee Relations Manager',

        // Operations & Administration
        'Operations Manager', 'Director of Operations', 'COO', 'VP of Operations',
        'Supply Chain Manager', 'Logistics Manager', 'Warehouse Manager',
        'Procurement Manager', 'Purchasing Manager', 'Inventory Manager',
        'Office Manager', 'Executive Assistant', 'Administrative Assistant',
        'Facilities Manager', 'Business Analyst', 'Operations Analyst',

        // Healthcare & Medical
        'Registered Nurse', 'Nurse Practitioner', 'Licensed Practical Nurse',
        'Physician', 'Surgeon', 'Anesthesiologist', 'Radiologist',
        'Medical Assistant', 'Pharmacy Technician', 'Pharmacist',
        'Physical Therapist', 'Occupational Therapist', 'Speech Therapist',
        'Medical Lab Technician', 'Phlebotomist', 'EMT', 'Paramedic',
        'Healthcare Administrator', 'Medical Coder', 'Medical Biller',
        'Dentist', 'Dental Hygienist', 'Dental Assistant',
        'Psychologist', 'Psychiatrist', 'Counselor', 'Social Worker',

        // Legal
        'Attorney', 'Lawyer', 'Associate Attorney', 'Partner',
        'Paralegal', 'Legal Assistant', 'Legal Secretary',
        'Corporate Counsel', 'General Counsel', 'Contract Attorney',
        'Litigation Attorney', 'Real Estate Attorney', 'Immigration Attorney',
        'Compliance Officer', 'Compliance Manager', 'Legal Analyst',

        // Education
        'Teacher', 'Elementary School Teacher', 'High School Teacher', 'Middle School Teacher',
        'Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer',
        'Principal', 'Vice Principal', 'School Administrator',
        'Academic Advisor', 'School Counselor', 'Special Education Teacher',
        'Curriculum Developer', 'Instructional Designer', 'Training Coordinator',
        'Tutor', 'Teaching Assistant', 'Education Administrator',

        // Creative & Media
        'Photographer', 'Videographer', 'Video Editor', 'Film Director',
        'Animator', 'Illustrator', '3D Artist', 'Game Designer',
        'Journalist', 'Reporter', 'Editor', 'Managing Editor',
        'Producer', 'Music Producer', 'Audio Engineer', 'Sound Designer',
        'Writer', 'Technical Writer', 'Author', 'Blogger',

        // Construction & Trades
        'Construction Manager', 'Project Superintendent', 'Site Manager',
        'Civil Engineer', 'Structural Engineer', 'Mechanical Engineer',
        'Electrical Engineer', 'Architect', 'Landscape Architect',
        'Carpenter', 'Electrician', 'Plumber', 'HVAC Technician',
        'Welder', 'Machinist', 'Construction Worker', 'Foreman',

        // Hospitality & Service
        'Hotel Manager', 'Restaurant Manager', 'General Manager',
        'Chef', 'Executive Chef', 'Sous Chef', 'Line Cook',
        'Server', 'Bartender', 'Barista', 'Host/Hostess',
        'Event Planner', 'Event Coordinator', 'Catering Manager',
        'Front Desk Agent', 'Concierge', 'Housekeeping Manager',

        // Retail & Customer Service
        'Store Manager', 'Assistant Store Manager', 'Retail Manager',
        'Sales Associate', 'Cashier', 'Customer Service Representative',
        'Call Center Agent', 'Customer Support Specialist', 'Help Desk Technician',
        'Visual Merchandiser', 'Buyer', 'Merchandise Planner',

        // Manufacturing & Logistics
        'Manufacturing Engineer', 'Production Manager', 'Plant Manager',
        'Quality Assurance Manager', 'Quality Control Inspector',
        'Industrial Engineer', 'Process Engineer', 'Safety Manager',
        'Maintenance Technician', 'Machine Operator', 'Assembly Line Worker',
        'Shipping Coordinator', 'Receiving Clerk', 'Delivery Driver', 'Truck Driver',

        // Real Estate
        'Real Estate Agent', 'Real Estate Broker', 'Property Manager',
        'Leasing Agent', 'Real Estate Analyst', 'Mortgage Loan Officer',
        'Appraiser', 'Home Inspector', 'Real Estate Developer',

        // Science & Research
        'Research Scientist', 'Lab Technician', 'Research Assistant',
        'Chemist', 'Biologist', 'Physicist', 'Environmental Scientist',
        'Clinical Research Associate', 'Biostatistician', 'Epidemiologist'
    ];

    // Simple Analytics placeholder
    const Analytics = {
        track(event, data = {}) {
            console.debug('Analytics:', event, data);
        }
    };

    // DOM Elements
    const elements = {
        form: document.getElementById('fairpay-form'),
        formSection: document.querySelector('.form-section'),
        resultsSection: document.getElementById('results'),
        loadingOverlay: document.getElementById('loading'),
        loadingText: document.getElementById('loading-text'),
        heroSection: document.getElementById('hero'),
        howItWorks: document.getElementById('how-it-works'),
        progressSteps: document.querySelectorAll('.progress-step'),
        formSteps: document.querySelectorAll('.form-step'),
        nextButtons: document.querySelectorAll('.btn-next'),
        backButtons: document.querySelectorAll('.btn-back'),
        submitButton: document.querySelector('.btn-submit'),
        startOverButton: document.getElementById('btn-start-over'),
        experienceSlider: document.getElementById('years_experience'),
        experienceDisplay: document.getElementById('experience-display'),
        countrySelect: document.getElementById('country'),
        currencySymbol: document.getElementById('currency-symbol'),
        bonusPrefix: document.querySelector('.bonus-prefix'),
        jobTitleInput: document.getElementById('job_title'),
        jobSuggestions: document.getElementById('job-suggestions'),
        skillsInput: document.getElementById('skills'),
        skillSuggestions: document.getElementById('skill-suggestions'),
        skillChips: document.getElementById('skill-chips'),
        themeToggle: document.getElementById('theme-toggle'),
        resultScore: document.getElementById('result-score'),
        resultVerdict: document.getElementById('result-verdict'),
        resultConfidence: document.getElementById('result-confidence'),
        resultSalaryMin: document.getElementById('result-salary-min'),
        resultSalaryMax: document.getElementById('result-salary-max'),
        resultReasons: document.getElementById('result-reasons'),
        resultDataUpdated: document.getElementById('result-data-updated'),
        resultDisclaimer: document.getElementById('result-disclaimer'),
        scoreRingProgress: document.querySelector('.score-ring-progress')
    };

    // State
    let currentStep = 1;
    let formData = {};
    let selectedSuggestionIndex = -1;
    let detectedRole = 'default';

    // ==========================================
    // Utility Functions
    // ==========================================
    function showElement(el) {
        if (el) el.classList.remove('hidden');
    }

    function hideElement(el) {
        if (el) el.classList.add('hidden');
    }

    function scrollToElement(el) {
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ==========================================
    // Dark Mode
    // ==========================================
    function initTheme() {
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else if (prefersDark) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        Analytics.track('theme_toggle', { theme: newTheme });
    }

    // ==========================================
    // Role Detection & Skill Suggestions
    // ==========================================
    function detectRoleFromTitle(title) {
        if (!title) return 'default';
        const lowerTitle = title.toLowerCase();

        for (const [role, keywords] of Object.entries(ROLE_KEYWORDS)) {
            for (const keyword of keywords) {
                if (lowerTitle.includes(keyword.toLowerCase())) {
                    return role;
                }
            }
        }
        return 'default';
    }

    function updateSkillSuggestions(role) {
        if (!elements.skillChips || !elements.skillSuggestions) return;

        const skills = ROLE_SKILL_SUGGESTIONS[role] || ROLE_SKILL_SUGGESTIONS['default'] || [];

        if (skills.length === 0) {
            hideElement(elements.skillSuggestions);
            return;
        }

        // Get currently entered skills
        const currentSkills = (elements.skillsInput.value || '')
            .split(',')
            .map(s => s.trim().toLowerCase())
            .filter(s => s);

        // Generate chips
        elements.skillChips.innerHTML = skills.slice(0, 12).map(skill => {
            const isSelected = currentSkills.includes(skill.toLowerCase());
            return `<span class="skill-chip${isSelected ? ' selected' : ''}" data-skill="${escapeHtml(skill)}">${escapeHtml(skill)}</span>`;
        }).join('');

        showElement(elements.skillSuggestions);
    }

    function addSkillFromChip(skill) {
        if (!elements.skillsInput) return;

        const currentValue = elements.skillsInput.value.trim();
        const currentSkills = currentValue
            .split(',')
            .map(s => s.trim())
            .filter(s => s);

        // Check if skill already exists
        if (currentSkills.some(s => s.toLowerCase() === skill.toLowerCase())) {
            // Remove it
            const newSkills = currentSkills.filter(s => s.toLowerCase() !== skill.toLowerCase());
            elements.skillsInput.value = newSkills.join(', ');
        } else {
            // Add it
            if (currentValue) {
                elements.skillsInput.value = currentValue + ', ' + skill;
            } else {
                elements.skillsInput.value = skill;
            }
        }

        // Update chip selection state
        updateSkillSuggestions(detectedRole);
    }

    // ==========================================
    // Form Handling
    // ==========================================
    function getFormData() {
        const data = {};
        const formElements = elements.form.elements;

        for (let i = 0; i < formElements.length; i++) {
            const el = formElements[i];
            if (el.name && el.name !== '') {
                if (el.type === 'radio') {
                    if (el.checked) {
                        data[el.name] = el.value === 'true' ? true : el.value === 'false' ? false : el.value;
                    }
                } else if (el.type === 'number') {
                    data[el.name] = el.value ? parseFloat(el.value) : null;
                } else {
                    data[el.name] = el.value;
                }
            }
        }
        return data;
    }

    function validateStep(step) {
        const stepElement = document.querySelector(`.form-step[data-step="${step}"]`);
        const requiredFields = stepElement.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value || field.value.trim() === '') {
                isValid = false;
                field.classList.add('error');
                field.addEventListener('input', function handler() {
                    field.classList.remove('error');
                    field.removeEventListener('input', handler);
                }, { once: true });
            } else {
                field.classList.remove('error');
            }
        });

        return isValid;
    }

    function goToStep(step) {
        if (step < 1 || step > 3) return;
        if (step > currentStep && !validateStep(currentStep)) return;

        elements.formSteps.forEach(s => {
            s.classList.remove('active');
            if (parseInt(s.dataset.step) === step) s.classList.add('active');
        });

        elements.progressSteps.forEach(p => {
            const pStep = parseInt(p.dataset.step);
            p.classList.remove('active', 'completed');
            if (pStep === step) p.classList.add('active');
            else if (pStep < step) p.classList.add('completed');
        });

        currentStep = step;

        // Update skill suggestions when entering step 2
        if (step === 2 && elements.jobTitleInput) {
            detectedRole = detectRoleFromTitle(elements.jobTitleInput.value);
            updateSkillSuggestions(detectedRole);
        }

        if (step > 1) Analytics.track(`form_step_${step}`);
        scrollToElement(elements.formSection);
    }

    function updateCurrency() {
        const country = elements.countrySelect.value;
        const currency = CURRENCIES[country] || CURRENCIES['USA'];
        if (elements.currencySymbol) elements.currencySymbol.textContent = currency.symbol;
        if (elements.bonusPrefix) elements.bonusPrefix.textContent = currency.symbol;
    }

    function updateExperienceDisplay() {
        if (elements.experienceSlider && elements.experienceDisplay) {
            elements.experienceDisplay.textContent = elements.experienceSlider.value;
        }
    }

    // ==========================================
    // Loading Animation
    // ==========================================
    const loadingMessages = [
        'Analyzing market data...',
        'Comparing salary benchmarks...',
        'Evaluating skill premiums...',
        'Calculating experience factors...',
        'Finalizing your assessment...'
    ];
    let loadingInterval = null;

    function startLoadingAnimation() {
        let msgIndex = 0;
        if (elements.loadingText) {
            elements.loadingText.textContent = loadingMessages[0];
            loadingInterval = setInterval(() => {
                msgIndex = (msgIndex + 1) % loadingMessages.length;
                elements.loadingText.textContent = loadingMessages[msgIndex];
            }, 1000);
        }

        // Reset and restart progress bar animation
        const progressBar = document.querySelector('.loading-bar');
        if (progressBar) {
            progressBar.style.animation = 'none';
            progressBar.offsetHeight; // Trigger reflow
            progressBar.style.animation = 'loadingProgress 5s ease-out forwards';
        }
    }

    function stopLoadingAnimation() {
        if (loadingInterval) {
            clearInterval(loadingInterval);
            loadingInterval = null;
        }
    }

    // ==========================================
    // API Submission
    // ==========================================
    async function submitForm() {
        formData = getFormData();
        showElement(elements.loadingOverlay);
        startLoadingAnimation();

        Analytics.track('form_submit', {
            country: formData.country,
            has_salary: !!formData.salary
        });

        try {
            const fetchPromise = fetch(API_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const delayPromise = new Promise(resolve => setTimeout(resolve, LOADING_DELAY));
            const [response] = await Promise.all([fetchPromise, delayPromise]);
            const result = await response.json();

            if (!response.ok) throw new Error(result.error || 'An error occurred');

            stopLoadingAnimation();
            hideElement(elements.loadingOverlay);
            displayResults(result);

        } catch (error) {
            stopLoadingAnimation();
            hideElement(elements.loadingOverlay);
            console.error('API Error:', error);
            alert('Sorry, there was an error processing your request. Please try again.');
        }
    }

    // ==========================================
    // Results Display
    // ==========================================
    function displayResults(result) {
        hideElement(elements.formSection);
        hideElement(elements.heroSection);
        if (elements.howItWorks) hideElement(elements.howItWorks);
        showElement(elements.resultsSection);

        animateScore(result.score, result.verdict_code);

        elements.resultVerdict.textContent = result.verdict;
        elements.resultVerdict.className = 'verdict ' + VERDICT_CLASSES[result.verdict_code];
        elements.resultConfidence.textContent = `Confidence: ${result.confidence}`;
        elements.resultSalaryMin.textContent = result.salary_range.formatted_min;
        elements.resultSalaryMax.textContent = result.salary_range.formatted_max;
        elements.resultReasons.innerHTML = result.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('');
        elements.resultDataUpdated.textContent = `Market data last updated: ${result.data_updated}`;
        elements.resultDisclaimer.textContent = result.disclaimer;

        scrollToElement(elements.resultsSection);

        Analytics.track('result_viewed', {
            score: result.score,
            verdict: result.verdict_code,
            confidence: result.confidence
        });
    }

    function animateScore(score, verdictCode) {
        const duration = 1000;
        const startTime = performance.now();
        const circumference = 339.292;
        const color = VERDICT_COLORS[verdictCode] || VERDICT_COLORS['fairly_paid'];

        elements.scoreRingProgress.style.stroke = color;

        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentScore = Math.round(easeOut * score);

            elements.resultScore.textContent = currentScore;
            const dashOffset = circumference - (easeOut * score / 100) * circumference;
            elements.scoreRingProgress.style.strokeDashoffset = dashOffset;

            if (progress < 1) requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    }

    function resetForm() {
        elements.form.reset();
        currentStep = 1;
        formData = {};
        detectedRole = 'default';

        goToStep(1);
        hideElement(elements.resultsSection);
        showElement(elements.heroSection);
        if (elements.howItWorks) showElement(elements.howItWorks);
        showElement(elements.formSection);
        hideElement(elements.skillSuggestions);

        updateExperienceDisplay();
        updateCurrency();

        elements.scoreRingProgress.style.strokeDashoffset = 339.292;
        elements.resultScore.textContent = '0';

        scrollToElement(elements.heroSection);
    }

    // ==========================================
    // Job Title Autocomplete
    // ==========================================
    function filterSuggestions(query) {
        if (!query || query.length < 2) return [];
        const q = query.toLowerCase();
        return JOB_SUGGESTIONS.filter(s => s.toLowerCase().includes(q)).slice(0, 8);
    }

    function showSuggestions(suggestions) {
        if (!elements.jobSuggestions) return;
        if (suggestions.length === 0) {
            hideSuggestions();
            return;
        }

        elements.jobSuggestions.innerHTML = suggestions.map((s, i) =>
            `<div class="suggestion-item${i === selectedSuggestionIndex ? ' selected' : ''}" data-index="${i}">${highlightMatch(s, elements.jobTitleInput.value)}</div>`
        ).join('');

        showElement(elements.jobSuggestions);
    }

    function hideSuggestions() {
        if (elements.jobSuggestions) {
            hideElement(elements.jobSuggestions);
            selectedSuggestionIndex = -1;
        }
    }

    function highlightMatch(text, query) {
        const idx = text.toLowerCase().indexOf(query.toLowerCase());
        if (idx === -1) return text;
        return text.substring(0, idx) + '<strong>' + text.substring(idx, idx + query.length) + '</strong>' + text.substring(idx + query.length);
    }

    function selectSuggestion(text) {
        elements.jobTitleInput.value = text;
        hideSuggestions();

        // Update detected role for skill suggestions
        detectedRole = detectRoleFromTitle(text);
    }

    function updateSelectedSuggestion(items) {
        items.forEach((item, i) => {
            item.classList.toggle('selected', i === selectedSuggestionIndex);
        });
        if (selectedSuggestionIndex >= 0 && items[selectedSuggestionIndex]) {
            items[selectedSuggestionIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    function initJobTitleAutocomplete() {
        if (!elements.jobTitleInput) return;

        elements.jobTitleInput.addEventListener('input', () => {
            const suggestions = filterSuggestions(elements.jobTitleInput.value);
            selectedSuggestionIndex = -1;
            showSuggestions(suggestions);
        });

        elements.jobTitleInput.addEventListener('keydown', (e) => {
            if (!elements.jobSuggestions || elements.jobSuggestions.classList.contains('hidden')) return;

            const items = elements.jobSuggestions.querySelectorAll('.suggestion-item');

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedSuggestionIndex = Math.min(selectedSuggestionIndex + 1, items.length - 1);
                updateSelectedSuggestion(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedSuggestionIndex = Math.max(selectedSuggestionIndex - 1, 0);
                updateSelectedSuggestion(items);
            } else if (e.key === 'Enter' && selectedSuggestionIndex >= 0) {
                e.preventDefault();
                selectSuggestion(items[selectedSuggestionIndex].textContent);
            } else if (e.key === 'Escape') {
                hideSuggestions();
            }
        });

        elements.jobTitleInput.addEventListener('blur', () => {
            setTimeout(hideSuggestions, 200);
        });

        if (elements.jobSuggestions) {
            elements.jobSuggestions.addEventListener('click', (e) => {
                const item = e.target.closest('.suggestion-item');
                if (item) selectSuggestion(item.textContent);
            });
        }
    }

    // ==========================================
    // Event Listeners
    // ==========================================
    function initEventListeners() {
        // Step navigation
        elements.nextButtons.forEach(btn => {
            btn.addEventListener('click', () => goToStep(parseInt(btn.dataset.next)));
        });

        elements.backButtons.forEach(btn => {
            btn.addEventListener('click', () => goToStep(parseInt(btn.dataset.back)));
        });

        // Form submission
        elements.form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validateStep(3)) submitForm();
        });

        // Start over
        if (elements.startOverButton) {
            elements.startOverButton.addEventListener('click', resetForm);
        }

        // Experience slider
        if (elements.experienceSlider) {
            elements.experienceSlider.addEventListener('input', updateExperienceDisplay);
        }

        // Country select
        if (elements.countrySelect) {
            elements.countrySelect.addEventListener('change', updateCurrency);
        }

        // Theme toggle
        if (elements.themeToggle) {
            elements.themeToggle.addEventListener('click', toggleTheme);
        }

        // Skill chip clicks
        if (elements.skillChips) {
            elements.skillChips.addEventListener('click', (e) => {
                const chip = e.target.closest('.skill-chip');
                if (chip) addSkillFromChip(chip.dataset.skill);
            });
        }

        // Track form start
        const firstInput = elements.form.querySelector('input, select');
        if (firstInput) {
            firstInput.addEventListener('focus', function handler() {
                Analytics.track('form_start');
                firstInput.removeEventListener('focus', handler);
            }, { once: true });
        }
    }

    function initKeyboardNav() {
        document.addEventListener('keydown', (e) => {
            if (elements.formSection.classList.contains('hidden')) return;

            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && e.target.id !== 'job_title') {
                const isLastStep = currentStep === 3;
                if (!isLastStep) {
                    e.preventDefault();
                    goToStep(currentStep + 1);
                }
            }
        });
    }

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    scrollToElement(target);
                }
            });
        });
    }

    function initFAQAccordion() {
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach(item => {
            item.addEventListener('toggle', () => {
                if (item.open) {
                    faqItems.forEach(other => {
                        if (other !== item && other.open) other.open = false;
                    });
                }
            });
        });
    }

    // ==========================================
    // Initialization
    // ==========================================
    function init() {
        initTheme();
        initEventListeners();
        initKeyboardNav();
        initSmoothScroll();
        initFAQAccordion();
        initJobTitleAutocomplete();
        updateExperienceDisplay();
        updateCurrency();

        Analytics.track('page_load');
        console.log('FairPayCheck initialized');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
