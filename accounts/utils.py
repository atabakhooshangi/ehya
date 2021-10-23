
def get_visitor_ipaddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # check of HTTP_X_FORWARDED_FOR not none
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # current ip address
    return ip
