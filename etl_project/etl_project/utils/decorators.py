from django.shortcuts import redirect
from ..utils.auth import refresh_token_if_needed

def login_required_session_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_details'):
            return redirect('login')

        if not refresh_token_if_needed(request):
            # Token refresh failed, logout user
            if 'access_token' in request.session:
                del request.session['access_token']
            if 'refresh_token' in request.session:
                del request.session['refresh_token']
            if 'user_details' in request.session:
                del request.session['user_details']

            return redirect('login')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
