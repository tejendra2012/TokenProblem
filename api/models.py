'''
    @Author: Tejendra Singh Kushwah
    @Copyright: Copyright (C) 2021 Tejendra Singh Kushwah
    @Version: 1.0
'''

from django.db import models

# Create your models here.

class Token(models.Model):
    token = models.CharField(max_length=254,default=0, blank=True)
    activate = models.BooleanField(default=False)
    username = models.CharField(max_length=254, blank=True,null=True)
    update_time = models.DateTimeField(auto_now_add=True)
