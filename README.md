# X-ray Image Management Application

This is a Streamlit-based application for uploading, labeling, and managing X-ray images. Users can upload images, assign specific labels, and search for images based on various criteria. Additionally, users can download the search results as a ZIP file.

## Features

- Upload X-ray images with specific labels.
- Search images based on type, view, main region, and sub-region.
- Download search results as a ZIP file.
- Track the percentage of image counts by categories.

## Requirements

- Python 3.7+
- Streamlit
- Pillow

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/x-ray-image-management.git
    cd x-ray-image-management
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2. **Open your web browser and navigate to:**

    ```
    http://localhost:8501
    ```

3. **Upload Images:**

    - Enter the patient ID (leave empty for new patients).
    - Select an image to upload.
    - Choose the type, view, main region, and sub-region.
    - Optionally, enter the patient's age and any comments.
    - Click the "Upload" button to save the image and its details.

4. **Search Images:**

    - Enter labels to search for (comma-separated).
    - Choose the type, view, main region, and sub-region to filter results.
    - Click the "Search" button to display the matching images.
    - Optionally, download the search results as a ZIP file.

## Database

- The application uses SQLite for storing image metadata.
- Images are saved in the `images` directory.

