# from django.db import models


# class OrderedModel(models.Model):
#     order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

#     class Meta:
#         abstract = True
#         ordering = ["order"]


# # =====================================================================
# # HOME SCREEN
# # =====================================================================

# class HomeBanner(OrderedModel):
#     title       = models.CharField(max_length=255)
#     subtitle    = models.CharField(max_length=500, blank=True)
#     image       = models.ImageField(upload_to="pages/home/banners/", blank=True)
#     button_text = models.CharField(max_length=100, blank=True)
#     button_link = models.CharField(max_length=500, blank=True)
#     is_active   = models.BooleanField(default=True)

#     class Meta(OrderedModel.Meta):
#         verbose_name        = "Home Banner"
#         verbose_name_plural = "Home Banners"

#     def __str__(self): return self.title


# class HomeFeaturedCourse(OrderedModel):
#     course    = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="featured_on_home")
#     label     = models.CharField(max_length=100, blank=True, help_text="e.g. 'Top Pick', 'New'")
#     is_active = models.BooleanField(default=True)

#     class Meta(OrderedModel.Meta):
#         verbose_name        = "Home Featured Course"
#         verbose_name_plural = "Home Featured Courses"

#     def __str__(self): return f"{self.course.title} (featured)"


# class HomeSection(OrderedModel):
#     title     = models.CharField(max_length=255)
#     subtitle  = models.CharField(max_length=500, blank=True)
#     is_active = models.BooleanField(default=True)

#     class Meta(OrderedModel.Meta):
#         verbose_name        = "Home Section"
#         verbose_name_plural = "Home Sections"

#     def __str__(self): return self.title


# # =====================================================================
# # COURSES SCREEN
# # =====================================================================

# class CourseCategory(OrderedModel):
#     name        = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     icon        = models.CharField(max_length=100, blank=True)
#     image       = models.ImageField(upload_to="pages/courses/categories/", blank=True)
#     is_active   = models.BooleanField(default=True)

#     class Meta(OrderedModel.Meta):
#         verbose_name        = "Course Category"
#         verbose_name_plural = "Course Categories"

#     def __str__(self): return self.name


# # =====================================================================
# # INFO PAGES (About, Terms, Privacy, FAQ, Contact, Course pages)
# # =====================================================================

# class InfoPage(models.Model):
#     PAGE_CHOICES = [
#         ("about",    "About Us"),
#         ("terms",    "Terms & Conditions"),
#         ("privacy",  "Privacy Policy"),
#         ("faq",      "FAQ"),
#         ("contact",  "Contact Us"),
#         ("custom",   "Custom Page"),
#     ]
#     slug       = models.SlugField(unique=True)
#     page_type  = models.CharField(max_length=20, choices=PAGE_CHOICES, default="custom")
#     title      = models.CharField(max_length=255)
#     body       = models.TextField()
#     image      = models.ImageField(upload_to="pages/info/", blank=True)
#     is_active  = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name        = "Info Page"
#         verbose_name_plural = "Info Pages"

#     def __str__(self): return self.title


# # =====================================================================
# # SITE SETTINGS — singleton
# # =====================================================================

# class SiteSettings(models.Model):
#     app_name            = models.CharField(max_length=100, default="Youth K.E.Y Series")
#     tagline             = models.CharField(max_length=255, blank=True)
#     logo                = models.ImageField(upload_to="pages/settings/", blank=True)
#     support_email       = models.EmailField(blank=True)
#     support_phone       = models.CharField(max_length=30, blank=True)
#     facebook_url        = models.URLField(blank=True)
#     twitter_url         = models.URLField(blank=True)
#     instagram_url       = models.URLField(blank=True)
#     whatsapp_number     = models.CharField(max_length=30, blank=True)
#     maintenance_mode    = models.BooleanField(default=False)
#     maintenance_message = models.TextField(blank=True)

#     class Meta:
#         verbose_name        = "Site Settings"
#         verbose_name_plural = "Site Settings"

#     def __str__(self): return "Site Settings"

#     def save(self, *args, **kwargs):
#         self.pk = 1
#         super().save(*args, **kwargs)

#     @classmethod
#     def get(cls):
#         obj, _ = cls.objects.get_or_create(pk=1)
#         return obj

# # courses/models.py (or pages/models.py)
# class Banner(models.Model):
#     LINK_TYPES = [
#         ('course', 'Course'),
#         ('category', 'Category'),
#         ('external', 'External URL'),
#     ]
    
#     title = models.CharField(max_length=200)
#     subtitle = models.CharField(max_length=300, blank=True)
#     image = models.ImageField(upload_to='banners/')
#     button_text = models.CharField(max_length=50, blank=True)
    
#     # Link configuration
#     link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='course')
#     course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.SET_NULL)
#     category_slug = models.CharField(max_length=100, blank=True)
#     external_url = models.URLField(blank=True)
    
#     order = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)
    
#     class Meta:
#         ordering = ['order']
    
#     def __str__(self):
#         return self.title

# C:\Users\Admin\Desktop\TheYKSApp\pages\models.py
from django.db import models


# =====================================================================
#  ABSTRACT BASE: OrderedModel (for consistent ordering)
# =====================================================================
class OrderedModel(models.Model):
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        abstract = True
        ordering = ["order"]


# =====================================================================
#  HOME SCREEN MODELS
# =====================================================================

class HomeBanner(OrderedModel):
    """
    Banner displayed on home page — now with CLICKABLE support!
    Supports linking to: Course, Category, or External URL
    """
    
    LINK_TYPES = [
        ('course', 'Course'),
        ('category', 'Category'),
        ('external', 'External URL'),
    ]
    
    title       = models.CharField(max_length=255)
    subtitle    = models.CharField(max_length=500, blank=True)
    image       = models.ImageField(upload_to="pages/home/banners/", blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Optional: URL path like '/course/123/' or external link"
    )
    is_active   = models.BooleanField(default=True)

    # ✅ NEW: Link configuration for clickable banners
    link_type = models.CharField(
        max_length=20, 
        choices=LINK_TYPES, 
        default='course',
        help_text="What happens when user taps this banner?"
    )
    
    # ✅ Link to a specific course (preferred method)
    linked_course = models.ForeignKey(
        'courses.Course',  # ← Correct: 'app_label.ModelName'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='home_banners',
        help_text="If set, tapping banner opens this course (overrides button_link)"
    )
    
    # ✅ Link to a category (fallback if no course)
    category_slug = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Category slug for category links (e.g., 'personal-development')"
    )
    
    # ✅ External URL support
    external_url = models.URLField(
        blank=True, 
        help_text="Full URL for external links (e.g., https://youtube.com/...)"
    )

    class Meta(OrderedModel.Meta):
        verbose_name        = "Home Banner"
        verbose_name_plural = "Home Banners"

    def __str__(self):
        return self.title


class HomeFeaturedCourse(OrderedModel):
    """Featured course slot on home page"""
    course    = models.ForeignKey(
        "courses.Course", 
        on_delete=models.CASCADE, 
        related_name="featured_on_home"
    )
    label     = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="e.g. 'Top Pick', 'New', 'Bestseller'"
    )
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name        = "Home Featured Course"
        verbose_name_plural = "Home Featured Courses"

    def __str__(self):
        return f"{self.course.title} (featured)"


class HomeSection(OrderedModel):
    """Content section on home page"""
    title     = models.CharField(max_length=255)
    subtitle  = models.CharField(max_length=500, blank=True)
    content   = models.TextField(blank=True, help_text="Optional rich text content")
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name        = "Home Section"
        verbose_name_plural = "Home Sections"

    def __str__(self):
        return self.title


# =====================================================================
#  COURSES SCREEN MODELS
# =====================================================================

class CourseCategory(OrderedModel):
    """Category for grouping courses"""
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon        = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Material Icon name (e.g., 'self_improvement')"
    )
    image       = models.ImageField(
        upload_to="pages/courses/categories/", 
        blank=True, 
        null=True
    )
    is_active   = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name        = "Course Category"
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.name


# =====================================================================
#  INFO PAGES (About, Terms, Privacy, FAQ, Contact, etc.)
# =====================================================================

class InfoPage(models.Model):
    PAGE_CHOICES = [
        ("about",    "About Us"),
        ("terms",    "Terms & Conditions"),
        ("privacy",  "Privacy Policy"),
        ("faq",      "FAQ"),
        ("contact",  "Contact Us"),
        ("custom",   "Custom Page"),
    ]
    slug       = models.SlugField(unique=True)
    page_type  = models.CharField(max_length=20, choices=PAGE_CHOICES, default="custom")
    title      = models.CharField(max_length=255)
    body       = models.TextField()
    image      = models.ImageField(upload_to="pages/info/", blank=True, null=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Info Page"
        verbose_name_plural = "Info Pages"

    def __str__(self):
        return self.title


# =====================================================================
#  SITE SETTINGS — Singleton pattern (only one instance)
# =====================================================================

class SiteSettings(models.Model):
    app_name            = models.CharField(max_length=100, default="Youth K.E.Y Series")
    tagline             = models.CharField(max_length=255, blank=True)
    logo                = models.ImageField(upload_to="pages/settings/", blank=True, null=True)
    support_email       = models.EmailField(blank=True)
    support_phone       = models.CharField(max_length=30, blank=True)
    facebook_url        = models.URLField(blank=True)
    twitter_url         = models.URLField(blank=True)
    instagram_url       = models.URLField(blank=True)
    whatsapp_number     = models.CharField(max_length=30, blank=True)
    maintenance_mode    = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)

    class Meta:
        verbose_name        = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        """Get or create the singleton instance"""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj