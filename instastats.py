import os, requests, json, argparse, sys, time, shutil
from config import *

parser = argparse.ArgumentParser(description='Track your instagram posts.')
parser.add_argument('-i', nargs='?', default=-1, dest='post_id',
                    help='The id of the post you want to track.')
parser.add_argument('-t', dest='duration', nargs='?', default=48,
                    help='Track post for a given amount of time in hours.')
parser.add_argument('-d', dest='target_dir', nargs='?', default='build/',
                    help='Destination for data and html.')
#NOTE: Can't make this an argument because it would be annoying to change it
#in the html template file programmatically. Can be manually changed though if needed.
filename = 'data.json'
#parser.add_argument('-f', dest='filename', nargs='?', default='data.json',
#                    help='Name of the file that will store the data.')
parser.add_argument('--display-info', dest='display_info', action='store_true',
                    help='Display information about the most recent posts.')

api_url = "https://api.instagram.com/v1/"
access_url = "/?access_token="+access_token

def recent_post_id():
    """
    Gets the id from the most recent post created by the user.

    Returns:
    String containing post id.
    """
    response = requests.get(api_url+"users/self/media/recent"+access_url)
    response.raise_for_status()
    return response.json()['data'][0]['id']

def print_recent_post_info():
    """
    Prints the most recent posts from a user's profile provided by the
    Instagram API. Displays a post's id, creation date, caption, and link.
    """
    response = requests.get(api_url+"users/self/media/recent"+access_url)
    response.raise_for_status()
    JSONdata = response.json()

    for post in JSONdata["data"]:
        date = time.ctime(int(post["created_time"]))
        caption = post['caption']['text'].encode(sys.stdout.encoding, errors='replace')

        print("""
        id: {0}
        date: {1}
        caption: {2}
        link: {3}
        """.format(post['id'], date, caption, post['link']))

def collect_data(post_id, duration):
    """
    Collects data every 30 secs for {duration} hours on post with {post_id}.
    Stores data as a list of objects. Each object contains the number of likes
    the post has and the time in secs.

    Args:
    post_id: String -- id of the post to track
    duration: Int -- Amount of time to track post in hours

    Returns:
    List of dictionarys containing data.
    """
    duration_secs = duration * 60**2
    start = t = time.time()

    data = []
    while t < start+duration_secs:
        if int(time.time() - t) == 30:
            response = requests.get(api_url+"media/"+post_id+access_url)
            response.raise_for_status()
            dataJSON = response.json()
            t = time.time()
            entry = {
                "time" : t,
                "likes" : dataJSON["data"]["likes"]["count"]
            }
            print(entry)
            data.append(entry)
    return data

def export_data(datafile, target_dir, data):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    with open(target_dir+datafile, 'w') as f:
        f.write('var JSONdata =\n')
        json.dump(data, f)
        shutil.copy("template.html", target_dir+"index.html")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.display_info:
        print_recent_post_info()
        exit()
    post_id = args.post_id if args.post_id != -1 else recent_post_id()

    print("Collecting data...");
    data = collect_data(post_id, float(args.duration))
    print("Collection finished! Exporting data...")

    export_data(filename, args.target_dir, data)
