from django.db import models


class ForcastOffice(models.Model):
    class Meta:
        verbose_name = 'Forcast office'

    type = models.CharField(max_length=32)
    office_id = models.CharField(max_length=3, db_index=True)
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=24)
    fax_number = models.CharField(max_length=24)
    email = models.CharField(max_length=255)
    nws_region = models.CharField(max_length=4)
    parent_organization = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
