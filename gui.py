import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cli import CLI


class App:
    def __init__(self, master):
        self.master = master
        master.title("Image Steganography")
        master.geometry("550x200")

        # create initial menu frame
        self.initial_menu_frame = tk.Frame(master)
        self.initial_menu_frame.pack()

        # create quit button
        self.quit_button = tk.Button(self.initial_menu_frame, text="Quit", command=self.quit)

        # create mode selection widgets
        self.mode_label = tk.Label(self.initial_menu_frame, text="Select a mode:")
        self.encrypt_button = tk.Button(self.initial_menu_frame, text="Encrypt", command=self.show_encrypt_menu)
        self.decrypt_button = tk.Button(self.initial_menu_frame, text="Decrypt", command=self.show_decrypt_menu)

        # pack mode selection widgets and quit button into initial menu frame
        self.mode_label.pack()
        self.mode_label.pack(pady=30)
        self.encrypt_button.pack(side=tk.LEFT)
        self.decrypt_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.RIGHT)

    def show_encrypt_menu(self):
        # remove initial menu widgets
        self.mode_label.pack_forget()
        self.encrypt_button.pack_forget()
        self.decrypt_button.pack_forget()
        self.quit_button.pack_forget()

        # create encryption window
        self.encrypt_window = tk.Frame(self.initial_menu_frame)
        self.encrypt_window.pack()

        # create encryption widgets
        self.input_image_label = tk.Label(self.encrypt_window, text="Input Image Path:")
        self.input_image_entry = tk.Entry(self.encrypt_window)
        self.input_image_button = tk.Button(self.encrypt_window, text="Browse", command=self.browse_input_image)
        self.output_image_label = tk.Label(self.encrypt_window, text="Output Stego-Image Path:")
        self.output_image_entry = tk.Entry(self.encrypt_window)
        self.output_image_button = tk.Button(self.encrypt_window, text="Browse", command=self.browse_output_image)
        self.message_label = tk.Label(self.encrypt_window, text="Secret Message:")
        self.message_entry = tk.Entry(self.encrypt_window)
        self.password_label = tk.Label(self.encrypt_window, text="Message Password:")
        self.password_entry = tk.Entry(self.encrypt_window, show="*")
        self.encrypt_button = tk.Button(self.encrypt_window, text="Encrypt", command=self.encrypt)
        self.back_button = tk.Button(self.encrypt_window, text="Back", command=self.show_initial_menu)

        # grid encryption widgets in encryption window
        self.input_image_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.input_image_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.input_image_button.grid(row=0, column=2, padx=5, pady=5)
        self.output_image_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.output_image_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.output_image_button.grid(row=1, column=2, padx=5, pady=5)
        self.message_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.message_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.password_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.password_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.encrypt_button.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.back_button.grid(row=4, column=1, padx=5, pady=5, sticky='e')

    def show_decrypt_menu(self):
        # remove initial menu widgets
        self.mode_label.pack_forget()
        self.encrypt_button.pack_forget()
        self.decrypt_button.pack_forget()
        self.quit_button.pack_forget()

        # create decryption window
        self.decrypt_window = tk.Frame(self.initial_menu_frame)
        self.decrypt_window.pack()

        # create decryption widgets
        self.output_image_label = tk.Label(self.decrypt_window, text="Output Image Path:")
        self.input_image_entry = tk.Entry(self.decrypt_window)
        self.output_image_button = tk.Button(self.decrypt_window, text="Browse", command=self.browse_input_image)
        self.message_password_label = tk.Label(self.decrypt_window, text="Message Password:")
        self.message_password_entry = tk.Entry(self.decrypt_window, show="*")
        self.pixel_location_password_label = tk.Label(self.decrypt_window, text="Pixel Location Password:")
        self.pixel_location_password_entry = tk.Entry(self.decrypt_window, show="*")
        self.len_encoded_message_label = tk.Label(self.decrypt_window, text="Length of Encoded Message:")
        self.len_encoded_message_entry = tk.Entry(self.decrypt_window)
        self.decrypt_button = tk.Button(self.decrypt_window, text="Decrypt", command=self.decrypt)
        self.back_button = tk.Button(self.decrypt_window, text="Back", command=self.show_initial_menu)

        # grid decryption widgets in decryption window
        self.output_image_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.input_image_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.output_image_button.grid(row=0, column=2, padx=5, pady=5)
        self.message_password_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.message_password_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.pixel_location_password_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.pixel_location_password_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.len_encoded_message_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.len_encoded_message_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.decrypt_button.grid(row=4, column=0, padx=5, pady=5)
        self.back_button.grid(row=4, column=1, padx=5, pady=5, sticky='e')

    def browse_input_image(self):
        # get file path using file dialog
        file_path = filedialog.askopenfilename()

        # set file path in input image entry widget
        self.input_image_entry.delete(0, tk.END)
        self.input_image_entry.insert(0, file_path)

    def browse_output_image(self):
        # get file path using file dialog
        file_path = filedialog.asksaveasfilename()

        # set file path in output image entry widget
        self.output_image_entry.delete(0, tk.END)
        self.output_image_entry.insert(0, file_path)

    def encrypt(self):
        try:
            # get input image file path
            input_image_path = self.input_image_entry.get()

            # get output image file path
            output_image_path = self.output_image_entry.get()

            # get message
            message = self.message_entry.get()

            # get password
            password = self.password_entry.get()

            # create CLI object and call encrypt function
            cli = CLI()
            pixel_location_password, len_encoded_message = cli.encrypt(input_image_path, output_image_path, message,
                                                                       password)

            # show success message box with pixel_location_password and len_encoded_message
            messagebox.showinfo("Success",
                                f"Encryption complete!\nPixel Location Password: {pixel_location_password}"
                                f"\nLength of Encoded Message: {len_encoded_message}")

            # reset input fields
            self.input_image_entry.delete(0, tk.END)
            self.output_image_entry.delete(0, tk.END)
            self.message_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt(self):
        # get output image file path
        output_image_path = self.input_image_entry.get()

        # get message password
        message_password = self.message_password_entry.get()

        # get pixel location password
        pixel_location_password = self.pixel_location_password_entry.get()

        # get length of encoded message
        len_encoded_message = self.len_encoded_message_entry.get()

        try:
            len_encoded_message = int(len_encoded_message)
        except ValueError:
            # show error message box for invalid input
            messagebox.showerror("Error", "Invalid input for 'Length of Encoded Message'")
            return

        # check if output image file exists
        if not os.path.exists(output_image_path):
            # show error message box for non-existent output file
            messagebox.showerror("Error", "Output image file does not exist")
            return

        # create CLI object and call decrypt function
        cli = CLI()

        try:
            decrypted_message = cli.decrypt(output_image_path, message_password, pixel_location_password,
                                            len_encoded_message)
        except Exception as e:
            # show error message box for decryption error
            messagebox.showerror("Error", str(e))
            return

        # show success message box
        messagebox.showinfo("Success", f"Decryption complete!\nDecoded message: {decrypted_message}")

        # reset input fields
        self.input_image_entry.delete(0, tk.END)
        self.message_password_entry.delete(0, tk.END)
        self.pixel_location_password_entry.delete(0, tk.END)
        self.len_encoded_message_entry.delete(0, tk.END)

    def quit(self):
        self.master.quit()

    def show_initial_menu(self):
        # remove encryption/decryption widgets
        if hasattr(self, 'encrypt_window'):
            self.encrypt_window.pack_forget()
        if hasattr(self, 'decrypt_window'):
            self.decrypt_window.pack_forget()

        # create initial menu widgets
        self.mode_label = tk.Label(self.initial_menu_frame, text="Select a mode:")
        self.encrypt_button = tk.Button(self.initial_menu_frame, text="Encrypt", command=self.show_encrypt_menu)
        self.decrypt_button = tk.Button(self.initial_menu_frame, text="Decrypt", command=self.show_decrypt_menu)
        self.quit_button = tk.Button(self.initial_menu_frame, text="Quit", command=self.master.destroy)

        # pack initial menu widgets into initial menu frame
        self.mode_label.pack()
        self.mode_label.pack(pady=30)
        self.encrypt_button.pack(side=tk.LEFT)
        self.decrypt_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.RIGHT)


if __name__ == '__main__':
    root = tk.Tk()
    gui = App(root)
    root.mainloop()
