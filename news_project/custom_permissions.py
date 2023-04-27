from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyLoggedSuperUser(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    # other methods and attributes here
   