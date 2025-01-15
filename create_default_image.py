from PIL import Image, ImageDraw

# Create a 300x300 white image
img = Image.new('RGB', (300, 300), 'white')
draw = ImageDraw.Draw(img)

# Draw a simple border
draw.rectangle([0, 0, 299, 299], outline='gray')
draw.text((100, 140), 'No Image', fill='gray')

# Save as default-recipe.jpg
img.save('static/images/default-recipe.jpg') 