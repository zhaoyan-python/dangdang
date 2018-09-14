from django.db import models

# Create your models here.
class TUser(models.Model):
    user_name = models.CharField(db_column='username',max_length=20,null=True)
    password = models.CharField(max_length=100,null=True)
    login_time = models.DateTimeField(null=True)
    salt = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 't_user'

