# Film Master

A Discord bot written with [Snips NLU][]
that posts film info via the [TMDB API][].

### Setup

Create a [Discord app][] for the bot and invite it to your server.

Generate a [TMDB API][] key for the bot.

Install `filmaster`:

```sh
$ pip install filmaster
```

Run the bot:

```sh
$ filmaster -d "DISCORD_TOKEN" -t "TMDB_API_KEY"
```

The command requires these parameters:

* `DISCORD_TOKEN`: The bot token of the app you created earlier.
* `TMDB_API_KEY`: The TMDB API key you generated earlier.

You may also pass the following options:

* `-p PREFIX`: Sets the command prefix of the bot.
  `PREFIX` must be a single character and defaults to `$`.
* `-v`: Increases the verbosity of the logs. Can be passed up to 4 times.

### Examples

#### Greetings

![greeting](.examples/greeting.png)

#### Help

![help](.examples/help.png)

#### Film info

![info-1](.examples/info-1.png)

![info-2](.examples/info-2.png)

![director](.examples/director.png)

![actor](.examples/actor.png)

#### Film cast

![cast-1](.examples/cast-1.png)

![cast-2](.examples/cast-2.png)

### Goodbye

![goodbye](.examples/goodbye.png)

### License

> Licensed under the [Academic Free License version 3.0][AFL-3.0]


[TMDB API]: https://developers.themoviedb.org/3/
[Snips NLU]: https://github.com/snipsco/snips-nlu
[Discord app]: https://discordapp.com/developers/applications
[AFL-3.0]: https://gitlab.com/ObserverOfTime/filmaster/-/blob/master/LICENSE.md
