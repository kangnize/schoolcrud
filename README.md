1. Clone the Repository
First, clone the repository to your local machine:

bash
Copy code
https://github.com/kangnize/schoolcrud.git
cd flaskcrud
2. Create a Virtual Environment
Create a virtual environment to manage dependencies:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
Install the necessary packages using pip:

bash
Copy code
pip install -r requirements.txt
4. Set Up Environment Variables
Set up the environment variables required for the application. Create a .env file in the root directory with the following content:

plaintext
Copy code
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///site.db
5. Initialize the Database
Initialize the SQLite database:

bash
Copy code
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
6. Run the Application
Start the Flask application:

bash
Copy code
python run.py


