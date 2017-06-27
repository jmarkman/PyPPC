import tkinter as tk
from tkinter import ttk
import database
import os

class GUI:
    data = None

    def __init__(self):
        """Window initializer"""
        script_directory = os.path.dirname(__file__)
        # script_directory = os.getcwd()

        self.main_window = tk.Tk()
        self.data = database.Query(script_directory + r'\lookup.sqlite') # Change before deployment
        self.main_window.title("PPC Lookup")
        #self.main_window.iconbitmap(script_directory + r'\search.ico')
        self.main_window.resizable(0, 0)
        self.create_widgets()

        self.main_window.mainloop()

    def create_widgets(self):
        """Creates the various elements of the tkinter GUI"""
        # Labels
        self.state_label = tk.Label(self.main_window, text="State")
        self.state_label.grid(column=0, row=0)

        self.county_label = tk.Label(self.main_window, text="County")
        self.county_label.grid(column=1, row=0)

        # Dropdowns
        self.state_dropdown = ttk.Combobox(self.main_window, state='readonly')
        self.state_dropdown.grid(column=0, row=1)
        self.state_dropdown['values'] = self.data.get_state_list()
        self.state_dropdown.bind('<<ComboboxSelected>>', self.populate_county_combobox)

        self.county_dropdown = ttk.Combobox(self.main_window, state='readonly')
        self.county_dropdown.grid(column=1, row=1)
        self.county_dropdown.bind('<<ComboboxSelected>>', self.populate_results_tree)

        # Treeview for results and corresponding sidebar
        self.results_tree = ttk.Treeview(self.main_window, columns=('Town', 'PPC Code'))
        self.results_tree.heading('Town', text='Town', anchor=tk.CENTER)
        self.results_tree.heading('PPC Code', text='PPC Code', anchor=tk.CENTER)
        self.results_tree.column('Town', stretch=tk.YES, minwidth=0, width=220)
        self.results_tree.column('PPC Code', stretch=tk.YES, minwidth=0, width=140, anchor=tk.CENTER)
        self.results_tree['show'] = 'headings'
        self.results_scroll = tk.Scrollbar(self.main_window, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=self.results_scroll.set)
        self.results_scroll.grid(column=3, row=2, sticky='ns')
        self.results_tree.grid(column=0, columnspan=2, row=2)

        for child in self.main_window.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        self.end_query()

    def populate_county_combobox(self, event):
        """Fills the county combobox based on the selection in """
        self.county_dropdown['values'] = self.data.get_county_list(self.state_dropdown.get())
        self.end_query()

    def populate_results_tree(self, event):
        """Fills the results treeview with the towns and associated protection codes"""
        # Get the current contents of the Treeview and store them
        tree_contents = self.results_tree.get_children()
        if len(tree_contents) > 0:
            for row in self.results_tree.get_children():
                self.results_tree.delete(row)
        results = self.data.get_ppc_codes(self.state_dropdown.get(), self.county_dropdown.get())
        for result in results:
            self.results_tree.insert('', tk.END, text='', values=(result[0], result[1]))
        self.end_query()

    def end_query(self):
        """Call to the database module that closes the connection after all is said and done"""
        self.data.close_connection()


def launch():
    window = GUI()

if __name__ == '__main__':
    launch()