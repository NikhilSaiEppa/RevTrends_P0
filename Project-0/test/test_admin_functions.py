import unittest
from unittest.mock import patch
from io import StringIO
from admin_functions import connect_to_database, execute_query, admin_menu, admin

class TestAdminFunctions(unittest.TestCase):

    # @patch('builtins.input', side_effect=['admin_username', 'admin_password'])
    # @patch('mysql.connector.connect')
    # def test_connect_to_database(self, mock_connect, mock_input):
    #     # Test successful database connection
    #     mock_connection = mock_connect.return_value
    #     result = connect_to_database('admin_username', 'admin_password', 'revtrends')
    #     self.assertEqual(result, mock_connection)

    #     # Test database connection failure
    #     mock_connect.side_effect = Exception("Connection error")
    #     result = connect_to_database('invalid_username', 'invalid_password', 'revtrends')
    #     self.assertIsNone(result)

    # @patch('builtins.input', side_effect=['admin_username', 'admin_password'])
    # @patch('mysql.connector.connect')
    # def test_execute_query(self, mock_connect, mock_input):
    #     mock_connection = mock_connect.return_value
    #     with patch.object(mock_connection, 'cursor') as mock_cursor:
    #         with patch.object(mock_cursor.return_value, 'execute') as mock_execute:
    #             # Test successful query execution
    #             execute_query(mock_connection, 'SELECT * FROM some_table')
    #             mock_execute.assert_called_once_with('SELECT * FROM some_table')
    #             mock_connection.commit.assert_called_once()

    #             # Test query execution failure
    #             mock_execute.side_effect = Exception("Query error")
    #             with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #                 execute_query(mock_connection, 'INVALID SQL')
    #                 self.assertIn("Error: Query error", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['admin_username', 'admin_password'])
    @patch('mysql.connector.connect')
    def test_admin_menu(self, mock_connect, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            admin_menu()
            expected_output = "Admin Menu:\n1. Add Categories\n2. Update Country Names\n3. See Which Test has Positive Sentiment\n4. Delete the data :\n5. Exit\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    # @patch('builtins.input', side_effect=['admin_username', 'admin_password'])
    # @patch('mysql.connector.connect')
    # def test_admin(self, mock_connect, mock_input):
    #     # Mocking the connection
    #     mock_connection = mock_connect.return_value
    #     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #         with patch.object(mock_connection, 'cursor') as mock_cursor:
    #             # Mocking successful login
    #             mock_cursor.fetchone.return_value = {'role': 'admin'}
    #             admin()
    #             expected_output = "Login successful. Welcome, admin_username!\nAdmin Menu:\n1. Add Categories\n2. Update Country Names\n3. See Which Test has Positive Sentiment\n4. Delete the data :\n5. Exit\n"
    #             self.assertIn(expected_output, mock_stdout.getvalue())

    #             # Mocking invalid login
    #             mock_cursor.fetchone.return_value = None
    #             with patch('sys.stdout', new_callable=StringIO) as mock_stdout_invalid_login:
    #                 admin()
    #                 self.assertIn("Error: Invalid username or password.", mock_stdout_invalid_login.getvalue())

    @patch('builtins.input', side_effect=['admin_username', 'admin_password'])
    @patch('mysql.connector.connect')
    def test_admin_menu(self, mock_connect, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            admin_menu()
            expected_output = "Admin Menu:\n1. Add Categories\n2. Update Country Names\n3. See Which Test has Positive Sentiment\n4. Delete the data :\n5. Exit\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    
    
    
if __name__ == '__main__':
    unittest.main()
