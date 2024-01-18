import unittest
from unittest.mock import patch
from user_functions import User  # Replace 'your_database_module' with your actual module name

class TestUserFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['existing_username', 'password', '2', 'exit'])
    @patch('user_functions.connect_to_database')
    @patch('user_functions.plt.show')
    def test_user_platform_analysis(self, mock_plt_show, mock_connect_to_database, mock_input):
        # Mock the user connection
        mock_user_connection = mock_connect_to_database.return_value
        mock_cursor = mock_user_connection.cursor.return_value

        # Mock the result of the SELECT query to simulate a regular user
        mock_cursor.fetchone.return_value = {'role': 'regular_user'}

        # Mock the result of the platform analysis query
        mock_cursor.fetchall.return_value = [
            {'platform': 'Platform1', 'TotalLikes': 100},
            {'platform': 'Platform2', 'TotalLikes': 150},
            {'platform': 'Platform3', 'TotalLikes': 120},
        ]

        # Run the function
        with patch('builtins.print') as mock_print:
            User()

        # Assert that the necessary SQL statements were executed
        mock_cursor.execute.assert_called()
        mock_plt_show.assert_called_once()  # Ensure plt.show is called once

        # Add more assertions based on your specific requirements

    @patch('builtins.input', side_effect=['existing_username', 'password', '3', 'exit'])
    @patch('user_functions.connect_to_database')
    @patch('user_functions.plt.show')
    def test_user_categories_analysis(self, mock_plt_show, mock_connect_to_database, mock_input):
        # Similar setup as the platform analysis test, but with different side_effect values
        pass  # Add your test logic here

    @patch('builtins.input', side_effect=['existing_username', 'password', '4', 'exit'])
    @patch('user_functions.connect_to_database')
    @patch('user_functions.plt.show')
    def test_user_sentiment_analysis(self, mock_plt_show, mock_connect_to_database, mock_input):
        # Similar setup as the platform analysis test, but with different side_effect values
        pass  # Add your test logic here

    @patch('builtins.input', side_effect=['existing_username', 'password', 'exit'])
    @patch('user_functions.connect_to_database')
    def test_user_exit(self, mock_connect_to_database, mock_input):
        # Mock the user connection
        mock_user_connection = mock_connect_to_database.return_value
        mock_cursor = mock_user_connection.cursor.return_value

        # Mock the result of the SELECT query to simulate a regular user
        mock_cursor.fetchone.return_value = {'role': 'regular_user'}

        # Run the function
        with patch('builtins.print') as mock_print:
            User()

        # Add assertions based on the expected behavior when the user chooses to exit

    @patch('builtins.input', side_effect=['existing_username', 'password', '5', 'exit'])
    @patch('user_functions.connect_to_database')
    def test_user_invalid_option(self, mock_connect_to_database, mock_input):
        # Mock the user connection
        mock_user_connection = mock_connect_to_database.return_value
        mock_cursor = mock_user_connection.cursor.return_value

        # Mock the result of the SELECT query to simulate a regular user
        mock_cursor.fetchone.return_value = {'role': 'regular_user'}

        # Run the function
        with patch('builtins.print') as mock_print:
            User()

        # Add assertions based on the expected behavior when the user enters an invalid option

    # Add more test methods for other functionality in the User function

if __name__ == '__main__':
    unittest.main()
