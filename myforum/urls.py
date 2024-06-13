from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from forum import views  # Importez explicitement les vues de votre application forum

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),  # Assurez-vous que views est importé correctement depuis forum
]
