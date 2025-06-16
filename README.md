WGUPS Delivery Routing System
🚚 Project Overview
This repository contains the implementation of the WGUPS (Western Governors University Package Service) Delivery Routing System. The application reads package, address, and distance data from CSV files, stores package records in a hash table, and computes optimized delivery routes for multiple trucks while respecting hard deadlines, special notes, and grouping constraints.
📂 Table of Contents
Features
Getting Started
Prerequisites
Installation
Usage
Loading Data
Assigning Trucks
Running Deliveries
Querying Status
Project Structure
Core Components
Data Structures
Routing Algorithm
Testing
Performance & Limitations
Future Improvements
References
🔑 Features
Data Import & Cleaning: Reads packages.csv, addresses.csv, and distances.csv and normalizes address data.
Hash Table Storage: O(1) average lookup, insert, and delete for package records.
Truck Assignment: Distributes packages across three trucks based on deadlines, required groupings, and special notes.
Route Optimization: Nearest-neighbor heuristic to minimize total mileage within the 140-mile constraint.
Real-Time Status: Query package and truck status at arbitrary times via CLI.
🛠️ Getting Started
Prerequisites
Python 3.8 or higher
pip package manager
Installation
Clone the repository
git clone https://github.com/yourusername/wgups-routing.git
cd wgups-routing
Install dependencies
pip install -r requirements.txt
Prepare data Place the following CSV files in the data/ directory:
packages.csv
addresses.csv
distances.csv
▶️ Usage
All interactions happen via the command-line interface in main.py.
Loading Data
from wgups import data_loader
hub, distances = data_loader.load_data("data/")
Assigning Packages to Trucks
from wgups import routing
trucks = routing.assign_packages(hub)
Running Deliveries
from wgups import simulation
simulation.run_deliveries(trucks, distances)
Querying Status
python main.py status --time "09:25"
Output:
Package 15: Delivered at 09:12
Package 7: In transit (Truck 2)
... etc.
📁 Project Structure
w gups-routing/
├── data/                   # CSV input files
├── wgups/                  # Source code package
│   ├── data_loader.py
│   ├── hash_table.py
│   ├── routing.py
│   ├── simulation.py
│   └── cli.py
├── tests/                  # Unit tests
├── docs/                   # Documentation and logs
├── requirements.txt
└── main.py                 # CLI entry point
⚙️ Core Components
Data Structures
Hash Table (HashTable): Uses separate chaining to store Package objects keyed by package ID. Ensures O(1) average complexity for CRUD operations.
Routing Algorithm
Nearest-Neighbor Heuristic:
Start at the hub.
Repeatedly visit the closest unvisited delivery address.
Return to hub when all packages are delivered.
Constraints:
Total mileage per day ≤ 140 miles.
Truck capacity: max 16 packages.
Handle special notes (e.g., late arrivals, address corrections).
🔍 Testing
This project includes unit tests covering:
CSV data loading and cleaning
Hash table operations
Truck assignment logic
Route computation and mileage checks
Run tests with:
pytest --maxfail=1 --disable-warnings -q
📈 Performance & Limitations
The nearest-neighbor heuristic is fast but may not find global optimum routes.
Hash table load factor should be monitored to avoid performance degradation.
🚀 Future Improvements
Implement 2-opt or genetic algorithms for improved routing.
Automate data cleaning for edge-case addresses.
Introduce a graphical dashboard for live tracking.
📚 References
Lysecky, R., et al. C 950: Data Structures and Algorithms II, Zyante Inc., 2022.
