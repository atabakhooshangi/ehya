from .models import Ticket
from accounts.models import AppSettings


def not_reached_answer_limit(user, obj: Ticket):
    """
    indicates user has reached ticket answer limit
    :param user:
    :param obj:
    :return: bool
    """
    bool_list = []
    if user == obj.user:
        if obj.answer_set.filter(user=user).count() < AppSettings.objects.last().ticket_answer_limit:
            return True
        return False
    for role in user.role.all():
        if role.name in ['کارشناس', 'کارشناس ارشد']:
            bool_list.append('True')
        return 'True' in bool_list
    return False
