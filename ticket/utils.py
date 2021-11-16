from .models import Answer, TicketAnswerLimit, Ticket


def reached_answer_limit(user, obj: Ticket):
    """
    indicates user has reached ticket answer limit
    :param user:
    :param obj:
    :return: bool
    """
    if user.role.name in ['کارشناس', 'کارشناس ارشد']:
        return True
    if user == obj.user:
        print(obj.answer_set.filter(user=user).count())
        if obj.answer_set.filter(user=user).count() < TicketAnswerLimit.objects.last().value:
            return True
        return False
    return False
