import json
import os
from wsgiref.util import FileWrapper

import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.conf import settings
from django.utils.http import http_date
from django.views.decorators.csrf import csrf_exempt

from core.models import Project, Video


def home(request):
    recent_projects = Project.objects.order_by('-created_at')[:3]

    recent_project_images = []
    for project in recent_projects:
        first_image = project.images.first()
        recent_project_images.append(first_image)
    return render(request, 'Portfolio/home.html',
                  {'recent_projects': recent_projects, 'recent_project_images': recent_project_images})


def portfolio(request):
    projects = Project.objects.all()

    for project in projects:
        project.first_image = project.images.first()
        try:
            project.project_video = project.video
        except Video.DoesNotExist:
            project.project_video = None

    return render(request, 'Portfolio/portfolio.html', {'projects': projects})


@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if first_name and last_name and email and subject and message:
            full_message = f"From: {first_name} {last_name}\nEmail: {email}\n\n{message}"
            response = send_mailgun_email(subject, full_message, email, ['jamesmatatamule@gmail.com'])
            if response.status_code == 200:
                return JsonResponse({'success': True})
            else:
                error_message = response.json().get('message', 'Failed to send email')
                return JsonResponse({'success': False, 'error': error_message})
        return JsonResponse({'success': False, 'error': 'All fields are required'})

    return render(request, 'Portfolio/contact.html')


def send_mailgun_email(subject, message, from_email, to_emails):
    print(subject, message, from_email, to_emails)
    return requests.post(
        f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN_NAME}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={
            "from": f"{from_email}",
            "to": to_emails,
            "subject": subject,
            "text": message,
        },
    )


def serve_media(request, path):
    try:
        # Build the full path to the media file
        media_path = os.path.join('media', path)
        extension = os.path.splitext(media_path)[1].lower()

        # Supported file extensions
        video_extensions = ['.mp4', '.avi', '.mov']
        audio_extensions = ['.wav', '.mp3']

        # Determine the content type
        if extension in video_extensions:
            content_type = 'video/mp4'
        elif extension in audio_extensions:
            content_type = 'audio/mpeg'
        else:
            return HttpResponseNotFound('<h1>File type not supported</h1>')

        # Get the file size
        file_size = os.path.getsize(media_path)
        file = open(media_path, 'rb')

        # Handle range requests
        content_range = request.headers.get('Range', None)
        if content_range:
            # Parse the range header
            content_range = content_range.strip().split('=')[-1]
            range_start, range_end = content_range.split('-')
            range_start = int(range_start)
            range_end = int(range_end) if range_end else file_size - 1
            length = range_end - range_start + 1

            # Set file pointer to the start of the requested range
            file.seek(range_start)

            # Create partial response
            response = HttpResponse(
                FileWrapper(file, length),
                status=206,  # Partial Content status
                content_type=content_type,
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'
        else:
            # Full content response
            response = HttpResponse(
                FileWrapper(file),
                content_type=content_type,
            )
            response['Content-Length'] = str(file_size)

        response['Accept-Ranges'] = 'bytes'
        response['Last-Modified'] = http_date(os.path.getmtime(media_path))
        return response

    except FileNotFoundError:
        return HttpResponseNotFound('<h1>File not found</h1>')
    except Exception as e:
        return HttpResponseServerError(f'<h1>Server error: {e}</h1>')
