import datetime

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from backend.events.models import event
from backend.events.serializers import EventSerializer


# Create your views here.


@api_view(['GET'])
def upcoming_events(request):
    if request.session['is_auth'] is not None and request.session['is_auth'] \
            and request.session['role'] is not 'supervisor':
        events = event.objects \
            .filter(event_attendance__student_id='') \
            .filter(start_datetime__gt=datetime.datetime.now()) \
            .values('event_id', 'title', 'type', 'start_datetime', 'description', 'poster_path')

        if events.exists():
            serializer = EventSerializer(events, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'the user did not register in any event yet'},
                                status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'error': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def event_details(request, pk):
    try:
        details = event.objects.get(pk=pk)
    except event.DoesNotExist:
        return JsonResponse({'error': 'The event does not exists'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(details, many=False)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_event(request):
    if request.session['is_auth'] is not None and request.session['is_auth'] \
            and (request.session['role'] == 'president' or request.session['role'] == 'officer'):

        event_data = JSONParser().parse(request.data)
        event_serializer = EventSerializer(data=event_data)
        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
