from datetime import timezone, timedelta

from django_filters import rest_framework as django_filters  #pip install django-filter
from api.models import University, User, Eslatma

class UniversityFilter(django_filters.FilterSet):
    university_name = django_filters.CharFilter(field_name="university_name", lookup_expr='icontains')
    state = django_filters.CharFilter(field_name="state", lookup_expr='icontains')
    level = django_filters.CharFilter(field_name="level", lookup_expr='icontains')
    grant_name = django_filters.CharFilter(field_name="grant_name", lookup_expr='icontains')
    grand_amount = django_filters.CharFilter(field_name="grand_amount", lookup_expr='icontains')
    grand_turi = django_filters.CharFilter(field_name="grand_turi", lookup_expr='icontains')
    directions = django_filters.CharFilter(field_name="directions", lookup_expr='icontains')
    reception_start = django_filters.DateFilter(field_name="reception_start", lookup_expr='gte')
    reception_end = django_filters.DateFilter(field_name="reception_end", lookup_expr='lte')

    class Meta:
        model = University
        fields = ['university_name', 'state', 'level', 'grant_name', 'grand_amount', 'grand_turi',
                  'directions', 'reception_start', 'reception_end']





class EslatmaFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user__id")
    university = django_filters.NumberFilter(field_name="university__id")
    eslatma_matni = django_filters.CharFilter(field_name="eslatma_matni", lookup_expr='icontains')
    qolgan_kun = django_filters.NumberFilter(method='filter_qolgan_kun')
    tugash_kun = django_filters.NumberFilter(method='filter_tugash_kun')

    class Meta:
        model = Eslatma
        fields = ['user', 'university', 'eslatma_matni', 'qolgan_kun', 'tugash_kun']

    def filter_qolgan_kun(self, queryset, name, value):
        # value = 5 (masalan)
        # bugun + 5 kun = maqsadli sana
        target_date = timezone.now().date() + timedelta(days=value)
        return queryset.filter(reception_start=target_date)

    def filter_tugash_kun(self, queryset, name, value):
        # reception_end bugundan boshlab 'value' kun ichida keladiganlari
        today = timezone.now().date()
        target_date = today + timedelta(days=value)

        # Bugun va 'value' kun oralig'idagi tugaydiganlarni olish
        return queryset.filter(reception_end__gte=today, reception_end__lte=target_date)


class UserFilter(django_filters.FilterSet):
    phone_number = django_filters.CharFilter(field_name="username", lookup_expr='icontains')
    email = django_filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['phone_number', 'email']