from django.contrib import admin

from ops.models import SlackBot, SlackInstallation, SlackOAuthState, SlackBotChannel


class SlackBotChannelInline(admin.StackedInline):
    model = SlackBotChannel
    extra = 0


class SlackBotAdmin(admin.ModelAdmin):
    inlines = [SlackBotChannelInline]
    list_display = ['client_id', 'app_id', 'enterprise_name', 'team_name', 'bot_token_expires_at', 'is_enterprise_install', 'installed_at', 'is_active']


class SlackInstallationAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'app_id', 'enterprise_name', 'team_name', 'bot_token_expires_at', 'is_enterprise_install', 'token_type', 'installed_at']


class SlackOAuthStateAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlackBot, SlackBotAdmin)
admin.site.register(SlackInstallation, SlackInstallationAdmin)
admin.site.register(SlackOAuthState, SlackOAuthStateAdmin)
