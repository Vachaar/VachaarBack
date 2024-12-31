from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import format_html

from user.models.user import User

ACCESS_DENIED_MESSAGE = "Access denied!"


def has_admin_access(user):
    return user.is_staff


@login_required
def render_admin_stats_view(request):
    if not has_admin_access(request.user):
        return HttpResponse(ACCESS_DENIED_MESSAGE, status=403)

    total_users = User.objects.count()

    html_content = format_html(
        """
        <html>
        <body>
            <p>Total users: {total}</p>
        </body>
        </html>
        """,
        total=total_users,
    )
    return HttpResponse(html_content)
