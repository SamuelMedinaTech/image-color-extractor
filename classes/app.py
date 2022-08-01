from tkinter import Button
from tkinter import Entry
from tkinter import IntVar
from tkinter import Label
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

from classes.color_handler import ColorHandler, ColorHandlerException
from classes.html_handler import HtmlHandler


class App:
    """The main UI for the application.

        Attributes:
            color_handler (ColorHandler): An instance of the ColorHandler class.
            html_handler (HtmlHandler): An instance of the HtmlHandler class.

            image (str): The current file path of the uploaded image.

            window (Tk): The main window for the application.
            upload_label (Label): A label that prompts for an image upload.
            upload_btn (Button): A button that lets uses upload an image from the computer.
            image_label (Label): A label for displaying the uploaded image.
            extract_colors_entry (Entry): An entry for the number of colors to extract.
            extract_colors_entry_label (Label): A label that prompts for the number of colors to extract.
            extract_colors_entry_variable (IntVar): An integer variable that is attached to the extract_colors_entry.
            extract_colors_btn (Button): A button that initiates color extraction from the uploaded image.
    """

    def __init__(self):
        # Class Components
        self.color_handler = ColorHandler()
        self.html_handler = HtmlHandler()

        # Accessible attributes
        self.image = None

        # Main UI
        self.window = Tk()
        self.window.title("Image Color Extractor")
        self.window.config(width=250, height=250)
        self.window.minsize(width=250, height=250)

        # Widgets
        self.upload_label = Label(self.window, text="Select image to extract colors from:")
        self.upload_btn = Button(self.window, text="Upload Image", width=20, command=self.upload_file)
        self.image_label = None
        self.extract_colors_entry = None
        self.extract_colors_entry_label = None
        self.extract_colors_entry_variable = IntVar()
        self.extract_colors_btn = None

        # Layout
        self.upload_label.pack(padx=10, pady=10)
        self.upload_btn.pack(padx=10, pady=10)

        self.window.mainloop()

    def upload_file(self):
        """Upload an image file of the JPEG format"""
        f_types = [("Jpg Files", "*.jpg")]
        filename = filedialog.askopenfilename(filetypes=f_types)

        # If user did not cancel the upload, display the image
        if filename:
            self.display_image(filename)

    def display_image(self, image):
        """Display the uploaded image in the UI

            Parameters:
                image (str): The filepath of the image
        """
        # Generate the Image Object
        self.image = Image.open(image)

        # Resize the image
        width, height = self.image.size
        width_new = int(width / 2)
        height_new = int(height / 2)
        img_resized = ImageTk.PhotoImage(self.image.resize((width_new, height_new)))

        # If an existing image is already displayed, clear it
        if self.image_label:
            self.image_label.destroy()

        # Display the image
        self.image_label = Label(self.window)
        self.image_label.image = img_resized  # Anchor the image
        self.image_label["image"] = img_resized
        self.image_label.pack(padx=10, pady=10)

        # Display an entry for number of colors to extract and a button for extraction
        self.display_extract_options()

    def display_extract_options(self):
        """Display the options for extracting colors from the uploaded image"""
        # Register the entry validation function as a callback in the main window
        entry_validate_function = self.window.register(self.validate_integer_entry)

        # Option Widgets
        self.extract_colors_entry_label = Label(self.window, text="How many colors to extract?")
        self.extract_colors_entry = Entry(self.window, textvariable=self.extract_colors_entry_variable)
        self.extract_colors_entry.config(validate="key", validatecommand=(entry_validate_function, "%P"))
        self.extract_colors_btn = Button(self.window, text="Extract Colors", width=20, command=self.extract_colors)

        # Option Layout
        self.extract_colors_entry_label.pack(padx=10, pady=10)
        self.extract_colors_entry.pack(padx=10, pady=10)
        self.extract_colors_btn.pack(padx=10, pady=10)

    def extract_colors(self):
        """Extract the colors from the displayed image"""
        try:
            colors = self.color_handler.extract_colors(self.image, self.extract_colors_entry_variable.get())
            self.generate_color_html(colors)
        except ColorHandlerException as e:
            messagebox.showerror(title="Error!", message=e.message)
        finally:
            messagebox.showinfo(title="Done!", message=f"{self.extract_colors_entry_variable.get()} colors "
                                                       f"have been extracted successfully")

    def generate_color_html(self, colors):
        """Create an HTML file with the extracted colors as a table, then open the generated file in a new browser tab.

            Parameters:
                colors (list[str]): A list of color hex code strings
        """
        self.html_handler.create_table()
        for color in colors:
            self.html_handler.add_table_row(color, "", background_color=color)
        filename = self.html_handler.create_html_file("extracted_colors")
        self.html_handler.open_html_in_browser(filename)

    # Static Methods
    @staticmethod
    def validate_integer_entry(val):
        """Validate if the value is an integer

            Parameters:
                val (obj): An integer

            Returns:
                boolean (boolean): True or False
        """
        if val.isdigit():
            return True
        elif val == "":
            return True
        else:
            return False
