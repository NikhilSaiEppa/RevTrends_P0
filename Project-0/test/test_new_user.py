import unittest
from unittest.mock import patch
from new_user_functions import new_user

class TestNewUserFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['new_username', 'new_password'])
    @patch('new_user_functions.connect_to_database')
    def test_new_user_success(self, mock_connect_to_database, mock_input):
        # Mock the admin connection
        mock_admin_connection = mock_connect_to_database.return_value
        mock_admin_cursor = mock_admin_connection.cursor.return_value

        # Mock the result of the SELECT query to check for existing user
        mock_admin_cursor.fetchone.return_value = None

        # Run the function
        new_user()

        # Assert that the necessary SQL statements were executed
        mock_admin_cursor.execute.assert_any_call("CREATE USER 'new_username'@'localhost' IDENTIFIED BY 'new_password';")
        mock_admin_cursor.execute.assert_any_call("GRANT SELECT ON revtrends.* TO 'new_username'@'localhost';")
        mock_admin_cursor.execute.assert_any_call("INSERT INTO db_users (username, password, role) VALUES (%s, %s, %s)",
                                                 ('new_username', 'new_password', 'regular_user'))
        mock_admin_connection.commit.assert_called()

    @patch('builtins.input', side_effect=['existing_username', 'password'])
    @patch('new_user_functions.connect_to_database')
    def test_new_user_existing_username(self, mock_connect_to_database, mock_input):
        # Mock the admin connection
        mock_admin_connection = mock_connect_to_database.return_value
        mock_admin_cursor = mock_admin_connection.cursor.return_value

        # Mock the result of the SELECT query to simulate an existing user
        mock_admin_cursor.fetchone.return_value = ('existing_username', 'password', 'regular_user')

        # Run the function
        with patch('builtins.print') as mock_print:
            new_user()

        # Assert that the function prints the appropriate message
        mock_print.assert_called_with("connection closed")
        mock_admin_cursor.execute.assert_called_once()

    @patch('builtins.input', side_effect=['new_username', 'new_password'])
    @patch('new_user_functions.connect_to_database')
    def test_new_user_success(self, mock_connect_to_database, mock_input):
        # Mock the admin connection
        mock_admin_connection = mock_connect_to_database.return_value
        mock_admin_cursor = mock_admin_connection.cursor.return_value

        # Mock the result of the SELECT query to check for existing user
        mock_admin_cursor.fetchone.return_value = None

        # Run the function
        new_user()

        # Assert that the necessary SQL statements were executed
        mock_admin_cursor.execute.assert_any_call("CREATE USER 'new_username'@'localhost' IDENTIFIED BY 'new_password';")
        mock_admin_cursor.execute.assert_any_call("GRANT SELECT ON revtrends.* TO 'new_username'@'localhost';")
        mock_admin_cursor.execute.assert_any_call("INSERT INTO db_users (username, password, role) VALUES (%s, %s, %s)",
                                                 ('new_username', 'new_password', 'regular_user'))
        mock_admin_connection.commit.assert_called()

if __name__ == '__main__':
    unittest.main()
