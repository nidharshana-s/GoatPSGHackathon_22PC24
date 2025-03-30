# Fleet Robots Navigation System

A Python-based fleet management system for autonomous robots with a graphical user interface for navigation and control.

## Features

- Interactive GUI for fleet management
- Navigation graph-based path planning
- Real-time robot status monitoring
- Logging system for tracking operations
- Modular architecture for easy extension

## Project Structure

```
fleet-robots/
├── src/
│   ├── gui/         # Graphical user interface components
│   ├── models/      # Core data models and algorithms
│   ├── utils/       # Utility functions and helpers
│   └── logs/        # Application logs
├── data/            # Data files including navigation graphs
├── main.py          # Application entry point
└── requirements.txt # Project dependencies
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fleet-robots
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure you have the required navigation graph file (`nav_graph_2.json`) in the appropriate location.

2. Run the application:
```bash
python main.py
```

3. The GUI will launch, allowing you to:
   - View and interact with the navigation graph
   - Monitor robot fleet status
   - Control robot movements
   - View operation logs

## Dependencies

- PyQt5: For the graphical user interface
- NetworkX: For graph-based navigation algorithms

## Development

The project follows a modular architecture:
- `gui/`: Contains all GUI-related components
- `models/`: Implements core data structures and algorithms
- `utils/`: Provides helper functions and utilities
- `logs/`: Stores application logs for debugging and monitoring

##Visual Output

Output Window:
![image](https://github.com/user-attachments/assets/82387dd8-d55b-4dd9-8245-9aec0887e241)

Robots Moving
![image](https://github.com/user-attachments/assets/82440a57-e60f-455f-958c-c2a60553cad4)

