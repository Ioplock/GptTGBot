from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards.admin_kb import admin_menu_kb, model_management_kb, prompt_management_kb, user_management_kb
from bot.models.database import User, Model, Prompt, session
from bot.config import ADMIN_PASSWORD

router = Router()
ADMIN_STATE = {}

# Admin FSM States
class AdminStates:
    AUTHENTICATED = 'authenticated'
    AWAITING_PASSWORD = 'awaiting_password'
    AWAITING_MODEL_NAME = 'awaiting_model_name'
    AWAITING_PROMPT_TEXT = 'awaiting_prompt_text'
    AWAITING_USER_ID = 'awaiting_user_id'
    AWAITING_ACCESS_ACTION = 'awaiting_access_action'

# @router.message(Command("admin"))
# async def admin_login(message: Message):
#     await message.answer("Enter admin password:")
#     ADMIN_STATE[message.from_user.id] = AdminStates.AWAITING_PASSWORD

# @router.message()
@router.message(Command("admin"))
async def admin_password_check(message: Message):
    await message.answer("Welcome to the admin panel.", reply_markup=admin_menu_kb())
    # user_id = message.from_user.id
    # if ADMIN_STATE.get(user_id) == AdminStates.AWAITING_PASSWORD:
    #     if message.text == ADMIN_PASSWORD:
    #         ADMIN_STATE[user_id] = AdminStates.AUTHENTICATED
    #         await message.answer("Welcome to the admin panel.", reply_markup=admin_menu_kb())
    #     else:
    #         await message.answer("Incorrect password. Try again.")
    #         del ADMIN_STATE[user_id]

@router.callback_query(lambda c: c.data == "admin_menu")
async def admin_menu(callback_query: CallbackQuery):
    pass

@router.callback_query(lambda c: c.data == "model_management")
async def model_management(callback_query: CallbackQuery):
    pass

@router.callback_query(lambda c: c.data == "add_model")
async def add_model(callback_query: CallbackQuery):
    pass

@router.message()
async def save_new_model(message: Message):
    pass

@router.callback_query(lambda c: c.data == "list_models")
async def list_models(callback_query: CallbackQuery):
    pass

@router.callback_query(lambda c: c.data == "remove_model")
async def remove_model(callback_query: CallbackQuery):
    pass

# @router.message()
# async def delete_model(message: Message):
#     pass

@router.callback_query(lambda c: c.data == "prompt_management")
async def prompt_management(callback_query: CallbackQuery):
    pass

@router.callback_query(lambda c: c.data == "add_prompt")
async def add_prompt(callback_query: CallbackQuery):
    pass

# @router.message()
# async def save_new_prompt(message: Message):
#     pass

@router.callback_query(lambda c: c.data == "list_prompts")
async def list_prompts(callback_query: CallbackQuery):
    prompts = session.query(Prompt).all()
    if prompts:
        prompt_list = "\n".join([f"{prompt.id}: {prompt.text[:30]}..." for prompt in prompts])
        await callback_query.message.edit_text(f"Available Prompts:\n{prompt_list}", reply_markup=prompt_management_kb())
    else:
        await callback_query.message.edit_text("No prompts available.", reply_markup=prompt_management_kb())

@router.callback_query(lambda c: c.data == "remove_prompt")
async def remove_prompt(callback_query: CallbackQuery):
    pass

# @router.message()
# async def delete_prompt(message: Message):
#     pass
