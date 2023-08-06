# django-readedit-switch-admin

Read item detail first, and click the Edit switch button to turn to edit view.


## Install

```shell
pip install django-readedit-switch-admin
```

## Usage

**pro/settings.py**

```python

INSTALLED_APPS = [
    ...
    'readedit_switch',
    ...
]
```

**app/admin.py**

```python
from django.contrib import admin
from .models import Category
from .models import Book

from readedit_switch.admin import ReadEditSwitchAdminMixin


class BookInline(admin.TabularInline):
    model = Book

class CategoryAdmin(ReadEditSwitchAdminMixin, admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        BookInline
    ]

admin.site.register(Category, CategoryAdmin)
```

## Releases

### v0.1.1 2020.02.20

- Fix add/change/delete permission problem in changelist view. Changelist view should obey the real permission.

### v0.1.0 2020.02.04

- First release.
