# from PyQt5 import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from data_table import DataTable
# from command_buttons import CommandButtons

# class Tabs(QTabWidget):
#     def __init__(self):
#         super().__init__()

#         self.datatable = DataTable()
#         self.command_buttons = CommandButtons()

#         self.command_buttons.buttons[0].clicked.connect(self.upload_waypoints)
#         self.tabs.addTab(self.datatable, "Data")
#         self.tabs.addTab(self.command_buttons, "Commands")
#         self.tabs.addTab(self.waypointEditor, "Flight Plan")
#         self.left_layout.addWidget(self.tabs)