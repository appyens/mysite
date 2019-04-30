from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You must be the owner of the object'

    def has_object_permission(self, request, view, obj):
        if request in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user




