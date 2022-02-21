from .models import Answer, TicketAnswerLimit, Ticket


def not_reached_answer_limit(user, obj: Ticket):
    """
    indicates user has reached ticket answer limit
    :param user:
    :param obj:
    :return: bool
    """
    bool_list = []
    for role in user.role.all():
        print(role)
        if role.name in ['کارشناس', 'کارشناس ارشد']:
            bool_list.append('True')
        return 'True' in bool_list
    if user == obj.user:
        if obj.answer_set.filter(user=user).count() < TicketAnswerLimit.objects.last().value:
            return True
        return False
    return False
