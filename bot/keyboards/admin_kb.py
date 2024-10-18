from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Model Management", callback_data="model_management"),
            InlineKeyboardButton(text="Prompt Management", callback_data="prompt_management")
        ],
        [
            InlineKeyboardButton(text="User Stats", callback_data="user_stats"),
            InlineKeyboardButton(text="Specific User Stats", callback_data="specific_user_stats")
        ],
        [
            InlineKeyboardButton(text="User Access Management", callback_data="user_access")
        ]
    ])
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
