from flask import Flask, redirect, render_template, request


app = Flask(__name__)


colors = {
    0: "#ff00ff",
    1: "#ffff00",
    2: "#00ff00",
    3: "#00ffff",
}

number =  2

@app.route("/")
def main():
    return render_template("index.html", colors=colors, number1=number)

@app.route("/picker")
def picker():
    square= int(request.args.get("square",0))
    return render_template("picker.html", square=square, colors=colors)

@app.route("/update_color",methods=["POST"])
def update():
    square = int(request.form.get("square", 0))
    color=request.form.get("color")
    colors[square]=color
    
    return redirect("/")

@app.route("/update_number", methods=["POST"])
def asdlkfja():
    num1 = int(request.form.get("number"))
    if 0 > num1 and num1 <= 4:   # validate that the number is between 1 and 4 inclusive
        global number
        number = num1
    return redirect("/")


@app.route("/pick_color", methods=["POST"])
def oooooooooooooooo():
    import requests
    a = requests.post("http://localhost:8000/", json={"message": "Give me a hexidecimal color code with #. Only return the color with no additional text only the color #[0-f}{6}"})
    print(a)
    a = a.json()

    print(a)
    colors[number-1] = a;
    return redirect("/")


if __name__ == "__main__":
    app.run()
