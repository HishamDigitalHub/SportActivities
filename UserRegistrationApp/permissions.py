from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOrReadOnly(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_method:
            return obj.created_by == request.user
        return True


class IsMainUserOrReadOnly(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT']

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeamAdminOrReadOnly(BasePermission):
    message = 'you must be the admin of this team'
    safe_method = ['PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_method:
            return obj.team.admin == request.user
        return True


class IsVenueAdminOrReadOnly(BasePermission):
    message = 'you must be the admin of this venue'
    safe_method = ['PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_method:
            return obj.venue.admin == request.user
        return True


class IsProfileOwnerOrReadOnly(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT']

    # to make always unavailable
    # def has_permission(self, request, view):
    #     if request.method in self.safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AllowAnonymous(BasePermission):
    message = "you cant create user"
    safe_method = ['POST']

    def has_permission(self, request, view):
        if request.method in self.safe_method:

                return True
        return True


class IsRelatedWithInvitation(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        if obj.from_user == request.user:
            return True
        elif obj.to_user == request.user:
            return True
        else:
            return False


class IsPlayerInActivity(BasePermission):
    message = 'you must a member of this activity'
    safe_method = ['GET', 'POST']

    def has_object_permission(self, request, view, obj):
        if request.user in obj.activity.players:
            return False
        return False
        # request.user in view.instance.activity.players  # and request.user.is_staff


class IsPlayerInTeam(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT', 'POST']

    # to make always unavailable
    # def has_permission(self, request, view):
    #     if request.method in self.safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        return obj.players == request.user.id


class IsMyInvitationRequest(BasePermission):
    message = 'you must be the owner of the object'
    safe_method = ['PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        return obj.from_user == request.user
