import re
import tkinter as tk
from tkinter import scrolledtext
import pandas as pd

PYTHON_KEYWORDS = (
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
)

TOKEN_PATTERNS = [
    (rf'\b({"|".join(PYTHON_KEYWORDS)})\b', 'keyword'),
    (r'\b[0-9]+(\.[0-9]+)?\b', 'literal'),
    (r'[+\-*/=<>!&|{}();,]', 'operator'),
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'identifier'),
]

TOKEN_COLORS = {
    'keyword': 'blue',
    'operator': 'green',
    'literal': 'red',
    'identifier': 'black'
}

def analyze_code():
    text_area.tag_remove('token', '1.0', tk.END) 
    code = text_area.get("1.0", tk.END)
    
    tokens = []  
    
    matches = []
    for pattern, tag in TOKEN_PATTERNS:
        for match in re.finditer(pattern, code):
            matches.append((match.start(), match.group(), tag))
    
    matches.sort() 
    
    for start, token, tag in matches:
        start_idx = text_area.index(f"1.0+{start}c")
        end_idx = text_area.index(f"1.0+{start+len(token)}c")
        text_area.tag_add(tag, start_idx, end_idx)
        tokens.append((token, tag))
    
    for tag, color in TOKEN_COLORS.items():
        text_area.tag_config(tag, foreground=color)
    
    df = pd.DataFrame(tokens, columns=['Token', 'Type'])
    df.to_csv("tokens.csv", index=False)

def create_gui():
    global text_area
    
    root = tk.Tk()
    root.title("Lexical Analyzer Visualizer")
    
    legend_frame = tk.Frame(root)
    legend_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
    
    for token, color in TOKEN_COLORS.items():
        label = tk.Label(legend_frame, text=token.capitalize(), fg=color, font=("Arial", 10, "bold"))
        label.pack(side=tk.LEFT, padx=5)
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, pady=0, padx=10)
    
    text_area = scrolledtext.ScrolledText(frame, width=60, height=20, font=("Courier", 12))
    text_area.pack(fill=tk.BOTH, expand=True) 
    
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill=tk.X, pady=5, padx=10)
    
    analyze_button = tk.Button(bottom_frame, text="Analyze", command=analyze_code, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
    analyze_button.pack(side=tk.LEFT, anchor=tk.SW)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
