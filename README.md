# Flask Color Picker

We're going to build a small web app with Flask. It'll show four colored squares, and when you click one, you can pick a new color for it.

Before we start: **Flask** is a Python library that lets you build websites. You write Python functions, and Flask turns them into web pages that anyone can visit in a browser.

# Step 1: Setup

Create a virtual environment. This is important. Do not skip this step or I will be upset.

```bash
python -m venv .venv
```

Activate it:

Windows:
```bash
./.venv/Scripts/activate
```

Mac/Linux:
```bash
. ./.venv/bin/activate
```

# Step 2: Dependencies

Install Flask.

If you're cool and using `uv`:
```bash
uv sync
```

If not:
```bash
pip install -r requirements.txt
```

---

# A Quick Intro to HTML

HTML is what web pages are made of. It's a bunch of **tags** that describe content. Tags look like this:

```html
<tagname>content goes here</tagname>
```

Tags have a start (`<tagname>`) and an end (`</tagname>`). Some common ones:
- `<h1>`, a big heading
- `<div>`, a generic box/container
- `<a>`, a link
- `<form>`, a form with inputs and a submit button
- `<input>`, an input field (text, color picker, hidden field, etc.)
- `<button>`, a button

Tags can also have **attributes**, extra info inside the opening tag:

```html
<a href="/somewhere">Click me</a>
<div style="background-color: red;">I'm a red box</div>
```

Every HTML file has this skeleton:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
    <!-- styles and metadata go here, not visible on the page -->
</head>
<body>
    <!-- your actual content goes here -->
</body>
</html>
```

- `<!DOCTYPE html>`, tells the browser this is an HTML file
- `<head>`, stuff that isn't shown on the page (title, CSS styles, etc.)
- `<body>`, everything the user actually sees

# A Quick Intro to Jinja2

Flask uses a system called **Jinja2** to let you put Python variables into your HTML. Any time you write `{{ something }}`, Flask will replace it with the actual value of that variable.

For example, if we pass `colors={0: "#ff00ff"}` to our template, we can write:

```html
<div style="background-color: {{ colors.get(0) }};"></div>
```

And the browser will see:

```html
<div style="background-color: #ff00ff;"></div>
```

You write the template once, and Flask fills in the values each time someone loads the page.

---

# Step 3: The Homepage

We need two things: a Flask route that serves the page, and an HTML template that defines what it looks like.

## The route

Open `app.py`. Find line 13, it should be right after the `colors` dictionary. Add this:

```python
@app.route("/")
def main():
    return render_template("index.html", colors=colors)
```

Line by line:
- `@app.route("/")`, this tells Flask "when someone visits the homepage (`/`), run the function below it"
- `def main():`, the function Flask will run
- `return render_template("index.html", colors=colors)`, load the template file `index.html` and pass our `colors` dictionary to it so the HTML can use it

## The template

Create a new folder called `templates` in the project root. Inside it, create a file called `index.html`. Add this:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Color Picker</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }

        .container {
            display: flex;
            gap: 20px;
        }

        .square {
            width: 150px;
            height: 150px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/picker?square=0"><div class="square" style="background-color: {{ colors.get(0) }};"></div></a>
        <a href="/picker?square=1"><div class="square" style="background-color: {{ colors.get(1) }};"></div></a>
        <a href="/picker?square=2"><div class="square" style="background-color: {{ colors.get(2) }};"></div></a>
        <a href="/picker?square=3"><div class="square" style="background-color: {{ colors.get(3) }};"></div></a>
    </div>
</body>
</html>
```

Line by line:
- `<style>`, CSS to make things look nice. The important part: `.square` sets each colored box to 150×150 pixels
- `<div class="container">`, a box that holds all four squares side by side (that's what `display: flex` does)
- `<a href="/picker?square=0">`, a link to the picker page. The `?square=0` part is a **URL parameter**, it tells the picker page which square the user clicked. We'll use this in the next step
- `<div class="square" style="background-color: {{ colors.get(0) }};">`, the colored square itself. `{{ colors.get(0) }}` pulls color #0 out of our Python dictionary and puts it directly into the CSS

## Run it

```bash
flask run
```

Open [localhost:5000](http://localhost:5000). You should see four colored squares. Clicking them won't work yet, that's next.

---

# Step 4: The Picker Page

This is the page where the user actually chooses a new color.

## The route

Add this to `app.py`, right after the `main` function:

```python
@app.route("/picker")
def picker():
    square = int(request.args.get("square", 0))
    return render_template("picker.html", square=square, colors=colors)
```

Line by line:
- `@app.route("/picker")`, handles requests to `/picker`
- `square = int(request.args.get("square", 0))`, reads the `?square=0` part from the URL. `request.args` is a dictionary of everything after the `?` in the URL. We wrap it in `int()` because URL parameters are always strings, and we want a number. The `0` is the default if nothing is passed
- `return render_template("picker.html", square=square, colors=colors)`, loads `picker.html`, passing both which square we're editing and the full colors dictionary

## The template

Create `templates/picker.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Pick a Color</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }

        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
        }

        input[type="color"] {
            width: 100px;
            height: 100px;
            border: none;
            cursor: pointer;
        }

        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pick a color for Square {{ square }}</h1>
        <form method="POST" action="/update_color">
            <input type="color" name="color" value="{{ colors.get(square) }}">
            <input type="hidden" name="square" value="{{ square }}">
            <button type="submit">Save</button>
        </form>
    </div>
</body>
</html>
```

Line by line:
- `<h1>Pick a color for Square {{ square }}</h1>`, the heading. `{{ square }}` inserts the square number from Python, so it'll say "Pick a color for Square 0", "Square 1", etc.
- `<form method="POST" action="/update_color">`, a form that sends data to `/update_color` when submitted. `method="POST"` means the data is sent in the request body (more on that in the next step). `action` is where the form gets sent
- `<input type="color" name="color" value="{{ colors.get(square) }}">`, the color picker. `type="color"` makes the browser show a color wheel. `value` sets the starting color to whatever the square is currently. `name="color"` is how we'll read it on the server
- `<input type="hidden" name="square" value="{{ square }}">`, invisible to the user, but sends the square number along with the form so we know which square to update. Without this, the server wouldn't know which one changed
- `<button type="submit">Save</button>`, submits the form

## Run it

Restart `flask run` and click a square. You should see the color picker with the current color already selected. Clicking Save will crash, that's fine, we haven't built that part yet.

---

# Step 5: Saving the Color

Last piece. Add this to `app.py`, after the `picker` function:

```python
@app.route("/update_color", methods=["POST"])
def update():
    square = int(request.form.get("square"))
    color = request.form.get("color")
    colors[square] = color
    return redirect("/")
```

Line by line:
- `@app.route("/update_color", methods=["POST"])`, this route only accepts POST requests, which is what forms send. If someone tries to visit this URL directly in a browser, Flask will reject it. The `methods=["POST"]` part is what makes that happen
- `square = int(request.form.get("square"))`, reads the square number from the form data. `request.form` is like `request.args` but for POST data, it contains everything the form sent
- `color = request.form.get("color")`, reads the chosen color (a hex string like `#ff0000`)
- `colors[square] = color`, updates our dictionary with the new color
- `return redirect("/")`, sends the user back to the homepage so they can see the updated square

---

# Step 6: Run it

```bash
flask run
```

Open [localhost:5000](http://localhost:5000). Click a square. Pick a color. Click Save. It should update. Click another one. Marvel at your creation.

---

# Finished `app.py` for reference

If something went wrong, here's what the complete `app.py` should look like:

```python
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

colors = {
    0: "#ff00ff",
    1: "#ffff00",
    2: "#00ff00",
    3: "#00ffff",
}

@app.route("/")
def main():
    return render_template("index.html", colors=colors)

@app.route("/picker")
def picker():
    square = int(request.args.get("square", 0))
    return render_template("picker.html", square=square, colors=colors)

@app.route("/update_color", methods=["POST"])
def update():
    square = int(request.form.get("square"))
    color = request.form.get("color")
    colors[square] = color
    return redirect("/")

if __name__ == "__main__":
    app.run()
```
