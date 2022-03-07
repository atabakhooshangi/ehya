from .models import SupportTicket
from accounts.models import AppSettings


def reached_support_answer_limit(user, obj: SupportTicket):
    """
    indicates user has reached ticket answer limit
    :param user:
    :param obj:
    :return: bool
    """

    if user == obj.user:
        if obj.supportanswer_set.filter(user=user).count() < AppSettings.objects.last().ticket_answer_limit:
            return True
        return False
    return True
