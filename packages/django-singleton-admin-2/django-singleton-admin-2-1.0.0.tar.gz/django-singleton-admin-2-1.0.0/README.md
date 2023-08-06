# Django Singleton Admin
In dynamic applications, it can be somewhat of a pain to have static settings that *have* to be set in `settings.py`. Django Singleton Admin adds an easy way to edit singleton models (e.g a SiteSetting model) to allow administrators to change configuration on the fly.

This is great for things like OAuth settings for third parties, or dynamic settings that you need to pull for your site. 

# Example
```
# models.py
from django.db import models

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=32)
    site_domain = models.CharField(max_length=32)
    site_description = models.CharField(max_length=32)

    @staticmethod
    def get_instance():
        return SiteSettings.objects.get_or_create(pk=0)
        
    def __str__(self):
        return "Site settings"
```

```
# admin.py
from django.contrib import admin

admin.site.register(SiteSettings, DjangoSingletonAdmin)
```