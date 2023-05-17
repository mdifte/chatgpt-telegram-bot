import logging
import os
import config
from openai_helper import OpenAIHelper, default_max_tokens
from telegram_bot import ChatGPTTelegramBot


def main():
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [value for value in required_values if getattr(config, value, None) is None]
    if len(missing_values) > 0:
        logging.error(f'The following environment values are missing in your config: {", ".join(missing_values)}')
        exit(1)

    # Setup configurations
    model = getattr(config, 'OPENAI_MODEL', 'gpt-3.5-turbo')
    max_tokens_default = default_max_tokens(model=model)
    openai_config = {
        'api_key': config.OPENAI_API_KEY,
        'show_usage': getattr(config, 'SHOW_USAGE', False),
        'stream': getattr(config, 'STREAM', True),
        'proxy': getattr(config, 'PROXY', None),
        'max_history_size': getattr(config, 'MAX_HISTORY_SIZE', 15),
        'max_conversation_age_minutes': getattr(config, 'MAX_CONVERSATION_AGE_MINUTES', 180),
        'assistant_prompt': getattr(config, 'ASSISTANT_PROMPT', 'You are a helpful assistant.'),
        'max_tokens': getattr(config, 'MAX_TOKENS', max_tokens_default),
        'n_choices': getattr(config, 'N_CHOICES', 1),
        'temperature': getattr(config, 'TEMPERATURE', 1.0),
        'image_size': getattr(config, 'IMAGE_SIZE', '512x512'),
        'model': model,
        'presence_penalty': getattr(config, 'PRESENCE_PENALTY', 0.0),
        'frequency_penalty': getattr(config, 'FREQUENCY_PENALTY', 0.0),
        'bot_language': getattr(config, 'BOT_LANGUAGE', 'en'),
    }

    telegram_config = {
        'token': config.TELEGRAM_BOT_TOKEN,
        'admin_user_ids': ",".join(getattr(config, 'ADMIN_USER_IDS', [])),
        'allowed_user_ids': "*",
        'mandatory_channel_id': config.MANDATORY_CHANNEL_ID,
        'mandatory_channel_link': config.MANDATORY_CHANNEL_LINK,
        'enable_quoting': getattr(config, 'ENABLE_QUOTING', True),
        'enable_image_generation': getattr(config, 'ENABLE_IMAGE_GENERATION', True),
        'enable_transcription': getattr(config, 'ENABLE_TRANSCRIPTION', True),
        'budget_period': getattr(config, 'BUDGET_PERIOD', 'monthly'),
        'user_budgets': getattr(config, 'USER_BUDGETS', '*'),
        'guest_budget': getattr(config, 'GUEST_BUDGET', 100.0),
        'stream': getattr(config, 'STREAM', True),
        'proxy': getattr(config, 'PROXY', None),
        'voice_reply_transcript': getattr(config, 'VOICE_REPLY_WITH_TRANSCRIPT_ONLY', False),
        'voice_reply_prompts': getattr(config, 'VOICE_REPLY_PROMPTS', '').split(';'),
        'ignore_group_transcriptions': getattr(config, 'IGNORE_GROUP_TRANSCRIPTIONS', True),
        'group_trigger_keyword': getattr(config, 'GROUP_TRIGGER_KEYWORD', ''),
        'token_price': getattr(config, 'TOKEN_PRICE', 0.002),
        'image_prices': [float(i) for i in getattr(config, 'IMAGE_PRICES', "0.016,0.018,0.02").split(",")],
        'transcription_price': getattr(config, 'TRANSCRIPTION_PRICE', 0.006),
        'bot_language': getattr(config, 'BOT_LANGUAGE', 'en'),
    }
    print(telegram_config)
    # Setup and run ChatGPT and Telegram bot
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = ChatGPTTelegramBot(config=telegram_config, openai=openai_helper)
    telegram_bot.run()

if __name__ == "__main__":
    main()

