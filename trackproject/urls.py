from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('site/',include('projectsite.urls')),
    path('',include('frontsite.urls')),
    path('',include('user.urls')),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header="Leaf Construction "
admin.site.site_title='Browser Title'
admin.site.index_title ="Welcome to Construction Project....."
