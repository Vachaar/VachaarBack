"""
URL configuration for VachaarBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from VachaarBack.settings import SHOW_SWAGGER

urlpatterns = [
    path("admin/", admin.site.urls),
    path("product/", include("product.urls")),
    path("usr/", include("user.urls")),
]

if SHOW_SWAGGER:
    urlpatterns += [
        # doc
        path(
            "api/schema/",
            staff_member_required(
                SpectacularAPIView.as_view(
                    custom_settings={"SCHEMA_PATH_PREFIX": "/v1/"}
                )
            ),
            name="schema",
        ),
        path(
            "api/docs/",
            staff_member_required(
                SpectacularSwaggerView.as_view(url_name="schema")
            ),
            name="swagger-ui",
        ),
    ]

# Admin
admin.site.site_header = "Vachaar Administration Panel"
admin.site.index_title = "vachaar"
admin.site.site_title = "Vachaar Admin"
