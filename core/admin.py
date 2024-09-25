from django.contrib import admin
from .models import Project, Image, Video, BookCall, HireMe


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
        'updated_at'
    )
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


@admin.register(HireMe)
class HireMeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'created_at')
    search_fields = ('name', 'email', 'project_details')

    # Override the save_model method
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(BookCall)
class BookCallAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'preferred_date', 'preferred_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'preferred_date')
    search_fields = ('name', 'email')

    # Override the save_model method
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
