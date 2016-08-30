import os, requests, json, argparse, sys, time, shutil
from config import *

#TODO:
#make target dir an option

parser = argparse.ArgumentParser(description='Track your instagram posts.')
parser.add_argument('-i', nargs='?', default=-1, dest='post_id',
        help='The id of the post you want to track.')
parser.add_argument('-t', dest='duration', nargs='?', defualt=48,
        help='Track post for a given amount of time in hours.')
parser.add_argument('-d', dest='args.target_dir', nargs='?', default='build/',
        help='Destination for build.')
parser.add_argument('-f', dest='filename', nargs='?', default='data.json',
        help='Name of the file that will store the data.')

api_url = "https://api.instagram.com/v1/"
access_url = "/?access_token="+access_token

def print_recent_post_ids():
    """
    Prints the most recent posts from a user's profile provided by the
    Instagram API. Displays a post's id, creation date, caption, and link.
    """
    response = requests.get(api_url+"users/self/media/recent"+access_url).json()

    for post in response["data"]:
        date = time.ctime(int(post["created_time"]))

        print("""
        id: {0}
        date: {1}
        caption: {2}
        link: {3}
        """.format(post['id'], date,
            post['caption']['text'], post['link'])
        )

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
    while int(t - time.time()) == 30 and t < startime+duration_secs:
        respose = requests.get(api_url+"media/"+post_id+access_url).json()
        t = time.time()
        entry = {
            "time" : t,
            "likes" : response["data"]["likes"]["count"]
        }
        data.append(entry)
    return data

if __name__ == "__main__":
    args = parser.parse_args()
    if args.post_id != -1:
        print("Collecting data...");
        JSONdata = collect_data(args.post_id).to_json()
        print("Collection finished! Exporting data...")

        if not os.path.isdir(args.target_dir)
            os.mkdir(args.target_dir)

        with open(args.target_dir+args.filename, 'w') as f:
            f.append('var JSONdata =\n')
            json.dump(JSONdata, f)
            shutil.copy(args.filename, args.target_dir+args.filename)
            shutil.cop("template.html", args.target_dir+"index.html")
    else:
        print_recent_post_ids()
        exit()
