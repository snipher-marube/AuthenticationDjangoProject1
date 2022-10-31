from django.contrib import admin
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'phone': PhoneNumberPrefixWidget,
        }
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'bio')
    list_filter = ('user', 'first_name', 'last_name', 'phone', 'bio')
    search_fields = ('user', 'first_name', 'last_name', 'phone', 'bio')
    ordering = ('user', 'first_name', 'last_name', 'phone', 'bio')
    fields = ('user', 'first_name', 'last_name', 'phone', 'bio')

    form = ProfileAdminForm


