# API Documentation

This API provides several endpoints to extract text from images using OpenAI's GPT-4 with Vision model and generate an image of a store menu using OpenAI's DALL-E model.

## Table of Contents

- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Setup

### Prerequisites

Before running the Flask API, make sure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Docker (optional)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/YounoussaBen/OpenAI_OCR.git
   cd OpenAI_OCR
   ```

2. Create a virtual environment named `env`:

   ```bash
   python3 -m venv env
   ```

3. Activate the virtual environment:

   ```bash
   source env/bin/activate
   ```

4. Install dependencies using pip within the virtual environment:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables:

   Create a `.env` file in the root directory of your project and add the following:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Server

You can run the Flask server using either Python directly or Gunicorn. Additionally, there's a script available to simplify the process.

#### Running with Python

To run the Flask server with Python, execute the following command:

```bash
python app.py
```

The server will start running on http://localhost:5000 by default.

#### Running with Gunicorn

You can also run the Flask server with Gunicorn. Use the provided `run.sh` script:

```bash
./run.sh
```

The server will start running with Gunicorn on http://localhost:5000 by default.

#### Running with Docker

Alternatively, you can run the Flask server using Docker:

```bash
docker build -t my-flask-app .
docker run -p 5000:5000 my-flask-app
```

### Endpoints

#### Extract Text from Image

- **URL:** `/extract_text`
- **Method:** POST
- **Request Body:**
  - `image` (file): An image file to extract text from.
- **Response:** Returns a JSON object with the extracted text or an error.

Example Request:

```bash
curl -X POST http://localhost:5000/extract_text -F "image=@path_to_your_image.jpg"
```

Example Response:

```json
{
  "extracted_text": "The extracted text will be here."
}
```

#### Generate Store Menu Image

- **URL:** `/generate_menu_image`
- **Method:** POST
- **Request Body:**
  - `products` (list): A list of products, where each product is a dictionary with a `name` and `price` key.
  - `description` (string): A description of the shop.
- **Response:** Returns a JSON object with the URL of the generated menu image or an error.

Example Request:

```json
{
  "products": [
    {"name": "Coffee", "price": 2.5},
    {"name": "Sandwich", "price": 5.0},
    {"name": "Salad", "price": 7.0},
    {"name": "Juice", "price": 3.5}
  ],
  "description": "A charming little bakery known for its fresh bread and pastries."
}
```

Example Response:

```json
{
  "image_url": "URL_of_the_generated_image"
}
```

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).