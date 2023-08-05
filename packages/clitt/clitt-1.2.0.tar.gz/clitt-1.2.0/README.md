# Clitt

Ever wanted to tweet straight from your terminal? Wait, is it just me?

## How to install it?

Install Clitt using pip or pipx

```bash
    pip install --user clitt \\ pipx install clitt
```

## How to use it?

Clitt is meant to be simple (or at least as simple as a command line client for Twitter can be), so you just need to call `clitt` or `tt`, choose an action and pass the required parameters to perform the action. 

Running `clitt` or `tt` for the first time will open a new tab on your browser with an authorization consent from Twitter, hit the authorize button, copy the code that will pop-up and paste it into the terminal. After the first time, your authorization token will be saved on your computer (and only there) for further uses.

## What can i do with Clitt?

#### Read your timeline

```$ clitt read```

![Clitt read](./docs/screenshot.png)

#### Write a Tweet

```$ clitt post "Hey, i'm using Clitt to write this!"```

#### DM someone

```$ clitt dm @target "Hey, i'm using Clitt to send you this DM!"```

#### Read your chat with another user

```$ clitt chat @target```

## Future features

- Search for tweets using keywords
- Display and attach images to tweets
- Implement filters and other customization options
- Support theme colors

## Contributing

Have you thought about any cool features you wanted to see in Clitt? Send a PR. Found any bugs in the current implementation? Feel free to open an issue. Here's a guide to some things you might need to work on Clitt.

##### Twitter dev account

You will need to make an application for a [Twitter developer account](https://developer.twitter.com/en/apply-for-access) if you want to publish your own version of Clitt, but for testing and development within this project you can use my key that is already included with this repository. If you have you own key, put it on the `config/keys.json` file inside the package.

##### Tweepy

Tweepy is a Python wrapper for the Twitter REST API, it really makes life much more easier, you can check their [docs](https://tweepy.readthedocs.io/en/latest/) and probably will find what you looking for, but if you don't, search in the [Twitter docs](https://developer.twitter.com/en/docs).

##### Clitt project structure

If you want to implement a new feature, write it in the `actions.py` file and if you need to, add a new argument treatment in `__main__.py`. Write simple and multiplatform code.