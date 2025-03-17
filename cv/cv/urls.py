# """
# URL configuration for cv project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from ..pdf.views import accept
# from ..pdf.views import create_cv
# from . import views
from .views import contact_view, share_cv_email, create_cv, resume, accept


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accept, name="accept"),
    path('<int:id>/', resume, name="resume"),
    path('list/', list, name="list"),
    path('contact/', contact_view, name='contact'),
    # path('contact/', views.contact_view, name='contact'),
    path('accept/', accept, name='accept'),
    path('share-cv/<int:cv_id>/', share_cv_email, name='share_cv_email'),
    path('resume/<int:id>/', resume, name='resume'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
