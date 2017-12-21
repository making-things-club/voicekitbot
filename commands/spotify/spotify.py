def init(config):
    pass


def list_actions():
    """ A list of actions in this file that can be called """
    return [
        {
            "description": "Play music",
            "content": ["play music", "put the needle on the record"],
            "function": "play"
        },
        {
            "description": "Pause music",
            "content": ["pause music", "stop music", "shut the front door"],
            "function": "pause"
        },
        {
            "description": "Skip track",
            "content": ["skip track", "next track", "skip song", "next song"],
            "function": "skip"
        },
        {
            "description": "Previous track",
            "content": ["back", "previous track", "previous song"],
            "function": "back"
        }
    ]


def play(text):
    return {
        "post": "play",
        "say": "Playing music"
    }


def pause(text):
    return {
        "post": "pause",
        "say": "Pausing music",
    }


def skip(text):
    return {
        "post": "skip",
        "say": "Skipping track"
    }


def back(text):
    return {
        "post": "back",
        "say": "Going back a track"
    }
