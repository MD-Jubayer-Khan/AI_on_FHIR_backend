from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuerySerializer
from .nlp_helper import parse_query, simulate_patients
from rest_framework.decorators import api_view

# Create your views here.

class QueryView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["query"]
            parsed = parse_query(text)
            results = simulate_patients(parsed)
            return Response({
                "query": text,
                "parsed": parsed,
                "simulated_fhir_request": parsed["fhir_request"],
                "results": results
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

EXAMPLES = [
    "Show me all diabetic patients over 50",
    "Patients with hypertension under 40",
    "List patients with asthma",
    "Diabetic patients under 60",
    "Patients with asthma over 30"
]

@api_view(["GET"])
def Suggestions(request):
    query = request.GET.get("q", "").lower()
    if not query:
        return Response([])
    
    # Filter examples that contain the typed substring
    filtered = [ex for ex in EXAMPLES if query in ex.lower()]
    return Response(filtered)