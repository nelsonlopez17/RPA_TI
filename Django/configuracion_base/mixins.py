from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages

class RoleRequiredMixin(AccessMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
            
        user_groups = request.user.groups.values_list('name', flat=True)
        if any(role in user_groups for role in self.allowed_roles):
            return super().dispatch(request, *args, **kwargs)
            
        messages.error(request, "No tienes permiso para acceder a este módulo.")
        return redirect('home')
