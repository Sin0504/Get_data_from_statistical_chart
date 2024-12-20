import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_original_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    image = cv2.imread(file_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig, ax = plt.subplots()
    ax.imshow(rgb_image)
    ax.set_title('Original Image')
    ax.axis('off')  # 不显示坐标轴
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=10, column=4, columnspan=4)
    canvas.draw()

def extract_coordinates(image, center_color, delta):
    lower_color = np.clip(center_color - delta, 0, 255)
    upper_color = np.clip(center_color + delta, 0, 255)
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb_image, lower_color, upper_color)
    points = np.argwhere(mask == 255)
    return points

def plot_data(points, origin, unit_x, unit_y):
    x_coords = (points[:, 1] - origin[0]) / unit_x
    y_coords = -(points[:, 0] - origin[1]) / unit_y
    fig, ax = plt.subplots()
    ax.scatter(x_coords, y_coords)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    return fig, x_coords, y_coords

def process_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    image = cv2.imread(file_path)
    
    try:
        center_r = int(center_r_entry.get())
        center_g = int(center_g_entry.get())
        center_b = int(center_b_entry.get())
        delta_r = int(delta_r_entry.get())
        delta_g = int(delta_r_entry.get())
        delta_b = int(delta_r_entry.get())
        origin_x = int(origin_x_entry.get())
        origin_y = int(origin_y_entry.get())
        unit_x = float(unit_x_entry.get())
        unit_y = float(unit_y_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")
        return
    
    center_color = np.array([center_r, center_g, center_b])
    delta = np.array([delta_r, delta_g, delta_b])
    
    points = extract_coordinates(image, center_color, delta)
    fig, x_coords, y_coords = plot_data(points, (origin_x, origin_y), unit_x, unit_y)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=10, column=0, columnspan=4)
    canvas.draw()
    
    # Store the coordinates for later export
    global exported_data
    exported_data = np.column_stack((x_coords, y_coords))

def export_data():
    if 'exported_data' not in globals():
        messagebox.showerror("No Data", "No data to export. Please process an image first.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return
    
    np.savetxt(file_path, exported_data, delimiter=",", header="X,Y", comments='', fmt='%f')
    messagebox.showinfo("Export Successful", "The data has been exported successfully.")

root = Tk()
root.title("Color Coordinate Extraction")




Label(root, text="Center R:").grid(row=0, column=0, padx=10, pady=10)
center_r_entry = Entry(root)
center_r_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Center G:").grid(row=0, column=2, padx=10, pady=10)
center_g_entry = Entry(root)
center_g_entry.grid(row=0, column=3, padx=10, pady=10)

Label(root, text="Center B:").grid(row=0, column=4, padx=10, pady=10)
center_b_entry = Entry(root)
center_b_entry.grid(row=0, column=5, padx=10, pady=10)

Label(root, text="Delta RGB:").grid(row=0, column=6, padx=10, pady=10)
delta_r_entry = Entry(root)
delta_r_entry.grid(row=0, column=7, padx=10, pady=10)

Label(root, text="Origin X:").grid(row=2, column=0, padx=10, pady=10)
origin_x_entry = Entry(root)
origin_x_entry.grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Origin Y:").grid(row=2, column=2, padx=10, pady=10)
origin_y_entry = Entry(root)
origin_y_entry.grid(row=2, column=3, padx=10, pady=10)

Label(root, text="Unit X:").grid(row=2, column=4, padx=10, pady=10)
unit_x_entry = Entry(root)
unit_x_entry.grid(row=2, column=5, padx=10, pady=10)



Label(root, text="Unit Y:").grid(row=2, column=6, padx=10, pady=10)
unit_y_entry = Entry(root)
unit_y_entry.grid(row=2, column=7, padx=10, pady=10)

Button(root, text="Process Image", command=process_image).grid(row=3, column=0, columnspan=3, pady=10)
Button(root, text="Export Data", command=export_data).grid(row=3, column=3, columnspan=3, pady=10)
Button(root, text="Show Original Image", command=show_original_image).grid(row=3, column=6, columnspan=3, pady=10)
root.mainloop()
