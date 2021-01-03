from django.db import models

# Create your models here.

class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class ProductGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class ProductFamily(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey('ProductGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class File(models.Model):
    id = models.IntegerField(primary_key=True)
    product_family = models.ForeignKey('ProductFamily', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=1024)
    sha1_hash = models.CharField(max_length=40)
    description = models.CharField(max_length=1024)
    language = models.ForeignKey('Language', null=True, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    posted_date = models.DateTimeField()
    size = models.DecimalField(max_digits=12, decimal_places=3)
    product_key_required = models.BooleanField()

    def __str__(self):
        return self.description
