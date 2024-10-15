import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.calculation_service import SectionCalculationsService
from projects.models import Block, Section, SectionBlock


class SectionCalculationsServiceTest(TestCase):
    def setUp(self):
        """
        Given a section with two types of blocks,
        And each block has a specific height, face area, and volume,
        When the service is initialized,
        Then it should be ready to perform calculations on that section.
        """

        User = get_user_model()
        self.user = User.objects.create(username="testuser")
        self.section = Section.objects.create(user=self.user, title="Test Section")

        self.block1 = Block.objects.create(
            name="Block 1",
            height=2.0,
            face_area=4.0,
            vol_per_block=0.5,
            width=1.5,
            depth=0.8,
        )
        self.block2 = Block.objects.create(
            name="Block 2",
            height=3.0,
            face_area=6.0,
            vol_per_block=1.0,
            width=2.0,
            depth=1.0,
        )

        SectionBlock.objects.create(section=self.section, block=self.block1, quantity=2)
        SectionBlock.objects.create(section=self.section, block=self.block2, quantity=3)

        self.service = SectionCalculationsService(self.section.id)

    def test_calculate_height(self):
        """
        Scenario: Calculate total height of the section

        Given a section with blocks of varying heights,
        When the calculate_height method is called,
        Then it should return the total height as the sum of each block's height multiplied by its quantity.
        """
        expected_height = (self.block1.height * 2) + (self.block2.height * 3)
        result = self.service.calculate_height()
        assert result == expected_height, f"Expected {expected_height}, got {result}"

    def test_calculate_face_area(self):
        """
        Scenario: Calculate total face area of the section

        Given a section with blocks of varying face areas,
        When the calculate_face_area method is called,
        Then it should return the total face area as the sum of each block's face area multiplied by its quantity.
        """
        expected_face_area = (self.block1.face_area * 2) + (self.block2.face_area * 3)
        result = self.service.calculate_face_area()
        assert (
            result == expected_face_area
        ), f"Expected {expected_face_area}, got {result}"

    def test_calculate_concrete_volume(self):
        """
        Scenario: Calculate total concrete volume of the section

        Given a section with blocks of varying volumes,
        When the calculate_concrete_volume method is called,
        Then it should return the total volume as the sum of each block's volume multiplied by its quantity.
        """
        expected_concrete_volume = (self.block1.vol_per_block * 2) + (
            self.block2.vol_per_block * 3
        )
        result = self.service.calculate_concrete_volume()
        assert (
            result == expected_concrete_volume
        ), f"Expected {expected_concrete_volume}, got {result}"

    def test_perform_all_calculations(self):
        """
        Scenario: Perform all calculations for the section

        Given a section with blocks of varying properties,
        When the perform_all_calculations method is called,
        Then it should return a dictionary with the total height, face area, and concrete volume of the section.
        """
        expected_results = {
            "height": (self.block1.height * 2) + (self.block2.height * 3),
            "face_area": (self.block1.face_area * 2) + (self.block2.face_area * 3),
            "concrete_volume": (self.block1.vol_per_block * 2)
            + (self.block2.vol_per_block * 3),
        }
        result = self.service.perform_all_calculations()
        assert result == expected_results, f"Expected {expected_results}, got {result}"
