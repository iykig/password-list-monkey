import tkinter as tk
from string import *
from itertools import islice, product

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.is_paused = False

        self.generate_button = tk.Button(root, text="Play", command=self.generate_passwords)
        self.generate_button.pack()

        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()
        self.pause_button["state"] = "disabled"

        self.resume_label = tk.Label(root, text="Resume from run:")
        self.resume_label.pack()

        self.resume_entry = tk.Entry(root)
        self.resume_entry.pack()

        self.count_label = tk.Label(root, text="Run Count: 0")
        self.count_label.pack()

        self.display = tk.Text(root, wrap="word")
        self.display.pack()

        self.value = ascii_letters + digits + punctuation
        self.cancel_generation = False
        self.current_run = 0  # Start from run 0 by default
        self.run_count = 0

        # Load the last saved run number and run count
        try:
            with open("last_run.txt", "r") as file:
                data = file.read().split(',')
                self.current_run = int(data[0])
                self.run_count = int(data[1])
        except FileNotFoundError:
            pass

    def custom_product(self, iterable, r):
        # Custom product generator that starts from the current run
        for j in islice(product(iterable, repeat=r), self.current_run, None):
            yield j

    def generate_passwords(self):
        self.generate_button["state"] = "disabled"
        self.pause_button["state"] = "normal"
        self.is_paused = False

        start_run = int(self.resume_entry.get())

        if start_run > self.current_run:
            self.current_run = start_run  # Update current_run to start_run
        else:
            self.current_run = 0  # Start from run 0 by default

        for i in range(8, 9):
            if self.cancel_generation:
                self.cancel_generation = False
                break

            for j in self.custom_product(self.value, i):
                word = "".join(j)
                self.display.insert(tk.END, word + '\n')
                self.display.see(tk.END)
                self.root.update()
                self.run_count += 1
                self.count_label.config(text=f"Run Count: {self.run_count}")
                if self.is_paused:
                    self.generate_button["state"] = "normal"
                    self.pause_button["state"] = "disabled"
                    return

        self.generate_button["state"] = "normal"
        self.pause_button["state"] = "disabled"

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def cancel_generation(self):
        self.cancel_generation = True
        self.resume_entry.delete(0, tk.END)  # Clear the resume entry

    def save_current_run(self):
        # Save the current run number and run count to a file
        with open("last_run.txt", "w") as file:
            file.write(f"{self.current_run},{self.run_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.save_current_run)  # Save the current run on window close
    root.mainloop()
