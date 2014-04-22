from django.db import models
# import django_databrowse


class Msg(models.Model):
    user_name = models.CharField(max_length=200, default='Anonymous')
    user = models.ForeignKey('accounts.User', blank=True, null=True)
    contact_email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True)
    TYPE_CHOICE = (
        ('0', 'message'),
        ('1', 'reply'),
    )
    msg_type = models.IntegerField(default=0)
    has_reply = models.BooleanField(default=False)
    msg_reply_to = models.ForeignKey('Msg', blank=True, null=True)
    content = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.user_name + ":" + self.content

# django_databrowse.site.register(Msg)