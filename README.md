<!DOCTYPE html>
<html lang="en">

  <h1>WGUPS Delivery Routing System</h1>

  <h2>🚚 Project Overview</h2>
  <p>This repository contains the implementation of the WGUPS (Western Governors University Package Service) Delivery Routing System. The application reads package, address, and distance data from CSV files, stores package records in a hash table, and computes optimized delivery routes for multiple trucks while respecting hard deadlines, special notes, and grouping constraints.</p>

  <h2>📂 Table of Contents</h2>
  <ul>
    <li>Features</li>
    <li>Getting Started
      <ul>
        <li>Prerequisites</li>
        <li>Installation</li>
      </ul>
    </li>
    <li>Usage
      <ul>
        <li>Loading Data</li>
        <li>Assigning Trucks</li>
        <li>Running Deliveries</li>
        <li>Querying Status</li>
      </ul>
    </li>
    <li>Project Structure</li>
    <li>Core Components
      <ul>
        <li>Data Structures</li>
        <li>Routing Algorithm</li>
      </ul>
    </li>
    <li>Testing</li>
    <li>Performance &amp; Limitations</li>
    <li>Future Improvements</li>
    <li>References</li>
  </ul>

  <h2>🔑 Features</h2>
  <ul>
    <li><strong>Data Import &amp; Cleaning</strong>: Reads <code>packages.csv</code>, <code>addresses.csv</code>, and <code>distances.csv</code> and normalizes address data.</li>
    <li><strong>Hash Table Storage</strong>: O(1) average lookup, insert, and delete for package records.</li>
    <li><strong>Truck Assignment</strong>: Distributes packages across three trucks based on deadlines, required groupings, and special notes.</li>
    <li><strong>Route Optimization</strong>: Nearest-neighbor heuristic to minimize total mileage within the 140-mile constraint.</li>
    <li><strong>Real-Time Status</strong>: Query package and truck status at arbitrary times via CLI.</li>
  </ul>

  <h2>🛠️ Getting Started</h2>
  <h3>Prerequisites</h3>
  <ul>
    <li>Python 3.8 or higher</li>
    <li><code>pip</code> package manager</li>
  </ul>

  <h3>Installation</h3>
  <ol>
    <li><strong>Clone the repository</strong>
      <pre><code>git clone https://github.com/yourusername/wgups-routing.git
cd wgups-routing</code></pre>
    </li>
    <li><strong>Install dependencies</strong>
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Prepare data</strong>
      <p>Place the following CSV files in the <code>data/</code> directory:</p>
      <ul>
        <li><code>packages.csv</code></li>
        <li><code>addresses.csv</code></li>
        <li><code>distances.csv</code></li>
      </ul>
    </li>
  </ol>

  <h2>▶️ Usage</h2>
  <p>All interactions happen via the command-line interface in <code>main.py</code>.</p>
  <h3>Loading Data</h3>
  <pre><code>from wgups import data_loader
hub, distances = data_loader.load_data("data/")</code></pre>

  <h3>Assigning Packages to Trucks</h3>
  <pre><code>from wgups import routing
trucks = routing.assign_packages(hub)</code></pre>

  <h3>Running Deliveries</h3>
  <pre><code>from wgups import simulation
simulation.run_deliveries(trucks, distances)</code></pre>

  <h3>Querying Status</h3>
  <pre><code>python main.py status --time "09:25"</code></pre>
  <p>Output:</p>
  <pre><code>Package 15: Delivered at 09:12
Package 7: In transit (Truck 2)
... etc.</code></pre>

  <h2>📁 Project Structure</h2>
  <pre><code>wgups-routing/
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
└── main.py                 # CLI entry point</code></pre>

  <h2>⚙️ Core Components</h2>
  <h3>Data Structures</h3>
  <p><strong>Hash Table</strong> (HashTable): Uses separate chaining to store Package objects keyed by package ID. Ensures O(1) average complexity for CRUD operations.</p>

  <h3>Routing Algorithm</h3>
  <p><strong>Nearest-Neighbor Heuristic</strong>:</p>
  <ol>
    <li>Start at the hub.</li>
    <li>Repeatedly visit the closest unvisited delivery address.</li>
    <li>Return to hub when all packages are delivered.</li>
  </ol>
  <p><strong>Constraints</strong>:</p>
  <ul>
    <li>Total mileage per day ≤ 140 miles.</li>
    <li>Truck capacity: max 16 packages.</li>
    <li>Handle special notes (e.g., late arrivals, address corrections).</li>
  </ul>

  <h2>🔍 Testing</h2>
  <p>This project includes unit tests covering:</p>
  <ul>
    <li>CSV data loading and cleaning</li>
    <li>Hash table operations</li>
    <li>Truck assignment logic</li>
    <li>Route computation and mileage checks</li>
  </ul>
  <p>Run tests with:</p>
  <pre><code>pytest --maxfail=1 --disable-warnings -q</code></pre>

  <h2>📈 Performance &amp; Limitations</h2>
  <ul>
    <li>The nearest-neighbor heuristic is fast but may not find global optimum routes.</li>
    <li>Hash table load factor should be monitored to avoid performance degradation.</li>
  </ul>

  <h2>🚀 Future Improvements</h2>
  <ul>
    <li>Implement 2-opt or genetic algorithms for improved routing.</li>
    <li>Automate data cleaning for edge-case addresses.</li>
    <li>Introduce a graphical dashboard for live tracking.</li>
  </ul>

  <h2>📚 References</h2>
  <ol>
    <li>Lysecky, R., et al. <em>C 950: Data Structures and Algorithms II</em>, Zyante Inc., 2022.</li>
  </ol>

</body>
</html>
