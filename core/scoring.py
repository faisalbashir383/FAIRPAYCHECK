"""
FairPayCheck Scoring Engine
Implements all scoring formulas and calculations.
"""

import re
from . import data


def clamp(value, min_val, max_val):
    """Clamp a value between min and max bounds."""
    return max(min_val, min(value, max_val))


def round_salary(amount, currency):
    """Round salary to appropriate threshold based on currency."""
    threshold = data.SALARY_ROUNDING.get(currency, 1000)
    return round(amount / threshold) * threshold


def get_experience_level(years):
    """Determine experience level based on years of experience."""
    for level, (min_years, max_years) in data.EXPERIENCE_LEVELS.items():
        if min_years <= years <= max_years:
            return level
    return 'principal'  # Default for high experience


def categorize_role(job_title):
    """Categorize a job title into a role category."""
    title_lower = job_title.lower()
    
    for category, keywords in data.ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    
    return 'default'


def get_market_median(role_category, experience_level, country, industry):
    """
    Get the market median salary for a given role/experience/country combination.
    Returns the median in local currency.
    """
    # Get base median from role/level
    role_data = data.ROLE_MEDIANS_USD.get(role_category, data.ROLE_MEDIANS_USD['default'])
    base_median_usd = role_data.get(experience_level, role_data['mid'])
    
    # Apply industry multiplier
    industry_mult = data.INDUSTRY_MULTIPLIERS.get(industry, 1.0)
    adjusted_usd = base_median_usd * industry_mult
    
    # Apply CMI to get local equivalent
    cmi = data.CMI.get(country, 1.0)
    adjusted_for_region = adjusted_usd * cmi
    
    # Convert to local currency
    currency_code = data.COUNTRY_CURRENCIES.get(country, {}).get('code', 'USD')
    exchange_rate = data.EXCHANGE_RATES.get(currency_code, 1.0)
    
    local_median = adjusted_for_region / exchange_rate
    
    return local_median, currency_code


def normalize_salary_to_usd(salary, country):
    """
    Normalize a local salary to USD using exchange rate and CMI.
    Formula: NormalizedSalaryUSD = (UserSalary × ExchangeRateToUSD) / CountryMarketIndex
    """
    currency_code = data.COUNTRY_CURRENCIES.get(country, {}).get('code', 'USD')
    exchange_rate = data.EXCHANGE_RATES.get(currency_code, 1.0)
    cmi = data.CMI.get(country, 1.0)
    
    # Convert to USD
    salary_usd = salary * exchange_rate
    
    # Normalize by CMI
    normalized_usd = salary_usd / cmi
    
    return normalized_usd


def calculate_market_score(salary, market_median, country):
    """
    Calculate the Market Score (max 30 points).
    Based on normalized salary vs market median.
    """
    MAX_SCORE = data.SCORE_WEIGHTS['market']
    
    # If salary not provided, return neutral score
    if salary is None or salary <= 0:
        return MAX_SCORE * 0.5  # Returns 15
    
    # Get currency code
    currency_code = data.COUNTRY_CURRENCIES.get(country, {}).get('code', 'USD')
    exchange_rate = data.EXCHANGE_RATES.get(currency_code, 1.0)
    cmi = data.CMI.get(country, 1.0)
    
    # Normalize both salary and median
    normalized_salary = (salary * exchange_rate) / cmi
    normalized_median = (market_median * exchange_rate) / cmi
    
    # Calculate market gap ratio
    if normalized_median > 0:
        gap_ratio = (normalized_median - normalized_salary) / normalized_median
    else:
        gap_ratio = 0
    
    # Clamp gap ratio between 0 and 1
    gap_ratio = clamp(gap_ratio, 0, 1)
    
    # Calculate score (higher gap = higher underpaid score)
    market_score = gap_ratio * MAX_SCORE
    
    return clamp(market_score, 0, MAX_SCORE)


def calculate_experience_score(years_experience, salary, market_median, country):
    """
    Calculate the Experience Score (max 20 points).
    Based on mismatch between experience level and expected pay tier.
    """
    MAX_SCORE = data.SCORE_WEIGHTS['experience']
    
    # Determine expected level based on experience
    exp_level = get_experience_level(years_experience)
    
    # If no salary provided, base only on experience years
    if salary is None or salary <= 0:
        # Higher experience without salary verification = moderate score
        experience_multiplier = min(years_experience / 15, 1.0)
        return experience_multiplier * MAX_SCORE * 0.5
    
    # Calculate expected salary ratio vs actual
    currency_code = data.COUNTRY_CURRENCIES.get(country, {}).get('code', 'USD')
    
    # For senior+ roles, expected pay should be higher
    level_multipliers = {
        'junior': 0.7,
        'mid': 0.9,
        'senior': 1.1,
        'lead': 1.25,
        'principal': 1.4,
    }
    
    expected_multiplier = level_multipliers.get(exp_level, 1.0)
    expected_salary = market_median * expected_multiplier
    
    # Calculate gap
    if expected_salary > 0:
        gap_ratio = (expected_salary - salary) / expected_salary
    else:
        gap_ratio = 0
    
    gap_ratio = clamp(gap_ratio, 0, 1)
    
    return clamp(gap_ratio * MAX_SCORE, 0, MAX_SCORE)


def calculate_skill_score(skills_text):
    """
    Calculate the Skill Premium Score (max 15 points).
    Based on weighted demand of listed skills.
    """
    MAX_SCORE = data.SCORE_WEIGHTS['skills']
    
    if not skills_text or not skills_text.strip():
        return MAX_SCORE * 0.3  # Default low score for no skills listed
    
    # Parse skills (comma or semicolon separated)
    skills = [s.strip().lower() for s in re.split(r'[,;]', skills_text) if s.strip()]
    
    if not skills:
        return MAX_SCORE * 0.3
    
    # Calculate total skill premium
    total_premium = 0
    matched_skills = 0
    
    for skill in skills:
        # Check direct match
        if skill in data.SKILL_PREMIUMS:
            total_premium += data.SKILL_PREMIUMS[skill]
            matched_skills += 1
        else:
            # Check partial match
            for known_skill, premium in data.SKILL_PREMIUMS.items():
                if known_skill in skill or skill in known_skill:
                    total_premium += premium * 0.7  # Partial match penalty
                    matched_skills += 1
                    break
    
    if matched_skills == 0:
        return MAX_SCORE * 0.4  # Skills listed but not recognized
    
    # Average premium, scaled by number of high-demand skills
    avg_premium = total_premium / matched_skills
    skill_count_bonus = min(matched_skills / 5, 1.0)  # Bonus for having multiple skills
    
    # Higher premium skills mean you're more likely underpaid if not compensated
    score = avg_premium * MAX_SCORE * (0.5 + 0.5 * skill_count_bonus)
    
    return clamp(score, 0, MAX_SCORE)


def calculate_company_score(company_size, country):
    """
    Calculate the Company Score (max 10 points).
    Adjusted by Region Company Multiplier (RCM).
    """
    MAX_SCORE = data.SCORE_WEIGHTS['company']
    
    # Base score by company size (smaller companies often pay less)
    size_scores = {
        'small': 0.7,  # Higher underpaid likelihood
        'medium': 0.5,
        'large': 0.3,   # Lower underpaid likelihood
    }
    
    base_score = size_scores.get(company_size, 0.5) * MAX_SCORE
    
    # Apply Region Company Multiplier
    if country in data.EMERGING_MARKETS:
        rcm = data.RCM['emerging']
    else:
        rcm = data.RCM['developed']
    
    adjusted_score = base_score * rcm
    
    return clamp(adjusted_score, 0, MAX_SCORE)


def calculate_progression_score(years_in_role, promotion_received):
    """
    Calculate the Career Progression Score (max 10 points).
    Based on years in same role + promotion history.
    """
    MAX_SCORE = data.SCORE_WEIGHTS['progression']
    
    # Longer time in same role without promotion = higher underpaid risk
    if years_in_role is None:
        years_in_role = 0
    
    # Years in role factor (3+ years without change is concerning)
    years_factor = min(years_in_role / 5, 1.0)
    
    # Promotion factor
    if promotion_received:
        promotion_factor = 0.3  # Recent promotion = lower underpaid risk
    else:
        promotion_factor = 0.7  # No promotion = higher risk
    
    score = ((years_factor * 0.6) + (promotion_factor * 0.4)) * MAX_SCORE
    
    return clamp(score, 0, MAX_SCORE)


def calculate_timing_score(role_category):
    """
    Calculate the Market Timing Score (max 10 points).
    Based on role demand trends.
    """
    MAX_SCORE = data.SCORE_WEIGHTS['timing']
    
    # Get demand trend for role (-1 to 1 scale)
    demand_trend = data.ROLE_DEMAND_TRENDS.get(role_category, data.ROLE_DEMAND_TRENDS['default'])
    
    # High demand roles = more likely underpaid if not compensated at market
    # Convert trend to score (higher demand = higher potential underpaid score)
    score = ((demand_trend + 1) / 2) * MAX_SCORE
    
    return clamp(score, 0, MAX_SCORE)


def calculate_confidence(salary_provided, country, role_category):
    """
    Calculate confidence level based on data quality.
    Returns: 'High', 'Medium', or 'Low'
    """
    base_confidence = 'Medium'
    
    # Start with country data reliability
    country_reliability = data.COUNTRY_DATA_RELIABILITY.get(country, 'low')
    
    if country_reliability == 'high':
        base_confidence = 'High'
    elif country_reliability == 'low':
        base_confidence = 'Low'
    
    # Downgrade if salary not provided
    if not salary_provided:
        if base_confidence == 'High':
            base_confidence = 'Medium'
        else:
            base_confidence = 'Low'
    
    # Check role commonality
    if role_category == 'default':
        if base_confidence == 'High':
            base_confidence = 'Medium'
        elif base_confidence == 'Medium':
            base_confidence = 'Low'
    
    return base_confidence


def get_verdict(score):
    """Get the verdict label and code based on total score."""
    if score >= data.VERDICT_THRESHOLDS['likely_underpaid']:
        return 'Likely underpaid', 'likely_underpaid'
    elif score >= data.VERDICT_THRESHOLDS['possibly_underpaid']:
        return 'Possibly underpaid', 'possibly_underpaid'
    elif score >= data.VERDICT_THRESHOLDS['fairly_paid']:
        return 'Fairly paid', 'fairly_paid'
    else:
        return 'Likely fairly or overpaid', 'fairly_overpaid'


def generate_reasons(scores, inputs):
    """Generate top 3 reasons explaining the score."""
    reasons = []
    
    # Analyze each component and generate relevant reasons
    if scores['market'] > 20:
        reasons.append({
            'priority': scores['market'],
            'text': 'Your current salary appears below the market median for similar roles in your location.'
        })
    elif scores['market'] > 10:
        reasons.append({
            'priority': scores['market'],
            'text': 'Your salary is slightly below market expectations for your role and location.'
        })
    
    if scores['experience'] > 14:
        reasons.append({
            'priority': scores['experience'],
            'text': f'With {inputs.get("years_experience", 0)}+ years of experience, your compensation may not reflect your seniority level.'
        })
    elif scores['experience'] > 8:
        reasons.append({
            'priority': scores['experience'],
            'text': 'Your experience level suggests you may be positioned for higher compensation.'
        })
    
    if scores['skills'] > 10:
        reasons.append({
            'priority': scores['skills'],
            'text': 'Your skill set includes high-demand capabilities that typically command premium pay.'
        })
    
    if scores['company'] > 6:
        reasons.append({
            'priority': scores['company'],
            'text': 'Smaller companies in your region often pay less than larger organizations for similar roles.'
        })
    
    if scores['progression'] > 6:
        years_in_role = inputs.get('years_in_role', 0)
        if years_in_role and years_in_role > 2:
            reasons.append({
                'priority': scores['progression'],
                'text': f'Being in the same role for {years_in_role}+ years without promotion may indicate stagnant compensation.'
            })
        else:
            reasons.append({
                'priority': scores['progression'],
                'text': 'Your career progression pattern suggests potential for better compensation elsewhere.'
            })
    
    if scores['timing'] > 7:
        reasons.append({
            'priority': scores['timing'],
            'text': 'Your role category is currently in high demand, which often creates pay gaps for existing employees.'
        })
    
    # Sort by priority and take top 3
    reasons.sort(key=lambda x: x['priority'], reverse=True)
    top_reasons = [r['text'] for r in reasons[:3]]
    
    # Ensure we have at least 3 reasons
    default_reasons = [
        'Market conditions vary significantly across regions and industries.',
        'Individual circumstances and company policies affect compensation.',
        'Consider discussing your contributions with your manager during performance reviews.'
    ]
    
    while len(top_reasons) < 3:
        for reason in default_reasons:
            if reason not in top_reasons:
                top_reasons.append(reason)
                break
    
    return top_reasons[:3]


def calculate_salary_range(market_median, currency_code):
    """Calculate the fair salary range based on market median."""
    # Range is typically -10% to +10% of median
    min_salary = market_median * 0.9
    max_salary = market_median * 1.1
    
    # Round to appropriate threshold
    min_salary = round_salary(min_salary, currency_code)
    max_salary = round_salary(max_salary, currency_code)
    
    return min_salary, max_salary


def format_salary(amount, currency_code, country):
    """Format salary amount with currency symbol."""
    currency_info = data.COUNTRY_CURRENCIES.get(country, {'symbol': '$'})
    symbol = currency_info['symbol']
    
    # Format with thousands separator
    formatted = f"{amount:,.0f}"
    
    return f"{symbol}{formatted}"


def calculate_full_score(inputs):
    """
    Main scoring function - calculates all components and returns full result.
    
    Expected inputs:
    - job_title: str
    - country: str
    - city: str (optional)
    - industry: str
    - years_experience: int
    - company_size: str (small/medium/large)
    - skills: str (comma-separated)
    - salary: float (optional)
    - bonus_equity: float (optional)
    - years_in_role: int (optional)
    - promotion_received: bool (optional)
    """
    # Extract inputs with defaults
    job_title = inputs.get('job_title', '')
    country = inputs.get('country', 'USA')
    industry = inputs.get('industry', 'other')
    years_experience = int(inputs.get('years_experience', 0))
    company_size = inputs.get('company_size', 'medium')
    skills = inputs.get('skills', '')
    salary = inputs.get('salary')
    years_in_role = inputs.get('years_in_role')
    promotion_received = inputs.get('promotion_received', False)
    
    # Convert salary to float if provided
    if salary:
        try:
            salary = float(salary)
        except (ValueError, TypeError):
            salary = None
    
    if years_in_role:
        try:
            years_in_role = int(years_in_role)
        except (ValueError, TypeError):
            years_in_role = None
    
    # Categorize role
    role_category = categorize_role(job_title)
    experience_level = get_experience_level(years_experience)
    
    # Get market median
    market_median, currency_code = get_market_median(
        role_category, experience_level, country, industry
    )
    
    # Calculate all score components
    scores = {
        'market': calculate_market_score(salary, market_median, country),
        'experience': calculate_experience_score(years_experience, salary, market_median, country),
        'skills': calculate_skill_score(skills),
        'company': calculate_company_score(company_size, country),
        'progression': calculate_progression_score(years_in_role, promotion_received),
        'timing': calculate_timing_score(role_category),
    }
    
    # Calculate total score with baseline
    total_score = sum(scores.values()) + data.SCORE_WEIGHTS['baseline']
    total_score = clamp(total_score, 0, 100)
    
    # Get verdict
    verdict, verdict_code = get_verdict(total_score)
    
    # Calculate confidence
    confidence = calculate_confidence(salary is not None, country, role_category)
    
    # Calculate salary range
    min_salary, max_salary = calculate_salary_range(market_median, currency_code)
    
    # Generate reasons
    reasons = generate_reasons(scores, inputs)
    
    # Build response
    result = {
        'version': '1.0',
        'score': round(total_score),
        'verdict': verdict,
        'verdict_code': verdict_code,
        'confidence': confidence,
        'salary_range': {
            'min': min_salary,
            'max': max_salary,
            'currency': currency_code,
            'formatted_min': format_salary(min_salary, currency_code, country),
            'formatted_max': format_salary(max_salary, currency_code, country),
        },
        'reasons': reasons,
        'data_updated': data.DATA_UPDATED_DISPLAY,
        'disclaimer': data.DISCLAIMER_TEXT.strip(),
        'job_recommendations': None,  # Placeholder for future feature
        'score_breakdown': {
            'market': round(scores['market'], 1),
            'experience': round(scores['experience'], 1),
            'skills': round(scores['skills'], 1),
            'company': round(scores['company'], 1),
            'progression': round(scores['progression'], 1),
            'timing': round(scores['timing'], 1),
            'baseline': data.SCORE_WEIGHTS['baseline'],
        },
        'debug': {
            'role_category': role_category,
            'experience_level': experience_level,
            'market_median': round(market_median),
        }
    }
    
    return result
