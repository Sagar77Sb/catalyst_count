# api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

class CompanyQueryAPI(APIView):
    def get(self, request, *args, **kwargs):
        print("888888888888888888888888")
        print(request)
        filters = {}
    
        # Filter based on provided fields
        if 'keyword' in request.data and request.data['keyword']:
            filters['keyword__icontains'] = request.data['keyword']
        if 'industry' in request.data and request.data['industry']:
            filters['industry'] = request.data['industry']
        if 'year_founded' in request.data and request.data['year_founded']:
            filters['year_founded'] = request.data['year_founded']
        if 'city' in request.data and request.data['city']:
            filters['city__icontains'] = request.data['city']
        if 'state' in request.data and request.data['state']:
            filters['state__icontains'] = request.data['state']
        if 'country' in request.data and request.data['country']:
            filters['country__icontains'] = request.data['country']
        if 'employees_from' in request.data and request.data['employees_from']:
            filters['employees__gte'] = request.data['employees_from']
        if 'employees_to' in request.data and request.data['employees_to']:
            filters['employees__lte'] = request.data['employees_to']
        
        # Query the database
        count = Company.objects.filter(**filters).count()
        
        # Return the result count
        return Response({'count': count})
