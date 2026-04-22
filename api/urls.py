from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.views import UserViewSet, UniversitetViewSet, EslatmaViewSet, ai_chat, super_ai_translate

from api.views.misc import ai_chat_result
from billing.views import ClickPaymentView, ClickCompleteView, ClickCreatePaymentView


# from api.views import super_ai_translate, ai_chat


class JWTSchemaGenerator(OpenAPISchemaGenerator):

    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions['Bearer'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="API  ScholarMap",
        default_version='v2',
        description='API documentation for ScholarMap ',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amanovjavlonbek25@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=JWTSchemaGenerator,
    url='https://scholarmap.uz/api/v1/',
)

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'universiteties', UniversitetViewSet)
router.register(r'eslatmalar', EslatmaViewSet)

# router.register(r'users', UserViewSet)
# router.register(r'shops', ShopViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),

    #  agar pustoy path() ga kirsa pastagi swaggerga kirib ketadi
    path('', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),

    # Urllarga Djoserni qo'shish uchun pastagi kodlar
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('v1/auth/token/verify/', TokenVerifyView.as_view(), name="token_verify"),

    # pastagi 3 qator kod hamma proyektlarga qo'shilishi shart

    # bu ham barcha proyektlarga qo'yib ketiladigan narsa
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ shu


    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc"),




#     Funksiyalar uchun url
#     path('v1/translate/', super_ai_translate, name="super_ai_translate"),
#     path('v1/function-based/', your_functional_view, name="test_functional_view"),


    path('v1/ai-chat/', ai_chat, name="ai_chat"),
    path('v1/super-ai-translate/', super_ai_translate, name="super_ai_translate"),
    path('v1/ai-chat/result/<str:task_id>/', ai_chat_result),


    path('click/pay/', ClickCreatePaymentView.as_view(), name='click-pay'),          # havola yaratish
    path('click/prepare/', ClickPaymentView.as_view(), name='click-prepare'),        # Click webhook 1
    path('click/complete/', ClickCompleteView.as_view(), name='click-complete'),
]

]