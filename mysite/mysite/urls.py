from django.conf import settings
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from blog.sitemaps import PostSitemap
from blog.views import greeting


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', greeting),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps},
         name = 'django.contrib.sitemaps.views.sitemap')
]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)