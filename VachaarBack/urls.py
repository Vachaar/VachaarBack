from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from VachaarBack import views
from VachaarBack.settings import SHOW_SWAGGER

urlpatterns = [
    path("api/login", views.login_user, name="login"),
    path("api/register", views.register_user),
    path("admin/", [admin.site](blocked).urls),
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
[admin.site](blocked).site_header = "Vachaar Administration Panel"
[admin.site](blocked).index_title = "vachaar"
[admin.site](blocked).site_title = "Vachaar Admin"