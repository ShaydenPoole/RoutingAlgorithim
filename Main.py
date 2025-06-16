"""
WGUPS Package Delivery System

This program simulates package delivery for WGUPS using three trucks. It lets users check 
package and truck status at different times. We use a nearest neighbor algorithm to plan 
routes and a hash table to store package info for quick lookups.

I'm still working on optimizing the route planning.

Student ID: 011160034
"""

import csv
from datetime import datetime
from DSA_A import minimal_standardize_location_name, load_distance_table_with_address_matching

class HashTable:
    """
    This is the hashtable data structure. 
    It helps us store and retrieve package data.
    """
    def __init__(self, capacity=40):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key):
        """This calculates where in our table we should put or find an item."""
        return hash(key) % self.capacity

    def insert(self, key, value):
        """This adds a new item to our table, or updates an existing one."""
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[hash_index].append([key, value])

    def get(self, key):
        """This retrieves an item from our table. If it's not there, it raises an error."""
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return item[1]
        raise KeyError(key)

    def remove(self, key):
        """This removes an item from our table. If it's not there, it raises an error."""
        hash_index = self._hash(key)
        for i, item in enumerate(self.table[hash_index]):
            if item[0] == key:
                del self.table[hash_index][i]
                return
        raise KeyError(key)

    def __iter__(self):
        """This lets us loop through all items in our table."""
        for bucket in self.table:
            for key, value in bucket:
                yield key, value

class Truck:
    """
    This is the delivery Truck class. It keeps track of its packages,
    where it is, what time it is, and how far it has traveled.
    """
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.current_location = 'HUB'
        self.time = 8 * 60  # Start at 8:00 AM
        self.distance_traveled = 0.0

def load_package_data(file_path):
    """
    This function reads the package data from our CSV file and places the information into a HashTable.
    Each package gets its own list. We start off with all packages at the hub and not currently delivered.
    """
    package_table = HashTable()
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            package_details = [
                row['PackageID'],
                row['Address'],
                row['DeliveryDeadline'],
                row['City'],
                row['Zip'],
                row['WeightKILO'],
                'At the hub',
                None,
                row['SpecialNotes']
            ]
            package_table.insert(row['PackageID'], package_details)
    return package_table

def manual_load_packages(package_table, trucks):
    """
    This function is my current solution for loading packages onto trucks.
    These are preset lists that decide which packages are grouped for what truck. 
    We loop through each truck's package list, grab the package from our package 
    table, and add it to the corresponding truck. In the future we could automate this function.
    """
    truck_1_packages = ['1', '13', '14', '15', '16', '19', '20', '29', '30', '31', '34', '37', '40', '4', '5', '8']
    truck_2_packages = ['3', '18', '25', '28', '32', '36', '38', '7', '10', '11', '12', '17', '21', '23', '24']
    truck_3_packages = ['2', '9', '6','22', '26', '27', '33', '35', '39']

    for package_id in truck_1_packages:
        package = package_table.get(package_id)
        if package:
            trucks[0].packages.append(package)
    
    for package_id in truck_2_packages:
        package = package_table.get(package_id)
        if package:
            trucks[1].packages.append(package)
    
    for package_id in truck_3_packages:
        package = package_table.get(package_id)
        if package:
            trucks[2].packages.append(package)

def calculate_distance(location1, location2, location_to_index, distance_table):
    """
    This function figures out distances between two package locations. It uses our 
    distance matrix to look up the distance. If it can't find one of the locations, 
    it just returns None. This is important for planning routes and figuring 
    out delivery times.
    """
    index1 = location_to_index.get(minimal_standardize_location_name(location1))
    index2 = location_to_index.get(minimal_standardize_location_name(location2))
    if index1 is not None and index2 is not None:
        return float(distance_table[index1][index2])
    return None

def plan_routes(trucks, location_to_index, distance_table):
    """
    This function plans routes for each truck using a simple Nearest Neighbor algorithm.
    For each truck, it will have it start at current location, initially the hub, 
    then it will find where the next nearest undelivered package is. It will then add the 
    package to the route and updates the truck's current location. It repeats this 
    until no undelivered packages are left.
    """
    for truck in trucks:
        current_location = truck.current_location
        remaining_packages = truck.packages[:]
        route = []

        while remaining_packages:
            nearest_package = min(remaining_packages, key=lambda pkg: calculate_distance(current_location, pkg[1], location_to_index, distance_table))
            route.append(nearest_package)
            remaining_packages.remove(nearest_package)
            current_location = nearest_package[1]

        truck.packages = route

def simulate_delivery(trucks, location_to_index, distance_table):
    """
    This function simulates delivering packages. It goes through 
    each truck, and calculates how long to arrive at each delivery, then marks the
    packages as delivered. Since truck 3 starts later, we 
    have to handle that one package with the wrong address thus delaying the trucks start time. 
    After all deliveries, it sends the trucks back to the hub.
    """
    for truck in trucks:
        if truck.truck_id == 3:
            truck.time = 10 * 60 + 20  # Truck 3 starts later due to package 9
            for package in truck.packages:
                if package[0] == '9':
                    package[1] = '410 S State St, Salt Lake City, UT 84111'

        for package in truck.packages:
            distance = calculate_distance(truck.current_location, package[1], location_to_index, distance_table)
            if distance is not None:
                travel_time = distance / 18 * 60  # 18 mph
                truck.time += travel_time
                truck.distance_traveled += distance
                package[6] = 'Delivered'
                package[7] = truck.time
                truck.current_location = package[1]
        
        if truck.truck_id == 3:
            truck.current_location = '410 S State St, Salt Lake City, UT 84111'
            package_9 = next((pkg for pkg in truck.packages if pkg[0] == '9'), None)
            if package_9 and truck.time >= 10 * 60 + 20:
                package_9[6] = 'Delivered'
                package_9[7] = truck.time
        
        distance_to_hub = calculate_distance(truck.current_location, "HUB", location_to_index, distance_table)
        if distance_to_hub:
            truck.distance_traveled += distance_to_hub
        truck.current_location = 'hub'

def get_package_status_at_time(trucks, time_in_minutes):
    """
    This function checks the status of all packages at a specific time.
    It figures out if each package is at the hub, out for delivery, or already delivered.
    """
    status_report = []
    for truck in trucks:
        for package in truck.packages:
            if package[7] is None:
                status = 'At the hub'
            elif package[7] <= time_in_minutes + 8 * 60:
                status = 'Delivered'
            else:
                status = 'En route'
            status_report.append((package[0], package[1], status, package[7]))
    return status_report

def display_status_report(status_report):
    """
    This function takes our status report and prints it out in a simple format.
    It shows each package's ID, address, status, and delivery time (if applicable).
    """
    print("\nPackage Status Report:")
    for package_id, address, status, delivery_time in status_report:
        if delivery_time is not None:
            hours, minutes = divmod(delivery_time, 60)
            time_display = f"{int(hours):02}:{int(minutes):02}"
        else:
            time_display = "N/A"
        print(f"Package {package_id} to {address} is {status}. Delivery time: {time_display}.")

def lookup_package(package_id, package_table, trucks, time_in_minutes):
    """
    Look up and return all relevant data for a specific package by ID.
    Includes delivery address, deadline, city, zip, weight, status, and delivery time.
    """
    package = package_table.get(package_id)
    if not package:
        return None

    # Check delivery status
    status_report = get_package_status_at_time(trucks, time_in_minutes)
    package_status = next((s for s in status_report if s[0] == package_id), None)
    
    if package_status:
        return {
            'Package ID': package[0],
            'Delivery Address': package[1],
            'Delivery Deadline': package[2],
            'City': package[3],
            'Zip Code': package[4],
            'Weight': package[5],
            'Status': package_status[2],  # Status from the status report
            'Delivery Time': package_status[3] if package_status[3] else "N/A"
        }
    else:
        return None

def get_truck_status_at_time(trucks, truck_id, time_in_minutes):
    """
    This function checks the status of a specific truck at a given time.
    It shows where the truck is and the status of all corresponding packages.
    """
    truck = next((t for t in trucks if t.truck_id == truck_id), None)
    if not truck:
        print(f"Truck {truck_id} not found.")
        return

    print(f"\nTruck {truck_id} Status at {time_in_minutes} minutes since 8:00 AM:")
    for package in truck.packages:
        if package[7] is None:
            status = 'At the hub'
        elif package[7] <= time_in_minutes + 8 * 60:
            status = 'Delivered'
        else:
            status = 'En route'
        if package[7] is not None:
            hours, minutes = divmod(package[7], 60)
            time_display = f"{int(hours):02}:{int(minutes):02}"
        else:
            time_display = "N/A"
        print(f"  Package {package[0]} to {package[1]} is {status}. Delivery time: {time_display}.")

def get_total_mileage(trucks):
    """
    This function adds up all the miles driven by all the trucks.
    It's useful for seeing how efficient our delivery routes are.
    """
    total_mileage = 0.0
    for truck in trucks:
        distance_to_hub = calculate_distance(truck.current_location, "HUB", location_to_index, distance_table)
        if distance_to_hub:
            truck.distance_traveled += distance_to_hub
        print(f"Truck {truck.truck_id} total mileage: {truck.distance_traveled:.2f} miles")
        total_mileage += truck.distance_traveled
    print(f"Total mileage for all trucks: {total_mileage:.2f} miles")

# Load package data
package_table = load_package_data('WGUPS_Package_File.csv')

# Load distance table
location_to_index, distance_table, cleaned_headers = load_distance_table_with_address_matching('WGUPS_Distance_Table_Cleaned.csv')

# Initialize trucks
trucks = [Truck(1), Truck(2), Truck(3)]

# Load packages onto trucks
manual_load_packages(package_table, trucks)

# Plan routes for each truck
plan_routes(trucks, location_to_index, distance_table)

# Simulate the delivery
simulate_delivery(trucks, location_to_index, distance_table)

# Output loaded data and initialized trucks
print("Package Data Loaded:", sum(1 for _ in package_table), "packages")
print("Distance Table Loaded:", len(distance_table), "locations")
print("Trucks Initialized:", len(trucks))

def display_menu():
    """
    This function uses a command line interface as a graphic user interface and 
    shows the main menu and handles user input. It lets the user choose an option 
    of what they want to do: check package status,
    check all packages, see total mileage, or check a specific truck's status.
    """
    while True:
        print("\nWGUPS Tracking System")
        print("1. Check package status")
        print("2. Check all packages")
        print("3. Check total mileage")
        print("4. Check truck status")
        print("5. Exit")
        choice = input("What would you like to do? ")

        if choice == '1':
            package_id = input("Enter package ID: ")
            time_input = input("Enter time (HH:MM AM/PM): ")
            time_obj = datetime.strptime(time_input, '%I:%M %p')
            time_in_minutes = time_obj.hour * 60 + time_obj.minute - 8 * 60
            if time_in_minutes < 0:
                time_in_minutes += 24 * 60

            status_report = get_package_status_at_time(trucks, time_in_minutes)
            package_status = next((s for s in status_report if s[0] == package_id), None)
            if package_status:
                display_status_report([package_status])
            else:
                print(f"Package {package_id} not found.")

        elif choice == '2':
            time_input = input("Enter time (HH:MM AM/PM): ")
            time_obj = datetime.strptime(time_input, '%I:%M %p')
            time_in_minutes = time_obj.hour * 60 + time_obj.minute - 8 * 60
            if time_in_minutes < 0:
                time_in_minutes += 24 * 60

            status_report = get_package_status_at_time(trucks, time_in_minutes)
            display_status_report(status_report)

        elif choice == '3':
            get_total_mileage(trucks)

        elif choice == '4':
            truck_id = int(input("Enter truck ID (1, 2, or 3): "))
            time_input = input("Enter time (HH:MM AM/PM): ")
            time_obj = datetime.strptime(time_input, '%I:%M %p')
            time_in_minutes = time_obj.hour * 60 + time_obj.minute - 8 * 60
            if time_in_minutes < 0:
                time_in_minutes += 24 * 60

            get_truck_status_at_time(trucks, truck_id, time_in_minutes)

        elif choice == '5':
            print("Thanks for using the WGUPS Tracking System. Have a great day!")
            break

        else:
            print("Oops! That's not a valid choice. Please enter a number between 1 and 5.")

# Run the menu
if __name__ == "__main__":
    display_menu()
