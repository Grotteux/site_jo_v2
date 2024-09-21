from django.shortcuts import redirect
from django_otp import user_has_device
from django.urls import reverse
from functools import wraps

def two_factor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if user_has_device(request.user):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse('two-factor-setup'))
        else:
            return redirect(reverse('account_login'))

    return _wrapped_view
