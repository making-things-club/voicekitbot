# Google Voice Kit Bot

Run a custom python script on a Google Voice Kit (Raspberry Pi) to do things, such control Spotify being played on another machine, via Slack and [Awkbot](https://github.com/thegingerbloke/awkbot-slack)

## Usage

Once this is set up, you can control Spotify using the following commands:

* "OK Google, play music"
* "OK Google, pause music"
* "OK Google, skip track"

## Installation

* Set up a Google Voice Kit with a Raspberry Pi, following the [online instructions](https://aiyprojects.withgoogle.com/voice)

* Set up an [awkbot](https://github.com/thegingerbloke/awkbot-slack) - the Google Voice Kit will be posting commands into Slack, but we need a separate bot with a 'direct' connection to Spotify to detect those instructions and act upon them.

* Register a new bot in Slack:

  * Install the _Bot_ Slack integration. Visit the following URL, replacing `{SLACK-ACCOUNT-NAME}` with your account:

    https://{SLACK-ACCOUNT-NAME}.slack.com/apps/A0F7YS25R-bots

  * Create a new bot user - e.g. `@voicekitbot`

    https://{SLACK-ACCOUNT-NAME}.slack.com/apps/new/A0F7YS25R-bots

  * Once saved, take a note of the bot API key

  * Add the bot user to the channel that you want it to post messages to (e.g. the `@awkbot` debug channel)

* Clone this repo onto the Pi into the directory:

  ```
  /home/pi/AIY-voice-kit-python/
  ```

* From this directory, start the virtualenv:

  ```
  source env/bin/activate
  ```

* Move into the cloned directory

  ```
  cd voicekitbot/
  ```

* Duplicate the `config.example.py` file, rename it to `config.py` and fill in the blanks

* Install the requirements:

  ```
  pip install -r requirements.txt
  ```

* Ensure the script works by running it manually:

  ```
  python voicekitbot.py
  ```

* Set up the script to start when you power up the Pi:

  ```
  sudo cp voicekitbot.service /lib/systemd/system/
  sudo systemctl enable voicekitbot.service
  ```

  * To manually start/stop this service, run:

    ```
    sudo service voicekitbot start
    sudo service voicekitbot stop
    sudo service voicekitbot status
    ```
