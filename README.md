# Telegram Support Bot

Welcome to the Telegram Support Bot, an interactive bot designed to guide users through a highly customizable menu. With the ability to design menu items, embed images, and lead users through a series of button clicks, the possibilities are vast.

For custom development projects, contact me with contact@tylernorman.com

## Main Features

- **100% Customizable Menu:** Designed to be flexible, adapt the menu to any use case.
- **Image Support:** Showcase visuals with each menu option.
- **Auto Message Deletion:** Keeps the chat tidy by deleting prior bot and user messages.
- **Configurable Callbacks:** Dynamically adapt to each button click.

## Getting Started

### 1. Setting up a Telegram Bot

1. Start a chat with the [BotFather](https://t.me/botfather) on Telegram.
2. Use the `/newbot` command to create a new bot.
3. After choosing a name and username for your bot, BotFather will provide you with a token.
4. Save this token in a `token.txt` file at the root directory of this project.

### 2. Configuring the Bot

All configurations are stored in a `config.json` file, which provides the structure for the menu.

#### Understanding the Config Structure:

- `message`: The message to be displayed for that particular menu.
- `image`: URL of the image to be displayed.
- `buttons`: An array of button objects.
  - `label`: The label of the button.
  - `id`: A unique ID for the button.
  - `line`: Determines the row in which the button should appear.
  - `next_menu`: The next menu to be shown when the button is clicked.

A sample `config.json` is provided with the project. Adjust the parameters as needed.

### 3. Running the Bot

To start the bot, execute the `main.py` file:

```bash
python main.py
```

## Usage

1. Start a chat with your Telegram bot.
2. Use the `/start` command to initialize the bot.
3. Navigate through the menu using the buttons provided.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
