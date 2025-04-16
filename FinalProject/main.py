from FreshTrack import create_app

app = create_app()

# imports the create_app function from the FreshTrack folder and creates an instance of the Flask application.
if __name__ == '__main__':
    app.run(debug=True)