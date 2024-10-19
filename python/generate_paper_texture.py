import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def create_paper_texture(width, height, noise_intensity=10, grain_density=0.3, base_color=(255, 247, 2240)):
    # Create a new image with the base color
    image = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(image)
    print(f'noise: ({type(noise_intensity)}) {noise_intensity}')
    print(f'grain: ({grain_density}) {grain_density}')
    # Add noise
    for x in range(width):
        for y in range(height):
            if random.random() < grain_density:
                noise = random.randint(-noise_intensity, noise_intensity)
                color = tuple(max(0, min(255, c + noise)) for c in base_color)
                draw.point((x, y), fill=color)
    # Add some random lines to simulate paper fibers
    for _ in range(int(width * height * 0.001)):
        start = (random.randint(0, width), random.randint(0, height))
        end = (start[0] + random.randint(-20, 20), start[1] + random.randint(-20, 20))
        color = tuple(max(0, min(255, c - random.randint(5, 15))) for c in base_color)
        draw.line([start, end], fill=color, width=1)
    return image

def crumple_paper(image, intensity=10):
    # Convert the image to numpy array
    img_array = np.array(image)
    # Create displacement maps
    x_displacement = np.random.rand(image.height, image.width) * 2 - 1
    y_displacement = np.random.rand(image.height, image.width) * 2 - 1
    # Smooth the displacement maps
    x_displacement = Image.fromarray((x_displacement * 127 + 128).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=5))
    y_displacement = Image.fromarray((y_displacement * 127 + 128).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=5))
    x_displacement = np.array(x_displacement).astype(np.float32) / 255 * 2 - 1
    y_displacement = np.array(y_displacement).astype(np.float32) / 255 * 2 - 1
    # Create mesh grid
    rows, cols = np.indices((image.height, image.width))
    # Apply displacement
    displaced_rows = rows + y_displacement * intensity
    displaced_cols = cols + x_displacement * intensity
    # Ensure the displacements are within image boundaries
    displaced_rows = np.clip(displaced_rows, 0, image.height - 1)
    displaced_cols = np.clip(displaced_cols, 0, image.width - 1)
    # Apply the displacement to create the crumpled effect
    crumpled_image = img_array[displaced_rows.astype(int), displaced_cols.astype(int)]
    # Convert back to PIL Image
    return Image.fromarray(crumpled_image)

def generate_paper_texture(w, h, noise, grain, path, crumpled=False, color =(250,247,240)):
    texture = create_paper_texture(w,h,noise, grain, color)
    if (crumpled): 
        texture = crumple_paper(texture)
    texture.save(path)


if __name__ == '__main__':
    white = (250,247,240)
    cool = (245, 245, 250) 
    yellow = (252, 250, 240)
    args = sys.argv
    USAGE = 'python generate_paper_texture <width> <height> <noise_int> <grain_int> <path>'
    if len(args) != 6:
        print(USAGE)
    w = int(args[1])
    h = int(args[2])
    n = int(args[3])
    g = float(args[4])
    path = args[5]
    generate_paper_texture(w, h, n, g, path, True, cool)
#    generate_paper_texture(w, h, n, g, 'crump_'+path)


