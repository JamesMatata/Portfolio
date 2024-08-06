from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=455)
    start_date = models.DateField()
    end_date = models.DateField()
    live_preview_link = models.URLField(max_length=200, blank=True, null=True)
    github_link = models.URLField(max_length=200, blank=True, null=True)
    tools_and_languages = models.CharField(max_length=255)  # A comma-separated list of tools and languages used
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    reference = models.CharField(max_length=50)  # e.g., 'image1', 'image2', etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} for project: {self.project.title}"


class Video(models.Model):
    project = models.OneToOneField(Project, related_name='video', on_delete=models.CASCADE)
    video = models.FileField(upload_to='project_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for project: {self.project.title}"
