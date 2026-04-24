import random
import math
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
def main():
    root = tk.Tk()
    root.title("Optimization Algorithm Selector")
    root.geometry("400x200")
    def select_algorithm(choice):
        root.destroy()
        if choice == "Genetic Algorithm":
            run_genetic_algorithm()
        elif choice == "Simulated Annealing":
            run_simulated_annealing()
    tk.Label(root, text="Select Optimization Algorithm", font=('Arial', 14)).pack(pady=20)

    genetic_btn = tk.Button(root, text="Genetic Algorithm",
                            command=lambda: select_algorithm("Genetic Algorithm"),
                            width=20, height=2)
    genetic_btn.pack(pady=10)

    sa_btn = tk.Button(root, text="Simulated Annealing",
                       command=lambda: select_algorithm("Simulated Annealing"),
                       width=20, height=2)
    sa_btn.pack(pady=10)
    root.mainloop()
def distance(a, b):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
def run_simulated_annealing():
    def handle_action(action_type):
        if action_type == 'generate':
            try:
                count = int(num_cities_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number of cities.")
                return
            for widget in city_frame.winfo_children():
                widget.destroy()
            city_entries.clear()
            for i in range(count):
                row = tk.Frame(city_frame)
                tk.Label(row, text=f"City {i + 1}").pack(side=tk.LEFT, padx=5)
                x = tk.Entry(row, width=5)
                y = tk.Entry(row, width=5)
                p = tk.Entry(row, width=5)
                w = tk.Entry(row, width=5)
                x.pack(side=tk.LEFT)
                y.pack(side=tk.LEFT)
                p.pack(side=tk.LEFT)
                w.pack(side=tk.LEFT)
                row.pack(pady=2)
                city_entries.append((x, y, p, w))
        elif action_type == 'run':
            try:
                truck = int(truck_entry.get())
                capacity = int(capacity_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter numeric values for truck and capacity.")
                return
            zero_city = [0, 0, 0, 0, 0]
            cities = []
            for i, (x_ent, y_ent, p_ent, w_ent) in enumerate(city_entries, 1):
                try:
                    x = int(x_ent.get())
                    y = int(y_ent.get())
                    p = int(p_ent.get())
                    w = int(w_ent.get())
                    if not (0 <= x <= 100 and 0 <= y <= 100 and 1 <= p <= 5 and w >= 0):
                        raise ValueError
                    cities.append([i, x, y, p, w])
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Invalid data for City {i}")
                    return
            additional = []
            for c in cities:
                if c[4] > capacity:
                    remaining = c[4] - capacity
                    c[4] = capacity
                    new = c.copy()
                    new[4] = remaining
                    additional.append(new)
            cities.extend(additional)
            if truck == 0:
                messagebox.showerror("Invalid Input", "Number of trucks cannot be zero.")
                return
            if len(cities) % 2 != 0:
                truck_city = (len(cities) // truck) + 1
            else:
                truck_city = (len(cities) // truck)
            work_city = cities.copy()
            random.shuffle(work_city)
            trucks = []
            Int_temperature = 1000
            cooling_rate = 0.99
            for t in range(truck):
                temperature = Int_temperature
                path = []
                for c in work_city:
                    if c[3] == 1:
                        path.append(c)
                        work_city.remove(c)
                        break
                else:
                    if work_city:
                        path.append(work_city.pop())
                if not path:
                    continue
                current_city = path[-1]
                t_weight = current_city[4]
                while len(path) < truck_city and work_city:
                    next_city = random.choice(work_city)
                    if t_weight + next_city[4] > capacity:
                        temperature *= cooling_rate
                        continue
                    a = distance(zero_city, next_city)
                    b = distance(zero_city, current_city)
                    accept_prob = math.exp((b - a) / temperature)
                    if random.random() < accept_prob or temperature <= 1:
                        path.append(next_city)
                        work_city.remove(next_city)
                        current_city = next_city
                        t_weight += current_city[4]
                    temperature *= cooling_rate
                trucks.append(path)
            output_text.delete(1.0, tk.END)
            final_distance = 0
            for i, truck_path in enumerate(trucks, 1):
                output_text.insert(tk.END, f"\n🚚 Truck {i} path:\n")
                total_distance = distance(zero_city, truck_path[0])
                for j in range(len(truck_path) - 1):
                    d = distance(truck_path[j], truck_path[j + 1])
                    total_distance += d
                    output_text.insert(tk.END,
                                       f"From City {truck_path[j][0]} to City {truck_path[j + 1][0]}: {d:.2f} Km\n")
                output_text.insert(tk.END, f"Total distance for Truck {i}: {total_distance:.2f} Km\n")
                final_distance += total_distance
            output_text.insert(tk.END, f"\nFinal total distance: {final_distance:.2f} Km\n")
    root = tk.Tk()
    root.title("Truck Routing Optimizer - Simulated Annealing")
    tk.Label(root, text="Number of Trucks:").pack()
    truck_entry = tk.Entry(root)
    truck_entry.pack()
    tk.Label(root, text="Truck Capacity (kg):").pack()
    capacity_entry = tk.Entry(root)
    capacity_entry.pack()
    tk.Label(root, text="Number of Cities:").pack()
    num_cities_entry = tk.Entry(root)
    num_cities_entry.pack()
    tk.Button(root, text="Generate City Inputs", command=lambda: handle_action('generate')).pack(pady=5)
    city_frame = tk.Frame(root)
    city_frame.pack()
    city_entries = []
    tk.Button(root, text="Run", command=lambda: handle_action('run'), bg="#4CAF50", fg="white").pack(pady=10)
    output_text = scrolledtext.ScrolledText(root, width=80, height=20)
    output_text.pack(padx=10, pady=10)
    root.mainloop()
def run_genetic_algorithm():
    def handle_action(action_type):
        if action_type == 'generate':
            try:
                num_vehicles = int(vehicle_count_entry.get())
                num_packages = int(package_count_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for vehicles and packages.")
                return
            for widget in vehicle_frame.winfo_children():
                widget.destroy()
            for widget in package_frame.winfo_children():
                widget.destroy()
            vehicle_entries.clear()
            package_entries.clear()
            for i in range(num_vehicles):
                row = tk.Frame(vehicle_frame)
                tk.Label(row, text=f"Vehicle {i + 1} Capacity:").pack(side=tk.LEFT, padx=5)
                entry = tk.Entry(row, width=10)
                entry.pack(side=tk.LEFT)
                row.pack(pady=2)
                vehicle_entries.append(entry)
            for i in range(num_packages):
                pkg_frame = tk.Frame(package_frame)
                tk.Label(pkg_frame, text=f"Package {i + 1}").pack(side=tk.LEFT, padx=5)
                tk.Label(pkg_frame, text="X:").pack(side=tk.LEFT)
                x_entry = tk.Entry(pkg_frame, width=5)
                x_entry.pack(side=tk.LEFT)
                tk.Label(pkg_frame, text="Y:").pack(side=tk.LEFT)
                y_entry = tk.Entry(pkg_frame, width=5)
                y_entry.pack(side=tk.LEFT)
                tk.Label(pkg_frame, text="Weight:").pack(side=tk.LEFT)
                w_entry = tk.Entry(pkg_frame, width=5)
                w_entry.pack(side=tk.LEFT)
                tk.Label(pkg_frame, text="Priority:").pack(side=tk.LEFT)
                p_entry = tk.Entry(pkg_frame, width=5)
                p_entry.pack(side=tk.LEFT)
                pkg_frame.pack(pady=2)
                package_entries.append((x_entry, y_entry, w_entry, p_entry))
        elif action_type == 'run':
            vehicles = {}
            for i, entry in enumerate(vehicle_entries, 1):
                try:
                    capacity = int(entry.get())
                    if capacity <= 0:
                        raise ValueError
                    vehicles[f"V{i}"] = capacity
                except ValueError:
                    messagebox.showerror("Invalid Input",
                                         f"Invalid capacity for Vehicle {i}. Must be positive integer.")
                    return
            packages = {}
            for i, (x_ent, y_ent, w_ent, p_ent) in enumerate(package_entries, 1):
                try:
                    x = int(x_ent.get())
                    y = int(y_ent.get())
                    weight = int(w_ent.get())
                    priority = int(p_ent.get())

                    if not (1 <= x <= 100 and 1 <= y <= 100):
                        messagebox.showerror("Invalid Input", f"Coordinates for Package {i} must be between 1-100.")
                        return
                    if weight <= 0:
                        messagebox.showerror("Invalid Input", f"Weight for Package {i} must be positive.")
                        return
                    if not 1 <= priority <= 5:
                        messagebox.showerror("Invalid Input", f"Priority for Package {i} must be between 1-5.")
                        return

                    packages[f"P{i}"] = [x, y, weight, priority]
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Invalid data for Package {i}. Please enter numeric values.")
                    return
            best_solution = run_ga_algorithm(vehicles, packages)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "=== Best Solution Found ===\n\n")
            total_distance = best_solution[1]
            solution = best_solution[0]
            for vehicle, packages_list in solution.items():
                output_text.insert(tk.END, f"🚛 {vehicle} (Capacity: {vehicles[vehicle]}kg) delivers:\n")
                current_location = [0, 0]
                vehicle_distance = 0
                for pkg in packages_list:
                    pkg_data = packages[pkg]
                    pkg_location = pkg_data[:2]
                    dist = math.sqrt(
                        (pkg_location[0] - current_location[0]) ** 2 + (pkg_location[1] - current_location[1]) ** 2)
                    vehicle_distance += dist
                    current_location = pkg_location
                    output_text.insert(tk.END,
                                       f"  📦 {pkg}: Location ({pkg_data[0]},{pkg_data[1]}), Weight {pkg_data[2]}kg, Priority {pkg_data[3]}\n")
                dist = math.sqrt((0 - current_location[0]) ** 2 + (0 - current_location[1]) ** 2)
                vehicle_distance += dist
                output_text.insert(tk.END, f"  Total distance for {vehicle}: {vehicle_distance:.2f} km\n\n")
            output_text.insert(tk.END, f"Final total distance: {total_distance:.2f} km\n")
    def run_ga_algorithm(vehicles, packages):
        parents = []
        children = []
        N = random.randint(50, 100)
        maxLoop = 0
        while len(parents) < N and maxLoop < 1000:
            maxLoop += 1
            V = list(vehicles.keys())
            keys = list(packages.keys())
            random.shuffle(keys)
            new_parent = {v: [] for v in V}
            vehicle_remaining = {v: vehicles[v] for v in V}
            success = True
            for pkg in keys:
                pkg_weight = packages[pkg][2]
                assigned = False
                random.shuffle(V)
                for v in V:
                    if vehicle_remaining[v] >= pkg_weight:
                        new_parent[v].append(pkg)
                        vehicle_remaining[v] -= pkg_weight
                        assigned = True
                        break
                if not assigned:
                    success = False
                    break
            if success:
                total_distance = distance_calc(new_parent, packages)
                parents.append((new_parent, total_distance))
        parents = best_distances(parents)
        first40 = divide_packages(len(packages))
        for i in range(500):
            cross_over(parents, children, first40, packages, vehicles)
            parents = children
            children = []
            parents.sort(key=lambda x: x[1])
        return parents[0]
    def distance_calc(parent, packages):
        total_distance = 0
        shop_coords = [0, 0]
        for vehicle, package_list in parent.items():
            if not package_list:
                continue
            first_package = package_list[0]
            first_coords = packages[first_package][:2]
            distance = math.sqrt((first_coords[0] - shop_coords[0]) ** 2 + (first_coords[1] - shop_coords[1]) ** 2)
            total_distance += distance
            for i in range(len(package_list) - 1):
                current_package = package_list[i]
                next_package = package_list[i + 1]
                current_coords = packages[current_package][:2]
                next_coords = packages[next_package][:2]
                priority = packages[current_package][3]
                distance = math.sqrt(
                    (next_coords[0] - current_coords[0]) ** 2 + (next_coords[1] - current_coords[1]) ** 2)
                total_distance += distance + priority
            last_package = package_list[-1]
            last_coords = packages[last_package][:2]
            priority = packages[last_package][3]
            distance = math.sqrt((last_coords[0] - shop_coords[0]) ** 2 + (last_coords[1] - shop_coords[1]) ** 2)
            total_distance += distance + priority
        return total_distance
    def best_distances(parents_with_distances):
        parents_with_distances.sort(key=lambda x: x[1])
        best_50 = parents_with_distances[:50]
        return best_50
    def divide_packages(n):
        first40 = math.floor(n * 0.4)
        return first40
    def cross_over(parents, children, first40, packages, vehicles):
        V = list(vehicles.keys())
        while parents:
            parent1_dict, _ = parents[0]
            parent2_dict, _ = parents[1]
            del parents[0]
            del parents[0]
            parent1_packages = []
            parent2_packages = []
            for v in V:
                parent1_packages.extend(parent1_dict.get(v, []))
                parent2_packages.extend(parent2_dict.get(v, []))
            first_child_packages = []
            used_packages = set()
            for pkg in parent1_packages[:first40]:
                if pkg not in used_packages:
                    first_child_packages.append(pkg)
                    used_packages.add(pkg)
            for pkg in parent2_packages:
                if pkg not in used_packages:
                    first_child_packages.append(pkg)
                    used_packages.add(pkg)
            second_child_packages = []
            used_packages = set()
            for pkg in parent2_packages[:first40]:
                if pkg not in used_packages:
                    second_child_packages.append(pkg)
                    used_packages.add(pkg)
            for pkg in parent1_packages:
                if pkg not in used_packages:
                    second_child_packages.append(pkg)
                    used_packages.add(pkg)
            first_child = assign_packages(first_child_packages, vehicles, packages)
            second_child = assign_packages(second_child_packages, vehicles, packages)
            n = random.randint(1, 100)
            if 0 < n < 11:
                first_child = mutation(first_child, vehicles, packages)
            total_distance = distance_calc(first_child, packages)
            children.append((first_child, total_distance))
            n = random.randint(1, 100)
            if 0 < n < 11:
                second_child = mutation(second_child, vehicles, packages)
            total_distance = distance_calc(second_child, packages)
            children.append((second_child, total_distance))
    def assign_packages(child_packages, vehicles, packages):
        total_packages = len(child_packages)
        child = {v: [] for v in vehicles}
        vehicle_remaining = {v: vehicles[v] for v in vehicles}
        unassigned_packages = []
        pkg_index = 0
        for v in vehicles:
            max_per_vehicle = random.randint(1, max(1, int(0.4 * total_packages)))
            assigned_count = 0
            while assigned_count < max_per_vehicle and pkg_index < total_packages:
                pkg = child_packages[pkg_index]
                pkg_weight = packages[pkg][2]
                if vehicle_remaining[v] >= pkg_weight:
                    child[v].append(pkg)
                    vehicle_remaining[v] -= pkg_weight
                    assigned_count += 1
                else:
                    unassigned_packages.append(pkg)
                pkg_index += 1
        unassigned_packages.extend(child_packages[pkg_index:])
        final_unassigned = []
        for pkg in unassigned_packages:
            pkg_weight = packages[pkg][2]
            placed = False
            for v in vehicles:
                if vehicle_remaining[v] >= pkg_weight:
                    child[v].append(pkg)
                    vehicle_remaining[v] -= pkg_weight
                    placed = True
                    break
            if not placed:
                final_unassigned.append(pkg)
        if final_unassigned:
            print("Warning: These packages could not fit in any vehicle:", final_unassigned)
        return child
    def mutation(child, vehicles_capacity, packages):
        vehicles = [v for v in child if child[v]]
        if len(vehicles) < 2:
            return child
        v1 = random.choice(vehicles)
        v2 = random.choice(vehicles)
        if not child[v1] or not child[v2]:
            return child
        pkg1 = random.choice(child[v1])
        pkg2 = random.choice(child[v2])
        w1 = packages[pkg1][2]
        w2 = packages[pkg2][2]
        sum1 = sum(packages[p][2] for p in child[v1])
        sum2 = sum(packages[p][2] for p in child[v2])
        if sum1 - w1 + w2 <= vehicles_capacity[v1] and sum2 - w2 + w1 <= vehicles_capacity[v2]:
            child[v1].remove(pkg1)
            child[v1].append(pkg2)
            child[v2].remove(pkg2)
            child[v2].append(pkg1)
        return child
    root = tk.Tk()
    root.title("Package Delivery Optimizer - Genetic Algorithm")
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)
    tk.Label(input_frame, text="Number of Vehicles:").grid(row=0, column=0, padx=5, pady=5)
    vehicle_count_entry = tk.Entry(input_frame, width=10)
    vehicle_count_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(input_frame, text="Number of Packages:").grid(row=1, column=0, padx=5, pady=5)
    package_count_entry = tk.Entry(input_frame, width=10)
    package_count_entry.grid(row=1, column=1, padx=5, pady=5)
    generate_btn = tk.Button(input_frame, text="Generate Input Fields",
                             command=lambda: handle_action('generate'))
    generate_btn.grid(row=2, column=0, columnspan=2, pady=10)
    vehicle_frame = tk.LabelFrame(root, text="Vehicle Capacities (kg)")
    vehicle_frame.pack(fill=tk.X, padx=10, pady=5)
    package_frame = tk.LabelFrame(root, text="Package Details")
    package_frame.pack(fill=tk.X, padx=10, pady=5)
    run_btn = tk.Button(root, text="Run Genetic Algorithm",
                        command=lambda: handle_action('run'),
                        bg="#4CAF50", fg="white")
    run_btn.pack(pady=10)
    output_text = scrolledtext.ScrolledText(root, width=80, height=20)
    output_text.pack(padx=10, pady=10)
    vehicle_entries = []
    package_entries = []
    root.mainloop()
if __name__ == '__main__':
    main()