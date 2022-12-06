"""
Tests for models.
"""
from django.test import TestCase
from core.configs import (
    DIGITAL_OCEAN_SPACE_NAME,
    DIGITAL_OCEAN_SPACE_API_KEY,
    DIGITAL_OCEAN_SPACE_SECRET_KEY)
from core.services.digitalocean_service import DigitalOceanService


class DigitalOceanTests(TestCase):
    """Test models"""

    def test_upload_file_to_storage(self):
        do_service = DigitalOceanService(
           region_name="sgp1",
           endpoint_url="https://sgp1.digitaloceanspaces.com",
           access_key_id=DIGITAL_OCEAN_SPACE_API_KEY,
           secret_access_key=DIGITAL_OCEAN_SPACE_SECRET_KEY)

        with open("core/tests/test.jpg", "rb") as file:
            url = do_service.upload_file_to_storage(
                DIGITAL_OCEAN_SPACE_NAME,
                file,
                "test/test.jpg")

