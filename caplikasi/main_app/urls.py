from django.urls import path
from .views import home, login_client, register_client, logout_client, archive_detail, recherche_archive, tout_archive


app_name = "main_app"

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_client, name='login_client'),
    path('register/', register_client, name='register_client'),
    path('logout/', logout_client, name='logout_client'),
    path('archive-liste/', tout_archive, name='tout_archive'),
    path('detail/archvie/<int:pk>/', archive_detail, name='archive_detail'),
    path('resultat/recherche/', recherche_archive, name='recherche_archive'),
]
