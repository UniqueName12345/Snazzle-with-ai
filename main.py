REPLIT_MODE = True
USE_SCRATCHDB = True
HOST, PORT = '127.0.0.1', 3000

"""
      **** Snazzle Server Code ****
 Made in Flask by the Snazzle team over at 
https://github.com/redstone-scratch/Snazzle/
"""

from flask import Flask, render_template, stream_template, request, redirect
from os import listdir
from werkzeug import exceptions as werkexcept
import scratchdb

app = Flask(__name__)

subforums_data = (("Welcome", ["Announcements", "New Scratchers"]),
        ("Making Scratch Projects", ["Help with Scripts", "Show and Tell", "Project Ideas", "Collaboration", "Requests", "Project Save & Level Codes"]),
        ("About Scratch", ["Questions about Scratch", "Suggestions", "Bugs and Glitches", "Advanced Topics", "Connecting to the Physical World", "Scratch Extensions", "Open Source Projects"]),
        ("Interests Beyond Scratch", ["Things I'm Making and Creating", "Things I'm Reading and Playing"]))

user_data = dict(
    theme="choco",
    user_name="CoolScratcher123",
    pinned_subforums=[],
    saved_posts=[],
    max_topic_posts=20,
    show_deleted_posts=True
)

scratchdb.use_scratchdb(True)

def get_themes():
    return [item[7:item.index(".css")] for item in listdir("static") if item.startswith("styles-") and item.endswith(".css")]

# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
@app.after_request
def add_header(r):
    """
    Stops the page from being cached so that the forums actually work correctly
    There's gotta be a better way, though, I don't want to stop all pages, just the forums
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

HOST, PORT = "127.0.0.1", 3000

subforums_data = (
    ("Welcome", ["Announcements", "New Scratchers"]),
    (
        "Making Scratch Projects",
        [
            "Help with Scripts",
            "Show and Tell",
            "Project Ideas",
            "Collaboration",
            "Requests",
            "Project Save & Level Codes",
        ],
    ),
    (
        "About Scratch",
        [
            "Questions about Scratch",
            "Suggestions",
            "Bugs and Glitches",
            "Advanced Topics",
            "Connecting to the Physical World",
            "Scratch Extensions",
            "Open Source Projects",
        ],
    ),
    (
        "Interests Beyond Scratch",
        ["Things I'm Making and Creating", "Things I'm Reading and Playing"],
    ),
)

user_data = dict(user_theme="choco", user_name="CoolScratcher123", pinned_subforums=[])

categories = {
    "Announcements": 5,
    "New Scratchers": 6,
    "Help with Scripts": 7,
    "Show and Tell": 8,
    "Project Ideas": 9,
    "Collaboration": 10,
    "Requests": 11,
    "Project Save & Level Codes": 60,
    "Questions about Scratch": 4,
    "Suggestions": 1,
    "Bugs and Glitches": 3,
    "Advanced Topics": 31,
    "Connecting to the Physical World": 32,
    "Developing Scratch Extensions": 48,
    "Open Source Projects": 49,
    "Things I'm Making and Creating": 29,
    "Things I'm Reading and Playing": 30,
}


def get_sfid_from_name(name):
    return categories[name] or 0


def get_name_from_sfid(sfid):
    arr = [None] * (max(categories.values()) + 1)
    for key, value in categories.items():
        arr[value] = key
    return arr


@app.context_processor
def context():
    # Play with this and the user_data dict to manipulate app state
    return dict(
        theme=user_data['theme'],
        username=user_data['user_name'],
        signed_in=False,
        to_str=lambda x: str(x),
        get_author_of=scratchdb.get_author_of,
        len=len,
        host=HOST,
    )


@app.get("/")
def index():
    """
    The home page of the app
    """
    projects = scratchdb.get_featured_projects()
    return stream_template(
        "index.html",
        featured_projects=projects["community_featured_projects"],
        featured_studios=projects["community_featured_studios"],
        trending_projects=projects["community_newest_projects"],
        loving=projects["community_most_loved_projects"],
        remixed=projects["community_most_remixed_projects"],
    )

@app.get("/editor")
def editor():
    """
    Unused editor page. Will be removed soon as part of cleanup
    """
    # unused editor page
    return render_template("editor.html")


@app.get("/trending")
def trending():
    """
    Explore page.
    """
    if filter := request.args.get('filter'):
        return render_template('trending.html', filter=filter)
        
    return render_template("trending.html")


@app.get("/forums")
def categories():
    """
    A page that lists all the subforums in the forums
    """
    return render_template('forums.html', data=subforums_data, pinned_subforums=user_data["pinned_subforums"])

@app.get('/forums/<subforum>')
def topics(subforum):
    """
    A page that lists all the topics in the subforum
    """
    
    show_deleted_topics = False
    
    response = scratchdb.get_topics(subforum)
    if response['error']:
        return render_template('scratchdb-error.html', err=response['message'])
    return stream_template('forum-topics.html', subforum=subforum, topics=response['topics'], pinned_subforums=user_data["pinned_subforums"], str=str)

@app.get('/forums/topic/<topic_id>')
def topic(topic_id):
    """
    Shows all posts in a topic.
    """
    
    show_deleted_posts = False
    
    topic_title = scratchdb.get_topic_data(topic_id)['title']
    topic_posts = scratchdb.get_topic_posts(topic_id)['posts']
    return stream_template('forum-topic.html', topic_id=topic_id, topic_title=topic_title, topic_posts=topic_posts, max_posts=user_data['max_topic_posts'], show_deleted=show_deleted_posts, list=list)

@app.route('/settings', methods=['GET'])
def settings():
    """
    Settings page.
    Change theme, status, link github account
    """
    for key, value in request.args.items():
        user_data[key.replace('-', '_')] = value
        
    return render_template('settings.html', 
                           themes=get_themes(),
                           str_title=str.title)


@app.get("/change_theme")
def theme_change():
    # to-be-unused route to change theme
    requested_theme = request.args.get("theme")
    user_data["user_theme"] = requested_theme
    return redirect("/settings")


@app.get("/downloads")
def downloads():
    """old download page"""
    return render_template('download.html')

@app.get("/secret/dl_mockup")
def dl_mockup():
    return render_template("dlm.html")
  
@app.get('/pin-subforum/<sf>')
def pin_sub(sf):
    """route that pins a subforum"""
    if not sf in user_data["pinned_subforums"]:
        arr = user_data["pinned_subforums"].copy()
        arr.append(sf)
        user_data['pinned_subforums'] = arr
        return f'<script>history.back();</script>'
    else:
        return '<script>alert("You already pinned this!"); history.back()</script>'
    
@app.get('/unpin-subforum/<sf>')
def unpin_sub(sf):
    """route that unpins a subforum"""
    if sf in user_data["pinned_subforums"]:
        arr = user_data["pinned_subforums"].copy()
        arr.remove(sf)
        user_data['pinned_subforums'] = arr
        return f'<script>history.back();</script>'

@app.errorhandler(werkexcept.NotFound)
def err404(e: Exception):
    # route for error
    return render_template('_error.html', errdata=e), 404

app.run(host=HOST, port=PORT, debug=True)
