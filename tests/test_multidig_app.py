import unittest
from unittest.mock import patch
import customtkinter
from multidig import App

class TestAppInit(unittest.TestCase):

    def test_custom_app_creation(self):
            app = App()
            self.assertIsInstance(
                  app,
                  customtkinter.CTk,
                  msg="App is correctly instantiated."
            )
