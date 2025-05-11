import os
import cv2
import pandas as pd

def place_logo_on_image(image_path, logo_path, output_path, position='bottom-right', scale=0.2):
    # Load main image and logo
    image = cv2.imread(image_path)
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

    # Resize logo
    h, w = image.shape[:2]
    logo = cv2.resize(logo, (int(w * scale), int(h * scale)))

    # Split alpha channel if present
    if logo.shape[2] == 4:
        alpha_channel = logo[:, :, 3] / 255.0
        logo_rgb = logo[:, :, :3]
    else:
        alpha_channel = None
        logo_rgb = logo

    lh, lw = logo_rgb.shape[:2]

    # Determine position
    if position == 'bottom-right':
        x, y = w - lw - 10, h - lh - 10
    elif position == 'top-left':
        x, y = 10, 10
    elif position == 'top-right':
        x, y = w - lw - 10, 10
    elif position == 'bottom-left':
        x, y = 10, h - lh - 10
    else:
        x, y = (w - lw) // 2, (h - lh) // 2  # center

    # Blend logo into image
    if alpha_channel is not None:
        for c in range(3):
            image[y:y+lh, x:x+lw, c] = (
                alpha_channel * logo_rgb[:, :, c] +
                (1 - alpha_channel) * image[y:y+lh, x:x+lw, c]
            )
    else:
        image[y:y+lh, x:x+lw] = logo_rgb

    # Save the output image
    cv2.imwrite(output_path, image)

# Example usage:
# place_logo_on_image('image.jpg', 'logo.png', 'output.jpg')

