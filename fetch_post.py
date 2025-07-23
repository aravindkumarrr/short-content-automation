import json
import praw
import random

# Load Reddit API credentials
with open("config.json") as f:
    cfg = json.load(f)

# Initialize Reddit client
r = praw.Reddit(
    client_id=cfg['reddit']['id'],
    client_secret=cfg['reddit']['secret'],
    user_agent=cfg['reddit']['user_agent']
)

# ✅ List of subreddits to rotate through
SUBREDDITS = ["TIFU", "AITA", "confessions", "AskReddit", "offmychest", "TrueOffMyChest", "AskWomen"]
TIME_FILTERS = ["day", "week", "month"]

def fetch_valid_stories(count=5, limit_per_subreddit=15):
    collected_stories = []
    tried_posts = set()

    while len(collected_stories) < count:
        subreddit = random.choice(SUBREDDITS)
        time_filter = random.choice(TIME_FILTERS)
        print(f"🔍 Searching r/{subreddit} ({time_filter})...")

        posts = r.subreddit(subreddit).top(time_filter=time_filter, limit=limit_per_subreddit)
        for post in posts:
            if post.id in tried_posts:
                continue
            tried_posts.add(post.id)

            if post.selftext and len(post.selftext.strip()) > 100:
                story = {
                    "id": post.id,
                    "subreddit": subreddit,
                    "title": post.title.strip(),
                    "body": post.selftext.strip()
                }
                collected_stories.append(story)
                print(f"✅ Got story {len(collected_stories)}: {post.title[:60]}...")
            
            if len(collected_stories) >= count:
                break
    
    return collected_stories

# Main execution
# if __name__ == "__main__":
#     stories = fetch_valid_stories(count=5)  # Fetch 5 stories
#     with open("story_list.json", "w", encoding="utf-8") as f:
#         json.dump(stories, f, indent=2, ensure_ascii=False)

#     print(f"\n🎉 Done! Saved {len(stories)} stories to story_list.json")
