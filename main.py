import tkinter as tk
from tkinter import messagebox
import time

def draw_array(canvas, arr, highlighted_index=None):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    bar_width = width / len(arr)
    max_val = max(arr)
    for i, val in enumerate(arr):
        x0 = i * bar_width
        y0 = height
        x1 = (i + 1) * bar_width
        y1 = height - (val / max_val) * height
        color = "sky blue" if highlighted_index is None or i not in highlighted_index else "salmon"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
        canvas.create_text((x0 + x1) / 2, y1 + 10, text=str(val), fill="white")

def bubble_sort(arr, canvas, steps_text):
    n = len(arr)
    steps = []
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append(arr[:])
    display_steps(steps_text, steps)
    return steps

def selection_sort(arr, canvas, steps_text):
    n = len(arr)
    steps = []
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])
    display_steps(steps_text, steps)
    return steps

def animate_sort(steps, canvas):
    for step in steps:
        draw_array(canvas, step)
        canvas.update()
        time.sleep(1)

def sort_array():
    arr = [int(x) for x in entry.get().split(",")]
    bubble_sorted = arr[:]
    selection_sorted = arr[:]
    
    bubble_steps = bubble_sort(bubble_sorted, bubble_canvas, bubble_steps_text)
    selection_steps = selection_sort(selection_sorted, selection_canvas, selection_steps_text)
    
    animate_sort(bubble_steps, bubble_canvas)
    animate_sort(selection_steps, selection_canvas)

def display_steps(text_widget, steps):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    for step in steps:
        text_widget.insert(tk.END, str(step) + "\n")
    text_widget.config(state=tk.DISABLED)

def toggle_steps(text_widget):
    if show_steps_var.get() == 1:
        text_widget.pack()
    else:
        text_widget.pack_forget()

# Tkinter GUI setup
root = tk.Tk()
root.title("Sorting Visualizer")

label = tk.Label(root, text="Enter numbers separated by comma:")
label.pack()

entry = tk.Entry(root)
entry.pack()

frame = tk.Frame(root, bd=2, relief=tk.RAISED)
frame.pack(pady=10)

bubble_frame = tk.Frame(frame, bd=2, relief=tk.RAISED)
bubble_frame.pack(side=tk.LEFT, padx=10)

selection_frame = tk.Frame(frame, bd=2, relief=tk.RAISED)
selection_frame.pack(side=tk.RIGHT, padx=10)

bubble_canvas = tk.Canvas(bubble_frame, width=400, height=200, bg="black")
bubble_canvas.pack()

bubble_steps_text = tk.Text(bubble_frame, height=10, width=20, state=tk.DISABLED)
bubble_steps_text.pack()

selection_canvas = tk.Canvas(selection_frame, width=400, height=200, bg="black")
selection_canvas.pack()

selection_steps_text = tk.Text(selection_frame, height=10, width=20, state=tk.DISABLED)
selection_steps_text.pack()

show_steps_var = tk.IntVar()
show_steps_var.set(1)  # Set to show steps by default
show_steps_checkbox = tk.Checkbutton(root, text="Show Steps", variable=show_steps_var, command=lambda: [toggle_steps(bubble_steps_text), toggle_steps(selection_steps_text)])
show_steps_checkbox.pack()

button = tk.Button(root, text="Sort", command=sort_array, bg="sky blue", fg="white", activebackground="light blue", activeforeground="white")
button.pack(pady=10)

root.mainloop()
