from .models import UserInfo

def user_context(request):
    """
    Context processor to make logged in user and profile available across ALL templates.
    """
    userid = request.session.get('userid')
    user = None
    if userid:
        user = UserInfo.objects.filter(email=userid).first()
    return {
        'userid': userid,
        'user': user,
        'profile': user.profile if user and user.profile else None,
        'user_name': user.name if user else '',
    }
