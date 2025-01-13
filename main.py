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
    upscale_factor = 4  # Scale up resolution for anti-aliasing

    # Upscaled resolution
    upscale_resolution = (resolution[0] * upscale_factor, resolution[1] * upscale_factor)
    upscale_center = (upscale_resolution[0] // 2, upscale_resolution[1] // 2)
    upscale_radius = radius * upscale_factor
    upscale_thickness = ring_thickness * upscale_factor
    upscale_rect_width = rect_width * upscale_factor
    upscale_rect_height = rect_height * upscale_factor

    for frame_number in range(total_frames + 1):
        progress = frame_number / total_frames
        # Adjust the angles for 12 o'clock start and clockwise direction
        start_angle = 270
        end_angle = 270 + int(360 * progress)  # Clockwise progression

        seconds_left = duration - int(frame_number / fps)

        # Create a transparent upscaled image with alpha channel
        image_upscaled = np.zeros((upscale_resolution[1], upscale_resolution[0], 4), dtype=np.uint8)

        # Draw the rounded rectangle as the green background (upscaled)
        rect_x = upscale_center[0] - upscale_rect_width // 2
        rect_y = upscale_center[1] - upscale_rect_height // 2
        rect = (rect_x, rect_y, rect_x + upscale_rect_width, rect_y + upscale_rect_height)

        cv2.rectangle(image_upscaled, (rect[0], rect[1]), (rect[2], rect[3]), (170, 234, 35, 255), -1)

        # Draw the dark gray transparent layer (depleted part of the ring, upscaled)
        cv2.ellipse(
            image_upscaled, upscale_center, (upscale_radius, upscale_radius), 0, 0, 360, (255, 255, 255, 255), upscale_thickness
        )

        # Draw the active progress ring (upscaled)
        if int(360 * progress) > 0:  # Only draw if there is progress
            cv2.ellipse(
                image_upscaled, upscale_center, (upscale_radius, upscale_radius), 0, start_angle, end_angle, (151, 206, 33, 128), upscale_thickness
            )

        # Add the remaining seconds in the center of the ring (upscaled)
        text = str(seconds_left)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2 * upscale_factor  # Scale up the font
        font_thickness = 3 * upscale_factor  # Scale up the thickness
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = upscale_center[0] - text_size[0] // 2
        text_y = upscale_center[1] + text_size[1] // 2

        cv2.putText(
            image_upscaled, text, (text_x, text_y), font, font_scale, (0, 0, 0, 255), font_thickness, cv2.LINE_AA
        )

        # Downscale the image to the target resolution
        image_downscaled = cv2.resize(image_upscaled, resolution, interpolation=cv2.INTER_AREA)

        # Save the frame with transparency
        frame_path = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_path, image_downscaled)
        print(f"Frame {frame_number}/{total_frames} saved.")

# Parameters
output_folder = "countdown_frames"
duration = 20  # Dynamic duration in seconds
fps = 30
resolution = (848, 480)

create_dynamic_countdown_ring(output_folder, duration, fps, resolution)
