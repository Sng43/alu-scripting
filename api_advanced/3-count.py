#!/usr/bin/python3
"""
3-count module
"""
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """
    Queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords (case-insensitive).
    """
    if not word_count:
        word_count = {word.lower(): 0 for word in word_list}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'python:word.counter:v1.0 (by /u/yourusername)'}
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            for child in data['data']['children']:
                title = child['data']['title'].lower().split()
                for word in word_count.keys():
                    word_count[word] += title.count(word)
            after = data['data']['after']
            if after:
                return count_words(subreddit, word_list, after, word_count)
            else:
                sorted_counts = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
                for word, count in sorted_counts:
                    if count > 0:
                        print(f"{word}: {count}")
        else:
            return
    except requests.RequestException:
        return

