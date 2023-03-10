import datetime

from django.http import QueryDict
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status

from .models import event
from .serializers import EventSerializer
from media_manager.media_uploader import upload_image
import json

# Create your views here.

@api_view(['GET', 'POST'])
def events(request):

    if request.method == 'GET':
        return upcoming_events(request)
    elif request.method == 'POST':
        return create_event(request)
    else:
        return JsonResponse({'error': 'Method not allowed, only accepts POST and GET'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def upcoming_events(request):
    print(f"is_auth: {request.session.get('is_auth')}, role: {request.session.get('role')}")
    if request.session.get('is_auth') is not None and request.session.get('is_auth') \
            and request.session.get('role') != 'supervisor':
        coming_events = event.objects \
            .filter(event_attendance__student_id=request.session.get('username')) \
            .filter(start_datetime__gt=datetime.datetime.now()) \
            .values('event_id', 'title', 'type', 'start_datetime', 'description', 'poster_path')

        if coming_events.exists():
            serializer = EventSerializer(coming_events, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'the user did not register in any event yet'},
                                status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'error': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)


def create_event(request):
    if request.session.get('is_auth') is not None and request.session.get('is_auth') \
            and (request.session.get('role') == 'president' or request.session.get('role') == 'officer'):

        req_data = json.loads(request.body)
        b64_image = req_data.get('poster')
        media_type = req_data.get('media_type')
        req_data['club_id'] = request.session.get('club_id')
        filename = str(timezone.now())
        print(req_data)
        event_serializer = EventSerializer(data=req_data)
        if event_serializer.is_valid():
            poster_url = upload_image(b64_image=b64_image, type=media_type, folder='events', filename=filename)
            req_data['poster_path'] = poster_url
            print(f'Poster Path: {poster_url}')
            event_serializer = EventSerializer(data=req_data)
            if event_serializer.is_valid():
                event_serializer.save()
                return JsonResponse({'message': 'event created'}, status=status.HTTP_201_CREATED)
            else:
                print(event_serializer.errors)
                print(event_serializer.errors.__str__())
                return JsonResponse({'error': str(event_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(event_serializer.errors)
            print(event_serializer.errors.__str__())
            return JsonResponse({'error': str(event_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def event_details(request, event_id):
    try:
        details = event.objects.get(event_id=event_id)
    except event.DoesNotExist:
        return JsonResponse({'error': 'The event does not exists'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(details, many=False)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


