# Modmail Alpha
Modmail Alpha is a Modmail Bot made in discord.py rewrite by SecretAyee
Modmail is a bot that creates a shared inbox for all moderators to use.

## Installation and Setup

Open [repl.it](https://repl.it/) and in the shell execute the command:
```
git clone https://github.com/SecretAyee/Modmail-Alpha
```
Input your token in the specified place.
Change the prefix if needed.
Run the repl.
Now register to [Uptime Robot](https://uptimerobot.com/) and create a new monitor. Select `HTTP(s)` and copy the webserver on your [repl.it](https://repl.it/) to the URL Section. Select a contact to notify. Then press `Create Monitor`

## Setup Command

The default Prefix is `=`

```bash
=setup <incoming mail channel> <resolved queries channel>
```
Where incoming mail channel = the channel where you want to receive DMs
And where the resolved channel is where you want resolved or cancelled queries to be sent
## Current Commands

```python
=invite
=setup <incoming mail channel> <resolved queries channel>
=reply <recipent id> <message>
=vote
```

## Need Help?
Join our Support server [here]( https://discord.gg/jcKUHR8pV8)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
