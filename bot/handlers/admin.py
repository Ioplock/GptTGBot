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

@router.message(Command("admin"))
async def admin_login(message: Message):
    await message.answer("Enter admin password:")
    ADMIN_STATE[message.from_user.id] = AdminStates.AWAITING_PASSWORD

@router.message()
async def admin_password_check(message: Message):
    user_id = message.from_user.id
    if ADMIN_STATE.get(user_id) == AdminStates.AWAITING_PASSWORD:
        if message.text == ADMIN_PASSWORD:
            ADMIN_STATE[user_id] = AdminStates.AUTHENTICATED
            await message.answer("Welcome to the admin panel.", reply_markup=admin_menu_kb())
        else:
            await message.answer("Incorrect password. Try again.")
            del ADMIN_STATE[user_id]

@router.callback_query(lambda c: c.data == "admin_menu")
async def admin_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Welcome to the admin panel.", reply_markup=admin_menu_kb())

@router.callback_query(lambda c: c.data == "model_management")
async def model_management(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Model Management:", reply_markup=model_management_kb())

@router.callback_query(lambda c: c.data == "add_model")
async def add_model(callback_query: CallbackQuery):
    await callback_query.message.answer("Enter the name of the new model:")
    ADMIN_STATE[callback_query.from_user.id] = AdminStates.AWAITING_MODEL_NAME

@router.message()
async def save_new_model(message: Message):
    if ADMIN_STATE.get(message.from_user.id) == AdminStates.AWAITING_MODEL_NAME:
        model_name = message.text.strip()
        new_model = Model(name=model_name)
        session.add(new_model)
        session.commit()
        await message.answer(f"Model '{model_name}' added successfully.", reply_markup=admin_menu_kb())
        ADMIN_STATE[message.from_user.id] = AdminStates.AUTHENTICATED

@router.callback_query(lambda c: c.data == "list_models")
async def list_models(callback_query: CallbackQuery):
    models = session.query(Model).all()
    if models:
        model_list = "\n".join([f"{model.id}: {model.name}" for model in models])
        await callback_query.message.edit_text(f"Available Models:\n{model_list}", reply_markup=model_management_kb())
    else:
        await callback_query.message.edit_text("No models available.", reply_markup=model_management_kb())

@router.callback_query(lambda c: c.data == "remove_model")
async def remove_model(callback_query: CallbackQuery):
    await callback_query.message.answer("Enter the ID of the model to remove:")
    ADMIN_STATE[callback_query.from_user.id] = 'awaiting_model_removal'

@router.message()
async def delete_model(message: Message):
    if ADMIN_STATE.get(message.from_user.id) == 'awaiting_model_removal':
        model_id = message.text.strip()
        model = session.query(Model).get(model_id)
        if model:
            session.delete(model)
            session.commit()
            await message.answer(f"Model '{model.name}' removed successfully.", reply_markup=admin_menu_kb())
        else:
            await message.answer("Model not found.", reply_markup=admin_menu_kb())
        ADMIN_STATE[message.from_user.id] = AdminStates.AUTHENTICATED

@router.callback_query(lambda c: c.data == "prompt_management")
async def prompt_management(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Prompt Management:", reply_markup=prompt_management_kb())

@router.callback_query(lambda c: c.data == "add_prompt")
async def add_prompt(callback_query: CallbackQuery):
    await callback_query.message.answer("Enter the text of the new prompt:")
    ADMIN_STATE[callback_query.from_user.id] = AdminStates.AWAITING_PROMPT_TEXT

@router.message()
async def save_new_prompt(message: Message):
    if ADMIN_STATE.get(message.from_user.id) == AdminStates.AWAITING_PROMPT_TEXT:
        prompt_text = message.text.strip()
        new_prompt = Prompt(text=prompt_text)
        session.add(new_prompt)
        session.commit()
        await message.answer("Prompt added successfully.", reply_markup=admin_menu_kb())
        ADMIN_STATE[message.from_user.id] = AdminStates.AUTHENTICATED

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
    await callback_query.message.answer("Enter the ID of the prompt to remove:")
    ADMIN_STATE[callback_query.from_user.id] = 'awaiting_prompt_removal'

@router.message()
async def delete_prompt(message: Message):
    if ADMIN_STATE.get(message.from_user.id) == 'awaiting_prompt_removal':
        prompt_id = message.text.strip()
        prompt = session.query(Prompt).get(prompt_id)
        if prompt:
            session.delete(prompt)
            session.commit()
            await message.answer("Prompt removed successfully.", reply_markup=admin_menu_kb())
        else:
            await message.answer("Prompt not found.", reply_markup=admin_menu_kb())
        ADMIN_STATE[message.from_user.id] = AdminStates.AUTHENTICATED
