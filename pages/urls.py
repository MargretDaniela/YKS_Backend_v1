# from django.urls import path
# from . import api

# urlpatterns = [
#     path("api/home/",             api.home_page_api,       name="api_home_page"),
#     path("api/categories/",       api.categories_page_api, name="api_page_categories"),
#     path("api/info/<slug:slug>/", api.info_page_api,       name="api_info_page"),
#     path("api/settings/",         api.site_settings_api,   name="api_site_settings"),
# ]

# C:\Users\Admin\Desktop\TheYKSApp\pages\urls.py
from django.urls import path
from . import api

urlpatterns = [
    # ── 🏠 HOME PAGE CONTENT ────────────────────────────────────
    path('home/', api.home_page_api, name='api_home_page'),
    
    # ── 📂 CATEGORIES PAGE ───────────────────────────────────────
    path('categories/', api.categories_page_api, name='api_page_categories'),
    
    # ── 📄 INFO PAGES (About, Terms, FAQ, etc.) ─────────────────
    path('info/<slug:slug>/', api.info_page_api, name='api_info_page'),
    
    # ── ⚙️ SITE SETTINGS ─────────────────────────────────────────
    path('settings/', api.site_settings_api, name='api_site_settings'),
]