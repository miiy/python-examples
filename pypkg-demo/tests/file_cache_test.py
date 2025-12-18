import time
import unittest
import sys
from pathlib import Path

# add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from pypkg_demo.file_cache import FileCache


class TestPypkgDemoClient(unittest.TestCase):

    def test_file_cache(self):
        file_cache = FileCache("test.json")
        file_cache.set("test", "test")
        self.assertEqual(file_cache.get("test"), "test")


if __name__ == "__main__":
    unittest.main(verbosity=2)