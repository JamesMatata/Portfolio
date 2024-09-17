from django.core.mail import send_mail
import os
from wsgiref.util import FileWrapper
from mimetypes import guess_type

import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.conf import settings
from django.utils.http import http_date
from django.views.decorators.csrf import csrf_exempt

from core.forms import HireMeForm, BookCallForm
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
        # Fetch the first image and video for the project
        project.first_image = project.images.first()
        try:
            project.project_video = project.video
        except Video.DoesNotExist:
            project.project_video = None

        # Prepare media data for frontend consumption
        project.media = []
        for image in project.images.all():
            project.media.append({
                'type': 'image',
                'url': image.image.name,  # Use 'name' instead of 'url'
                'reference': image.reference
            })
        if project.project_video:
            project.media.append({
                'type': 'video',
                'url': project.project_video.video.name,  # Use 'name' instead of 'url'
                'reference': 'video'
            })

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

            try:
                # Send the email using Django's send_mail function
                send_mail(
                    subject,
                    full_message,
                    'jamesmatatamule@gmail.com',  # From email
                    ['jamesmatatamule@gmail.com'],  # To email
                    fail_silently=False,
                )

                # Pass success message to the template
                return render(request, 'Portfolio/contact.html',
                              {'success': 'Your message has been sent successfully.'})

            except Exception as e:
                # Pass error message to the template
                return render(request, 'Portfolio/contact.html', {'error': f'Failed to send email: {str(e)}'})

        # If any field is missing, show an error message
        return render(request, 'Portfolio/contact.html', {'error': 'All fields are required.'})

    # Render the contact form if not a POST request
    return render(request, 'Portfolio/contact.html')


def serve_media(request, path):
    try:
        # Build the full path to the media file
        media_path = os.path.join(settings.MEDIA_ROOT, path)
        extension = os.path.splitext(path)[1].lower()

        # Guess the content type if not specified
        content_type, _ = guess_type(media_path)

        # If content type could not be guessed, default to 'application/octet-stream'
        if content_type is None:
            content_type = 'application/octet-stream'

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



def book_call(request):
    if request.method == 'POST':
        form = BookCallForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})


def hire_me(request):
    if request.method == 'POST':
        form = HireMeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})
