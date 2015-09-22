from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/iframe")
def iframe_test():
	return render_template("iframe_test.html")


@app.route("/dummydata/<string:filename>")
def dummy_path(filename):
	return send_from_directory('dummydata', filename)



if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
