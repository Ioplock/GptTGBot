from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_kb import user_menu_kb, model_selection_kb, prompt_selection_kb, endpoint_selection_kb, back_to_menu
from bot.models.database import User, Model, Prompt
from bot.models import crud
from bot.config import OPENAI_API_KEY

import openai

openai.api_key = OPENAI_API_KEY

router = Router()
USER_STATE = {}

# User FSM States
class UserStates:
    SELECTING_MODEL = 'selecting_model'
    SELECTING_PROMPT = 'selecting_prompt'
    IN_CONVERSATION = 'in_conversation'

# @router.message(lambda message: True)
# async def handle_message(message: Message):
#     await message.answer(message.sticker.file_id)

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = crud.get_user(message.from_user.id)
    if not user:
        crud.create_user(message.from_user.id, message.from_user.username)
    await message.answer_sticker("CAACAgEAAxkBAAIBLWcUPgYx1YvjPfK2PJvmzNjkgkq1AAKgBQAC6Ql0JF8pui4vENIBNgQ")
    await message.answer("Welcome to GPT Bot! This bot made by @ioplock, ask them for any help!\nTo start with bot, use /settings command and choose your model and api enpoint.")
    USER_STATE[message.from_user.id] = {}

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    user = crud.get_user(message.from_user.id)
    if not user:
        crud.create_user(message.from_user.id, message.from_user.username)
    await message.answer("Main settings menu:", reply_markup=user_menu_kb())
    USER_STATE[message.from_user.id] = {}

@router.callback_query(lambda c: c.data == "select_model")
async def select_model(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Select model:", reply_markup=model_selection_kb([]))

@router.callback_query(lambda c: c.data == "select_prompt")
async def select_prompt(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Select model:", reply_markup=prompt_selection_kb([]))

@router.callback_query(lambda c: c.data == "select_endpoint")
async def select_endpoint(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Select endpoint:", reply_markup=endpoint_selection_kb([]))

@router.callback_query(lambda c: c.data == "enter_api_key")
async def enter_api_key(callback_query: CallbackQuery):
    await callback_query.message.edit_text("[Placeholder] Enter API Key:", reply_markup=back_to_menu())

@router.callback_query(lambda c: c.data == "view_stats")
async def view_stats(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Your statistics:\n[Placeholder]", reply_markup=back_to_menu())

@router.callback_query(lambda c: c.data == "keep_context")
async def keep_context(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "back_to_main_menu")
async def main_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Main settings menu:", reply_markup=user_menu_kb())

# @router.message(lambda message: message.text == "Select Model")
# async def select_model(message: Message):
#     user = crud.get_user(message.from_user.id)
#     models = user.models
#     if not models:
#         await message.answer("You have no models assigned. Please contact admin.")
#         return
#     kb = model_selection_kb(models)
#     await message.answer("Select a model:", reply_markup=kb)
#     USER_STATE[message.from_user.id]['state'] = UserStates.SELECTING_MODEL

# @router.callback_query(lambda c: c.data.startswith('model_'))
# async def model_selected(callback_query: CallbackQuery):
#     model_id = int(callback_query.data.split('_')[1])
#     model = session.query(Model).get(model_id)
#     USER_STATE[callback_query.from_user.id]['model'] = model.name
#     await callback_query.message.answer(f"Model '{model.name}' selected.", reply_markup=user_menu_kb())
#     await callback_query.answer()

# @router.message(lambda message: message.text == "Select Prompt")
# async def select_prompt(message: Message):
#     user = session.get(User, message.from_user.id)
#     prompts = user.prompts
#     if not prompts:
#         await message.answer("You have no prompts assigned. Please contact admin.")
#         return
#     kb = prompt_selection_kb(prompts)
#     await message.answer("Select a prompt:", reply_markup=kb)
#     USER_STATE[message.from_user.id]['state'] = UserStates.SELECTING_PROMPT

# @router.callback_query(lambda c: c.data.startswith('prompt_'))
# async def prompt_selected(callback_query: CallbackQuery):
#     prompt_id = int(callback_query.data.split('_')[1])
#     prompt = session.query(Prompt).get(prompt_id)
#     USER_STATE[callback_query.from_user.id]['prompt'] = prompt.text
#     await callback_query.message.answer("Prompt selected.", reply_markup=user_menu_kb())
#     await callback_query.answer()

# @router.message(lambda message: message.text == "Keep Context")
# async def keep_context(message: Message):
#     user_id = message.from_user.id
#     USER_STATE[user_id]['keep_context'] = True
#     await message.answer("Context will be kept for this conversation.", reply_markup=user_menu_kb())

# @router.message(lambda message: message.text == "View Stats")
# async def view_stats(message: Message):
#     # Implement stats retrieval (e.g., request count, token usage)
#     await message.answer("Your stats: [Placeholder for stats]", reply_markup=user_menu_kb())

@router.message(~F.text.startswith('/'))
async def handle_user_input(message: Message):
    user_id = message.from_user.id
    state = USER_STATE.get(user_id, {})
    model_name = state.get('model')
    prompt_text = state.get('prompt')
    keep_context = state.get('keep_context', False)
    if not model_name or not prompt_text:
        await message.answer("Please select a model and prompt first.", reply_markup=user_menu_kb())
        return
    if keep_context:
        conversation = state.get('conversation', [])
        conversation.append({'role': 'user', 'content': message.text})
    else:
        conversation = [{'role': 'system', 'content': prompt_text}, {'role': 'user', 'content': message.text}]
    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=conversation
        )
        reply = response['choices'][0]['message']['content']
        await message.answer(reply)
        if keep_context:
            conversation.append({'role': 'assistant', 'content': reply})
            USER_STATE[user_id]['conversation'] = conversation
        else:
            USER_STATE[user_id]['conversation'] = []
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
