import cv2

# Read the image
image = cv2.imread('coin_image.png')

# Known width of the bounding rectangles (each side of the square) in millimeters
known_width_mm = 23

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and help contour detection
blurred = cv2.GaussianBlur(gray, (15, 15), 0)

# Apply edge detection using Canny
edges = cv2.Canny(blurred, 30, 150)

# Find contours in the edged image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours based on area
min_contour_area = 500
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Create a copy of the original image for drawing rectangles
result_image = image.copy()

# Known width in pixels
known_width_pixels = 23  # Adjust as needed

# Draw bounding rectangles around the detected coins
for contour in filtered_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Calculate the size in millimeters
    pixel_per_mm = w / known_width_mm
    size_mm = w / pixel_per_mm
    text = f'{size_mm:.2f}mm'
    cv2.putText(result_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Save the image with bounding rectangles and size information
output_path = 'detected_coins_image.png'
cv2.imwrite(output_path, result_image)

# Display the result
cv2.imshow('Detected Coins', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Image with bounding rectangles and size information saved to: {output_path}")
