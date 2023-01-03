import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.http import JsonResponse
import boto3
import os
from django.conf import settings
from boto3.dynamodb.conditions import Key
import subprocess

# Dynamodb configuration
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET,
    region_name='eu-central-1')

# Get CSRF Token
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

# Login
@require_POST
def login_view(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return JsonResponse({'detail': 'Please provide email and password.'}, status=400)
    user = authenticate(username=email, password=password)
    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})

# Register
@require_POST
def register_view(request):
    form = UserCreationForm(json.loads(request.body))
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return JsonResponse({'detail': 'Successfully registered.'})
    else:
        return JsonResponse({'error': form.errors})


# Logout
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})

# Who am I
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})
    
    return JsonResponse({'username': request.user.username})

# Get Information about my tenant
def mytenant_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({})
    table = dynamodb.Table('tenants')
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(str(request.user))
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 or len(response['Items']) == 0:
        return HttpResponse('')
    return JsonResponse(response['Items'][0], safe=False)

# Set my subscription type
@require_POST
def subscription_view(request):
    data = json.loads(request.body)
    subscription = data.get('subscription')
    city = data.get('city')
    table = dynamodb.Table('tenants')
    subscription_type = ''
    
    terraform_dir = os.path.join(os.path.dirname(__file__), '../terraform-commands/')
    if (subscription == 'Free'):
        subscription_type = 0
        process = subprocess.Popen([terraform_dir + 'prod.sh'], shell=True)
    elif (subscription == 'Standard'):
        subscription_type = 1
        process = subprocess.Popen([terraform_dir + 'standard.sh'], shell=True)
    elif (subscription == 'Enterprise'):
        subscription_type = 2        
        process = subprocess.Popen([terraform_dir + 'enterprise.sh'], shell=True)

    if subscription_type == '':
        return JsonResponse({})

    response = table.update_item(
        Key={'city': city},
        UpdateExpression="set subscription_type = :s",
        ExpressionAttributeValues={
            ':s': subscription_type,
        },
        ReturnValues="UPDATED_NEW")
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return HttpResponse('')
    return JsonResponse(data)
