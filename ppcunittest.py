#! python3
"""Unit test for database module"""
import unittest
import os
import database as ppcDB

class TestSQLiteQuery(unittest.TestCase):
    """Unit testing for database module"""
    def setUp(self):
        database_home = os.path.join(os.path.dirname(__file__), 'lookup.sqlite')
        self.data = ppcDB.Query(database_home)

    def tearDown(self):
        self.data.close_connection()

    def test_if_states_are_returned(self):
        """Assert that:
            - we get SOMETHING at all from the function
            - the "something" returned is a list
            - the size of the list equals the number of db_states we have on file
            - for each item in the returned list, make sure it's actually what's on file
        """
        state_test_path = self.build_path('states.txt')
        db_states = self.data.get_state_list()
        states = self.populate_list(state_test_path)

        self.assertIsNotNone(db_states) # Assert that SOMETHING is returned
        self.assertIsInstance(db_states, list) # Assert that a list is returned
        self.assertEqual(len(db_states), len(states)) # Assert list sizes are equal
        # For each state, assert that the contents of the file equal the list returned
        for item in enumerate(states):
            self.assertEqual(db_states[item[0]], states[item[0]])

    def test_if_counties_are_returned(self):
        """Assert that:
            - we get SOMETHING at all from the function
            - the "something" returned is a list
            - the size of the list equals the number of counties we have for that state
            - for each item in the returned list, make sure it's actually what's on file
        """
        # Find path for list of counties in Alabama
        county_test_path = self.build_path('alabama.txt')
        counties = self.data.get_county_list('AL')
         # Put list of counties from .txt file into list
        alabama_counties = self.populate_list(county_test_path)

        self.assertIsNotNone(counties)
        self.assertIsInstance(counties, list)
        self.assertEqual(len(counties), len(alabama_counties))
        for item in enumerate(alabama_counties):
            self.assertEqual(counties[item[0]], alabama_counties[item[0]])

    def test_if_correct_codes_returned(self):
        """Assert that:
            - we get SOMETHING at all from the function
            - the "something" returned is a list
            - the size of the list equals the number of db_states we have on file
            - for each item in the returned list, make sure it's actually what's on file
        """
        code_test_path = self.build_path('AL_codes.txt')
        town_test_path = self.build_path('AL_towns.txt')
        codes = self.data.get_ppc_codes('AL', 'Autauga')
        code_list = self.populate_list(code_test_path)
        town_list = self.populate_list(town_test_path)

        self.assertIsNotNone(codes)
        self.assertIsInstance(codes, list)
        self.assertEqual(len(codes), len(town_list))
        for item in enumerate(codes):
            self.assertEqual(codes[item[0]][0], town_list[item[0]])
            self.assertEqual(codes[item[0]][1], code_list[item[0]])

    def populate_list(self, file):
        """Populate a list with the contents of a .txt file for testing"""
        with open(file, 'r') as test_file:
            test_list = test_file.read().splitlines()
        return test_list

    def build_path(self, file):
        """Wrapper function for os.path.join()"""
        path = os.path.join(os.path.dirname(__file__), 'testing', '{0}'.format(file))
        return path

if __name__ == '__main__':
    unittest.main()
