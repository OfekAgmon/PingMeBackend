__author__ = 'ofeka_000'
from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            if request.method in permissions.SAFE_METHODS:
                return True