###
# Accounts Admin
###


from django.contrib import admin
from accounts.models import User

###
# Models
###

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'last_login', 'email', 'is_staff',
              'is_active', 'date_joined']
    list_display = ['id', 'name', 'email', 'last_login']
    search_fields = ['name', 'email']


