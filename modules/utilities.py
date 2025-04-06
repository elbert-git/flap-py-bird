import pygame

BASE_IMAGE_PATH = "assets/sprites"

class Asset_Loader:
    @classmethod
    def load_image(cls, file_name):
        return pygame.image.load(f"{BASE_IMAGE_PATH}/{file_name}")


def map_range(value, from_min, from_max, to_min, to_max):
    # Calculate the scale factor
    scaled_value = (value - from_min) / (from_max - from_min)  # Normalize the value to a 0-1 range
    # Return the mapped value in the new range
    return to_min + (scaled_value * (to_max - to_min))
        

def lerp(start, end, t):
    return (1 - t) * start + t * end