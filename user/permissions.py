from rest_framework.permissions import BasePermission


class IsStaffPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, (list, tuple)):
            return super().has_object_permission(request, view, obj)

        user = request.user

        if not user.is_authenticated and not user.is_staff:
            return False

        result = True
        for instance in obj:
            if instance.status:
                result = False
        return result
