import tkinter as tk
import threading
import time
import sys
from playsound import playsound


# Function to stop the alarm
def stop_alarm():
    print("alarm stopped!")
    global alarm_triggered
    alarm_triggered = False
    alarm_window.destroy()
    print("♡♡♡♡ Take 5 mins rest buddy ♡♡♡♡")
    time.sleep(5 * 60)
    print("♡♡♡♡♡♡♡♡♡♡♡♡ get to work best orca ever, one day you'll be proud! ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡")


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
    while True:
        minutes, seconds = divmod(time_remaining, 60)
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        time.sleep(1)

# Function to run the timer
def run_timer():
    print('timer start counting!')
    global time_remaining
    while True:
        time_remaining = 20 * 60 # 20 minutes in seconds
        while time_remaining > 0:
            time.sleep(1)
            time_remaining -= 1

        show_alarm()

# Function to handle closing the main window
def on_closing():
    print("Program terminated!")
    stop_event.set()  # Signal threads to stop
    root.destroy()  # Close the Tkinter window


# Main function to set up the GUI
if __name__ == "__main__":
    alarm_triggered = False
    stop_event = threading.Event()  # Event to signal threads to stop

    # Set up the main window
    root = tk.Tk()
    root.title("20-Minute Timer")

    # Add a label to display the timer
    timer_label = tk.Label(root, text="20:00", font=("Arial", 48))
    timer_label.pack(pady=20)

    # Bind the close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the timer in a separate thread
    threading.Thread(target=run_timer, daemon=True).start()

    # Start updating the timer label
    threading.Thread(target=update_timer, daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()
