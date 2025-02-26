import cv2
import numpy as np

def process_frame(frame):
    """
    Process the frame to detect the red line and calculate its center.
    """
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2

    # Apply Gaussian blur to smooth the mask
    blurred_mask = cv2.GaussianBlur(red_mask, (5, 5), 0)

    # Find contours in the mask
    contours, _ = cv2.findContours(blurred_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate the center of the largest contour
        moments = cv2.moments(largest_contour)
        if moments["m00"] > 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            return cx, cy, red_mask

    return None, None, red_mask

def control_auv(cx, frame_width):
    """
    Generate control commands for the AUV based on the position of the red line's center.
    """
    if cx is None:
        return "STOP"  # Red line not detected

    # Calculate the error from the center of the frame
    center_error = cx - frame_width // 2

    if abs(center_error) < 20:
        return "FORWARD"  # The AUV is aligned with the line
    elif center_error > 0:
        return "TURN RIGHT"  # The AUV needs to turn right
    else:
        return "TURN LEFT"  # The AUV needs to turn left

def main():
    """
    Main function to process video and control the AUV.
    """
    # Capture video from a camera or a video file
    cap = cv2.VideoCapture(0)  # Change to a video file path if needed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        cx, cy, red_mask = process_frame(frame)

        # Draw the detected center on the frame
        if cx is not None and cy is not None:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Generate control command
        command = control_auv(cx, frame.shape[1])

        # Display the command on the frame
        cv2.putText(frame, f"Command: {command}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the original frame and the mask
        cv2.imshow("Frame", frame)
        cv2.imshow("Red Mask", red_mask)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
