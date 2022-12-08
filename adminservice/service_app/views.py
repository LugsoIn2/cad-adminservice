from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django.http import JsonResponse
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Attr
from django.conf import settings

# Dynamodb configuration
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET,
    region_name='eu-central-1')

# Get All Files
def list(request):
    #city = request.GET.get('tenants')
    table = dynamodb.Table('tenants')
    response = table.scan()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        try:
            items = response['Items']
        except KeyError as e:
            print('Something went wrong')
        return JsonResponse(items, safe=False)
