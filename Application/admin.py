#admin.py
from django.contrib import admin
from .models import CustomUser

# Register your models here.
def reset_timer(modeladmin, request, queryset):
    for user in queryset:
        user.last_reward_claim_time = None
        user.save()
    modeladmin.message_user(request, "Timer reset successfully.")

reset_timer.short_description = "Reset timer for selected users"

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_reward_claim_time')
    actions = [reset_timer]

admin.site.register(CustomUser, CustomUserAdmin)