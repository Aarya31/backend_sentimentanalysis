import snscrape.modules.twitter as sntwitter

def fetch_twitter_replies(tweet_url, max_comments=50):
    """
    Fetch replies to a tweet using snscrape.
    Args:
        tweet_url (str): Full tweet URL.
        max_comments (int): Max number of replies to fetch.
    Returns:
        List of reply texts (strings).
    """
    tweet_id = tweet_url.rstrip('/').split("/")[-1]
    query = f"conversation_id:{tweet_id}"

    comments = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_comments:
            break
        comments.append(tweet.content)
    return comments
