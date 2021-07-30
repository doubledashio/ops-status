from django.contrib import admin

from ops.models import SlackBot, SlackInstallation, SlackOAuthState


class SlackBotAdmin(admin.ModelAdmin):
    pass


class SlackInstallationAdmin(admin.ModelAdmin):
    pass


class SlackOAuthStateAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlackBot, SlackBotAdmin)
admin.site.register(SlackInstallation, SlackInstallationAdmin)
admin.site.register(SlackOAuthState, SlackOAuthStateAdmin)
