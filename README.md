# Step 1: Setup
Create a virtual environment, please. This is important. You need to do this otherwise I'll be mad

```bash
python -m venv .venv
```

Activate the virtual environment


windows
```bash
./.venv/Scripts/activate
```

mac/linux
```bash
. ./.venv/bin/activate
```

# Step 2: Dependencies

Install the required libraries.

If you are cool and using `uv`
```bash
uv sync
```

If you are not cool and have not installed `uv`
```bash
pip install -r requirements.txt
```


# A Quick Note on Templates
You don't need to touch the `templates` folder. It's all there for you.

They work by using **Jinja2** (kind of a standard among templating engines nowadays), which lets us put Python variables into HTML. Any time you see `{{ thing }}`, that's Python inserting data into the page.

# Step 3: The Homepage
Let's build the app. Open `app.py`. It has a dictionary of colors, but doesn't actually do anything yet.

Find line 13. It should be empty code right after the `colors` dictionary ends.

Add this code there:

```python
@app.route("/")
def main():
    return render_template("index.html", colors=colors)
```

**What did we just do?**
We created a "route" for `/`. This means when someone visits the homepage, Flask will run this function. It renders the `index.html` template and passes our `colors` dictionary to it so the HTML can display them.

# Step 4: The Picker Page
Now we need a screen where we can actually choose a new color.

Add this code right after the `main` function you just wrote:

```python
@app.route("/picker")
def picker():
    square = int(request.args.get("square", 0))
    return render_template("picker.html", square=square, colors=colors)
```

**What is happening here?**
This adds a route for `/picker`. It looks at the URL for a `?square=0` (or 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, etc.) parameter. This tells the page *which* square we are trying to change. Then it loads `picker.html`.

# Step 5: Handling the Update
Finally, we need to actually save the changes when the user clicks "Save".

Add this code next:

```python
@app.route("/update_color", methods=["POST"])
def update():
    square = int(request.form.get("square"))
    color = request.form.get("color")
    colors[square] = color

    return redirect("/")
```

**The logic:**
This route only accepts `POST` requests (which is what forms send). It grabs the `square` ID and the chosen `color` from the form data, updates our `colors` dictionary, and then sends the user back to the homepage (`/`) to see their masterpiece.

# Step 6: Run it
Time to see if it works.

```bash
flask run
```

# Step 7: Test it

Open [`localhost:5000`](http://localhost:5000) in your browser.

Click a square. Pick a color. Save it. Marvel at your creation.
