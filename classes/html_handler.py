import os
import pathlib
import platform
from urllib.parse import quote
import webbrowser
from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

from airium import Airium


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
                self.template.meta(
                    name="viewport",
                    content="width=device-width, initial-scale=1"
                )
                self.template.title(_t="Extracted Colors")
                self.template.link(
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css",
                    rel="stylesheet",
                    integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx",
                    crossorigin="anonymous"
                )

    def create_color_table(self, num_of_rows, colors):
        """Create a table in the HTML file that displays color hex codes and sample colors inside table cells

        Equivalent to creating the following:
        <table>
            <tr>
                <td>#888888</td>
                <td>Cell with background of given color</td>
            </tr>
        </table>

            Args:
                num_of_rows (int): The number of rows to create
                colors (list[str]): The list of color hex codes
        """
        with self.template.body():
            with self.template.table(klass="table"):
                with self.template.thead():
                    with self.template.tr():
                        self.template.th(_t="#", scope="col")
                        self.template.th(_t="Hex Code", scope="col")
                        self.template.th(_t="Sample", scope="col")
                with self.template.tbody():
                    for i in range(num_of_rows):
                        with self.template.tr():
                            self.template.th(_t=(i + 1), scope="row")
                            self.template.td(_t=colors[i])
                            self.template.td(style=f"background-color:{colors[i]}")

    def create_html_file(self, filename):
        """Create an HTML file with the given filename

            Args:
                filename (str): The name of the HTML file
        """
        with open(f"./outputs/{filename}.html", mode="w") as file:
            file.write(str(self.template))
            return os.path.realpath(file.name)

    # Static Methods
    @staticmethod
    def open_html_in_browser(filename):
        """Open the HTML file in a new browser.

        The function automatically retrieves the default browser used by the current OS.

        NOTE: Only Windows and macOS are supported at the moment.

            Args:
                filename (str): The path to the HTML file
        """
        # Retrieve the current OS of the machine
        try:
            current_platform = platform.system()
            if current_platform == "Windows":
                filename = f"file:///{pathlib.PureWindowsPath(filename).as_posix()}"
            else:
                filename = f"file:///{pathlib.Path(filename).as_posix()}"
            filename = quote(filename, safe=':/')
            webbrowser.open(filename)
        except Exception as e:
            raise HtmlHandlerException("Error occurred when opening the file in the web browser.")


class HtmlHandlerException(Exception):
    """Raised for exceptions related to the HtmlHandler class"""
    def __init__(self, message="An error occurred in the HtmlHandler class"):
        super().__init__()

        self.message = message
