import tkinter as tk
from collections import deque

class CacheSimulatorGUI:
    def _init_(self, master):
        self.master = master
        master.title("Cache Simulator")
        self.cache_size_label = tk.Label(master, text="Cache Size:")
        self.cache_size_label.grid(row=0, column=0)
        self.cache_size_entry = tk.Entry(master)
        self.cache_size_entry.grid(row=0, column=1)
        self.block_size_label = tk.Label(master, text="Block Size:")
        self.block_size_label.grid(row=1, column=0)
        self.block_size_entry = tk.Entry(master)
        self.block_size_entry.grid(row=1, column=1)
        self.mapping_type_label = tk.Label(master, text="Mapping Type:")
        self.mapping_type_label.grid(row=2, column=0)
        self.mapping_type_var = tk.StringVar(master)
        self.mapping_type_var.set("Direct Mapping")
        self.mapping_type_menu = tk.OptionMenu(master, self.mapping_type_var, "Direct Mapping", "Fully Associative", "Set Associative", command=self.toggle_sets_option)
        self.mapping_type_menu.grid(row=2, column=1)
        self.sets_label = tk.Label(master, text="Number of Sets (for Set Associative):")
        self.sets_entry = tk.Entry(master)
        self.memory_trace_label = tk.Label(master, text="Memory Trace (comma-separated addresses):")
        self.memory_trace_label.grid(row=4, column=0)
        self.memory_trace_entry = tk.Entry(master)
        self.memory_trace_entry.grid(row=4, column=1)
        self.run_button = tk.Button(master, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=5, columnspan=2)
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=6, columnspan=2)
        self.cache_frame = tk.Frame(master)
        self.cache_frame.grid(row=7, columnspan=2)
        self.cache_labels = None
        self.hide_sets_option()

    def toggle_sets_option(self, *args):
        mapping_type = self.mapping_type_var.get()
        if mapping_type == "Set Associative":
            self.show_sets_option()
        else:
            self.hide_sets_option()

    def show_sets_option(self):
        self.sets_label.grid(row=3, column=0)
        self.sets_entry.grid(row=3, column=1)

    def hide_sets_option(self):
        self.sets_label.grid_forget()
        self.sets_entry.grid_forget()

    def run_simulation(self):
        cache_size_input = self.cache_size_entry.get()
        block_size_input = self.block_size_entry.get()
        mapping_type = self.mapping_type_var.get()
        memory_trace_input = self.memory_trace_entry.get()
        if not cache_size_input.isdigit() or not block_size_input.isdigit():
            self.result_label.config(text="Error: Cache size and block size must be positive integers.")
            return
        cache_size = int(cache_size_input)
        block_size = int(block_size_input)
        memory_trace = list(map(int, memory_trace_input.split(',')))
        if block_size >= cache_size or block_size <= 0:
            self.result_label.config(text="Error: Block size should be a positive integer less than cache size.")
            return
        hits = 0
        misses = 0
        hit_miss_text = ""
        if mapping_type == "Direct Mapping":
            cache = Cache(cache_size, block_size)
        elif mapping_type == "Fully Associative":
            cache = Cache(cache_size, block_size, associativity=cache_size // block_size)
        elif mapping_type == "Set Associative":
            sets_input = self.sets_entry.get()
            if not sets_input.isdigit() or int(sets_input) <= 0:
                self.result_label.config(text="Error: Number of sets must be a positive integer.")
                return
            num_sets = int(sets_input)
            cache = SetAssociativeCache(cache_size, block_size, num_sets)
        else:
            self.result_label.config(text="Error: Invalid mapping type.")
            return
        for address in memory_trace:
            if cache.read(address):
                hits += 1
                hit_miss_text += f"Address {address}: Cache Hit\n"
            else:
                misses += 1
                cache.write(address)
                hit_miss_text += f"Address {address}: Cache Miss\n"
        result_text = f"Total Hits: {hits}, Total Misses: {misses}\n\n{hit_miss_text}"
        self.result_label.config(text=result_text)

class Cache:
    def _init_(self, cache_size, block_size, associativity=1):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.cache = deque(maxlen=cache_size // block_size)

    def read(self, address):
        block_address = address // self.block_size
        for block in self.cache:
            if block == block_address:
                return True
        return False

    def write(self, address):
        block_address = address // self.block_size
        if block_address not in self.cache:
            self.cache.append(block_address)

class SetAssociativeCache(Cache):
    def _init_(self, cache_size, block_size, num_sets):
        associativity = cache_size // (block_size * num_sets)
        super()._init_(cache_size, block_size, associativity)

def main():
    root = tk.Tk()
    app = CacheSimulatorGUI(root)
    root.mainloop()

if _name_ == "_main_":
    main()
