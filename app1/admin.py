from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, Like, Comment, Tag, Story, Conversation, Message

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'location']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'location', 'birth_date', 'profile_picture', 'website')}),
    )

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['participants']
    inlines = [MessageInline]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Story)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message)

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username', 'bio', 'location', 'birth_date', 'is_staff']
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('bio', 'location', 'birth_date', 'profile_picture', 'website')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('bio', 'location', 'birth_date', 'profile_picture', 'website')}),
#     )

