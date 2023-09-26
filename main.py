import os
import praw

from post import Post

# connect praw
reddit = praw.Reddit(
    client_id="6BTa-Zg0LzSof23gsNnmCw",
    client_secret="dWPGy38FvVtaYZIZnMlq5BMb_c5v7w",
    user_agent="chrome:com.myredditapp:v1.0 (by u/Zone-Embarrassed)",
)
if not reddit:
    print("PRAW unable to connect through")
else:
    print("PRAW successfully connected")

print("enter subreddit:")

entered_subreddit = input()

# use user input to search under specific subreddit
print("searching r/" + entered_subreddit)
print(type(entered_subreddit))
submissions = reddit.subreddit(entered_subreddit).top(time_filter="day", limit=3)

for submission in submissions:
    post = Post(submission)
