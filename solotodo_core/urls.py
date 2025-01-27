"""solotodo_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.facebook.views import \
    FacebookOAuth2Adapter
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_auth.registration.views import SocialLoginView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, \
    TokenObtainPairView
from solotodo.router import router as solotodo_router
from category_templates.router import router as category_templates_router
from category_specs_forms.router import router as category_specs_forms_router
from reports.router import router as reports_router
from wtb.router import router as wtb_router
from category_columns.router import router as category_columns_router
from notebooks.router import router as notebooks_router
from hardware.router import router as hardware_router
from carousel_slides.router import router as carousel_slides_router
from alerts.router import router as alerts_router
from banners.router import router as banners_router
from brand_comparisons.router import router as brand_comparisons_router
from lg_pricing.router import router as lg_pricing_router
from keyword_search_positions.router import router as keyword_search_router
from store_subscriptions.router import router as store_subscription_router
from microsite.router import router as microsite_router
from .custom_default_router import CustomDefaultRouter
from metamodel.routers import router as metamodel_router
from website_slides.router import router as website_slides_router

router = CustomDefaultRouter()
router.extend(solotodo_router)
router.extend(category_templates_router)
router.extend(category_specs_forms_router)
router.extend(reports_router)
router.extend(wtb_router)
router.extend(category_columns_router)
router.extend(notebooks_router)
router.extend(hardware_router)
router.extend(carousel_slides_router)
router.extend(alerts_router)
router.extend(banners_router)
router.extend(brand_comparisons_router)
router.extend(lg_pricing_router)
router.extend(keyword_search_router)
router.extend(store_subscription_router)
router.extend(microsite_router)
router.extend(metamodel_router)
router.extend(website_slides_router)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^obtain-auth-token/$', obtain_auth_token),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^metamodel/', include('metamodel.urls')),
    # url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    url(r'^', include(router.urls)),
    url(r'^', include('django.contrib.auth.urls')),
]
