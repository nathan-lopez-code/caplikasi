from django.urls import path
from .views import dashboard, register_archive, edit_archive, delete_archive, show_archive


app_name = 'archive_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('enregistre/', register_archive, name='register_archive'),
    path('toute/', show_archive, name='show_archive'),
    path('modifier/<int:pk>/', edit_archive, name='edit_archive'),
    path('delete/<int:pk>/', delete_archive, name='delete_archive'),
]
