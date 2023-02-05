## Some notes for running on Replit

Setting up a bot on replit is fairly complicated,
and some things must be taken note of.

Firstly, directly import the whole GitHub repo into the Replit repl.

Secondly, some config variables must be manually set. For example, under `.config/pip`,
look for `pip.conf`.
Replace its whole contents with the following:

```
[global]
disable-pip-version-check = yes
index-url = https://package-proxy.replit.com/pypi/simple/

[install]
content-addressable-pool-symlink = yes
```

Under the `Secrets` tab, add a new environment variable:
`DISCORD_TOKEN`. Set the value to the Discord bot's token.

The rest of the setup should be taken care of by the bot code.

## About setting up Uptime Robot

Uptime Robot ensures that the bot stays awake on Replit.

To set up Uptime Robot, go to the Uptime Robot website, and click `Add New Monitor`.

Under `Monitor Type`, select `HTTP(s)`.
Under `Friendly Name`, enter a name for the monitor.
Under `URL (or IP)`, enter the URL of the Replit repl. (An example is `https://mzbot-v2-1.jmuzhen.repl.co`)

Set the monitoring interval to 5 minutes. You can leave everything else as default.

Click `Create Monitor`, and the uptime robot is now up and running!

---

*For debug purposes*:
Python version 3.8.12, pip version 22.3.1, discord.py commit `da317ad84b0f34a574c2a40248ba5ce23c2f6597`,
mzbot commit `48ca1950f2ed95114b07d273dc505e423593c2b9`
