from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import redirect


def eh_moderador(user):
    return (
        user.is_authenticated
        and user.tipo_usuario in ['moderador', 'admin']
    )


def eh_moderador_ou_admin(user):
    return (
        user.is_authenticated
        and user.tipo_usuario in ['moderador', 'admin']
    )


def eh_admin(user):
    return (
        user.is_authenticated
        and user.tipo_usuario == 'admin'
    )


def requer_moderador(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not eh_moderador(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def requer_moderador_ou_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not eh_moderador_ou_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def requer_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not eh_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper