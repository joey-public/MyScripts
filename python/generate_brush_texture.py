import numpy as np
from PIL import Image
import sys

def generate_procedural_brush_circle(size=64, hardness=0.7, noise_amount=0.2):
    """
    Generate a circular procedural brush texture with transparency.
    
    Args:
    size (int): The width and height of the square brush texture.
    hardness (float): Controls the brush edge softness. Range 0 to 1, where 1 is hardest.
    noise_amount (float): Amount of noise to add. Range 0 to 1.
    
    Returns:
    numpy.ndarray: A 2D numpy array representing the circular brush texture with transparency.
    """
    # Create a grid of coordinates
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    # Calculate the distance from the center
    distance = np.sqrt(x*x + y*y)
    # Create a mask for the circle
    mask = distance <= size/2
    # Create the basic circular gradient
    gradient = np.zeros((size, size))
    gradient[mask] = 1 - distance[mask] / (size/2)
    # Apply hardness
    gradient = (gradient - (1 - hardness)) / hardness
    gradient = np.clip(gradient, 0, 1)
    # Add some noise for a more natural look
    noise = np.random.rand(size, size) * noise_amount
    texture = np.clip(gradient + noise, 0, 1)
    # Apply the circular mask
    texture *= mask
    # Convert to 8-bit alpha values
    alpha = (texture * 255).astype(np.uint8)
    return alpha


def generate_procedural_brush_circle2(size=64, hardness=0.7, noise_amount=0.2, transparency_variation=0.3):
    """
    Generate a circular procedural brush texture with variable pixel transparency.
    
    Args:
    size (int): The width and height of the square brush texture.
    hardness (float): Controls the brush edge softness. Range 0 to 1, where 1 is hardest.
    noise_amount (float): Amount of noise to add. Range 0 to 1.
    transparency_variation (float): Amount of random transparency variation. Range 0 to 1.
    
    Returns:
    numpy.ndarray: A 2D numpy array representing the circular brush texture with transparency.
    """
    # Create a grid of coordinates
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    # Calculate the distance from the center
    distance = np.sqrt(x*x + y*y)
    # Create a mask for the circle
    mask = distance <= size/2
    # Create the basic circular gradient
    gradient = np.zeros((size, size))
    gradient[mask] = 1 - distance[mask] / (size/2)
    # Apply hardness
    gradient = (gradient - (1 - hardness)) / hardness
    gradient = np.clip(gradient, 0, 1)
    # Add some noise for a more natural look
    noise = np.random.rand(size, size) * noise_amount
    texture = np.clip(gradient + noise, 0, 1)
    # Apply the circular mask
    texture *= mask
    # Add variable transparency
    transparency = np.random.rand(size, size) * transparency_variation
    transparency *= gradient  # Make transparency correlate with distance from center
    texture *= (1 - transparency)
    # Convert to 8-bit alpha values
    alpha = (texture * 255).astype(np.uint8)
    return alpha

def generate_procedural_brush(size=64, hardness=0.7, noise_amount=0.2):
    """
    Generate a procedural brush texture with transparency.
    
    Args:
    size (int): The width and height of the square brush texture.
    hardness (float): Controls the brush edge softness. Range 0 to 1, where 1 is hardest.
    noise_amount (float): Amount of noise to add. Range 0 to 1.
    
    Returns:
    numpy.ndarray: A 2D numpy array representing the brush texture with transparency.
    """
    # Create a grid of coordinates
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    # Calculate the distance from the center
    distance = np.sqrt(x*x + y*y)
    # Create the basic circular gradient
    gradient = 1 - distance / (size/2)
    # Apply hardness
    gradient = (gradient - (1 - hardness)) / hardness
    gradient = np.clip(gradient, 0, 1)
    # Add some noise for a more natural look
    noise = np.random.rand(size, size) * noise_amount
    texture = np.clip(gradient + noise, 0, 1)
    # Convert to 8-bit alpha values
    alpha = (texture * 255).astype(np.uint8)
    return alpha

def save_brush_to_png(brush_texture, filename, color=(0, 0, 0)):
    """
    Save the brush texture as a PNG file with transparency.
    
    Args:
    brush_texture (numpy.ndarray): The 2D brush texture array.
    filename (str): The name of the file to save (including .png extension).
    color (tuple): The RGB color of the brush (default is black).
    """
    # Create an RGBA image
    rgba = np.zeros((brush_texture.shape[0], brush_texture.shape[1], 4), dtype=np.uint8)
    rgba[..., :3] = color  # Set the color channels
    rgba[..., 3] = brush_texture  # Set the alpha channel
    # Create a PIL Image from the RGBA array
    image = Image.fromarray(rgba, mode='RGBA')
    # Save the image as PNG
    image.save(filename, format='PNG')
    print(f"Brush texture saved as {filename}")

if __name__ == '__main__':
    # Example usage:
    args = sys.argv
    USAGE = 'python generate_brush_texture <gen_size> <hardness> <noise_amount>  <r> <g> <b> <outfile>'
    if len(args) != 8:
        print(USAGE)
    else:
        gen_size = int(args[1]) 
        hardness = float(args[2])
        noise_amount = float(args[3])
        r = float(args[4])
        g = float(args[5])
        b = float(args[6])
        file_path = args[7]
        brush_texture = generate_procedural_brush_circle2(gen_size, hardness, noise_amount)
        save_brush_to_png(brush_texture, file_path, (r,g,b))
