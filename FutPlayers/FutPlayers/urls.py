from django.contrib import admin
from django.urls import path, include

apiv1 = "api/v1/"

urlpatterns = [
    path('admin/', admin.site.urls),
    path(apiv1, include("players.urls"))
]
