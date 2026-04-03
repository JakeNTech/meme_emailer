# meme_emailer
Why use Fax? Why use RSS? You can use Email!

## How to use
The scripts in the utils folder are designed to be generic, those can be used for any other project or use you may have.

### Installation
#### Virtual Environment
You will probably want to use a virtual environment for this:
```
python -m venv venv
```
This creates a virtual environment within the repository, this is part of the gitignore so isn't included in the repo. Once downloaded the below commands can be run:

Linux/MacOS:
```
source ./venv/bin/activate
```
Windows (via PowerShell):
```
./venv/bin/activate.ps1
```
#### Python Library requirements
To install, assuming you have pip installed:
```
pip install -r requirements.txt
```

#### Google Token - via Google Cloud Console
To get a key from the GCP Developer console follow the below steps:

\<TO DO\>

#### Google Refresh Token
Once the initial credentials have been obtained a refresh token needs to be made, this is done with:

\<TO DO\>

#### Weather API
\<TO DO\>

#### Constants
The constants file contains all the variables for the script:
- WEATHER_API_ROOT
  - This is the root URL to weather API
- SCOPES
  - This is for the Google Credentials
- JOKE_CSV_PATH
  - This is where the CSV file for the jokes are stored, this can moved.
- EMAIL_SUBJECT
  - The subject the emails will have
- EMAIL_TEXT_WITH_WEATHER
  - The body of the email if the weather is retrieved from the weather API successfully
- EMAIL_TEXT_FAILED_WEATHER
  - The body of the email if the weather isn't retrieved from the weather API successfully

#### Meme vault
Create the meme directory:
```
mkdir meme_vault
```
Once created, fill this with memes! One will be randomly chosen from this directory! 

#### jokes.csv
This can be placed either inside the "meme vault" folder or not, this is set in constants. To stick with the defaults:

Linux/MacOS:
```
printf "joke,puchline\nwhat I don't understand about driving,Who's the central reservation reserved for?" > ./meme_vault/jokes.csv
```

Windows:
```
<TO DO>
```

## GitHub Actions
\<TO DO\>