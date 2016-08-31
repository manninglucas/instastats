Instastats
=============
Chart likes on your Instagram posts.

## Installation
Requires Python 3.x and the requests library.

1. Clone this repo with `git clone https://github.com/manninglucas/instastats.git`
2. Obtain an access token for your account (Easiest way is through setting up a dummy project
in the developer portal).
3. create a file named config.py in the same repo. In it name create a variable called `access token`
with the value being a string of your access token.
4. Run instastats.

## Usage
instastats.py [-h] [-i [POST_ID]] [-t [DURATION]] [-d [TARGET_DIR]]
    [--display-info]

Track your instagram posts.

optional arguments:
  -h, --help       show this help message and exit
  -i [POST_ID]     The id of the post you want to track.
  -t [DURATION]    Track post for a given amount of time in hours.
  -d [TARGET_DIR]  Destination for data and html.
  --display-info   Display information about the most recent posts.

- Once the data is finished collecting, you run `python -m http.server` in your
build directory with the data.
- Navigate to localhost:8000 to view your chart.
