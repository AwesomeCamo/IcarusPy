
# ICARUS RESULTS BOT

A project to automatically gather race results for a pre-defined list of iRacing users and send notifications to a specified discord channel.




## Prerequisites

- Create a discord bot and add it to the server you want it to function on
- Install mysql and make sure it's running on your machine
## Run Locally


Clone the project

```bash
  git clone git@github.com:AwesomeCamo/IcarusPy.git
```

Go to the project directory and create .env file with variables as described in Environment Variables

```bash
  cd IcarusPy
```

Install dependencies

```bash
  pip install -r requirements.txt
```


The first time you start the program you need to run the file that creates your database and tables. Not needed on further program starts

```bash
  python3 db_creator.py
```

Then start the program with

```bash
  python3 icarus_bot.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DISCORD_TOKEN`

`DISCORD_CHANNEL_ID`

`DATABASE_PASSWORD`




## Authors

- Marco Schmitz - [@AwesomeCamo](https://www.github.com/AwesomeCamo)

