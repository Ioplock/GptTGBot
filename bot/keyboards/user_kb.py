from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def user_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Keep Context"),
                KeyboardButton(text="Select Model"),
            ],
            [
                KeyboardButton(text="Select Prompt"),
                KeyboardButton(text="View Stats"),
            ],
        ],
    resize_keyboard=True
    )
    return kb

def model_selection_kb(models):
    buttons = [[InlineKeyboardButton(model.name, callback_data=f"model_{model.id}")] for model in models]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def prompt_selection_kb(prompts):
    buttons = [[InlineKeyboardButton(prompt.text[:20] + "...", callback_data=f"prompt_{prompt.id}")] for prompt in prompts]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb
