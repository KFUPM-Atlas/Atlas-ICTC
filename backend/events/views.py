import datetime

from django.http import QueryDict
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status

from .models import event, event_attendance
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
        return JsonResponse({'error': 'Method not allowed, only accepts POST and GET', 'success': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def upcoming_events(request):
    print(f"is_auth: {request.session.get('is_auth')}, role: {request.session.get('role')}")
    if request.session.get('is_auth') is not None and request.session.get('is_auth') \
            and request.session.get('role') != 'supervisor':
        coming_events = event.objects \
            .filter(event_attendance__student_id=request.session.get('username')) \
            .filter(start_datetime__gt=datetime.datetime.now()) \
            .values('event_id', 'title', 'type', 'start_datetime', 'end_datetime', 'description', 'poster_path', 'club_id')

        if coming_events.exists():
            print(coming_events)
            serializer = EventSerializer(coming_events, many=True)
            return JsonResponse({'message': 'success',
                                 'data': serializer.data,
                                 'success': True}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'the user did not register in any event yet',
                                 'success': True},
                                status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'error': 'Not Authorized', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)


def create_event(request):
    if request.session.get('is_auth') is not None and request.session.get('is_auth') \
            and (request.session.get('role') == 'president' or request.session.get('role') == 'officer'):

        req_data = json.loads(request.body)
        b64_image = req_data.get('poster')
        media_type = req_data.get('media_type')
        req_data['club_id'] = request.session.get('club_id')
        filename = str(timezone.now())
        event_serializer = EventSerializer(data=req_data)
        if event_serializer.is_valid():
            poster_url = upload_image(b64_image=b64_image, type=media_type, folder='events', filename=filename)
            req_data['poster_path'] = poster_url
            event_serializer = EventSerializer(data=req_data)
            if event_serializer.is_valid():
                event_serializer.save()
                return JsonResponse({'message': 'event created', 'success': True}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': str(event_serializer.errors), 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': str(event_serializer.errors), 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Not Authorized', 'success': True}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def event_details(request, event_id):
    try:
        details = event.objects.get(event_id=event_id)
        print(details)
    except event.DoesNotExist:
        return JsonResponse({'error': 'The event does not exists', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(details, many=False)
    return JsonResponse({'message': 'success',
                         'data': serializer.data,
                         'success': True}, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def attend_event(request, event_id):
    if request.session.get('is_auth') is not None and request.session.get('is_auth')\
            and request.session.get('role') != 'supervisor':
        try:
            attendance = event_attendance(student_id=request.session.get('username'), event_id=event_id)
            attendance.save()
        except Exception as e:
            return JsonResponse({'error': 'Internal server error',
                                 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message': 'student has been registered for the event', 'success': True},
                            status=status.HTTP_200_OK)

