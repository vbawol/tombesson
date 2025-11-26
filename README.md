# Art by Tom Besson - Site Manager

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server**:
    ```bash
    python manage.py
    ```

3.  **Access the UI**:
    *   **Public Site (Preview)**: [http://localhost:5000](http://localhost:5000)
    *   **Admin Interface**: [http://localhost:5000/admin](http://localhost:5000/admin)

## Features

*   **Manage Artworks**: Add, edit, or delete artworks in `photoapp/data.json` via the Admin UI.
*   **Live Preview**: The server serves the static files directly, so you can see changes immediately.
*   **Publish to GitHub**: Click the "Publish to GitHub" button in the Admin UI to commit and push all changes to the repository.

## Directory Structure

*   `manage.py`: The Flask application for the admin UI and server.
*   `photoapp/data.json`: The database of artworks.
*   `images/gallery/`: The folder where artwork images are stored.
*   `index.html`: The main entry point for the website.
