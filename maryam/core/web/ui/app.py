from flask import Flask, render_template

app = Flask(__name__)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def home():
    return render_template('index.html')

# run the application
if __name__ == "__main__":
    app.run(debug=True)