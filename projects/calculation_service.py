# calculation_service.py

from .models import Section, SectionBlock


class SectionCalculationsService:
    def __init__(self, section_id):
        self.section_id = section_id
        self.section = Section.objects.get(id=section_id)

    def calculate_height(self):
        """Calculate the total height of the section."""
        section_blocks = SectionBlock.objects.filter(section=self.section)
        total_height = sum(
            [block.block.height * block.quantity for block in section_blocks]
        )
        return total_height

    def calculate_face_area(self):
        """Calculate the total face area of the section."""
        section_blocks = SectionBlock.objects.filter(section=self.section)
        total_face_area = sum(
            [block.block.face_area * block.quantity for block in section_blocks]
        )
        return total_face_area

    def calculate_concrete_volume(self):
        """Calculate the total concrete volume of the section."""
        section_blocks = SectionBlock.objects.filter(section=self.section)
        total_concrete_volume = sum(
            [block.block.vol_per_block * block.quantity for block in section_blocks]
        )
        return total_concrete_volume

    def perform_all_calculations(self):
        """Perform all calculations for the section."""
        return {
            "height": self.calculate_height(),
            "face_area": self.calculate_face_area(),
            "concrete_volume": self.calculate_concrete_volume(),
        }
