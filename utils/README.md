# Professor Flitwick Discord Bot Utils

This directory contains utility files, which have functions to interact with the various services Professor Flitwick uses.

## Discord Utils

The `is_in_guild` function is used to check if the bot command was used in the Dueling server.

## Google Utils

The `create_gspread_client` function creates a client for `gspread`, which allows us to interact with google spreadsheets. It requires the `client_secret.json` file, or environment variables to exist (such as in a `.env` file) with the values required (namely, those specified in the `client_secret.json` file).

## Logging Utils

The `log_command` function gets information about which commands were used, and outputs this information to the `#bot-logs` channel in the Dueling server. Primarily for debugging purposes.

## Reddit Utils

The `create_reddit_client` function creates a client to interact with `Praw`, which is a library enabling us to interface with Reddit using python.
It uses the environment variables from the `.env` file to fill in the client information such as username and password.
