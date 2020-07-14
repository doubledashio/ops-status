from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import HomeView, ProfileView

admin.site.site_header = f'Ops Status v{settings.VERSION}'
admin.site.site_title = 'Ops Status Admin Panel'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls, namespace='djdt')),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    except Exception:
        pass
