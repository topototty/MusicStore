from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

class CRUDPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:  # Если пользователь - администратор
            return True

        if request.user.is_staff:  # Если пользователь - сотрудник
            return request.method in ['GET', 'POST']

        return request.method in SAFE_METHODS # GET, HEAD, OPTIONS, TRACE
