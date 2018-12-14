from rest_framework.permissions import BasePermission


class GradePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.grade < obj.user.grade or obj.user == request.user
