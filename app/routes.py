from app import app

# Show the input form
@app.route('/')
def hello_world():
    return "hello world"