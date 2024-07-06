#!/usr/bin/python3
"""
3-count module

This module contains a function to query the Reddit API, parse the titles
of all hot articles in a given subreddit, and print a sorted count of
specified keywords.
"""
import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """
    Queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords (case-insensitive).

    Args:
        subreddit (str): The name of the subreddit to query.
        word_list (list): A list of keywords to count in the titles.
        after (str, optional): The "after" parameter for pagination. Defaults to None.
        word_count (dict, optional): A dictionary to store the counts of keywords. Defaults to {}.

    Returns:
        None
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

