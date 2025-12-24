"""
FairPayCheck Views
Handles page rendering and API endpoints.
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import data
from . import scoring


def index_view(request):
    """Render the main FairPayCheck page."""
    context = {
        'countries': data.COUNTRIES,
        'industries': data.INDUSTRIES,
        'company_sizes': data.COMPANY_SIZES,
        'country_currencies': json.dumps(data.COUNTRY_CURRENCIES),
        'role_skill_suggestions': json.dumps(data.ROLE_SKILL_SUGGESTIONS),
        'role_keywords': json.dumps(data.ROLE_KEYWORDS),
    }
    return render(request, 'index.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_score_api(request):
    """
    API endpoint for calculating salary fairness score.
    Accepts JSON POST data and returns scoring results.
    """
    try:
        # Parse JSON body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON in request body',
                'version': '1.0'
            }, status=400)
        
        # Validate required fields
        required_fields = ['job_title', 'country', 'industry', 'years_experience', 'company_size']
        missing_fields = [f for f in required_fields if not body.get(f)]
        
        if missing_fields:
            return JsonResponse({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'version': '1.0'
            }, status=400)
        
        # Validate country
        valid_countries = [c['value'] for c in data.COUNTRIES]
        if body.get('country') not in valid_countries:
            return JsonResponse({
                'error': f'Invalid country. Must be one of: {", ".join(valid_countries)}',
                'version': '1.0'
            }, status=400)
        
        # Validate company size
        valid_sizes = ['small', 'medium', 'large']
        if body.get('company_size') not in valid_sizes:
            return JsonResponse({
                'error': f'Invalid company_size. Must be one of: {", ".join(valid_sizes)}',
                'version': '1.0'
            }, status=400)
        
        # Calculate score
        result = scoring.calculate_full_score(body)
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred while processing your request.',
            'version': '1.0',
            'debug_error': str(e)  # Remove in production
        }, status=500)
