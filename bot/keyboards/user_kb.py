from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def user_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Keep Context ✅", callback_data="keep_context"),
            ],
            [
            InlineKeyboardButton(text="Select Endpoint", callback_data="select_endpoint"),
            InlineKeyboardButton(text="Enter API key", callback_data="enter_api_key"),
            ],
            [
            InlineKeyboardButton(text="Select Model", callback_data="select_model"),
            InlineKeyboardButton(text="Select Prompt", callback_data="select_prompt"),
            ],
            [
            InlineKeyboardButton(text="View Stats", callback_data="view_stats"),
            ],
    ])
    return kb

def model_selection_kb(models):
    buttons = []
    if models:
        buttons = [[InlineKeyboardButton(model.name, callback_data=f"model_{model.id}")] for model in models]
    buttons.append([InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def prompt_selection_kb(prompts):
    buttons = []
    if prompts:
        buttons = [[InlineKeyboardButton(prompt.text[:20] + "...", callback_data=f"prompt_{prompt.id}")] for prompt in prompts]
    buttons.append([InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def endpoint_selection_kb(endpoints):
    buttons = []
    if endpoints:
        buttons = [[InlineKeyboardButton(endpoint.url[:20] + "...", callback_data=f"endpoint_{endpoint.id}")] for endpoint in endpoints]
    buttons.append([InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def back_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")]])
