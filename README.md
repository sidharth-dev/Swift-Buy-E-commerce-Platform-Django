# Swift-Buy E-commerce Platform

Swift-Buy is a full-stack e-commerce website built with Django, Bootstrap, and PostgreSQL. It offers a comprehensive online shopping experience with features like product management, user authentication, and order processing.

## Features

- Responsive design for seamless desktop and mobile experience
- Dynamic product listings with search functionality
- Robust shopping cart system with real-time updates
- Secure checkout process
- User account management (registration, login, profile)
- Product details page with reviews and ratings
- Admin panel for efficient backend management

## Technologies Used

- Backend: Django 5.1.1
- Frontend: Bootstrap 5.3
- Database: PostgreSQL
- Additional: Django REST framework (for API endpoints)

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/swift-buy.git
   cd swift-buy
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database and update the `DATABASES` configuration in `settings.py`

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Visit `http://127.0.0.1:8000/` in your browser to view the application

## Project Structure

- `swift_buy/`: Main project directory
- `store/`: App directory containing models, views, and templates
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
