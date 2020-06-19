import re

# Increments
INCREMENT_HASH = re.compile(r"(#0*#)")
INCREMENT_NO_HASH = re.compile(r"(\$0*#)")

# Placeholder - Standard
GAME_NAME = re.compile(r"(@@game_name@@)")
CREATOR = re.compile(r"(@@creator@@)")
STREAM_NAME = re.compile(r"(@@stream_name@@)")
NUM = re.compile(r"(@@num@@)")
NUM_OTHERS = re.compile(r"(@@num_others@@)")

# Placeholder - Premium
NATO = re.compile(r"(@@nato@@)")
NUM_PLAYING = re.compile(r"(@@num_playing@@)")
PARTY_SIZE = re.compile(r"(@@party_size@@)")
PARTY_DETAILS = re.compile(r"(@@party_details@@)")
PARTY_STATE = re.compile(r"(@@party_state@@)")


# Converters
STR_MANIPULATOR = re.compile(r'""(\w)+?: (\w+)?""')
