
# from django.urls import path
# from . import views, api

# urlpatterns = [
#     path("no-access/",              views.no_access_view,         name="no_access"),

#     # ── Auth ──────────────────────────────────────────────────────────
#     path("api/register/",           api.register_api,             name="api_register"),
#     path("api/login/",              api.login_api,                name="api_login"),
#     path("api/verify-otp/",         api.verify_otp_api,           name="api_verify_otp"),
#     path("api/resend-otp/",         api.resend_otp_api,           name="api_resend_otp"),
#     path("api/refresh/",            api.refresh_token_api,        name="api_refresh"),
#     path("api/me/",                 api.me_api,                   name="api_me"),

#     # ── Forgot Password ───────────────────────────────────────────────
#     path("api/forgot-password/",    api.forgot_password_api,      name="api_forgot_password"),
#     path("api/verify-reset-otp/",   api.verify_reset_otp_api,     name="api_verify_reset_otp"),
#     path("api/reset-password/",     api.reset_password_api,       name="api_reset_password"),
# ]

# C:\Users\Admin\Desktop\TheYKSApp\accounts\urls.py
from django.urls import path
from . import api

urlpatterns = [
    path('register/', api.register_api, name='api_register'),
    path('login/', api.login_api, name='api_login'),
    path('me/', api.me_api, name='api_me'),
    path('refresh/', api.refresh_token_api, name='api_refresh'),
    path('verify-otp/', api.verify_otp_api, name='api_verify_otp'),
    path('resend-otp/', api.resend_otp_api, name='api_resend_otp'),
    path('forgot-password/', api.forgot_password_api, name='api_forgot_password'),
    path('verify-reset-otp/', api.verify_reset_otp_api, name='api_verify_reset_otp'),
    path('reset-password/', api.reset_password_api, name='api_reset_password'),
]