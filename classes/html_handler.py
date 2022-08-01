import os
import webbrowser

from airium import Airium

CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"


class HtmlHandler:
    """The handler for HTML creation and updates.

        Attributes:
            template (Airium): The starter template based on the Airium package.
    """

    def __init__(self):
        self.template = Airium()
        self.create_starter_html()

    def create_starter_html(self):
        """Generate a starter HTML template"""
        self.template('<!DOCTYPE html>')
        with self.template.html(lang="pl"):
            with self.template.head():
                self.template.meta(charset="utf-8")
                self.template.link(href='https://unpkg.com/@picocss/pico@1.4.1/css/pico.css', rel='stylesheet')
                self.template.title(_t="Extracted Colors")
            with self.template.body():
                self.template.h1("Extracted Colors:")

    def create_table(self):
        """Create a table in the HTML file

        Equivalent to creating the following:
        <table>
        </table>
        """
        with self.template.body():
            self.template.table(border="1px solid white")

    def add_table_row(self, *args, **kwargs):
        """Add a row in a table

            Args:
                args: The number of columns to add, as well as their text content.
                kwargs: The CSS styles that can be applied to a specific cell.
        """
        with self.template.table():
            with self.template.tr():
                for column in args:
                    if kwargs["background_color"] is not None and column == "":
                        self.template.td(_t=column, style=f"background-color:{kwargs['background_color']}")
                    else:
                        self.template.td(_t=column)

    def create_html_file(self, filename):
        """Create an HTML file with the given filename

            Parameters:
                filename (str): The name of the HTML file
        """
        with open(f"./outputs/{filename}.html", mode="w") as file:
            file.write(str(self.template))
            return os.path.realpath(file.name)

    # Static Methods
    @staticmethod
    def open_html_in_browser(filename):
        """Open the HTML file in a new browser

            Parameters:
                filename (str): The path to the HTML file
        """
        webbrowser.get(CHROME_PATH).open(filename, new=2)
