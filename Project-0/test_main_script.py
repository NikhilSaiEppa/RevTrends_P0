import unittest
from unittest.mock import patch
from io import StringIO
from main_script import admin, new_user, User  # Import functions directly

class TestMainScript(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', 'existing_username', 'password', 'exit'])
    def test_new_user_option_existing_username(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_user()
        expected_output = "Username already exists. Please choose a different username.\nconnection closed\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)



    @patch('builtins.input', side_effect=['4', 'exit'])
    def test_invalid_option(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print("Invalid choice.")
        self.assertIn("Invalid choice.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
