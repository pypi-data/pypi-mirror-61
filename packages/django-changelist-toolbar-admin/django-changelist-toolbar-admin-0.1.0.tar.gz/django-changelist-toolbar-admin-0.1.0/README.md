# django-changelist-toolbar-admin

Provides custom button management function on changelist page of django admin site.

## Install

```shell
pip install django-changelist-toolbar-admin
```

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'fontawesome',
    'changelist_toolbar',
    ...
]
```

**app/admin.py**

```python
from django.contrib import admin
from changelist_toolbar.admin import ChangelistToolbarAdminMixin
from .models import Category


class CategoryAdmin(ChangelistToolbarAdminMixin, admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    changelist_toolbar_buttons = [
        "export",
        "say_hi",
    ]

    def export(self, request):
        return "/export"
    export.title = "Export"
    export.icon = "fas fa-file-export"
    export.target = "_blank"
    
    def say_hi(self, request):
        return {
            "href": "javascript:alert('hi');",
            "title": "Say Hi",
            "icon": "fas fa-music",
        } 

admin.site.register(Category, CategoryAdmin)
```

## Releases

### v0.1.0 2020/02/13

- First release.
