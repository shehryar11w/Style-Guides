# Django Style Guide and Design Patterns

## Overview

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. This guide provides comprehensive style guidelines, directory patterns, and best practices for Django projects.

## Design Philosophy

- **DRY (Don't Repeat Yourself)**: Django emphasizes code reusability
- **Explicit is better than implicit**: Clear, readable code
- **Loose coupling**: Apps should be independent and reusable
- **Separation of concerns**: Models, views, and templates should be distinct

## Directory Structure

```
project_name/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── requirements-dev.txt               # Development dependencies
├── .env                               # Environment variables (not in git)
├── .gitignore                         # Git ignore rules
├── README.md                          # Project documentation
├── project_name/                      # Main project directory
│   ├── __init__.py
│   ├── settings/                      # Settings split by environment
│   │   ├── __init__.py
│   │   ├── base.py                   # Base settings
│   │   ├── development.py            # Development settings
│   │   ├── production.py             # Production settings
│   │   └── testing.py                # Testing settings
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI config for production
│   └── asgi.py                        # ASGI config for async
├── apps/                              # All Django apps
│   ├── __init__.py
│   ├── core/                         # Core/shared functionality
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── serializers.py           # If using DRF
│   │   ├── permissions.py
│   │   ├── exceptions.py
│   │   ├── utils.py
│   │   ├── managers.py
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── core/
│   │   ├── static/
│   │   │   └── core/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_utils.py
│   │   └── management/
│   │       └── commands/
│   └── [other_apps]/                 # Feature-specific apps
├── static/                           # Static files (collected)
├── media/                            # User-uploaded files
├── templates/                        # Global templates
│   ├── base.html
│   └── includes/
├── locale/                           # Translation files
└── docs/                             # Project documentation
```

### Directory Structure Explanation

- **`project_name/`**: Main project package containing settings and configuration
- **`apps/`**: All Django applications organized by feature/domain
- **`apps/core/`**: Shared utilities, base models, common functionality
- **`settings/`**: Split settings by environment for better configuration management
- **`static/`**: Collected static files (CSS, JS, images)
- **`media/`**: User-uploaded content
- **`templates/`**: Global template files and base templates
- **`locale/`**: Internationalization files

## Naming Conventions

### Files and Directories
- **Apps**: Use lowercase with underscores (`user_profile`, `blog_posts`)
- **Files**: Use lowercase with underscores (`user_views.py`, `blog_models.py`)
- **Classes**: Use PascalCase (`UserProfile`, `BlogPost`, `CustomManager`)
- **Functions/Methods**: Use snake_case (`get_user_profile`, `create_blog_post`)
- **Variables**: Use snake_case (`user_name`, `blog_title`)
- **Constants**: Use UPPER_SNAKE_CASE (`MAX_LENGTH`, `DEFAULT_SETTINGS`)

### Models
- **Model names**: Singular, PascalCase (`User`, `BlogPost`, `Comment`)
- **Field names**: snake_case (`first_name`, `created_at`, `is_active`)
- **Related names**: Use descriptive names (`author`, `blog_posts`, `comments`)

### URLs
- **URL patterns**: Use kebab-case in URLs (`/user-profile/`, `/blog-posts/`)
- **URL names**: Use snake_case (`user_profile_detail`, `blog_post_list`)

### Templates
- **Template files**: Use snake_case (`user_profile.html`, `blog_post_detail.html`)
- **Template directories**: Match app structure (`apps/blog/templates/blog/`)

## Code Style Guidelines

### Python Style
- Follow **PEP 8** guidelines
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **88 characters** (Black formatter default)
- Use **double quotes** for strings (or follow project consistency)
- Import order: Standard library → Third-party → Local imports

### Django-Specific Style
- Use **explicit imports** instead of `from django.db import *`
- Prefer **class-based views** for complex views, function-based for simple ones
- Use **queryset methods** instead of Python loops when possible
- Always use **select_related** and **prefetch_related** for related objects

### Example Code Style

```python
# Good
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
    """Blog post model with author and content."""
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title

# Bad
from django.db import models
from django.contrib.auth.models import User

class blogpost(models.Model):  # Wrong naming
    Title=models.CharField(max_length=200)  # Wrong style
    content=models.TextField()  # Missing spaces
    author=models.ForeignKey(User,on_delete=models.CASCADE)  # Poor formatting
```

## Component Patterns

### Models Pattern

```python
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class CustomManager(models.Manager):
    """Custom manager with common queryset methods."""
    
    def active(self):
        return self.filter(is_active=True)
    
    def recent(self):
        return self.order_by('-created_at')
```

### Views Pattern

#### Class-Based Views (Preferred for complex views)

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    """List view for blog posts."""
    
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.active().select_related('author')


class BlogPostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create view for blog posts."""
    
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_message = 'Blog post created successfully!'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

#### Function-Based Views (For simple views)

```python
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BlogPost


@login_required
def blog_post_detail(request, pk):
    """Detail view for a blog post."""
    post = get_object_or_404(
        BlogPost.objects.select_related('author'),
        pk=pk,
        is_published=True
    )
    return render(request, 'blog/blogpost_detail.html', {'post': post})
```

### Forms Pattern

```python
from django import forms
from django.core.exceptions import ValidationError
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Form for creating/editing blog posts."""
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError('Title must be at least 10 characters.')
        return title
```

### Admin Pattern

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin configuration for BlogPost model."""
    
    list_display = ['title', 'author', 'created_at', 'is_published', 'actions']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Metadata', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )
    
    def actions(self, obj):
        return format_html(
            '<a href="/admin/blog/blogpost/{}/change/">Edit</a>',
            obj.pk
        )
    actions.short_description = 'Actions'
```

## State Management

Django doesn't use client-side state management like React. Instead, state is managed through:

### Session Management

```python
# Storing in session
request.session['key'] = 'value'

# Retrieving from session
value = request.session.get('key', 'default')
```

### Context Processors (Global template context)

```python
# apps/core/context_processors.py
def site_settings(request):
    return {
        'site_name': 'My Site',
        'site_url': 'https://example.com'
    }

# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'apps.core.context_processors.site_settings',
        ],
    },
}]
```

## Routing Patterns

### URL Configuration

```python
# project_name/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    path('', include('apps.blog.urls')),
]

# apps/blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='list'),
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='detail'),
    path('create/', views.BlogPostCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete'),
]
```

### URL Naming Best Practices
- Use `app_name` for namespacing
- Use descriptive URL names
- Keep URLs RESTful when possible
- Use path parameters for resource IDs

## API Integration

### Django REST Framework Pattern

```python
# apps/api/serializers.py
from rest_framework import serializers
from apps.blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model."""
    
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'author_name', 
                  'created_at', 'is_published']
        read_only_fields = ['author', 'created_at']

# apps/api/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """ViewSet for BlogPost model."""
    
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        return Response({'status': 'published'})
```

### Error Handling

```python
# apps/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """Custom exception handler for API."""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', 'An error occurred'),
                'data': response.data
            }
        }
        response.data = custom_response_data
    
    return response
```

## Testing Patterns

### Test Structure

```python
# apps/blog/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from apps.blog.models import BlogPost


class BlogPostModelTest(TestCase):
    """Test cases for BlogPost model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_post_creation(self):
        """Test blog post creation."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertFalse(self.post.is_published)
    
    def test_post_str_representation(self):
        """Test string representation of blog post."""
        self.assertEqual(str(self.post), 'Test Post')

# apps/blog/tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.blog.models import BlogPost


class BlogPostViewTest(TestCase):
    """Test cases for blog post views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_list_view(self):
        """Test blog post list view."""
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_detail_view(self):
        """Test blog post detail view."""
        response = self.client.get(
            reverse('blog:detail', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
```

### Test Organization
- One test file per module (`test_models.py`, `test_views.py`, `test_forms.py`)
- Use descriptive test method names (`test_post_creation`, `test_user_can_create_post`)
- Use `setUp` and `tearDown` for common test data
- Test both success and failure cases

## Best Practices

### Security
- Always use `@login_required` or `LoginRequiredMixin` for protected views
- Use Django's built-in CSRF protection
- Validate and sanitize all user input
- Use `get_object_or_404` instead of `Model.objects.get()` to avoid exceptions
- Never commit secrets to version control (use environment variables)

### Performance
- Use `select_related()` for ForeignKey relationships
- Use `prefetch_related()` for ManyToMany and reverse ForeignKey
- Use database indexes for frequently queried fields
- Implement pagination for list views
- Use `only()` and `defer()` to limit queried fields

### Code Organization
- Keep apps focused on a single feature/domain
- Use `apps/` directory to organize all Django apps
- Split settings by environment
- Create reusable utilities in `core` app
- Use custom managers for common queryset operations

### Database
- Always create migrations for model changes
- Use `null=True` and `blank=True` appropriately
- Set appropriate `max_length` for CharField
- Use `db_index=True` for frequently queried fields
- Consider using `db_table` for custom table names

## Common Patterns

### Custom Manager Pattern

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class BlogPost(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    # ... fields
```

### Signal Pattern

```python
# apps/blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def notify_on_publish(sender, instance, created, **kwargs):
    if instance.is_published and not created:
        # Send notification
        pass
```

### Middleware Pattern

```python
# apps/core/middleware.py
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code executed before view
        response = self.get_response(request)
        # Code executed after view
        return response
```

## Dependencies

### Core Dependencies
- **Django**: 4.2+ (LTS version recommended)
- **python-decouple**: For environment variable management
- **django-environ**: Alternative to python-decouple

### Development Dependencies
- **black**: Code formatter
- **flake8**: Linter
- **pytest-django**: Testing framework
- **django-debug-toolbar**: Development debugging

### Production Dependencies
- **gunicorn**: WSGI HTTP server
- **whitenoise**: Static file serving
- **psycopg2-binary**: PostgreSQL adapter (if using PostgreSQL)

### Example requirements.txt

```
Django==4.2.7
python-decouple==3.8
django-cors-headers==4.3.1
djangorestframework==3.14.0
```

### Example requirements-dev.txt

```
black==23.11.0
flake8==6.1.0
pytest-django==4.7.0
django-debug-toolbar==4.2.0
```

## Additional Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) (Book)

