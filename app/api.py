from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app)
# Load environment variables
load_dotenv()

# Get OpenAI API Key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key directly in the client
client = OpenAI(api_key=api_key) 

# Function to encode the image
def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in request'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image selected for uploading'}), 400

    try:
        image_data = image_file.read()
        base64_image = encode_image(image_data)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is the menu in this image? Please provide it in JSON format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_store_menu_image(product_list, description):
    """
    Generate an image of a store menu based on a list of product names and their prices,
    and a shop description.

    Args:
    - product_list (list of tuple): A list of tuples where each tuple contains
                                    a product name and its price.
    - description (str): A description of the shop.

    Returns:
    - str: URL of the generated image.
    """
    # Create the prompt for the image
    prompt = f"Create an image of a store menu for a shop with the following description:\n{description}\n"
    prompt += "The menu should include the following items and prices:\n"
    
    for product, price in product_list:
        prompt += f"- {product}: ${price}\n"
    
    # Generate the image using DALL-E API
    response = client.images.generate(model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    n=1,
    response_format='url'  # Request response as URL
    )

    # Get the URL of the generated image
    image_url = response.data[0].url

    return image_url

@app.route('/generate_menu_image', methods=['POST'])
def generate_menu_image():
    """
    Endpoint for generating a store menu image.

    Expects a JSON payload with a list of products and their prices.
    Example payload:
    {
        "products": [
            {"name": "Coffee", "price": 2.5},
            {"name": "Sandwich", "price": 5.0},
            {"name": "Salad", "price": 7.0},
            {"name": "Juice", "price": 3.5}
        ],
        "description": "A charming little bakery known for its fresh bread and pastries."
    }
    """
    data = request.get_json()

    if 'products' not in data:
        return jsonify({'error': 'No products found in request'}), 400
    
    if 'description' not in data:
        return jsonify({'error': 'No description found in request'}), 400

    # Extract product list and description from the request data
    product_list = [(product['name'], product['price']) for product in data['products']]
    description = data['description']

    try:
        # Generate the store menu image and return the URL
        image_url = generate_store_menu_image(product_list, description)
        return jsonify({'image_url': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_image_variation', methods=['POST'])
def create_image_variation():
    """
    Endpoint for creating a variation of an input image.

    Expects a POST request with an image file.
    """
    try:
        # Check if the request contains an image file
        if 'image' not in request.files:
            return jsonify({'error': 'No image found in request'}), 400
        
        image_file = request.files['image']
        
        # Check if the image file is empty
        if image_file.filename == '':
            return jsonify({'error': 'No image selected for uploading'}), 400
        
        # Read the content of the image file
        image_data = image_file.read()
        
        # Call the OpenAI client to create a variation of the input image
        response = client.images.create_variation(
            model="dall-e-2",
            image=image_data,
            n=1,
            size="1024x1024"
        )

        # Get the URL of the generated variation image
        image_url = response.data[0].url
        
        return jsonify({'image_url': image_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add Swagger UI to the application
swagger_url = "/swagger"
api_url = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={"app_name": "My Flask API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

if __name__ == '__main__':
    app.run(debug=True)
