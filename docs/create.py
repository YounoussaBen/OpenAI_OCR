from openai import OpenAI
import os

# Get your API key from environment variables or any other secure source
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

response = client.images.create_variation(
  model="dall-e-2",
  image=open("app/static/images/menu.png", "rb"),  # Pass the image data instead of the file object
  size="1024x1024",
  n=1,
)

image_url = response.data[0].url

# Print the image URL (you can handle the image URL as needed)
print(f"Generated image URL: {image_url}")
