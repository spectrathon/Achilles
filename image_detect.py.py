from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration
from PIL import Image

# Define the image path using a raw string literal
image_path = 'C:/Users/91766/Desktop/imgg.jpeg'


# Open the image file
image = Image.open(image_path)

# Initialize Pix2Struct processor and model
processor = Pix2StructProcessor.from_pretrained('google/deplot')
model = Pix2StructForConditionalGeneration.from_pretrained('google/deplot')

# Process the image and generate predictions
inputs = processor(images=image, text="Generate underlying data table of the figure below:", return_tensors="pt")
predictions = model.generate(**inputs, max_new_tokens=512)

# Decode and print the predictions
print(processor.decode(predictions[0], skip_special_tokens=True))
