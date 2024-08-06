from django.urls import path

from core import views
from core.views import contact_view

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', contact_view, name='contact'),
]
