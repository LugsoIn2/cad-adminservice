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
from random import randint
from boto3.dynamodb.conditions import Attr

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
    data = json.loads(request.body)
    city = data.get('city')
    cnr = "cad-" + str(randint(10000000, 99999999))
    if form.is_valid():
        form.save()
        # Register User
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        # Login User
        login(request, user)
        # Create entry for tenant table
        table = dynamodb.Table(settings.TEN_TABLE_NAME)
        item = table.put_item(Item={"customer_nr": cnr, "city": city, "subscription_type": 0, "user_id": username})

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
    table = dynamodb.Table(settings.TEN_TABLE_NAME)
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(str(request.user))
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 or len(response['Items']) == 0:
        return HttpResponse('')
    return JsonResponse(response['Items'][0], safe=False)

# TODO: only give back theme type!!!!
# Get Information about specific tenant
def specifictenant_view(request):
    customer_nr = request.GET.get('customer_nr')
    table = dynamodb.Table(settings.TEN_TABLE_NAME)
    response = table.query(
        IndexName='customer_nr-index',
        KeyConditionExpression=Key('customer_nr').eq(customer_nr)
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 or len(response['Items']) == 0:
        return HttpResponse('')
    items = response['Items'][0]
    return JsonResponse(items, safe=False)

# Set my subscription type
@require_POST
def subscription_view(request):
    data = json.loads(request.body)
    subscription = data.get('subscription')
    # Get my Tenant information
    table = dynamodb.Table(settings.TEN_TABLE_NAME)
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(str(request.user))
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 or len(response['Items']) == 0:
        return HttpResponse('')
    my_tenant = response['Items'][0]
    city = my_tenant.get('city')
    c_nr = my_tenant.get('customer_nr')
    old_subs_type = my_tenant.get('subscription_type')

    # Get old subscription type
    old_subscription_chdir = ''
    if old_subs_type == 1:
        old_subscription_chdir = 'subsc_standard'
    elif old_subs_type == 2:
        old_subscription_chdir = 'subsc_enterprise'

    # Set subscription type
    subscription_type = ''
    terraform_dir = os.path.join(os.path.dirname(__file__), '../terraform-commands/')
    if (subscription == 'Free'):
        subscription_type = 0
        script = terraform_dir + 'destroy.sh ' + c_nr + ' ' + city + ' ' + old_subscription_chdir
        subprocess.Popen([script], shell=True)
    elif (subscription == 'Standard'):
        subscription_type = 1
        script = terraform_dir + 'standard.sh ' + c_nr + ' ' + city + ' ' + old_subscription_chdir
        subprocess.Popen([script], shell=True)
    elif (subscription == 'Enterprise'):
        subscription_type = 2
        script = terraform_dir + 'enterprise.sh ' + c_nr + ' ' + city + ' ' + old_subscription_chdir
        subprocess.Popen([script], shell=True)

    if subscription_type == '':
        return JsonResponse({})

    # Update subscription type in tenants table
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

# Set my subscription type
@require_POST
def theme_view(request):
    data = json.loads(request.body)
    theme = data.get('theme')
    # Get my Tenant information
    table = dynamodb.Table(settings.TEN_TABLE_NAME)
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(str(request.user))
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200 or len(response['Items']) == 0:
        return HttpResponse('')
    my_tenant = response['Items'][0]
    city = my_tenant.get('city')

    # Update subscription type
    response = table.update_item(
        Key={'city': city},
        UpdateExpression="set theme_type = :s",
        ExpressionAttributeValues={
            ':s': theme,
        },
        ReturnValues="UPDATED_NEW")

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return HttpResponse('')
    return JsonResponse(data)

# Get array of free tenants
def freetenants_view(request):
    table = dynamodb.Table(settings.TEN_TABLE_NAME)
    filter=Attr("subscription_type").eq(0) | Attr("subscription_type").eq(1)
    response = table.scan(
        FilterExpression=filter,
    )
    free_tenants = list(map(lambda x: x['city'], response['Items']))
    return JsonResponse(free_tenants, safe=False)
