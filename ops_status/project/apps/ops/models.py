from django.db import models


class SlackBot(models.Model):
    client_id = models.CharField(null=False, max_length=32)
    app_id = models.CharField(null=False, max_length=32)
    enterprise_id = models.CharField(null=True, max_length=32)
    enterprise_name = models.TextField(null=True)
    team_id = models.CharField(null=True, max_length=32)
    team_name = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_refresh_token = models.TextField(null=True)
    bot_token_expires_at = models.DateTimeField(null=True)
    bot_id = models.CharField(null=True, max_length=32)
    bot_user_id = models.CharField(null=True, max_length=32)
    bot_scopes = models.TextField(null=True)
    is_enterprise_install = models.BooleanField(null=True)
    installed_at = models.DateTimeField(null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['client_id', 'enterprise_id', 'team_id', 'installed_at']
            ),
        ]

    def __str__(self):
        return f'SlackBot for {self.team_name}'


class SlackInstallation(models.Model):
    client_id = models.CharField(null=False, max_length=32)
    app_id = models.CharField(null=False, max_length=32)
    enterprise_id = models.CharField(null=True, max_length=32)
    enterprise_name = models.TextField(null=True)
    enterprise_url = models.TextField(null=True)
    team_id = models.CharField(null=True, max_length=32)
    team_name = models.TextField(null=True)
    bot_token = models.TextField(null=True)
    bot_refresh_token = models.TextField(null=True)
    bot_token_expires_at = models.DateTimeField(null=True)
    bot_id = models.CharField(null=True, max_length=32)
    bot_user_id = models.TextField(null=True)
    bot_scopes = models.TextField(null=True)
    user_id = models.CharField(null=False, max_length=32)
    user_token = models.TextField(null=True)
    user_refresh_token = models.TextField(null=True)
    user_token_expires_at = models.DateTimeField(null=True)
    user_scopes = models.TextField(null=True)
    incoming_webhook_url = models.TextField(null=True)
    incoming_webhook_channel = models.TextField(null=True)
    incoming_webhook_channel_id = models.TextField(null=True)
    incoming_webhook_configuration_url = models.TextField(null=True)
    is_enterprise_install = models.BooleanField(null=True)
    token_type = models.CharField(null=True, max_length=32)
    installed_at = models.DateTimeField(null=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'client_id',
                    'enterprise_id',
                    'team_id',
                    'user_id',
                    'installed_at',
                ]
            ),
        ]

    def __str__(self):
        return f'SlackInstallation for {self.team_name}'


class SlackOAuthState(models.Model):
    state = models.CharField(null=False, max_length=64)
    expire_at = models.DateTimeField(null=False)


class SlackBotChannel(models.Model):
    bot = models.ForeignKey(SlackBot, related_name='channels', on_delete=models.CASCADE)

    channel_id = models.CharField(max_length=32)

    def __str__(self):
        return f'SlackBotChannel for {self.channel_id}'
