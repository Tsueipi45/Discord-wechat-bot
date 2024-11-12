# Discord-wechat-bot

This is a Discord bot designed to relay messages between WeChat and Discord. It uses the `wxauto` library to read messages from WeChat and sends them to a designated Discord channel. The bot also includes some interactive commands and a role-based shutdown feature.

## Features

- **WeChat Message Relay**: Automatically retrieves messages from WeChat and sends them to a specified Discord channel.
- **Custom Commands**:
  - `/say`: Repeat a specified message.
  - `/hello`: Responds with "Hello!"
  - `/pat`: Allows users to "pat" another user with a customizable verb.
  - `/shutdown`: Shuts down the bot if the user has the required role.
- **Special Message Responses**: Replies to specific users and keywords with customized responses.

## Requirements

- Python 3.8+
- Dependencies: Install the required libraries using `pip install -r requirements.txt`.

### Required Python Libraries

```bash
pip install discord.py wxauto
```

## Setup

1. **Install Dependencies**: Use the command above to install necessary libraries.
2. **Prepare JSON Configuration**:
   - `settings.json`: Add the following keys in this file:
     ```json
     {
       "TOKEN": "your_discord_bot_token",
       "channel_id": "your_channel_id"
     }
     ```
   - `last_messages.json`: An optional file to store the last WeChat messages retrieved. If the file does not exist, it will be created on the first run.
3. **Run the Bot**:
   - Run the bot using the command:
     ```bash
     python bot.py
     ```

## Bot Commands

- **/say [text]**: The bot will say the text provided by the user. If no text is provided, it will reply with "點點點".
- **/hello**: Replies with "Hello" to greet users.
- **/pat [user] [verb]**: Allows users to "pat" or interact with another user using a customizable verb.
- **/shutdown**: Shuts down the bot if the user has the specified role.

## Inside-jokes
- **on_message**: Listens for messages and responds to certain conditions:
  - Replies to specific users with "出門右轉" based on a random chance.
  - Replies with "出門右轉" if the message ends with "點點點".
- **on_ready**: Indicates the bot is online and begins listening for WeChat messages.

## Configuration Notes

- `channel_id`: ID of the Discord channel where WeChat messages will be sent.
- `role_id` in `/shutdown`: This is the role ID required to shut down the bot.

## Notes on WeChat Integration

The `wxauto` library is used to retrieve messages from WeChat. Ensure that WeChat is open on your desktop when running the bot, as `wxauto` relies on the WeChat desktop application for message access.
