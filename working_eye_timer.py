import tkinter as tk
import threading
import time
from playsound import playsound

# Function to stop the alarm
def stop_alarm():
    print("alarm stopped!")
    global alarm_triggered
    alarm_triggered = False
    alarm_window.destroy()

# Function to play the alarm sound
def play_alarm():
    print("alarm triggered!")
    global alarm_triggered
    alarm_triggered = True
    while alarm_triggered:  # Continue playing alarm until acknowledged
        playsound('alarm_sound.mp3')

# Function to create the alarm acknowledgment GUI
def show_alarm():
    global alarm_window
    alarm_window = tk.Tk()
    alarm_window.title("Alarm!")

    label = tk.Label(alarm_window, text="Time's up! Click the button to stop the alarm.", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(alarm_window, text="Stop Alarm", command=stop_alarm, font=("Arial", 14))
    button.pack(pady=20)

    threading.Thread(target=play_alarm).start()
    alarm_window.mainloop()

# Function to update the timer display
def update_timer():
    while not stop_event.is_set():
        minutes, seconds = divmod(time_remaining, 60)
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        time.sleep(1)

# Function to run the timer
def run_timer():
    print('timer start counting!')
    global time_remaining
    while not stop_event.is_set():
        time_remaining = 20 * 60  # 20 minutes in seconds
        while time_remaining > 0 and not stop_event.is_set():
            time.sleep(1)
            time_remaining -= 1

        if not stop_event.is_set():  # Only show the alarm if not stopping
            show_alarm()

# Function to handle closing the main window
def on_closing():
    print("Program terminated!")
    stop_event.set()  # Signal threads to stop
    root.destroy()  # Close the Tkinter window

# Function to minimize the window
def minimize_window():
    root.attributes('-alpha', 0)  # Hide the window by setting transparency to 0
    root.after(10, root.iconify)  # Minimize the window after hiding

# Function to show close and minimize buttons on hover
def show_controls(event=None):
    close_button.place(x=width-40, y=10)
    minimize_button.place(x=width-80, y=10)

# Function to hide close and minimize buttons when not hovering
def hide_controls(event=None):
    # Check if the mouse is still within the window boundaries or the buttons themselves
    if (event.widget == root) or (event.widget == close_button) or (event.widget == minimize_button):
        return
    close_button.place_forget()
    minimize_button.place_forget()

# Function to enable dragging the window
def start_drag(event):
    global startX, startY
    startX = event.x
    startY = event.y

def do_drag(event):
    x = root.winfo_x() + event.x - startX
    y = root.winfo_y() + event.y - startY
    root.geometry(f"+{x}+{y}")

# Main function to set up the GUI
if __name__ == "__main__":
    alarm_triggered = False
    stop_event = threading.Event()  # Event to signal threads to stop

    # Set up the main window
    root = tk.Tk()
    root.title("20-Minute Timer")

    # Make window black, more transparent, and always on top
    root.configure(bg='black')
    root.attributes('-alpha', 0.5)  # Set transparency (0.0 to 1.0), adjusted to 0.5 for increased transparency
    root.attributes('-topmost', True)  # Keep window on top
    root.overrideredirect(True)  # Remove window borders

    # Set initial geometry and size
    width = 300  # Width of the window
    height = 150  # Height of the window
    root.geometry(f"{width}x{height}")

    # Add a label to display the timer
    timer_label = tk.Label(root, text="20:00", font=("Arial", 48), fg="white", bg="black")
    timer_label.pack(pady=20)

    # Create close and minimize buttons
    close_button = tk.Button(root, text="✖", command=on_closing, font=("Arial", 12), bg="black", fg="white", bd=0)
    minimize_button = tk.Button(root, text="—", command=minimize_window, font=("Arial", 12), bg="black", fg="white", bd=0)

    # Hide controls initially
    close_button.place_forget()
    minimize_button.place_forget()

    # Bind events for hover and dragging
    root.bind('<Enter>', show_controls)
    root.bind('<Leave>', hide_controls)
    root.bind('<ButtonPress-1>', start_drag)
    root.bind('<B1-Motion>', do_drag)

    # Bind the close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the timer in a separate thread
    threading.Thread(target=run_timer, daemon=True).start()

    # Start updating the timer label
    threading.Thread(target=update_timer, daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()
