import os
import tempfile
import zipfile

from django.test import TestCase

from hesma.utils.zip_generator import ZipFileGenerator


class ZipFileGeneratorTestCase(TestCase):
    def setUp(self):
        # Set up a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

        # Create some test files in the temporary directory
        self.file_paths = [
            os.path.join(self.temp_dir, "test_file1.txt"),
            os.path.join(self.temp_dir, "test_file2.txt"),
        ]
        for file_path in self.file_paths:
            with open(file_path, "w") as f:
                f.write(f"Test content for file: {os.path.basename(file_path)}")

    def tearDown(self):
        # Clean up the temporary directory and files
        for file_path in self.file_paths:
            os.remove(file_path)
        os.rmdir(self.temp_dir)

    def test_zip_file_generation(self):
        # Test the generation of the zip file
        zip_generator = ZipFileGenerator(self.file_paths)
        buffer = tempfile.SpooledTemporaryFile()

        # Generate the zip file in the buffer
        zip_generator.generate_zip(buffer)

        # Seek to the beginning of the buffer
        buffer.seek(0)

        # Verify that the generated zip file contains the expected files
        with zipfile.ZipFile(buffer, "r") as zipf:
            zip_file_contents = set(zipf.namelist())
            expected_file_names = {os.path.basename(file_path) for file_path in self.file_paths}
            self.assertEqual(zip_file_contents, expected_file_names)
