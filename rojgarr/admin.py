from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from.forms import UserAdminCreationForm, UserAdminChangeForm, RegisterEmployerForm, RegisterEmployerChangeForm

User = get_user_model()

# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email']
#     form = UserAdminChangeForm # update view
#     add_form = UserAdminCreationForm # create view
#     class Meta:
#         model = User

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'employer', 'employe','active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'employer', 'employe','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
class Register_Company_DetailAdmin(admin.ModelAdmin):
    form = RegisterEmployerForm
    add_form = RegisterEmployerChangeForm
    # list_display = ('email', 'employer')
    # fieldsets = {
    #     (None, {'fields': ('company_address','company_contact','company_bussiness','company_bussiness','address_latitude','address_longitude')}),
    # }
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('full_name','company_address','company_contact','company_bussiness','email')}
    #     ),
    # )


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Vacancy_Detail)
admin.site.register(Advertisement_Detail)
admin.site.register(Profile)
admin.site.register(Register_Company_Detail)
admin.site.register(Company_Review)