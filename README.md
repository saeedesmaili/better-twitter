## Better-Twitter
A simple python tool that makes your twitter timeline much better.

### Installation
```bash
pip3 install better-twitter
```

### Twitter API
To be able to use this package, you need to [register a Twitter app](https://github.com/saeedesmaili/better-twitter/blob/main/docs/twitter_app.md) and add its credentials when you use this package for the first time. This package will connect to your Twitter account using that app's credentials on behalf of you.

### Get started
#### Block from file
To block multiple users of a file:
```bash
better-twitter --block-file test_file.csv
```
Note: The csv file should have two columns named `user_id` and `screen_name`.

#### Mute from file
To mute multiple users of a file:
```bash
better-twitter --mute-file test_file.csv
```
Note: The csv file should have two columns named `user_id` and `screen_name`.

#### Update Twitter API
To update twitter API credentials:
```bash
better-twitter --update-api
```

### To Do
- [x] Add "mute from file" functionality
- [x] Add "block from file" functionality
- [ ] Rewrite the functions in OOP style
- [ ] Splite functions to be separated in different files and directories (instead of a single main.py file)
- [ ] Add "block/mute retweeters of a tweet" functionality
- [ ] Add "block/mute likes of a tweet" functionality
- [ ] Add "check a fake user's retweets" functionality
- [ ] Add "remove my tweets older than N days" functionality
- [ ] Add "remove my likes older than N days" functionality
- [ ] Add "search for tweets containing a specific word/hashtag and block/mute them"
- [ ] Add "export an account's tweets/followers/followings/likes"
- [ ] Add "block accounts tweeting about a specific hashtag"
- [ ] Add "export block list"