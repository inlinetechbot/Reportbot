import sys
import re
import json
from pyrogram import Client, errors


def main(Target, String):

    # workdir = 'session/'
    # pyrogram.errors.exceptions.bad_request_400.UsernameNotOccupied
    SessionString = String
    with Client(name="Session", session_string=SessionString) as app:
        User = app.get_me()
        if app.get_me():
            user_info = {"id": User.id, "first_name": User.first_name}
            print(json.dumps(user_info))
            try:
                app.join_chat(Target)
            except errors.UserAlreadyParticipant:
                app.get_chat(Target)
            except:
                pass
        else:
            sys.exit("Loggined Failed !")


if __name__ == "__main__":

    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python your_script.py <channel_username> <session_string>")
        sys.exit(1)

    # Get command-line arguments
    channel_username = sys.argv[1]
    session_string = sys.argv[2]

    main(Target=channel_username, String=session_string)
