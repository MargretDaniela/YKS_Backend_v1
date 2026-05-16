# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from .models import (
#     HomeBanner, HomeFeaturedCourse, HomeSection,
#     CourseCategory, InfoPage, SiteSettings,
# )


# def _abs(request, image):
#     if image:
#         return request.build_absolute_uri(image.url)
#     return None


# # GET /pages/api/home/
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def home_page_api(request):
#     banners  = HomeBanner.objects.filter(is_active=True)
#     featured = HomeFeaturedCourse.objects.filter(is_active=True).select_related("course", "course__trainer")
#     sections = HomeSection.objects.filter(is_active=True)

#     return Response({
#         "success": True,
#         "banners": [
#             {
#                 "id":          b.pk,
#                 "title":       b.title,
#                 "subtitle":    b.subtitle,
#                 "image":       _abs(request, b.image),
#                 "button_text": b.button_text,
#                 "button_link": b.button_link,
#                 "order":       b.order,
#             }
#             for b in banners
#         ],
#         "featured_courses": [
#             {
#                 "id":    f.pk,
#                 "label": f.label,
#                 "order": f.order,
#                 "course": {
#                     "id":         f.course.pk,
#                     "title":      f.course.title,
#                     "category":   f.course.category,
#                     "price":      f"US${float(f.course.price):.2f}",
#                     "instructor": f.course.trainer.full_name if hasattr(f.course.trainer, "full_name") else str(f.course.trainer),
#                     "thumbnail":  _abs(request, f.course.thumbnail),
#                 },
#             }
#             for f in featured
#         ],
#         "sections": [
#             {"id": s.pk, "title": s.title, "subtitle": s.subtitle, "order": s.order}
#             for s in sections
#         ],
#     })


# # GET /pages/api/categories/
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def categories_page_api(request):
#     cats = CourseCategory.objects.filter(is_active=True)
#     return Response({
#         "success": True,
#         "categories": [
#             {
#                 "id":          c.pk,
#                 "name":        c.name,
#                 "description": c.description,
#                 "icon":        c.icon,
#                 "image":       _abs(request, c.image),
#                 "order":       c.order,
#             }
#             for c in cats
#         ],
#     })


# # GET /pages/api/info/<slug>/
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def info_page_api(request, slug):
#     try:
#         page = InfoPage.objects.get(slug=slug, is_active=True)
#     except InfoPage.DoesNotExist:
#         return Response({"success": False, "error": "Page not found."}, status=404)

#     return Response({
#         "success": True,
#         "page": {
#             "id":        page.pk,
#             "title":     page.title,
#             "slug":      page.slug,
#             "page_type": page.page_type,
#             "body":      page.body,
#             "image":     _abs(request, page.image),
#             "updated_at": str(page.updated_at),
#         },
#     })


# # GET /pages/api/settings/
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def site_settings_api(request):
#     s = SiteSettings.get()
#     return Response({
#         "success": True,
#         "settings": {
#             "app_name":            s.app_name,
#             "tagline":             s.tagline,
#             "logo":                _abs(request, s.logo),
#             "support_email":       s.support_email,
#             "support_phone":       s.support_phone,
#             "facebook_url":        s.facebook_url,
#             "twitter_url":         s.twitter_url,
#             "instagram_url":       s.instagram_url,
#             "whatsapp_number":     s.whatsapp_number,
#             "maintenance_mode":    s.maintenance_mode,
#             "maintenance_message": s.maintenance_message,
#         },
#     })


# C:\Users\Admin\Desktop\TheYKSApp\pages\api.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.urls import resolve
from urllib.parse import urlparse, parse_qs

# Your existing models
from .models import (
    HomeBanner, HomeFeaturedCourse, HomeSection,
    CourseCategory, InfoPage, SiteSettings,
)

# Import Course model and helper from courses app
from courses.models import Course
# ✅ New
from courses.api import _course_dict

def _abs(request, image):
    """Helper to build absolute URL for images"""
    if image:
        return request.build_absolute_uri(image.url)
    return None


def _extract_course_id_from_link(button_link, request=None):
    """
    Extract course_id from button_link if it's a course URL.
    Supports formats:
    - '/course/123/'
    - '/courses/api/courses/123/'
    - 'https://yoursite.com/course/123/'
    Returns course_id as int or None.
    """
    if not button_link:
        return None
    
    # Parse the URL
    parsed = urlparse(button_link)
    path = parsed.path
    
    # Pattern 1: /course/123/ or /courses/123/
    if '/course/' in path:
        parts = path.strip('/').split('/')
        try:
            idx = parts.index('course')
            if idx + 1 < len(parts):
                return int(parts[idx + 1])
        except (ValueError, IndexError):
            pass
    
    # Pattern 2: /courses/api/courses/123/
    if 'courses' in path and 'api' in path:
        parts = path.strip('/').split('/')
        try:
            idx = parts.index('courses')
            if idx + 2 < len(parts) and parts[idx + 1] == 'api':
                return int(parts[idx + 2])
        except (ValueError, IndexError):
            pass
    
    # Pattern 3: Query param ?course_id=123
    query_params = parse_qs(parsed.query)
    if 'course_id' in query_params:
        try:
            return int(query_params['course_id'][0])
        except (ValueError, IndexError):
            pass
    
    return None


# ======================================================================
# GET /pages/api/home/ — WITH CLICKABLE BANNERS
# ======================================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def home_page_api(request):
    banners  = HomeBanner.objects.filter(is_active=True).order_by('order')
    featured = HomeFeaturedCourse.objects.filter(is_active=True).select_related("course", "course__trainer")
    sections = HomeSection.objects.filter(is_active=True).order_by('order')

    return Response({
        "success": True,
        "banners": [
            {
                "id":          b.pk,
                "title":       b.title,
                "subtitle":    b.subtitle,
                "image":       _abs(request, b.image),
                "button_text": b.button_text,
                "button_link": b.button_link,
                "order":       b.order,
                # ✅ NEW: Add course_id for clickable banners
                "course_id":   _extract_course_id_from_link(b.button_link, request),
                # Optional: Add link_type for frontend logic
                "link_type":   "course" if _extract_course_id_from_link(b.button_link) else 
                               ("external" if b.button_link and b.button_link.startswith('http') else "internal"),
            }
            for b in banners
        ],
        "featured_courses": [
            {
                "id":    f.pk,
                "label": f.label,
                "order": f.order,
                # ✅ Use your existing _course_dict for full course data
                "course": _course_dict(f.course, request),
            }
            for f in featured
        ],
        "sections": [
            {
                "id": s.pk, 
                "title": s.title, 
                "subtitle": s.subtitle, 
                "order": s.order,
                # Optional: Add content/body if your sections have it
                "content": getattr(s, 'content', None),
            }
            for s in sections
        ],
    })


# ======================================================================
# GET /pages/api/categories/ — UNCHANGED
# ======================================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def categories_page_api(request):
    cats = CourseCategory.objects.filter(is_active=True).order_by('order')
    return Response({
        "success": True,
        "categories": [
            {
                "id":          c.pk,
                "name":        c.name,
                "description": c.description,
                "icon":        c.icon,
                "image":       _abs(request, c.image),
                "order":       c.order,
            }
            for c in cats
        ],
    })


# ======================================================================
# GET /pages/api/info/<slug>/ — UNCHANGED
# ======================================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def info_page_api(request, slug):
    try:
        page = InfoPage.objects.get(slug=slug, is_active=True)
    except InfoPage.DoesNotExist:
        return Response({"success": False, "error": "Page not found."}, status=404)

    return Response({
        "success": True,
        "page": {
            "id":         page.pk,
            "title":      page.title,
            "slug":       page.slug,
            "page_type":  page.page_type,
            "body":       page.body,
            "image":      _abs(request, page.image),
            "updated_at": str(page.updated_at),
        },
    })


# ======================================================================
# GET /pages/api/settings/ — UNCHANGED
# ======================================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def site_settings_api(request):
    s = SiteSettings.get()
    return Response({
        "success": True,
        "settings": {
            "app_name":            s.app_name,
            "tagline":             s.tagline,
            "logo":                _abs(request, s.logo),
            "support_email":       s.support_email,
            "support_phone":       s.support_phone,
            "facebook_url":        s.facebook_url,
            "twitter_url":         s.twitter_url,
            "instagram_url":       s.instagram_url,
            "whatsapp_number":     s.whatsapp_number,
            "maintenance_mode":    s.maintenance_mode,
            "maintenance_message": s.maintenance_message,
        },
    })