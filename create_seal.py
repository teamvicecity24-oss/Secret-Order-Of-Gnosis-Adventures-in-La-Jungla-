"""
Create the Secret Order of Gnosis seal image programmatically
"""
import pygame
import math

# Initialize pygame
pygame.init()

# Create a large square surface for the seal
size = 800
surface = pygame.Surface((size, size), pygame.SRCALPHA)

# Fill with black background
surface.fill((0, 0, 0))

center = size // 2

# Draw outer white glowing circle
for i in range(15, 0, -1):
    alpha = 255 - i * 15
    radius = 380 - i * 3
    pygame.draw.circle(surface, (255, 255, 255, alpha), (center, center), radius, 3)

# Draw main white circle border
pygame.draw.circle(surface, (255, 255, 255), (center, center), 380, 8)
pygame.draw.circle(surface, (255, 255, 255), (center, center), 365, 3)

# Draw inner gold circle
pygame.draw.circle(surface, (255, 215, 0), (center, center), 350, 6)

# Draw decorative X symbols around the outer ring
num_symbols = 16
for i in range(num_symbols):
    angle = (i / num_symbols) * 2 * math.pi
    x = center + int(365 * math.cos(angle))
    y = center + int(365 * math.sin(angle))
    # Draw small X
    size_x = 8
    pygame.draw.line(surface, (255, 215, 0), (x - size_x, y - size_x), (x + size_x, y + size_x), 3)
    pygame.draw.line(surface, (255, 215, 0), (x + size_x, y - size_x), (x - size_x, y + size_x), 3)

# Draw the golden arch/dna-like structure on sides
# Left arch
left_points = []
for angle in range(-60, 61, 2):
    rad = math.radians(angle + 180)
    r = 280
    x = center + int(r * math.cos(rad)) - 80
    y = center + int(r * math.sin(rad) * 0.5)
    left_points.append((x, y))
if len(left_points) > 1:
    pygame.draw.lines(surface, (255, 215, 0), False, left_points, 6)

# Right arch
right_points = []
for angle in range(-60, 61, 2):
    rad = math.radians(angle)
    r = 280
    x = center + int(r * math.cos(rad)) + 80
    y = center + int(r * math.sin(rad) * 0.5)
    right_points.append((x, y))
if len(right_points) > 1:
    pygame.draw.lines(surface, (255, 215, 0), False, right_points, 6)

# Draw vertical lines on the arches
for i in range(-50, 51, 10):
    rad = math.radians(i + 180)
    r = 280
    x1 = center + int(r * math.cos(rad)) - 80
    y1 = center + int(r * math.sin(rad) * 0.5)
    x2 = center + int((r-40) * math.cos(rad)) - 80
    y2 = center + int((r-40) * math.sin(rad) * 0.5)
    pygame.draw.line(surface, (255, 215, 0), (x1, y1), (x2, y2), 2)
    
    rad = math.radians(i)
    x1 = center + int(r * math.cos(rad)) + 80
    y1 = center + int(r * math.sin(rad) * 0.5)
    x2 = center + int((r-40) * math.cos(rad)) + 80
    y2 = center + int((r-40) * math.sin(rad) * 0.5)
    pygame.draw.line(surface, (255, 215, 0), (x1, y1), (x2, y2), 2)

# Draw pyramid
pyramid_height = 280
pyramid_width = 260
pyramid_top = 180
pyramid_base_y = pyramid_top + pyramid_height

# Pyramid points
pyramid_points = [
    (center, pyramid_top),  # Top
    (center - pyramid_width // 2, pyramid_base_y),  # Bottom left
    (center + pyramid_width // 2, pyramid_base_y),  # Bottom right
]

# Draw pyramid bricks
for row in range(8):
    y = pyramid_top + (row * pyramid_height // 8)
    next_y = pyramid_top + ((row + 1) * pyramid_height // 8)
    width_at_y = pyramid_width * (pyramid_height - (y - pyramid_top)) // pyramid_height
    next_width = pyramid_width * (pyramid_height - (next_y - pyramid_top)) // pyramid_height
    
    # Draw brick row
    color_val = 180 + row * 8
    brick_color = (color_val, color_val - 20, color_val - 40)
    
    points = [
        (center - width_at_y // 2, y),
        (center + width_at_y // 2, y),
        (center + next_width // 2, next_y),
        (center - next_width // 2, next_y),
    ]
    pygame.draw.polygon(surface, brick_color, points)
    pygame.draw.polygon(surface, (100, 80, 60), points, 2)

# Draw outer pyramid border
pygame.draw.polygon(surface, (255, 215, 0), pyramid_points, 6)

# Draw banana in center of pyramid
banana_y = pyramid_top + pyramid_height // 2 + 20
# Banana body (crescent shape)
for i in range(20):
    t = i / 19.0
    angle = math.pi + t * math.pi
    r = 50
    bx = center + int(r * math.cos(angle) * 0.6)
    by = banana_y + int(r * math.sin(angle) * 0.3) - 20
    pygame.draw.circle(surface, (255, 215, 0), (bx, by), 12 - i//3)
    pygame.draw.circle(surface, (200, 150, 0), (bx, by), 8 - i//4)

# Draw top circle with UGA symbol
top_circle_y = 100
top_circle_radius = 50
# Red outer ring
pygame.draw.circle(surface, (255, 50, 50), (center, top_circle_y), top_circle_radius, 8)
# White inner circle
pygame.draw.circle(surface, (255, 255, 255), (center, top_circle_y), top_circle_radius - 8)
# Draw UGA symbol
pygame.draw.arc(surface, (180, 140, 0), 
                (center - 25, top_circle_y - 30, 50, 40), 
                0.2, math.pi - 0.2, 6)
pygame.draw.arc(surface, (180, 140, 0), 
                (center - 25, top_circle_y - 5, 50, 40), 
                math.pi + 0.2, -0.2, 6)

# Draw bottom symbols
bottom_y = 700
symbols = [
    (center - 100, (0, 200, 0), "club"),  # Green club
    (center - 35, (255, 215, 0), "sun"),  # Gold sun
    (center, (255, 255, 255), "ankh"),  # White ankh
    (center + 35, (255, 215, 0), "moon"),  # Gold moon
    (center + 100, (0, 200, 0), "club"),  # Green club
]

for x, color, symbol_type in symbols:
    if symbol_type == "club":
        # Draw club symbol
        pygame.draw.circle(surface, color, (x - 8, bottom_y - 8), 8)
        pygame.draw.circle(surface, color, (x + 8, bottom_y - 8), 8)
        pygame.draw.circle(surface, color, (x, bottom_y - 18), 8)
        pygame.draw.rect(surface, color, (x - 3, bottom_y - 8, 6, 20))
    elif symbol_type == "sun":
        # Draw sun
        pygame.draw.circle(surface, color, (x, bottom_y), 12)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = x + int(15 * math.cos(rad))
            y1 = bottom_y + int(15 * math.sin(rad))
            x2 = x + int(22 * math.cos(rad))
            y2 = bottom_y + int(22 * math.sin(rad))
            pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)
    elif symbol_type == "ankh":
        # Draw ankh
        pygame.draw.circle(surface, color, (x, bottom_y - 10), 8)
        pygame.draw.rect(surface, color, (x - 3, bottom_y - 10, 6, 25))
        pygame.draw.line(surface, color, (x - 12, bottom_y + 5), (x + 12, bottom_y + 5), 4)
    elif symbol_type == "moon":
        # Draw crescent moon
        pygame.draw.circle(surface, color, (x + 3, bottom_y), 12)
        pygame.draw.circle(surface, (0, 0, 0), (x + 8, bottom_y), 10)

# Save the image
pygame.image.save(surface, 'assets/images/ui/logo.png')
print("Seal image created successfully!")
