# JutiBot #

This is an [Errbot](http://errbot.io) setup with some custom plugins
thrown in.

## Running ##

This bot is currently set up for Telegram. To run it, get a Telegram
token for it and put it in an environment variable called
`TELEGRAM_TOKEN`. Then fire up the bot, start a chat with it and say
`!whoami` to get your user ID, which is a number. Then put that number
in an environment variable called `BOT_ADMINS` along with the numbers
of other admins, separated by whitespace. Restart the bot and you're
off to the races.
