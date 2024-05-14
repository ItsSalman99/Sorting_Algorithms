import tkinter as tk
import time
from tkinter import messagebox
import timeit

def draw_array(canvas, arr, highlighted_indices=None):
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
        color = "sky blue" if highlighted_indices is None or i not in highlighted_indices else "salmon"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
        canvas.create_text((x0 + x1) / 2, y1 + 10, text=str(val), fill="white")

def bubble_sort(arr, canvas=None, steps_text=None):
    n = len(arr)
    steps = []
    for i in range(n-1):
        for j in range(0, n-i-1):
            steps.append((arr[:], [j, j+1]))  # Add current state before the swap
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append((arr[:], [j, j+1]))  # Add current state after the swap
    if steps_text:
        display_steps(steps_text, steps)
    return steps

def selection_sort(arr, canvas=None, steps_text=None):
    n = len(arr)
    steps = []
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            steps.append((arr[:], [j, min_idx]))  # Add current state with comparison highlighted
            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append((arr[:], [j, min_idx]))  # Add current state with new min highlighted
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append((arr[:], [i, min_idx]))  # Add current state after the swap
    if steps_text:
        display_steps(steps_text, steps)
    return steps

def animate_sort(steps, canvas):
    for step, highlighted_indices in steps:
        draw_array(canvas, step, highlighted_indices)
        canvas.update()
        time.sleep(1)

def sort_array():
    arr = [int(x) for x in entry.get().split(",")]
    bubble_sorted = arr[:]
    selection_sorted = arr[:]

    bubble_start = timeit.default_timer()
    bubble_steps = bubble_sort(bubble_sorted, bubble_canvas, bubble_steps_text)
    bubble_end = timeit.default_timer()
    bubble_time = bubble_end - bubble_start

    selection_start = timeit.default_timer()
    selection_steps = selection_sort(selection_sorted, selection_canvas, selection_steps_text)
    selection_end = timeit.default_timer()
    selection_time = selection_end - selection_start

    animate_sort(bubble_steps, bubble_canvas)
    animate_sort(selection_steps, selection_canvas)

    compare_sorts(len(bubble_steps), len(selection_steps), bubble_time, selection_time)
    visualize_comparison(arr)

def display_steps(text_widget, steps):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    for i, (step, highlighted_indices) in enumerate(steps):
        text_widget.insert(tk.END, f"Step {i+1}: {step}\n")
    text_widget.config(state=tk.DISABLED)

def toggle_steps(text_widget):
    if show_steps_var.get() == 1:
        text_widget.pack()
    else:
        text_widget.pack_forget()

def compare_sorts(bubble_steps, selection_steps, bubble_time, selection_time):
    messagebox.showinfo("Comparison", f"Bubble Sort took {bubble_steps} steps and {bubble_time:.5f} seconds.\n"
                                      f"Selection Sort took {selection_steps} steps and {selection_time:.5f} seconds.")

def visualize_comparison(arr):
    sizes = list(range(1, len(arr) + 1))
    bubble_times = []
    selection_times = []

    for size in sizes:
        test_array = arr[:size]

        bubble_start = timeit.default_timer()
        bubble_sort(test_array[:])
        bubble_end = timeit.default_timer()
        bubble_times.append(bubble_end - bubble_start)

        selection_start = timeit.default_timer()
        selection_sort(test_array[:])
        selection_end = timeit.default_timer()
        selection_times.append(selection_end - selection_start)

    complexity_canvas.delete("all")
    width = complexity_canvas.winfo_width()
    height = complexity_canvas.winfo_height()

    max_time = max(max(bubble_times), max(selection_times))
    norm_bubble_times = [time / max_time for time in bubble_times]
    norm_selection_times = [time / max_time for time in selection_times]

    prev_x = 0
    prev_y = height
    for i, time in enumerate(norm_bubble_times):
        x = (i / len(norm_bubble_times)) * width
        y = height - (time * height)
        complexity_canvas.create_line(prev_x, prev_y, x, y, fill='blue', width=2)
        prev_x, prev_y = x, y

    prev_x = 0
    prev_y = height
    for i, time in enumerate(norm_selection_times):
        x = (i / len(norm_selection_times)) * width
        y = height - (time * height)
        complexity_canvas.create_line(prev_x, prev_y, x, y, fill='red', width=2)
        prev_x, prev_y = x, y

    complexity_canvas.create_text(width * 0.1, height * 0.1, text="Bubble Sort", fill="blue")
    complexity_canvas.create_text(width * 0.1, height * 0.2, text="Selection Sort", fill="red")

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

bubble_canvas = tk.Canvas(bubble_frame, width=800, height=100, bg="white")
bubble_canvas.pack()

bubble_steps_text = tk.Text(bubble_frame, height=10, width=40, state=tk.DISABLED)
bubble_steps_text.pack()

selection_canvas = tk.Canvas(selection_frame, width=800, height=100, bg="white")
selection_canvas.pack()

selection_steps_text = tk.Text(selection_frame, height=10, width=40, state=tk.DISABLED)
selection_steps_text.pack()

complexity_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
complexity_frame.pack(pady=10)

complexity_canvas = tk.Canvas(complexity_frame, width=800, height=400, bg="white")
complexity_canvas.pack()

show_steps_var = tk.IntVar()
show_steps_var.set(1)  # Set to show steps by default
show_steps_checkbox = tk.Checkbutton(root, text="Show Steps", variable=show_steps_var, command=lambda: [toggle_steps(bubble_steps_text), toggle_steps(selection_steps_text)])
show_steps_checkbox.pack()

button = tk.Button(root, text="Sort", command=sort_array, bg="sky blue", fg="white", activebackground="light blue", activeforeground="white")
button.pack(pady=10)

root.mainloop()
