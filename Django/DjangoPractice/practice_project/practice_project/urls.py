from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter
from webApp.views import UserViewSet, PublisherAPIView, BookAPIView  

# 🔹 Router setup
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path("admin/", admin.site.urls),

    #  API Routes (from ViewSet)
    path('api/', include(router.urls)),

    #  Swagger / Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Like FastAPI /docs
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    # Like FastAPI /redoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),

    path('api/publishers/', PublisherAPIView.as_view(), name='publisher-list-create'),
    path('api/books/', BookAPIView.as_view(), name='book-list-create'),
]