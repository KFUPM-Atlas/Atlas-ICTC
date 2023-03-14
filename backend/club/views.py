import asyncio

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from .models import club
from django.core.paginator import Paginator
from .serializers import ClubSerializer
import json
from media_manager.media_uploader import upload_image


# Create your views here.
@api_view(['POST', 'GET'])
def clubs_view(request):
    if request.method == 'GET':
        return list_clubs(request)
    # elif request.method == 'POST' TODO: create club
    else:
        return JsonResponse({'error': 'Method not allowed, only accepts GET and POST', 'success': False},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['UPDATE', 'GET'])
def club_details_view(request, club_id):
    if request.method == 'GET':
        return get_club_details(request, club_id)
    elif request.method == 'UPDATE':
        return update_club_details(request, club_id)
    else:
        return JsonResponse({'error': 'Method not allowed, only accepts UPDATE and GET', 'success': False},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


def list_clubs(request):
    clubs = club.objects.order_by('club_id')

    if not clubs.exists():
        return JsonResponse({'message': 'the are no clubs', 'success': False}, status=status.HTTP_204_NO_CONTENT)

    paginator = Paginator(clubs, per_page=10)

    page_number = json.loads(request.body)['page']
    page = paginator.get_page(page_number)

    clubs_data = [{'club_id': club_var.club_id, 'name': club_var.name, 'logo_path': club_var.logo_path} for club_var in
                  page.object_list]
    response_data = {
        'clubs': clubs_data,
        'previous_page': page.previous_page_number() if page.has_previous() else None,
        'next_page': page.next_page_number() if page.has_next() else None
    }

    return JsonResponse({'message': 'success',
                         'data': response_data,
                         'success': True}, status=status.HTTP_200_OK)


def update_club_details(request, club_id):
    if request.session.get('is_auth') is not None and request.session.get('is_auth') \
            and (request.session.get('role') == 'president' or request.session.get('role') == 'officer'):
        try:
            club_var = club.objects.get(club_id=club_id)
            # Get the updated fields from the request data
            updated_data = json.loads(request.body)
            description = updated_data.get('description')
            b64_logo = updated_data.get('logo')
            media_type = updated_data.get('media_type')
            # If logo is passed, upload the logo and get the URL
            if b64_logo is not None:
                print('b64 not none')
                logo_url = upload_image(b64_image=b64_logo, type=media_type, folder='clubs',
                                        filename=f'club_{club_id}_logo')
            else:
                logo_url = club_var.logo_path

            print(logo_url)
            # Update the club model with the new data
            club_var.description = description
            club_var.logo_path = logo_url
            club_var.save()

            serializer = ClubSerializer(club_var)
            return JsonResponse({'message': 'club updated',
                                 'data': serializer.data,
                                 'success': True}, status=status.HTTP_200_OK)
        except club.DoesNotExist:
            JsonResponse({'error': 'The club does not exists', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'error': 'Not Authorized', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)


def get_club_details(request, club_id):
    try:
        details = club.objects.get(club_id=club_id)
    except club.DoesNotExist:
        return JsonResponse({'error': 'The club does not exists', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClubSerializer(details, many=False)
    return JsonResponse({'message': 'success',
                         'data': serializer.data,
                         'success': True}, safe=False, status=status.HTTP_200_OK)
