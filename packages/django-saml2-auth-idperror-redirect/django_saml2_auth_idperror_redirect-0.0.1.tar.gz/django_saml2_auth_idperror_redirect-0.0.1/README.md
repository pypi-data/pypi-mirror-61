# django-saml2-auth-idperror-redirect
A plugin to redirect users to a URL (usually the login page) in response to an authentication error in 
`django-saml2-auth`.

# Introduction

By default, `django-saml2-auth` redirects users to the `:denied` page in response to authentication errors.
`django-saml2-auth-idperror-redirect` will instead redirect the user to another URL (or view), usually the
login page. 

# Example

In settings.py:

    INSTALLED_APPS += (
        ...
        'django_saml2_auth',
        # ensure the plugin is loaded
        'django_saml2_auth_idperror_redirect',
        ...
    )
    
    # this is the "usual" config object from django-saml2-auth
    SAML2_AUTH = {
        'DEFAULT_NEXT_URL': '/',
        'PLUGINS': {
            # use this package in lieu of DEFAULT IDP Error plugin 
            'IDP_ERROR': ['REDIRECT'],
        },
        # must provide a URL or VIEW
        'IDP_ERROR_REDIRECT_VIEW': 'login',
        'IDP_ERROR_REDIRECT_URL': 'https://...',
    }
