# Clipboard Sharing Web Application

A simple web application for sharing text snippets securely. Users can save text content and retrieve it using a unique clip ID. The application also includes an admin panel for managing saved clips.

## Features

- **Save Text**: Users can save text content and receive a unique clip ID.
- **Retrieve Text**: Users can retrieve saved text using the clip ID.
- **Admin Panel**: Admins can view, sort, and delete all saved clips.
- **Responsive Design**: Built with Tailwind CSS for a clean and responsive UI.
- **Database Integration**: Uses PostgreSQL for storing clipboard data.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: PostgreSQL (supabase.com)
- **Deployment**: Vercel
- **Environment Management**: `python-dotenv`

## Setup Instructions

### Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **PostgreSQL**: Set up a PostgreSQL database.
3. **Environment Variables**: Create a `.env` file to store sensitive information.

### Installation

1. Clone the repository:

   ```bash
   https://github.com/Rutiktorambe/Online-Clipboard.git
   cd online-clipboard
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   Create a `.env` file in the root directory and add the following variables:

   ```env
   DATABASE_URL=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   ```

4. Initialize the database:
   Run the following SQL commands to create the `clipboard` table:

   ```sql
   CREATE TABLE clipboard (
       id SERIAL PRIMARY KEY,
       clip_id VARCHAR(10) NOT NULL,
       content TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Access the application:
   Open your browser and navigate to `http://localhost:5000`.

## Usage

### Save Text

1. Navigate to the homepage (`/`).
2. Enter your text in the textarea and click "Save".
3. You will receive a unique clip ID to retrieve the text later.

### Retrieve Text

1. Navigate to the "Get" page (`/get`).
2. Enter the clip ID to retrieve the saved text.

### Admin Panel

1. Navigate to the admin login page (`/admin`).
2. Log in using the admin credentials.
3. View, sort, or delete all saved clips.

## API Endpoints

- **Save Text**: `POST /save`

  - Request Body: `{"content": "your text here"}`
  - Response: `{"success": true, "clip_id": "1234"}`

- **Retrieve Text**: `GET /get/<clip_id>`

  - Response: `{"success": true, "content": "your text here"}`

- **Admin Login**: `POST /admin`

  - Request Body: `{"username": "admin", "password": "admin123"}`
  - Response: `{"success": true}`

- **Fetch Data**: `GET /admin/data?sort=asc|desc`

  - Response: List of clipboard entries.

- **Delete All Data**: `DELETE /admin/delete`
  - Response: `{"message": "All clipboard data deleted successfully"}`

## Screenshots
### HomePage
![homepage](https://github.com/user-attachments/assets/7e90a905-e13f-401a-a995-794e4857da31)

### RetrievePage
![retriveoage](https://github.com/user-attachments/assets/4f608369-57f4-44e5-8914-a1db217e2d73)

### AdminPage
![admin](https://github.com/user-attachments/assets/3aad1026-93ae-4287-9fe9-4b3c2432531f)



## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the backend framework.
- Tailwind CSS for the frontend styling.
- PostgreSQL for database management.

```

```
