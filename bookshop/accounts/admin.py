from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import OtpCode
from django import forms
from  .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("email", "phone_num", "full_name")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password from <a href=\"../password/\"> here </a>")
    class Meta:
        model = User
        fields = ("email", "phone_num", "full_name", "last_login")



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    search_fields = ("email", "full_name")
    list_display = ("email", "phone_num", "is_admin")
    list_filter = ("is_admin",)
    ordering = ("full_name",)
    readonly_fields = ("last_login",)
    fieldsets = (
        ("Main", {"fields":("email", "phone_num", "full_name", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_active", "last_login", "groups", "user_permissions", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"fields": ("phone_num", "email", "full_name", "password1", "password2")}),
    )
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)

