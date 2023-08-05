===============================
Backstage OAuth2
===============================

Introduction
============

- Inclua no seu requirements
- Inclua o código no seu urls.py
```python
from backstage_oauth2.views import BackstageOAuthRedirect
# admin.site.login deve vir depois do admin.autodiscover()
admin.site.login = BackstageOAuthRedirect.as_view(provider='backstage')
urlpatterns += patterns(
        '',
        url(r'^accounts/', include('backstage_oauth2.urls')),
)
```

- Adicione no INSTALLED_APPS:
```
    'allaccess',
    'backstage_oauth2'
```

- No settings, adicionar no AUTHENTICATION_BACKENDS:
```python
    AUTHENTICATION_BACKENDS = [
        'allaccess.backends.AuthorizedServiceBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]
```

- Crie um arquivo json para o provider backstage. Ex de dev:
```json
    [
        {
            "pk": 1,
            "model": "allaccess.provider",
            "fields": {
                "name": "backstage",
                "authorization_url": "https://accounts.backstage.dev.globoi.com/authorize",
                "secret": "SEU SECRET",
                "access_token_url": "https://accounts.backstage.dev.globoi.com/token",
                "key": "SEU KEY",
                "request_token_url": "",
                "profile_url": "https://accounts.backstage.dev.globoi.com/user"
            }
        }
    ]
```

- Carregue o json
```
    ./manage.py loaddata caminho/para/seu/arquivo.json
```

* Free software: BSD license

Features
--------

* TODO
- Fazer integração com a barra do backstage

