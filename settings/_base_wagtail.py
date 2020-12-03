"""
http://docs.wagtail.io/en/latest/advanced_topics/settings.html
"""
from ._base_django import *

INSTALLED_APPS+= [
    'modelcluster',
    'taggit',

    'wagtail.contrib.modeladmin',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
]

MIDDLEWARE+= [
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]


WAGTAIL_SITE_NAME = 'site name'
