from django.shortcuts import render
from .serializers import HighlightSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Highlight 

# Create your views here.
@api_view(['GET'])
def get_highlights(request):
    highlights = Highlight.objects.all()
    serializer = HighlightSerializer(highlights, many=True,context={'request': request})
    return Response(serializer.data)


