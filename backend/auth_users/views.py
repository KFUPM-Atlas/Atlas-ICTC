from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from pycognito import Cognito
from django.conf import settings
from rest_framework.parsers import JSONParser
from .models import club_officer, supervisor
from django.db.models import Case, When, Value, BooleanField, Exists
import requests

# Create your views here.
@api_view(['POST'])
def login_view(request):

    data = request.data
    # Get the user's credentials from the request
    print(data)
    username = data['username']
    password = data['password']
    print(f'{username}, {password}')
    client = Cognito(user_pool_id=settings.COGNITO_USER_POOL_ID, user_pool_region=settings.COGNITO_AWS_REGION,
                     client_id=settings.COGNITO_APP_CLIENT_ID, client_secret=settings.COGNITO_CLIENT_SECRET,
                     username=username)

    try:
        client.authenticate(password=password)
        role = get_user_role(username)

        # Calling Student API to fetch user information

        if role != 'supervisor':
            response = requests.get(
                url=f'https://stoplight.io/mocks/kfupm-atlas/atlas-student-api/54617661/student/{username}')
        else:
            response = requests.get(
                url=f'https://stoplight.io/mocks/kfupm-atlas/atlas-student-api/54617661/student/{username}')

        response_json = JSONParser().parse(response.content)
        request.session['username'] = username
        request.session['email'] = response_json['email']
        request.session['name_en'] = response_json['name_en']
        request.session['gender'] = response_json['gender']
        request.session['major_code'] = response_json['major_code']
        request.session['is_auth'] = True
        request.session['role'] = role

        return JsonResponse({'message': 'success login'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'email or password is wrong'}, status=status.HTTP_401_UNAUTHORIZED)


def get_user_role(user_id):
    queryset = club_officer.objects.annotate(
        is_officer=Case(
            When(officer_id=id, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        is_president=Case(
            When(officer_id=id, president_id=id, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    ).annotate(
        is_supervisor=Exists(supervisor.objects.filter(id=id))
    )

    is_officer = queryset.filter(is_officer=True).exists()
    is_supervisor = queryset.filter(is_supervisor=True).exists()
    is_president = queryset.filter(is_president=True).exists()

    if is_supervisor:
        return 'supervisor'
    elif is_officer:
        if is_president:
            return 'president'
        else:
            return 'officer'
    else:
        return 'student'
