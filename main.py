import cv2
import numpy as np
import os

def create_dynamic_countdown_ring(output_folder, duration, fps, resolution=(848, 480)):
    os.makedirs(output_folder, exist_ok=True)
    total_frames = duration * fps
    center = (resolution[0] // 2, resolution[1] // 2)
    radius = 100  # Radius of the ring
    ring_thickness = 10  # Thickness of the ring
    rect_width = (radius + 20) * 2  # Width of rounded rectangle
    rect_height = (radius + 20) * 2  # Height of rounded rectangle
    corner_radius = 31  # Rounded corner blur kernel size (must be odd)

    for frame_number in range(total_frames + 1):
        progress = frame_number / total_frames
        angle = int(360 * (1 - progress))  # Calculate remaining angle
        seconds_left = duration - int(frame_number / fps)

        # Create a transparent image with alpha channel
        image = np.zeros((resolution[1], resolution[0], 4), dtype=np.uint8)

        # Draw the rounded rectangle as the green background
        rect_x = center[0] - rect_width // 2
        rect_y = center[1] - rect_height // 2
        rect = (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)

        # Draw rounded rectangle with anti-aliasing
        sub_image = np.zeros_like(image)
        cv2.rectangle(sub_image, (rect[0], rect[1]), (rect[2], rect[3]), (170, 234, 35, 255), -1)
        
        # # Ensure GaussianBlur kernel size is odd
        # sub_image = cv2.GaussianBlur(sub_image, (corner_radius, corner_radius), 0)
        image = cv2.addWeighted(image, 1, sub_image, 1, 0)

        # Draw the dark gray transparent layer (depleted part of the ring)
        cv2.ellipse(
            image, center, (radius, radius), 0, 0, 360, (151,206,33,255), ring_thickness
        )

        # Draw the active progress ring
        if angle > 0:
            cv2.ellipse(
                image, center, (radius, radius), 0, 0, angle, (255, 255, 255, 255), ring_thickness
            )

        # Add the remaining seconds in the center of the ring
        text = str(seconds_left)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 3
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] + text_size[1] // 2

        # Use anti-aliasing for the text
        cv2.putText(
            image, text, (text_x, text_y), font, font_scale, (0, 0, 0, 255), font_thickness, cv2.LINE_AA
        )

        # Save the frame with transparency
        frame_path = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_path, image)
        print(f"Frame {frame_number}/{total_frames} saved.")

# Parameters
output_folder = "countdown_frames"
duration = 20  # Dynamic duration in seconds
fps = 30
resolution = (848, 480)

create_dynamic_countdown_ring(output_folder, duration, fps, resolution)
