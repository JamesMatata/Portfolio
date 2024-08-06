from django.contrib import admin
from .models import Project, Image, Video


class ImageInline(admin.TabularInline):
    model = Image
    extra = 8  # Ensure there are 8 images


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1  # Ensure there is 1 video


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_date', 'end_date', 'live_preview_link', 'github_link', 'tools_and_languages', 'created_at',
        'updated_at')
    inlines = [ImageInline, VideoInline]
    search_fields = ('title', 'description', 'tools_and_languages')
    list_filter = ('start_date', 'end_date')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'reference', 'image', 'uploaded_at')
    search_fields = ('project__title', 'reference')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('project', 'video', 'uploaded_at')
    search_fields = ('project__title',)
