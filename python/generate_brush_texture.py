import numpy as np
from PIL import Image
import sys

def generate_brush_texture(size=64):
    """
    Generate a brush texture as a numpy array with an alpha channel.
    
    Args:
    size (int): The width and height of the square texture.
    
    Returns:
    numpy.ndarray: A 3D numpy array representing the brush texture with transparency.
    """
    # Create a grid of coordinates
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    # Calculate the distance from the center
    distance = np.sqrt(x*x + y*y)
    # Create the basic circular gradient
    texture = 1 - (distance / (size/2))
    # Clip values to [0, 1] range
    texture = np.clip(texture, 0, 1)
    # Add some noise for a more natural look
    noise = np.random.rand(size, size) * 0.2
    texture = np.clip(texture + noise, 0, 1)
    # Convert to 8-bit grayscale and create alpha channel
    alpha = (texture * 255).astype(np.uint8)
    # Create RGBA array (all channels are the same for grayscale)
    rgba = np.dstack([alpha, alpha, alpha, alpha])
    return rgba

def downscale_texture(texture, new_size):
    """
    Downscale the texture to a new size.
    
    Args:
    texture (numpy.ndarray): The original texture as a 3D numpy array (RGBA).
    new_size (int): The desired size for the new texture (width and height).
    
    Returns:
    numpy.ndarray: The downscaled texture as a 3D numpy array (RGBA).
    """
    image = Image.fromarray(texture, mode='RGBA')
    resized_image = image.resize((new_size, new_size), Image.LANCZOS)
    return np.array(resized_image)

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
    USAGE = 'python generate_brush_texture <gen_size> <scale_size> <outfile>'
    print(args)
    if len(args) != 4:
        print(USAGE)
    else:
        gen_size = int(args[1]) 
        scale_size = int(args[2])
        file_path = args[3]
        brush_texture = generate_brush_texture(gen_size)
        #if not(scale_size == gen_size):
        #    brush_texture = downscale_texture(brush_texture, scale_size)
        save_texture_to_png(brush_texture, file_path)
