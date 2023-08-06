# Film Master

A Discord bot written with [Snips NLU][]
that posts film info via the [TMDB API][].

### Setup

Create a [Discord app][] for the bot and invite it to your server.

Generate a [TMDB API][] key for the bot.

Install the package and run the bot:

```sh
$ pip install filmaster
$ filmaster -d "DISCORD_TOKEN" -t "TMDB_API_KEY"
```

Or, you can use the Docker image:

```sh
$ docker pull registry.gitlab.com/observeroftime/filmaster:latest
$ docker run filmaster -d "DISCORD_TOKEN" -t "TMDB_API_KEY"
```

In both cases, the bot command requires these parameters:

* `DISCORD_TOKEN`: The bot token of the app you created earlier.
* `TMDB_API_KEY`: The TMDB API key you generated earlier.

You may also pass the following options:

* `-p PREFIX`: Sets the command prefix of the bot. (defaults to `$`)
* `-v`: Increases the verbosity of the logs. Can be passed up to 4 times.

### Examples

#### Greetings

![greeting](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/greeting.png)

#### Help

![help](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/help.png)

#### Film info

![info-1](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/info-1.png)

![info-2](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/info-2.png)

![director](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/director.png)

![actor](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/actor.png)

#### Film cast

![cast-1](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/cast-1.png)

![cast-2](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/cast-2.png)

### Goodbye

![goodbye](https://gitlab.com/ObserverOfTime/filmaster/-/raw/master/.examples/goodbye.png)

### License

> Licensed under the [Academic Free License version 3.0][AFL-3.0]


[TMDB API]: https://developers.themoviedb.org/3/
[Snips NLU]: https://github.com/snipsco/snips-nlu
[Discord app]: https://discordapp.com/developers/applications
[AFL-3.0]: https://gitlab.com/ObserverOfTime/filmaster/-/blob/master/LICENSE.md
