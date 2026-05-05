from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def group_required(group_name):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


def require_owner(request, obj):
    if obj.user_id != request.user.id:
        raise PermissionDenied


class GroupRequiredMixin(LoginRequiredMixin):
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.groups.filter(name=self.group_name).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
