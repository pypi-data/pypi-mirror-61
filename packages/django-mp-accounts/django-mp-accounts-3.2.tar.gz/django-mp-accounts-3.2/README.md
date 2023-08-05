# MP-Accounts

Django accounts app.

### Installation

Install with pip:

```
pip install django-mp-accounts
```

Add accounts to urls.py:

```
urlpatterns += i18n_patterns(
    
    path('account/', include('apps.accounts.urls')),
    
)
```

Add accounts to settings.py:
```
INSTALLED_APPS = [
    'accounts',
]

LOGIN_REDIRECT_URL = '/'
```

### Profile model

models.py

```

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)

    mobile = models.CharField(_('Mobile number'), max_length=255, blank=True)

    address = models.CharField(_('Address'), max_length=255, blank=True)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):

    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)

```

urls.py

```
from accounts import urls


app_name = urls.app_name


urlpatterns = urls.urlpatterns + [
    # Custom patterns
]
```

Run migrations:
```
$ python manage.py migrate
```
