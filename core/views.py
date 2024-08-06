import json

import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from core.models import Project


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

    project_images = []
    for project in projects:
        first_image = project.images.first()
        project_images.append(first_image)

    return render(request, 'Portfolio/portfolio.html', {'projects': projects, 'project_images': project_images})


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
