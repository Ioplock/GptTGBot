from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Endpoints Management", callback_data="model_management"),
        ],
        [
            InlineKeyboardButton(text="Models Management", callback_data="model_management"),
            InlineKeyboardButton(text="Prompts Management", callback_data="prompt_management")
        ],
        [
            InlineKeyboardButton(text="Usage Stats", callback_data="usage_stats"),
            InlineKeyboardButton(text="User Stats", callback_data="user_stats")
        ],
        [
            InlineKeyboardButton(text="User Access Management", callback_data="user_access")
        ]
    ])
    return kb

def admin_input_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="back_to_main_menu"),
            InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")
        ]
    ])
    return kb

def user_selection_kb(users):
    buttons = []
    if users:
        buttons = [[InlineKeyboardButton(user.username, callback_data=f"sel_user_{user.id}")] for user in users]
    buttons.append([InlineKeyboardButton(text="◀ Back to menu", callback_data="back_to_main_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def model_management_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add Model", callback_data="add_model"),
            InlineKeyboardButton(text="List Models", callback_data="list_models")
        ],
        [
            InlineKeyboardButton(text="Remove Model", callback_data="remove_model"),
            InlineKeyboardButton(text="Back to Main Menu", callback_data="admin_menu")
        ]
    ])
    return kb

def prompt_management_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add Prompt", callback_data="add_prompt"),
            InlineKeyboardButton(text="List Prompts", callback_data="list_prompts")
        ],
        [
            InlineKeyboardButton(text="Remove Prompt", callback_data="remove_prompt"),
            InlineKeyboardButton(text="Back to Main Menu", callback_data="admin_menu")
        ]
    ])
    return kb

def user_management_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Grant Model Access", callback_data="grant_model_access"),
            InlineKeyboardButton(text="Revoke Model Access", callback_data="revoke_model_access")
        ],
        [
            InlineKeyboardButton(text="Back to Main Menu", callback_data="admin_menu")
        ]
    ])
    return kb
