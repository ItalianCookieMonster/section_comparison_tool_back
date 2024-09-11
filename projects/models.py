from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True) 
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    concrete_density = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=255, default="USD", blank=True, null=True)
    concrete_cost = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    labour_cost = models.DecimalField(max_digits=8, decimal_places=2,  blank=True, null=True,)
    avg_truck_capacity = models.FloatField(blank=True, null=True,)
    infill_density = models.FloatField( blank=True, null=True,)
    infill_cost = models.DecimalField(max_digits=8, decimal_places=2,  blank=True, null=True,)
    avg_truck_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,)
    avg_production_time = models.FloatField( blank=True, null=True,)
    royalty = models.DecimalField(max_digits=8, decimal_places=2)
    pur_per_year = models.FloatField( blank=True, null=True,)
    cem_content = models.FloatField( blank=True, null=True,)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, default="en", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Section(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) 
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True, related_name='sections')
    title = models.CharField(max_length=255, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    face_area = models.FloatField(null=True, blank=True)
    labour_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    concrete = models.FloatField(null=True, blank=True)
    concrete_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    infill = models.FloatField(null=True, blank=True)
    infill_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    delivery_weight = models.FloatField(null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    co2_emissions = models.FloatField(null=True, blank=True)
    royalties = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class Block(models.Model):
    name = models.CharField(max_length=255)
    vol_per_block = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()
    face_area = models.FloatField()
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SectionBlock(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()

    def __str__(self):
        return f"{self.section.title} - {self.block.name}"