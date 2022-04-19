from django.contrib.auth.views import get_user_model

User = get_user_model()


def post_permission_checker(user: User, role_list: list) -> bool:
    for role in user.role.all():
        if role.name in role_list:
            return True
