
from django.contrib import admin
from django.urls import include,path
from . import views
 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('myapp.urls')),
    path('login/', views.login_user),
    path('register/', views.register_user),
    path('generateImage/', views.genAIPrompt2),
    path('getImages/', views.get_images),
    path('sendEmail/', views.send_email, name='send_email'),
]
