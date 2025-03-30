import sys
from PyQt5.QtWidgets import QApplication
from models.nav_graph import NavGraph
from gui.fleet_gui import FleetGUI

def main():
    app = QApplication(sys.argv)
    nav_graph = NavGraph("nav_graph_2.json")  # Ensure this file exists
    gui = FleetGUI(nav_graph)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()