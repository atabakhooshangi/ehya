from accounts.models import User


def common_data(list1, list2):
    result = False

    # traverse in the 1st list
    for x in list1:

        # traverse in the 2nd list
        for y in list2:

            # if one common
            if x == y:
                result = True
                return result

    return result


def role_permission_checker(related_role: str, user: User) -> bool:
    if user.is_superuser:
        return True
    for role in user.role.all():
        if related_role in role.get_role_permissions:
            return True


supports_pers = ['support.add_supportanswer', 'support.change_supportanswer', 'support.view_supportanswer',
                 'support.delete_supportanswer', 'support.add_supportticket', 'support.change_supportticket',
                 'support.view_supportticket', 'support.delete_supportticket']


def support_permission_checker(user: User) -> bool:
    if user.is_superuser:
        return True
    for role in user.role.all():
        if common_data(supports_pers, role.get_role_permissions):
            return True


def ticket_permission_checker(user: User, role_list: list) -> bool:
    if user.is_superuser:
        return True
    for role in user.role.all():
        if role.name in role_list:
            return True
