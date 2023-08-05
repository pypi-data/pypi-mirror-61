# Serie TV info
Works with only **Python 3** and give all infos about serie TV info.

Infos are taken from [@SerieTvItaly_bot Telegram Bot](https://t.me/SerieTvItaly_bot) and availability depend on bot's users.

For example if noone open Stranger Things to watch the 3x01 in streaming, bot will not compile all infos and our API will not be sensible to serie TV and/or episodes.

Another example, if Stranger Things was opened but not the first episode of the third season, API give serie TV info but not about the third season.

In general, if bot's user open an episode automaticalli API became sensible to that info.

# How it works
There is only one dependecies: **requests**

This module give you the JSON info complete (except cast, crew and guest star) about serie, episode and season.

You can have visual simple infos if you execute from the command-line, you can have all infos if execute from python code.

Cast, Crew, Guest Star, Season info and Episode info will not be shown with 'beauty print' due to info richness, so only essential info will be shown and have a beautiful appearance.

# How to install

This code can be installed with [pip](https://pypi.org/project/info_serie_tv/), if you have pip installed execute the pip command to install new package `pip install info_serie_tv`

# Example of usage

You have 2 ways to use my package from command-line, simply write `info_serie_tv` and creation start!

You can also use with your python project, here an example:

```python
import info_serie_tv

my_username = 'example'
my_password = 'example_pw'

# For first create our API Object (very simple)
api_account = Bot_API('terminal_api', 'terminal_api') # credential are irrilevant

# Now get info from SerieTvItalt_bot
bot_accout = SerieTvItaly_bot(api_account)

# This API command will retrive all infos
bot_accout.terminal_api()

# if everything is okay, JSON info is in attribute 'serie_json'
Complete_Info = bot_accout.serie_json

# If you wanna see the beauty print
bot_accout.beauty_print()
```
