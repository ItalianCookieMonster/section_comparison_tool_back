from rest_framework import serializers
from .models import Project, Block, Section



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
        'title',
        'user',
        'company_name',
        'concrete_density',
        'currency',
        'concrete_cost',
        'labour_cost',
        'avg_truck_capacity',
        'infill_density',
        'infill_cost',
        'avg_truck_cost',
        'avg_production_time',
        'royalty',
        'pur_per_year',
        'cem_content',
        'address',
        'zip_code',
        'language'
    ]


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = [
            'id',
            'name',
            'vol_per_block',
            'width',
            'height',
            'depth',
            'face_area',
            'image'
        ]
            


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'user',
            'project',
            'title',
            'height',
            'face_area',
            'labour_cost',
            'concrete',
            'concrete_cost',
            'infill',
            'infill_cost',
            'delivery_weight',
            'delivery_cost',
            'co2_emissions',
            'royalties'
        ]


