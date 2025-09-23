# 代码生成时间: 2025-09-23 11:04:47
from django.conf.urls import url
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import DocumentSerializer
import os
from docx import Document as DocxDocument
from docx.oxml.text.paragraph import CT_P
import re

# Models
from django.db import models

class Document(models.Model):
    """Model for storing documents"""
    file = models.FileField(upload_to='documents/')
    
    def __str__(self):
        """String representation of the Document model"""
        return f'Document {self.file.name}'

# Serializers
from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    class Meta:
        model = Document
        fields = '__all__'

# Views
class DocumentConverterView(APIView):
    """View for converting documents"""
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (JSONRenderer,)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request for document conversion"""
        file = request.data.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = DocumentSerializer(data={'file': file})
            if document.is_valid():
                document.save()
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                document = Document.objects.get(file=file.name)
                return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
            else:
                return Response(document.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# URLs
from django.conf.urls import url

urlpatterns = [
    url(r'^convert/$', DocumentConverterView.as_view(), name='document-convert'),
]
