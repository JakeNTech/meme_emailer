import argparse

from utils import helpers, weather_api_client, gmail_client, constants, email_constructor

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gmail-token", dest="gmail_token", help="Path to Gmail API Refresh Token", default=None)
    parser.add_argument("--weather-token", dest="weather_token", help="Weather API Token", default=None)
    parser.add_argument("--config", dest="config_json", help="Path to configuration JSON", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    print("Send a meme!")
    # See if local files are being used for the inputs
    args = get_args()
    
    # Get the configuration
    gmail_token = helpers.get_google_token(args.gmail_token)
    weather_token = helpers.get_wether_token(args.weather_token)
    config = helpers.get_config(args.config_json)
    
    # Create the Managers
    gmail = gmail_client.gmail(gmail_token)
    weather_client = weather_api_client.weather_client(weather_token)

    # Get the meme and joke for the body
    selected_meme, image = email_constructor.load_memes()
    # As only one image is returned we can convert image to an array
    image = [image]
    print(f"Selected Meme: {selected_meme}")
    joke, punch_line = email_constructor.load_joke()

    # Get the weather -> This determines what body text to use
    weather_client.get_location_weather(config["location"])
    temp, conditions = weather_client._extract_weather_for_email()

    if weather_client.current_weather_json == None:
        email_text = constants.EMAIL_TEXT_FAILED_WEATHER.format(
            joke=joke,
            punchline=punch_line
        )

    else:
        email_text = constants.EMAIL_TEXT_WITH_WEATHER.format(
            current_temp=temp,
            current_conditions=conditions,
            joke=joke,
            punchline=punch_line
        )
    
    # Build the message
    message = email_constructor.message_builder(
        sender=config["sender"],
        recipient=config["recipients"],
        bcc=config["bcc"],
        body=email_text,
        images=image
    )

    success, email = gmail.send_email(message)

    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send Email!")
        print(email["error"])