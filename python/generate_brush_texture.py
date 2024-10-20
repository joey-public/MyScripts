import numpy as np
from PIL import Image
import sys


#def generate_brush_texture(size=64):
#    """
#    Generate a brush texture as a numpy array with an alpha channel.
#    
#    Args:
#    size (int): The width and height of the square texture.
#    
#    Returns:
#    numpy.ndarray: A 3D numpy array representing the brush texture with transparency.
#    """
#    # Create a grid of coordinates
#    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
#    # Calculate the distance from the center
#    distance = np.sqrt(x*x + y*y)
#    # Create the basic circular gradient
#    texture = 1 - (distance / (size/2))
#    # Clip values to [0, 1] range
#    texture = np.clip(texture, 0, 1)
#    # Add some noise for a more natural look
#    noise = np.random.rand(size, size) * 0.2
#    texture = np.clip(texture + noise, 0, 1)
#    # Convert to 8-bit grayscale and create alpha channel
#    alpha = (texture * 255).astype(np.uint8)
#    # Create RGBA array (all channels are the same for grayscale)
#    rgba = np.dstack([alpha, alpha, alpha, alpha])
#    return rgba


def generate_brush_texture(size=64, center_darkness=0.8, edge_lightness=0.2):
    """
    Generate a brush texture as a numpy array with an alpha channel.
    The brush has a dark center and lighter edges.
    
    Args:
    size (int): The width and height of the square texture.
    center_darkness (float): Darkness of the center (0 to 1, where 1 is black).
    edge_lightness (float): Lightness of the edges (0 to 1, where 1 is white).
    
    Returns:
    numpy.ndarray: A 3D numpy array representing the brush texture with transparency.
    """
    # Create a grid of coordinates
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    # Calculate the distance from the center
    distance = np.sqrt(x*x + y*y)
    # Normalize the distance
    normalized_distance = distance / (size/2)
    # Create the gradient (dark center, light edges)
    texture = normalized_distance * (1 - center_darkness) + center_darkness
    # Adjust the gradient to make edges lighter
    texture = 1 - (1 - texture) * (1 - edge_lightness)
    # Clip values to [0, 1] range
    texture = np.clip(texture, 0, 1)
    # Add some noise for a more natural look
    noise = np.random.rand(size, size) * 0.1
    texture = np.clip(texture + noise, 0, 1)
    # Convert to 8-bit grayscale
    grayscale = (texture * 255).astype(np.uint8)
    # Create alpha channel (fully opaque in the center, transparent at the edges)
    alpha = ((1 - normalized_distance) * 255).astype(np.uint8)
    # Create RGBA array
    rgba = np.dstack([grayscale, grayscale, grayscale, alpha])
    return rgba

def save_texture_to_png(texture, filename):
    """
    Save the generated brush texture to a PNG file with transparency.
    
    Args:
    texture (numpy.ndarray): The brush texture as a 3D numpy array (RGBA).
    filename (str): The name of the file to save the texture to.
    """
    # Create a PIL Image from the numpy array
    image = Image.fromarray(texture, mode='RGBA')
    
    # Save the image as PNG
    image.save(filename, format='PNG')
    print(f"Texture saved as {filename}")

if __name__ == '__main__':
    # Example usage:
    args = sys.argv
    USAGE = 'python generate_brush_texture <gen_size> <outfile>'
    if len(args) != 3:
        print(USAGE)
    else:
        gen_size = int(args[1]) 
        file_path = args[2]
        #brush_texture = generate_procedural_brush_circle2(gen_size, hardness, noise_amount)
        brush_texture = generate_brush_texture(gen_size)
        save_texture_to_png(brush_texture, file_path)
