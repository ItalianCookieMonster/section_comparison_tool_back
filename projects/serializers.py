from rest_framework import serializers
from .models import Project, Block, Section





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

class ProjectCreateSerializer(serializers.ModelSerializer):
    new_section_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
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
            'language',
            'new_section_id' 
        ]
        
        read_only_fields = ['id', 'user'] 
    
    
    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        section = Section.objects.create(
            user=self.context['request'].user,
            project=project,
            title=f"{project.title} S1"
        )
        
        validated_data['new_section_id'] = section.id
        project.new_section_id = section.id
        
        return project


class ProjectSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Project
        fields = [
            'id',
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
            'language',
            'sections' 
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
            




