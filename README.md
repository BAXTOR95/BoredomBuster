# Boredom Buster

Boredom Buster is a web application that helps users find fun and engaging activities when they're feeling bored. The application fetches random activities from the Bored API and retrieves related images from the Unsplash API.

## Features

- **Random Activity Generator**: Users can click a button to get a random activity suggestion.
- **Activity Categories**: Users can filter activities by type (e.g., recreational, social, DIY, etc.) and specify the number of participants to get suitable activities.
- **Save Favorite Activities**: Users can save their favorite activities for later.

## Technologies Used

- **Python**: Backend language
- **Flask**: Web framework for Python
- **Bootstrap 5 (Bootstrap-Flask)**: Frontend framework for responsive design
- **WTForms**: For creating forms
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Flask-Migrate**: Database migration handling
- **aiohttp**: Asynchronous HTTP client
- **Bored API**: For fetching random activities based on user parameters
- **Unsplash API**: For fetching related images

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/BAXTOR95/BoredomBuster.git
   cd BoredomBuster
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Unsplash API access key:

   ```env
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=your_database_location
   UNSPLASH_ACCESS_KEY=your_unsplash_access_key
   PROD=False
   ```

5. **Initialize the database**:

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the application**:

   ```bash
   flask run
   ```

## Usage

1. **Home Page**:

   - Use the form to filter activities by type and number of participants.
   - Click the button to fetch a random activity.
   - If available, an activity with it's related image will be displayed.

2. **Login/Register**:

   - Register a new account or login with existing credentials to save your favorite activities.

3. **Favorites**:
   - View and manage your saved favorite activities.

## Project Structure

```arduino
boredom-buster/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── favorites.html
├── migrations/
│   ├── versions/
│   └── ...
├── .env
├── .gitignore
├── README.md
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. **Fork the repository**.
2. **Create a new branch**: `git checkout -b feature-branch-name`.
3. **Commit your changes**: `git commit -m 'Add some feature'`.
4. **Push to the branch**: `git push origin feature-branch-name`.
5. **Open a pull request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Bored API](https://www.boredapi.com/) for providing the activity data.
- [Unsplash API](https://unsplash.com/developers) for providing the images.
