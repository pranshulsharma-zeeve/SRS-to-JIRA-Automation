"""Frontend smoke tests."""

import os
import unittest

from frontend.src.app import login_page_title


class FrontendSmokeTests(unittest.TestCase):
    def test_login_page_title(self) -> None:
        self.assertEqual(login_page_title(), "Login")

    def test_frontend_src_directory_exists(self) -> None:
        self.assertTrue(os.path.isdir("frontend/src"))


if __name__ == "__main__":
    unittest.main()
