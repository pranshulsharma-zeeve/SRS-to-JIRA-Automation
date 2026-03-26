"""Backend smoke tests."""

import os
import unittest

from backend.src.app import health_status


class BackendSmokeTests(unittest.TestCase):
    def test_health_status(self) -> None:
        self.assertEqual(health_status(), {"status": "ok"})

    def test_backend_src_directory_exists(self) -> None:
        self.assertTrue(os.path.isdir("backend/src"))


if __name__ == "__main__":
    unittest.main()
