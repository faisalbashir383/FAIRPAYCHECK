"""
FairPayCheck Static Data Definitions
Contains all market data, indices, and configuration values.
Data version: 2025-01
"""

# Data version for API response
DATA_VERSION = "2025-01"
DATA_UPDATED_DISPLAY = "2025 (est.)"

# Country Market Index (CMI)
# Used to normalize regional pay levels
CMI = {
    'USA': 1.00,
    'UK': 0.90,
    'Germany': 0.85,
    'Canada': 0.88,
    'Australia': 0.92,
    'India': 0.35,
}

# Exchange Rates to USD (approximate)
EXCHANGE_RATES = {
    'USD': 1.0,
    'GBP': 1.27,
    'EUR': 1.10,
    'CAD': 0.74,
    'AUD': 0.65,
    'INR': 0.012,
}

# Country to Currency mapping
COUNTRY_CURRENCIES = {
    'USA': {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'},
    'UK': {'code': 'GBP', 'symbol': '£', 'name': 'British Pound'},
    'Germany': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'Canada': {'code': 'CAD', 'symbol': 'C$', 'name': 'Canadian Dollar'},
    'Australia': {'code': 'AUD', 'symbol': 'A$', 'name': 'Australian Dollar'},
    'India': {'code': 'INR', 'symbol': '₹', 'name': 'Indian Rupee'},
}

# Rounding thresholds by currency
SALARY_ROUNDING = {
    'USD': 1000,
    'GBP': 1000,
    'EUR': 1000,
    'CAD': 1000,
    'AUD': 1000,
    'INR': 10000,
}

# Region classification for Company Multiplier
DEVELOPED_MARKETS = ['USA', 'UK', 'Germany', 'Canada', 'Australia']
EMERGING_MARKETS = ['India']

# Region Company Multiplier (RCM)
RCM = {
    'developed': 1.0,
    'emerging': 0.8,
}

# Country list for dropdown
COUNTRIES = [
    {'value': 'USA', 'label': 'United States'},
    {'value': 'UK', 'label': 'United Kingdom'},
    {'value': 'Germany', 'label': 'Germany'},
    {'value': 'Canada', 'label': 'Canada'},
    {'value': 'Australia', 'label': 'Australia'},
    {'value': 'India', 'label': 'India'},
]

# Industry list for dropdown
INDUSTRIES = [
    {'value': 'technology', 'label': 'Technology / Software'},
    {'value': 'finance', 'label': 'Finance / Banking'},
    {'value': 'healthcare', 'label': 'Healthcare / Medical'},
    {'value': 'consulting', 'label': 'Consulting / Professional Services'},
    {'value': 'manufacturing', 'label': 'Manufacturing / Industrial'},
    {'value': 'retail', 'label': 'Retail / E-commerce'},
    {'value': 'education', 'label': 'Education / Research'},
    {'value': 'government', 'label': 'Government / Public Sector'},
    {'value': 'media', 'label': 'Media / Entertainment'},
    {'value': 'telecom', 'label': 'Telecommunications'},
    {'value': 'energy', 'label': 'Energy / Utilities'},
    {'value': 'transportation', 'label': 'Transportation / Logistics'},
    {'value': 'hospitality', 'label': 'Hospitality / Travel'},
    {'value': 'nonprofit', 'label': 'Non-profit / NGO'},
    {'value': 'other', 'label': 'Other'},
]

# Company size definitions
COMPANY_SIZES = [
    {'value': 'small', 'label': 'Small (1-50 employees)'},
    {'value': 'medium', 'label': 'Medium (51-500 employees)'},
    {'value': 'large', 'label': 'Large (500+ employees)'},
]

# Base market medians by role category (in USD)
# These are simplified estimates - in production would use real data
ROLE_MEDIANS_USD = {
    'engineering': {
        'junior': 70000,
        'mid': 100000,
        'senior': 140000,
        'lead': 170000,
        'principal': 200000,
    },
    'design': {
        'junior': 55000,
        'mid': 80000,
        'senior': 110000,
        'lead': 130000,
        'principal': 155000,
    },
    'product': {
        'junior': 65000,
        'mid': 95000,
        'senior': 130000,
        'lead': 160000,
        'principal': 190000,
    },
    'marketing': {
        'junior': 50000,
        'mid': 70000,
        'senior': 95000,
        'lead': 120000,
        'principal': 145000,
    },
    'sales': {
        'junior': 55000,
        'mid': 80000,
        'senior': 110000,
        'lead': 140000,
        'principal': 170000,
    },
    'finance': {
        'junior': 60000,
        'mid': 85000,
        'senior': 115000,
        'lead': 145000,
        'principal': 175000,
    },
    'hr': {
        'junior': 45000,
        'mid': 65000,
        'senior': 85000,
        'lead': 105000,
        'principal': 130000,
    },
    'operations': {
        'junior': 45000,
        'mid': 65000,
        'senior': 90000,
        'lead': 115000,
        'principal': 140000,
    },
    'data': {
        'junior': 65000,
        'mid': 95000,
        'senior': 130000,
        'lead': 160000,
        'principal': 190000,
    },
    'default': {
        'junior': 50000,
        'mid': 75000,
        'senior': 100000,
        'lead': 125000,
        'principal': 150000,
    }
}

# Role keywords for categorization
ROLE_KEYWORDS = {
    'engineering': [
        'engineer', 'developer', 'programmer', 'software', 'backend', 'frontend',
        'fullstack', 'devops', 'sre', 'infrastructure', 'platform', 'architect',
        'cto', 'tech lead', 'technical lead', 'coding', 'development'
    ],
    'design': [
        'designer', 'ux', 'ui', 'graphic', 'visual', 'creative', 'art director',
        'brand', 'motion', 'product design'
    ],
    'product': [
        'product manager', 'product owner', 'product lead', 'pm', 'program manager',
        'project manager', 'scrum master', 'agile coach'
    ],
    'marketing': [
        'marketing', 'growth', 'seo', 'content', 'social media', 'brand manager',
        'communications', 'pr', 'public relations', 'digital marketing'
    ],
    'sales': [
        'sales', 'account executive', 'business development', 'bdr', 'sdr',
        'account manager', 'customer success', 'partnerships'
    ],
    'finance': [
        'finance', 'accountant', 'controller', 'cfo', 'financial analyst',
        'treasury', 'audit', 'tax', 'investment', 'banking analyst'
    ],
    'hr': [
        'hr', 'human resources', 'recruiter', 'talent', 'people operations',
        'compensation', 'benefits', 'hrbp', 'training'
    ],
    'operations': [
        'operations', 'supply chain', 'logistics', 'procurement', 'facilities',
        'administration', 'office manager', 'executive assistant', 'warehouse', 'inventory'
    ],
    'data': [
        'data scientist', 'data analyst', 'data engineer', 'machine learning',
        'ml engineer', 'ai', 'analytics', 'business intelligence', 'bi analyst',
        'statistician', 'quantitative'
    ],
    'healthcare': [
        'nurse', 'physician', 'doctor', 'medical', 'healthcare', 'hospital',
        'therapist', 'pharmacist', 'dentist', 'clinical', 'patient', 'emt',
        'paramedic', 'surgeon', 'rn', 'lpn', 'anesthesiologist', 'radiologist'
    ],
    'legal': [
        'attorney', 'lawyer', 'legal', 'paralegal', 'counsel', 'litigation',
        'compliance', 'contract', 'law', 'esquire', 'jd'
    ],
    'education': [
        'teacher', 'professor', 'instructor', 'education', 'principal',
        'curriculum', 'tutor', 'lecturer', 'academic', 'school'
    ],
    'construction': [
        'construction', 'carpenter', 'electrician', 'plumber', 'hvac',
        'foreman', 'superintendent', 'builder', 'contractor', 'welder',
        'machinist', 'civil engineer', 'architect'
    ],
    'hospitality': [
        'hotel', 'restaurant', 'chef', 'cook', 'server', 'bartender',
        'hospitality', 'catering', 'concierge', 'housekeeping', 'event planner'
    ],
    'retail': [
        'retail', 'store manager', 'sales associate', 'cashier', 'merchandiser',
        'buyer', 'customer service'
    ],
    'creative': [
        'photographer', 'videographer', 'editor', 'animator', 'illustrator',
        'journalist', 'reporter', 'producer', 'writer', 'author', 'film'
    ]
}

# High-demand skills with premium weights (0-1 scale)
SKILL_PREMIUMS = {
    # Tech skills
    'python': 0.8,
    'javascript': 0.7,
    'typescript': 0.75,
    'react': 0.75,
    'node': 0.7,
    'aws': 0.85,
    'azure': 0.8,
    'gcp': 0.8,
    'kubernetes': 0.9,
    'docker': 0.75,
    'terraform': 0.85,
    'golang': 0.85,
    'rust': 0.9,
    'java': 0.7,
    'sql': 0.65,
    'nosql': 0.7,
    'mongodb': 0.7,
    'postgresql': 0.7,
    'machine learning': 0.95,
    'ml': 0.95,
    'ai': 0.95,
    'deep learning': 0.95,
    'pytorch': 0.9,
    'tensorflow': 0.85,
    'data science': 0.85,
    'spark': 0.85,
    'hadoop': 0.7,
    'kafka': 0.8,
    'elasticsearch': 0.75,
    'redis': 0.7,
    'graphql': 0.75,
    'microservices': 0.8,
    'system design': 0.85,
    'security': 0.85,
    'cybersecurity': 0.9,
    'blockchain': 0.75,
    'web3': 0.7,
    'ios': 0.8,
    'android': 0.75,
    'flutter': 0.75,
    'react native': 0.75,
    
    # Business skills
    'leadership': 0.7,
    'management': 0.65,
    'strategy': 0.7,
    'analytics': 0.75,
    'excel': 0.5,
    'powerpoint': 0.4,
    'salesforce': 0.65,
    'hubspot': 0.6,
    'sap': 0.7,
    'tableau': 0.7,
    'power bi': 0.7,
    'project management': 0.6,
    'agile': 0.6,
    'scrum': 0.55,
    'pmp': 0.6,
    'negotiation': 0.65,
    'communication': 0.5,
    'presentation': 0.5,
}

# Role-based skill suggestions (for autocomplete)
ROLE_SKILL_SUGGESTIONS = {
    'engineering': [
        'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'AWS', 'Docker',
        'Kubernetes', 'SQL', 'Git', 'System Design', 'Microservices', 'REST APIs',
        'CI/CD', 'Agile', 'Java', 'Go', 'PostgreSQL', 'MongoDB', 'Redis'
    ],
    'design': [
        'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator', 'UI Design',
        'UX Research', 'Prototyping', 'Wireframing', 'Design Systems', 'Typography',
        'Color Theory', 'User Testing', 'Responsive Design', 'Accessibility'
    ],
    'product': [
        'Product Strategy', 'Roadmapping', 'User Research', 'A/B Testing', 'Agile',
        'Scrum', 'Jira', 'Analytics', 'SQL', 'Stakeholder Management', 'OKRs',
        'PRDs', 'Market Research', 'Competitive Analysis', 'Go-to-Market'
    ],
    'marketing': [
        'SEO', 'SEM', 'Google Analytics', 'Content Strategy', 'Social Media',
        'Email Marketing', 'HubSpot', 'Copywriting', 'Brand Strategy', 'PPC',
        'Marketing Automation', 'Lead Generation', 'CRM', 'A/B Testing'
    ],
    'sales': [
        'Salesforce', 'CRM', 'Negotiation', 'B2B Sales', 'Lead Generation',
        'Cold Calling', 'Pipeline Management', 'Account Management', 'Presentations',
        'Contract Negotiation', 'Relationship Building', 'Forecasting', 'SaaS Sales'
    ],
    'finance': [
        'Financial Modeling', 'Excel', 'Financial Analysis', 'Budgeting',
        'Forecasting', 'SAP', 'QuickBooks', 'Accounting', 'Auditing', 'Tax',
        'Compliance', 'Risk Management', 'Valuation', 'M&A', 'SQL'
    ],
    'hr': [
        'Recruiting', 'Talent Acquisition', 'HRIS', 'Workday', 'Employee Relations',
        'Performance Management', 'Compensation', 'Benefits Administration',
        'Onboarding', 'Training', 'Compliance', 'SHRM', 'Diversity & Inclusion'
    ],
    'operations': [
        'Process Improvement', 'Supply Chain', 'Logistics', 'Project Management',
        'Vendor Management', 'Excel', 'ERP', 'Lean', 'Six Sigma', 'Inventory Management',
        'Procurement', 'Quality Assurance', 'Scheduling', 'Budget Management'
    ],
    'data': [
        'Python', 'SQL', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Pandas',
        'NumPy', 'Tableau', 'Power BI', 'Statistics', 'A/B Testing', 'R',
        'Deep Learning', 'NLP', 'Computer Vision', 'Spark', 'Data Visualization'
    ],
    'healthcare': [
        'Patient Care', 'EMR/EHR', 'HIPAA', 'Medical Terminology', 'Vital Signs',
        'Medication Administration', 'CPR/BLS', 'Patient Assessment', 'Care Planning',
        'Clinical Documentation', 'Infection Control', 'ACLS', 'Phlebotomy', 'Triage'
    ],
    'legal': [
        'Legal Research', 'Contract Drafting', 'Litigation', 'Legal Writing',
        'Case Management', 'Westlaw', 'LexisNexis', 'Due Diligence', 'Discovery',
        'Client Counseling', 'Negotiation', 'Regulatory Compliance', 'E-Discovery'
    ],
    'education': [
        'Curriculum Development', 'Lesson Planning', 'Classroom Management',
        'Student Assessment', 'Differentiated Instruction', 'Educational Technology',
        'IEP Development', 'Google Classroom', 'Canvas', 'Blackboard', 'Tutoring'
    ],
    'construction': [
        'Project Management', 'Blueprint Reading', 'AutoCAD', 'OSHA Safety',
        'Cost Estimation', 'Scheduling', 'Building Codes', 'Quality Control',
        'Site Management', 'Contract Management', 'Procore', 'MS Project'
    ],
    'hospitality': [
        'Customer Service', 'POS Systems', 'Inventory Management', 'Menu Planning',
        'Food Safety', 'ServSafe', 'Event Planning', 'Reservations', 'Guest Relations',
        'Revenue Management', 'Housekeeping', 'Front Desk Operations', 'Mixology'
    ],
    'retail': [
        'Customer Service', 'POS Systems', 'Visual Merchandising', 'Inventory Management',
        'Sales', 'Cash Handling', 'Loss Prevention', 'Product Knowledge',
        'Team Leadership', 'Store Operations', 'Retail Analytics', 'Upselling'
    ],
    'creative': [
        'Adobe Creative Suite', 'Photography', 'Video Editing', 'Premiere Pro',
        'After Effects', 'Final Cut Pro', 'Lightroom', 'Cinematography',
        'Color Grading', 'Storytelling', 'Audio Editing', 'Motion Graphics', '3D Modeling'
    ],
    'default': [
        'Microsoft Office', 'Excel', 'PowerPoint', 'Communication', 'Leadership',
        'Project Management', 'Problem Solving', 'Teamwork', 'Time Management',
        'Analytical Skills', 'Presentation', 'Organization', 'Attention to Detail'
    ]
}

# Role demand trends (current market hot/cold)
# Scale: -1 (declining) to 1 (high growth)
ROLE_DEMAND_TRENDS = {
    'engineering': 0.7,
    'design': 0.4,
    'product': 0.6,
    'marketing': 0.3,
    'sales': 0.4,
    'finance': 0.3,
    'hr': 0.2,
    'operations': 0.2,
    'data': 0.9,
    'default': 0.3,
}

# Industry pay multipliers (relative to tech baseline)
INDUSTRY_MULTIPLIERS = {
    'technology': 1.0,
    'finance': 1.1,
    'healthcare': 0.85,
    'consulting': 1.0,
    'manufacturing': 0.8,
    'retail': 0.75,
    'education': 0.7,
    'government': 0.75,
    'media': 0.85,
    'telecom': 0.9,
    'energy': 0.95,
    'transportation': 0.8,
    'hospitality': 0.7,
    'nonprofit': 0.65,
    'other': 0.8,
}

# Company size pay multipliers
COMPANY_SIZE_MULTIPLIERS = {
    'small': 0.85,
    'medium': 0.95,
    'large': 1.1,
}

# Confidence data reliability by country
COUNTRY_DATA_RELIABILITY = {
    'USA': 'high',
    'UK': 'high',
    'Germany': 'medium',
    'Canada': 'high',
    'Australia': 'medium',
    'India': 'medium',
}

# Experience level thresholds (years)
EXPERIENCE_LEVELS = {
    'junior': (0, 2),
    'mid': (3, 5),
    'senior': (6, 10),
    'lead': (11, 15),
    'principal': (16, 100),
}

# Score component maximums
SCORE_WEIGHTS = {
    'market': 30,
    'experience': 20,
    'skills': 15,
    'company': 10,
    'progression': 10,
    'timing': 10,
    'baseline': 5,  # Neutral starting point
}

# Verdict thresholds
VERDICT_THRESHOLDS = {
    'likely_underpaid': 70,
    'possibly_underpaid': 45,
    'fairly_paid': 30,
    # Below 30 = likely fairly or overpaid
}

# Disclaimer text
DISCLAIMER_TEXT = """
This assessment is based on estimated market data and general industry patterns. 
It is not a substitute for professional career or financial advice. 
Individual circumstances, company policies, and local market conditions may vary significantly. 
FairPayCheck provides insights for educational purposes only.
"""
