import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

def find_longest_common_prefix(productions):
    if not productions:
        return ""
    
    prefix = productions[0]
    for prod in productions[1:]:
        while not prod.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def left_factor(grammar):
    new_grammar = {}
    created_non_terminals = set()

    for non_terminal, productions in grammar.items():
        prefix_map = defaultdict(list)
        
        for prod in productions:
            for i in range(1, len(prod) + 1):
                prefix_map[prod[:i]].append(prod)

        longest_common_prefix = ""
        for prefix, group in prefix_map.items():
            if len(group) > 1 and len(prefix) > len(longest_common_prefix):
                longest_common_prefix = prefix

        if not longest_common_prefix:
            new_grammar[non_terminal] = productions
            continue

        new_non_terminal = non_terminal + "'"
        while new_non_terminal in created_non_terminals:
            new_non_terminal += "'"
        created_non_terminals.add(new_non_terminal)

        factored_productions = []
        remaining_productions = []
        
        for prod in productions:
            if prod.startswith(longest_common_prefix):
                remaining_part = prod[len(longest_common_prefix):]
                factored_productions.append(remaining_part if remaining_part else 'ε')
            else:
                remaining_productions.append(prod)
        new_grammar[non_terminal] = [longest_common_prefix + new_non_terminal] + remaining_productions
        new_grammar[new_non_terminal] = factored_productions

    return new_grammar

def process_grammar():
    try:
        input_grammar = input_text.get("1.0", "end-1c").strip()
        if not input_grammar:
            messagebox.showerror("Input Error", "Please enter a valid grammar.")
            return

        grammar = defaultdict(list)
        for line in input_grammar.splitlines():
            # Split the input like `S -> iEtS | iEtSeS`
            non_terminal, productions_str = line.split("->")
            non_terminal = non_terminal.strip()
            productions = [prod.strip() for prod in productions_str.split("|")]
            grammar[non_terminal] = productions

        factored_grammar = left_factor(grammar)

        result_text = ""
        for non_terminal, productions in factored_grammar.items():
            result_text += f"{non_terminal} -> {' | '.join(productions)}\n"

        # Show the factored grammar in a pop-up window
        messagebox.showinfo("Factored Grammar", result_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the GUI
root = tk.Tk()
root.title("Left Factoring of Grammar")

# Create widgets
input_label = tk.Label(root, text="Enter the grammar (one rule per line):", font=("Arial", 10))
input_label.pack(padx=10, pady=5)

# Text area for input grammar
input_text = tk.Text(root, height=10, width=50)
input_text.pack(padx=10, pady=5, expand=True, fill="both")

# Left factoring button
factoring_button = tk.Button(root, text="Left Factoring", bg="green", fg="white", command=process_grammar, font=("Arial", 10, "bold"))
factoring_button.pack(padx=10, pady=10, anchor="w")

# Start the Tkinter event loop
root.mainloop()
