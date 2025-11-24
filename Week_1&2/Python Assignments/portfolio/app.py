import json
from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

def load_project_data():
    """Loads project data from the JSON file."""
    try:
        # Assumes projects.json is in the same directory as app.py
        with open('projects.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Error: projects.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Could not read JSON data. Check the projects.json format.")
        return []

@app.route('/')
def home():
    """Route for the Home page."""
    return render_template('index.html')

@app.route('/projects')
def projects():
    """Route for the Projects page, loading data from JSON."""
    project_list = load_project_data()
    # Pass the list of projects to the projects.html template
    return render_template('projects.html', projects=project_list)

@app.route('/contact')
def contact():
    """Route for the Contact page."""
    return render_template('contact.html')

if __name__ == '__main__':
    # Run the application in debug mode for easy testing
    app.run(debug=True)