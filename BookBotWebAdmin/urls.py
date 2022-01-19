from django.contrib import admin
from django.urls import path, include
from BookBotWebAdmin import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BookBotAdmin.urls'))
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
