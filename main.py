import cv2
import numpy as np
import os

def create_transparent_countdown_ring(output_folder, duration, fps, resolution=(848, 480)):
    os.makedirs(output_folder, exist_ok=True)
    total_frames = duration * fps
    center = (resolution[0] // 2, resolution[1] // 2)
    radius = 100  # Radius of the ring
    thickness = 10  # Thickness of the ring

    for frame_number in range(total_frames + 1):
        progress = frame_number / total_frames
        angle = int(360 * (1 - progress))  # Calculate remaining angle

        # Create an empty transparent image with an alpha channel
        image = np.zeros((resolution[1], resolution[0], 4), dtype=np.uint8)

        # Only draw the ring if the angle is greater than 0
        if angle > 0:
            cv2.ellipse(
                image, center, (radius, radius), 0, 0, angle, (0, 255, 0, 255), thickness
            )

        # Debug: Add the frame number for verification (optional)
        cv2.putText(
            image, f"Frame {frame_number}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 2
        )

        # Save the frame with transparency
        frame_path = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_path, image)
        print(f"Frame {frame_number}/{total_frames} saved.")

# Parameters
output_folder = "countdown_frames"
duration = 20  # in seconds
fps = 30
resolution = (848, 480)

create_transparent_countdown_ring(output_folder, duration, fps, resolution)
