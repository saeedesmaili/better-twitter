## Better-Twitter
A simple python tool that makes your twitter timeline much better.

### Installation
```bash
pip3 install better-twitter
```

### Twitter API
To be able to use this package, you need to [register a Twitter app](https://github.com/saeedesmaili/better-twitter/blob/main/docs/twitter_app.md) and add its credentials when you use this package for the first time. This package will connect to your Twitter account using that app's credentials on behalf of you.

### Get started
#### Using in command line
To block multiple users of a file:
```bash
better-twitter --block-file test_file.csv
```
Note: The csv file should have two columns named `user_id` and `screen_name`.

To mute multiple users of a file:
```bash
better-twitter --mute-file test_file.csv
```
Note: The csv file should have two columns named `user_id` and `screen_name`.

To update twitter API credentials:
```bash
better-twitter --update-api
```