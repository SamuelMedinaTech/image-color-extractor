import colorgram


class ColorHandler:
    """The handler for HTML creation and updates.

        Attributes:
            current_colors (list[str]): The list of color hex codes.
    """

    def __init__(self):
        self.current_colors = []

    def extract_colors(self, image, num_of_colors):
        """Extract a specified number of colors from the given image.
            Args:
                image (str): The filepath of the image
                num_of_colors (int): The number of colors to extract

            Returns:
                current_colors (list[str]): The list of color hex codes.
        """
        self.current_colors = ["#%02x%02x%02x" % color.rgb for color in colorgram.extract(image, num_of_colors)]
        print(self.current_colors)
        return self.current_colors


class ColorHandlerException(Exception):
    """Raised for exceptions related to the ColorHandler class"""
    def __init__(self, message="An error occurred in the ColorHandler class"):
        super().__init__()
        self.message = message
