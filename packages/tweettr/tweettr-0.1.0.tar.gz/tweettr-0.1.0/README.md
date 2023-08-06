# Tweettr - thin attrdict like wrapper around (a few) Tweet objects

[![PyPI](https://img.shields.io/pypi/v/tweettr)](https://pypi.org/project/tweettr/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tweettr?label=pypi)](https://pypi.org/project/tweettr/)
[![MIT license](http://img.shields.io/badge/license-MIT-yellowgreen.svg)](http://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/ap--/python-tweettr.svg)](https://github.com/ap--/tweettr/issues)
[![Github Sponsors](https://img.shields.io/badge/github-sponsors-blue)](https://github.com/sponsors/ap--)

Tweettr gives you a convenient attribute interface to (some) tweet objects without any copying overhead.
And if your editor or IDE understands type annotations it let's you do attribute auto completion.

It also add a way to provide emoji parsing with a similar interface to `.entities.hashtags`. :sparkling_heart:

So when you receive a json object from the twitter streaming api you can access it in a nicer way:

```yaml
# json blob returned from twitter streaming api
{
  "id": 11223344556677889900,
  "id_str": "11223344556677889900",
  "created_at": "Sun Feb 16 13:16:19 +0000 2020",
  "user": {
    "id": 11223344556677889900,
    "id_str": "11223344556677889900",
    "screen_name": "AAAAAAAA",
    # ...
  },
  "entities": {
    "hashtags": [{
        "indices": [12, 21],
        "text": "MyHashTag"
      }]
  },
  "text": "Hello World #MyHashTag",
  "favorite_count": 0,
  "favorited": false,
  "timestamp_ms": "1500000000000",
  "truncated": false,
  # ...
}
```

becomes:
```python
>>> import tweettr
>>> tweet = tweettr.Tweet(json_blob)
>>> tweet.user.id
11223344556677889900
>>> tweet.user.screen_name
'AAAAAAAA'
>>> tweet.emojis  # extract emojis like HashTags and Urls...
[Emoji(...), Emoji(...)]
>>> ...  # etc, etc... 
```
