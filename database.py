#! python3
"""User-defined SQLite database access and reading"""
import sqlite3

class Query:
    """Class representation of the connection to the sqlite database
    and the queries made to it to retrieve the PPC codes
    """
    # Class variables
    db_conn = None
    db_cursor = None

    def __init__(self, connect):
        """Initializer for Query class"""
        self.connect = connect
        self.db_conn = sqlite3.connect(self.connect)
        self.db_cursor = self.db_conn.cursor()

    def get_state_list(self):
        """Gets list of states for combobox population"""
        self.db_cursor.execute('select State from States')
        db_states = self.db_cursor.fetchall()

        gui_states = []
        for state in db_states:
            gui_states.append(state[0])
        return gui_states

    def get_county_list(self, state):
        """Gets list of counties for combobox population"""
        self.db_cursor.execute('select County from Counties where State like \'{0}\''.format(state))
        db_counties = self.db_cursor.fetchall()

        gui_counties = []
        for county in db_counties:
            gui_counties.append(county[0])
        return gui_counties

    def get_ppc_codes(self, state, county):
        """Gets the towns and PPC codes associated with a given state and county"""
        self.db_cursor.execute(
            'select Town, Code from Towns where State like \'{0}\' and County like \'{1}\''
            .format(state, county)
        )
        ppc_codes = self.db_cursor.fetchall()

        gui_ppc_codes = []
        for code in ppc_codes:
            gui_ppc_codes.append(code)
        return gui_ppc_codes

    def close_connection(self):
        """Wrapper for closing the connection to the database"""
        self.db_conn.close()
