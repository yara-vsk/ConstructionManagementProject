from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class CustomPermMixin(AccessMixin):
    """Verify that the current user has all specified permissions."""

    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """

        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()

        try:
            project_id=self.kwargs['pk_p']

        except KeyError:
            project_id = None

        if project_id:
            perms = perms + ('drawingdoc.project_' + str(project_id),)
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


