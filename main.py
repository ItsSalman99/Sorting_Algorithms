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
        color = "blue" if highlighted_index is None or i not in highlighted_index else "red"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="rect")
        canvas.create_text((x0 + x1) / 2, y1 + 10, text=str(val))

def bubble_sort(arr, canvas):
    n = len(arr)
    steps = []
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append((arr[:], [j, j+1]))
    return steps

def selection_sort(arr, canvas):
    n = len(arr)
    steps = []
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append((arr[:], [i, min_idx]))
    return steps

def animate_sort(steps, canvas):
    for step, indices in steps:
        draw_array(canvas, step, indices)
        canvas.update()
        time.sleep(1)

def sort_array():
    arr = [int(x) for x in entry.get().split(",")]
    bubble_sorted = arr[:]
    selection_sorted = arr[:]
    
    messagebox.showinfo("Bubble Sort Explanation", "Bubble Sort works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they are in the wrong order. This process is repeated until the list is sorted.")
    bubble_steps = bubble_sort(bubble_sorted, bubble_canvas)
    
    messagebox.showinfo("Selection Sort Explanation", "Selection Sort divides the input list into two parts: the sorted sublist and the unsorted sublist. It repeatedly finds the minimum element from the unsorted sublist and moves it to the beginning of the sorted sublist.")
    selection_steps = selection_sort(selection_sorted, selection_canvas)
    
    animate_sort(bubble_steps, bubble_canvas)
    animate_sort(selection_steps, selection_canvas)

# Tkinter GUI setup
root = tk.Tk()
root.title("Sorting Visualizer")

label = tk.Label(root, text="Enter numbers separated by comma:")
label.pack()

entry = tk.Entry(root)
entry.pack()

frame = tk.Frame(root)
frame.pack()

bubble_canvas = tk.Canvas(frame, width=400, height=200, bg="white")
bubble_canvas.pack(side=tk.LEFT, padx=10)

selection_canvas = tk.Canvas(frame, width=400, height=200, bg="white")
selection_canvas.pack(side=tk.RIGHT, padx=10)

button = tk.Button(root, text="Sort", command=sort_array)
button.pack()

root.mainloop()
