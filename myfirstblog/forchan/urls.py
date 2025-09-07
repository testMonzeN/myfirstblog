from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from search.views import search_ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include("search.urls")),
    path('blog/', include('blog.urls')),
    path('stepik/', include('stepik.urls')),
    path('api/', include('api.urls')),
    path('animals/', include('animals.urls')),
    path('chat/', include('group.urls')),
    path('', include('cards.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)