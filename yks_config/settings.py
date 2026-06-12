
# from pathlib import Path
# from datetime import timedelta

# BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'youthkey-series-django-secret-key-2026-very-long-string'
# DEBUG = True
# # 2 DEBUG = False
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.16.39.74', '0.0.0.0', '*']
# # 3 ALLOWED_HOSTS = ['*']
# AUTH_USER_MODEL = 'accounts.User'
# LOGIN_URL = '/admin/login/'
# LOGIN_REDIRECT_URL = '/admin/'

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
# ]

# # ======================================================================
# #  INSTALLED APPS
# # ======================================================================
# INSTALLED_APPS = [
#     'jazzmin',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django_otp',
#     'django_otp.plugins.otp_totp',
#     'corsheaders',
#     # Custom Apps
#     'accounts',
#     'mentor_dashboard',
#     'mentorship',
#     'courses',          # ✅ Already present
#     'pages',
#     'payments',
#     'attendance',
#     'certificates',
#     'resources',
#     'marketplace',
#     'jobs',
#     'notifications',
#     'dashboards',
#     # Third-party
#     'rest_framework',
#     'rest_framework_simplejwt',
# ]

# # ======================================================================
# #  MIDDLEWARE
# # ======================================================================
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # ✅ MUST BE FIRST
#     'django.middleware.security.SecurityMiddleware',
#     # 4 'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'accounts.middleware.RoleBasedAccessMiddleware',
# ]

# ROOT_URLCONF = 'yks_config.urls'

# # ======================================================================
# #  TEMPLATES
# # ======================================================================
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': False,
#         'OPTIONS': {
#             'loaders': [
#                 'django.template.loaders.filesystem.Loader',
#                 'django.template.loaders.app_directories.Loader',
#             ],
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'yks_config.wsgi.application'

# # ======================================================================
# #  DATABASE
# # ======================================================================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 30,
#             'init_command': 'PRAGMA journal_mode=WAL;',
#         }
#     }
# }

# # ======================================================================
# #  PASSWORD VALIDATION
# # ======================================================================
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ======================================================================
# #  INTERNATIONALIZATION
# # ======================================================================
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'  # Change to 'Africa/Nairobi' if needed
# USE_I18N = True
# USE_TZ = True

# # ======================================================================
# #  STATIC & MEDIA FILES
# # ======================================================================
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# # STATIC_ROOT = BASE_DIR / 'staticfiles'

# MEDIA_URL = '/media/'                     # ✅ Already present
# MEDIA_ROOT = BASE_DIR / 'media'           # ✅ Already present

# # ✅ MISSING: Upload size limits (2 GB max for video uploads)
# DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024      # 2 GB
# FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024      # 2 GB

# # Optional: Allowed video extensions for extra validation
# ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ======================================================================
# #  CORS
# # ======================================================================
# CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_HEADERS = [
#     'accept',
#     'authorization',
#     'content-type',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# ]

# CORS_ALLOW_METHODS = [
#     'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
# ]

# # ======================================================================
# #  CSRF
# # ======================================================================
# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost",
#     "http://127.0.0.1",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
#     "http://localhost:*",
#     "http://127.0.0.1:*",
# ]

# # ======================================================================
# #  SESSION
# # ======================================================================
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 3600
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE = 'Lax'

# # ======================================================================
# #  JAZZMIN ADMIN THEME
# # ======================================================================
# JAZZMIN_SETTINGS = {
#     "site_title":   "Youth Key Admin",
#     "site_header":  "Youth Key Series",
#     "site_brand":   "Youth Key",
#     "welcome_sign": "Welcome back. Please sign in.",
#     "copyright":    "Youth Key Series 2026",
#     "site_logo":    None,
#     "search_model": ["accounts.User"],
#     "custom_css":   "css/jazzmin_custom.css",
#     "custom_js":    "js/youthkey.js",
#     "show_ui_builder":      False,
#     "navigation_expanded":  True,
#     "show_sidebar":         True,
#     "related_modal_active": True,
#     "changeform_format":    "horizontal_tabs",

#     "topmenu_links": [
#         {"name": "Dashboard", "url": "admin:index"},
#         {"name": "Users",     "url": "/admin/accounts/user/",    "permissions": ["accounts.view_user"]},
#         {"name": "Payments",  "url": "/admin/payments/payment/", "permissions": ["payments.view_payment"]},
#     ],
#     "usermenu_links": [
#         {"name": "My Profile", "url": "admin:accounts_user_change", "icon": "fas fa-user-circle"},
#         {"name": "Sign Out",   "url": "/admin/logout/",             "icon": "fas fa-sign-out-alt"},
#     ],
#     "custom_links": {
#         "pages": [
#             {"name": "Pages Dashboard", "url": "/admin/pages/pagesdashboard/", "icon": "fas fa-layer-group"},
#         ]
#     },
#     "order_with_respect_to": [
#         "accounts", "pages", "mentorship", "payments",
#         "attendance", "certificates", "jobs", "notifications",
#     ],
#     "hide_apps":   ["courses"],
#     "hide_models": [
#         "pages.homebanner", "pages.homefeaturedcourse", "pages.homesection",
#         "pages.coursecategory", "pages.infopage", "pages.sitesettings",
#         "pages.pagesdashboard", "pages.maindashboard",
#     ],
#     "icons": {
#         "accounts": "fas fa-users",
#         "accounts.user": "fas fa-user-shield",
#         "accounts.adminuser": "fas fa-user-shield",
#         "accounts.mentoruser": "fas fa-chalkboard-teacher",
#         "accounts.studentuser": "fas fa-user-graduate",
#         "auth": "fas fa-lock",
#         "auth.Group": "fas fa-users-cog",
#         "pages": "fas fa-layer-group",
#         "mentorship": "fas fa-chalkboard-teacher",
#         "mentorship.mentorshipsession": "fas fa-calendar-alt",
#         "mentorship.booking": "fas fa-bookmark",
#         "payments": "fas fa-credit-card",
#         "payments.payment": "fas fa-receipt",
#         "attendance": "fas fa-calendar-check",
#         "attendance.attendance": "fas fa-check-circle",
#         "certificates": "fas fa-certificate",
#         "jobs": "fas fa-briefcase",
#         "notifications": "fas fa-bell",
#     },
#     "default_icon_parents":  "fas fa-folder",
#     "default_icon_children": "fas fa-circle",
# }

# JAZZMIN_UI_TWEAKS = {
#     "navbar": "navbar-dark",
#     "navbar_small_text": False,
#     "no_navbar_border": True,
#     "navbar_fixed": True,
#     "sidebar": "sidebar-dark-primary",
#     "sidebar_fixed": True,
#     "sidebar_nav_small_text": False,
#     "sidebar_nav_child_indent": True,
#     "sidebar_nav_compact_style": True,
#     "sidebar_nav_flat_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_disable_expand": False,
#     "accent": "accent-warning",
#     "brand_colour": "navbar-dark",
#     "brand_small_text": False,
#     "body_small_text": False,
#     "footer_small_text": True,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "theme": "default",
#     "default_theme_mode": "light",
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-outline-info",
#         "warning": "btn-warning",
#         "danger": "btn-outline-danger",
#         "success": "btn-success",
#     },
# }

# # ======================================================================
# #  REST FRAMEWORK
# # ======================================================================
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
#     # ✅ Added: Pagination for list endpoints
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
#     # ✅ Added: Renderers & Parsers
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     ],
#     'DEFAULT_PARSER_CLASSES': [
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.FormParser',
#         'rest_framework.parsers.MultiPartParser',  # ✅ Required for video uploads
#     ],
# }

# # ======================================================================
# #  JWT (SimpleJWT)
# # ======================================================================
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME':  timedelta(hours=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS':  True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
# }

# # ======================================================================
# #  EMAIL
# # ======================================================================
# EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST          = 'smtp.gmail.com'
# EMAIL_PORT          = 587
# EMAIL_USE_TLS       = True
# EMAIL_HOST_USER     = 'danielamargret6@gmail.com'
# EMAIL_HOST_PASSWORD = 'mxwt jrmk fcvm sroz'
# DEFAULT_FROM_EMAIL  = 'Youth KEY Series <danielamargret6@gmail.com>'

# # ======================================================================
# #  DEVELOPMENT: SERVE MEDIA FILES (Optional)
# # ======================================================================
# # In urls.py (project level), add this for local dev:
# #
# # from django.conf import settings
# # from django.conf.urls.static import static
# #
# # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# #
# # ⚠️ In production, serve media via Nginx/Apache, NOT Django.

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
# 7SECRET_KEY = 'youthkey-series-django-secret-key-2026-very-long-string'
# DEBUG = True 2
DEBUG = False
# 3ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.16.39.74', '0.0.0.0', '*']
ALLOWED_HOSTS = ['yks-backend-v1.onrender.com', '127.0.0.1', 'localhost']
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ======================================================================
#  INSTALLED APPS
# ======================================================================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'corsheaders',
    # Custom Apps
    'accounts',
    'mentor_dashboard',
    'mentorship',
    'courses',          # ✅ Already present
    'pages',
    'payments',
    'attendance',
    'certificates',
    'resources',
    'marketplace',
    'jobs',
    'notifications',
    'dashboards',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
]

# ======================================================================
#  MIDDLEWARE
# ======================================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',#4
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.RoleBasedAccessMiddleware',
]

ROOT_URLCONF = 'yks_config.urls'

# ======================================================================
#  TEMPLATES
# ======================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yks_config.wsgi.application'

# ======================================================================
#  DATABASE
# ======================================================================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 30,
#             'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
#         }
#     }
# }
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 30,
                'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
            }
        }
    }

# ======================================================================
#  PASSWORD VALIDATION
# ======================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================================================================
#  INTERNATIONALIZATION
# ======================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Change to 'Africa/Nairobi' if needed
USE_I18N = True
USE_TZ = True

# ======================================================================
#  STATIC & MEDIA FILES
# ======================================================================

# STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ MISSING: Upload size limits (2 GB max for video uploads)
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024      # 2 GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024 * 1024      # 2 GB

# Optional: Allowed video extensions for extra validation
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================================================
#  CORS
# ======================================================================
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]


# ======================================================================
#  CSRF
# ======================================================================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:*",
    "http://127.0.0.1:*",
    "https://yks-backend-v1.onrender.com",
]

# ======================================================================
#  SESSION
# ======================================================================
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
# ======================================================================
#  JAZZMIN ADMIN THEME
# ======================================================================
JAZZMIN_SETTINGS = {
    "site_title":   "Youth Key Admin",
    "site_header":  "Youth Key Series",
    "site_brand":   "Youth Key",
    "welcome_sign": "Welcome back. Please sign in.",
    "copyright":    "Youth Key Series 2026",
    "site_logo":    None,
    "search_model": ["accounts.User"],
    "custom_css":   "css/jazzmin_custom.css",
    "custom_js":    "js/youthkey.js",
    "show_ui_builder":      False,
    "navigation_expanded":  True,
    "show_sidebar":         True,
    "related_modal_active": True,
    "changeform_format":    "horizontal_tabs",

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index"},
        {"name": "Users",     "url": "/admin/accounts/user/",    "permissions": ["accounts.view_user"]},
        {"name": "Payments",  "url": "/admin/payments/payment/", "permissions": ["payments.view_payment"]},
    ],

    "usermenu_links": [
    {"name": "My Profile", "url": "/admin/accounts/user/", "icon": "fas fa-user-circle"},
    {"name": "Sign Out",   "url": "/admin/logout/",        "icon": "fas fa-sign-out-alt"},
      ],
    # "usermenu_links": [
    #     {"name": "My Profile", "url": "admin:accounts_user_change", "icon": "fas fa-user-circle"},
    #     {"name": "Sign Out",   "url": "/admin/logout/",             "icon": "fas fa-sign-out-alt"},
    # ],

    # ── Sidebar menu order (controls what appears and in what order) ──
    "order_with_respect_to": [
        "accounts",
        "courses",
        "mentorship",
        "attendance",
        "payments",
        "certificates",
        "jobs",
        "notifications",
        "pages",
    ],

    # ── Nothing hidden globally — permissions handle access per role ──
    "hide_apps":   [],
    "hide_models": [
        "pages.homebanner",
        "pages.homefeaturedcourse",
        "pages.homesection",
        "pages.coursecategory",
        "pages.infopage",
        "pages.sitesettings",
        "pages.pagesdashboard",
        "pages.maindashboard",
    ],

    "icons": {
        # Accounts
        "accounts":              "fas fa-users",
        "accounts.user":         "fas fa-user-shield",
        "accounts.adminuser":    "fas fa-user-shield",
        "accounts.mentoruser":   "fas fa-chalkboard-teacher",
        "accounts.studentuser":  "fas fa-user-graduate",
        # Courses
        "courses":               "fas fa-book-open",
        "courses.course":        "fas fa-book",
        "courses.category":      "fas fa-tags",
        "courses.module":        "fas fa-layer-group",
        "courses.lesson":        "fas fa-play-circle",
        "courses.enrollment":    "fas fa-user-check",
        "courses.review":        "fas fa-star",
        # Mentorship
        "mentorship":                      "fas fa-chalkboard-teacher",
        "mentorship.mentorshipsession":    "fas fa-calendar-alt",
        "mentorship.booking":              "fas fa-bookmark",
        "mentorship.mentorshipvideo":      "fas fa-video",
        # Attendance
        "attendance":            "fas fa-calendar-check",
        "attendance.attendance": "fas fa-check-circle",
        # Payments
        "payments":              "fas fa-credit-card",
        "payments.payment":      "fas fa-receipt",
        # Others
        "certificates":          "fas fa-certificate",
        "jobs":                  "fas fa-briefcase",
        "notifications":         "fas fa-bell",
        "auth":                  "fas fa-lock",
        "auth.Group":            "fas fa-users-cog",
        "pages":                 "fas fa-layer-group",
    },

    "default_icon_parents":  "fas fa-folder",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark",
    "navbar_small_text": False,
    "no_navbar_border": True,
    "navbar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_fixed": True,
    "sidebar_nav_small_text": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_flat_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_disable_expand": False,
    "accent": "accent-warning",
    "brand_colour": "navbar-dark",
    "brand_small_text": False,
    "body_small_text": False,
    "footer_small_text": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "theme": "default",
    "default_theme_mode": "light",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-outline-info",
        "warning":   "btn-warning",
        "danger":    "btn-outline-danger",
        "success":   "btn-success",
    },
}
# # ======================================================================
# #  JAZZMIN ADMIN THEME
# # ======================================================================
# JAZZMIN_SETTINGS = {
#     "site_title":   "Youth Key Admin",
#     "site_header":  "Youth Key Series",
#     "site_brand":   "Youth Key",
#     "welcome_sign": "Welcome back. Please sign in.",
#     "copyright":    "Youth Key Series 2026",
#     "site_logo":    None,
#     "search_model": ["accounts.User"],
#     "custom_css":   "css/jazzmin_custom.css",
#     "custom_js":    "js/youthkey.js",
#     "show_ui_builder":      False,
#     "navigation_expanded":  True,
#     "show_sidebar":         True,
#     "related_modal_active": True,
#     "changeform_format":    "horizontal_tabs",

#     "topmenu_links": [
#         {"name": "Dashboard", "url": "admin:index"},
#         {"name": "Users",     "url": "/admin/accounts/user/",    "permissions": ["accounts.view_user"]},
#         {"name": "Payments",  "url": "/admin/payments/payment/", "permissions": ["payments.view_payment"]},
#     ],
#     "usermenu_links": [
#         {"name": "My Profile", "url": "admin:accounts_user_change", "icon": "fas fa-user-circle"},
#         {"name": "Sign Out",   "url": "/admin/logout/",             "icon": "fas fa-sign-out-alt"},
#     ],
#     "custom_links": {
#         "pages": [
#             {"name": "Pages Dashboard", "url": "/admin/pages/pagesdashboard/", "icon": "fas fa-layer-group"},
#         ]
#     },
#     "order_with_respect_to": [
#         "accounts", "pages", "mentorship", "payments",
#         "attendance", "certificates", "jobs", "notifications",
#     ],
#     "hide_apps":   ["courses"],
#     "hide_models": [
#         "pages.homebanner", "pages.homefeaturedcourse", "pages.homesection",
#         "pages.coursecategory", "pages.infopage", "pages.sitesettings",
#         "pages.pagesdashboard", "pages.maindashboard",
#     ],
#     "icons": {
#         "accounts": "fas fa-users",
#         "accounts.user": "fas fa-user-shield",
#         "accounts.adminuser": "fas fa-user-shield",
#         "accounts.mentoruser": "fas fa-chalkboard-teacher",
#         "accounts.studentuser": "fas fa-user-graduate",
#         "auth": "fas fa-lock",
#         "auth.Group": "fas fa-users-cog",
#         "pages": "fas fa-layer-group",
#         "mentorship": "fas fa-chalkboard-teacher",
#         "mentorship.mentorshipsession": "fas fa-calendar-alt",
#         "mentorship.booking": "fas fa-bookmark",
#         "payments": "fas fa-credit-card",
#         "payments.payment": "fas fa-receipt",
#         "attendance": "fas fa-calendar-check",
#         "attendance.attendance": "fas fa-check-circle",
#         "certificates": "fas fa-certificate",
#         "jobs": "fas fa-briefcase",
#         "notifications": "fas fa-bell",
#     },
#     "default_icon_parents":  "fas fa-folder",
#     "default_icon_children": "fas fa-circle",
# }

# JAZZMIN_UI_TWEAKS = {
#     "navbar": "navbar-dark",
#     "navbar_small_text": False,
#     "no_navbar_border": True,
#     "navbar_fixed": True,
#     "sidebar": "sidebar-dark-primary",
#     "sidebar_fixed": True,
#     "sidebar_nav_small_text": False,
#     "sidebar_nav_child_indent": True,
#     "sidebar_nav_compact_style": True,
#     "sidebar_nav_flat_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_disable_expand": False,
#     "accent": "accent-warning",
#     "brand_colour": "navbar-dark",
#     "brand_small_text": False,
#     "body_small_text": False,
#     "footer_small_text": True,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "theme": "default",
#     "default_theme_mode": "light",
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-outline-info",
#         "warning": "btn-warning",
#         "danger": "btn-outline-danger",
#         "success": "btn-success",
#     },
# }

# ======================================================================
#  REST FRAMEWORK
# ======================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    # ✅ Added: Pagination for list endpoints
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # ✅ Added: Renderers & Parsers
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # ✅ Required for video uploads
    ],
}

# ======================================================================
#  JWT (SimpleJWT)
# ======================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':  True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ======================================================================
#  EMAIL
# ======================================================================
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
# EMAIL_PORT          = 587
EMAIL_PORT    = 465
EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# EMAIL_USE_TLS       = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# 8EMAIL_HOST_USER     = 'danielamargret6@gmail.com'
# 9EMAIL_HOST_PASSWORD = 'mxwt jrmk fcvm sroz'
DEFAULT_FROM_EMAIL  = 'Youth KEY Series <danielamargret6@gmail.com>'

# ======================================================================
#  DEVELOPMENT: SERVE MEDIA FILES (Optional)
# ======================================================================
# In urls.py (project level), add this for local dev:
#
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# ⚠️ In production, serve media via Nginx/Apache, NOT Django.