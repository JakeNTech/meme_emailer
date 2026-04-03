# weatherapi
WEATHER_API_ROOT = "https://api.weatherapi.com"

# Google Scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Joke Path
JOKE_CSV_PATH = "meme_vault/jokes.csv"

# Email Subject
EMAIL_SUBJECT = "Meme of {date_string}!"

# Body text
EMAIL_TEXT_WITH_WEATHER = """
<p>Hello! It's me!</p>
<h4>The current weather in Sandford:</h4>
<p>{current_temp}C {current_conditions}</p>
<h4>Let's get down to the nitty gritty</h4>
<p>{joke}</p>
<p>{punchline}</p>
<br>
<img src=\"cid:image_0\" style=\"max-width:900px\">
"""

EMAIL_TEXT_FAILED_WEATHER = """
<p>Hello! It's me!</p>
<h4>The current weather in Sandford:</h4>
<p>It looks like the weather has gone missing...must have been nicked</p>
<p>It must have been the swan...can we ask for it back?</p>
<h4>Let's get down to the nitty gritty</h4>
<p>{joke}</p>
<p>{punchline}</p>
<br>
<img src=\"cid:image_0\" style=\"max-width:900px\">
"""