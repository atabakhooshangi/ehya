from .models import SupportTicket, SupportTicketAnswerLimit


def reached_support_answer_limit(user, obj: SupportTicket):
    """
    indicates user has reached ticket answer limit
    :param user:
    :param obj:
    :return: bool
    """
    if user.is_support:
        return True
    if user == obj.user:
        if obj.supportanswer_set.filter(user=user).count() < SupportTicketAnswerLimit.objects.last().value:
            return True
        return False
    return False
