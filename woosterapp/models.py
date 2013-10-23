from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=50)
    ldapid = models.CharField(max_length=20)
    allowed = models.BooleanField()
    ip = models.CharField(max_length=20)
    lastAccessed = models.DateTimeField('Last accessed')
    
    def __unicode__(self):
        return self.name