from django.db import models


class Good(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=500,
                                   blank=True,
                                   null=False,
                                   default='No description!')
    date_created = models.DateTimeField(auto_now_add=True)
