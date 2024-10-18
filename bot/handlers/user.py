from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_kb import user_menu_kb, model_selection_kb, prompt_selection_kb
from bot.models.database import User, Model, Prompt, session
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

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = session.get(User, message.from_user.id)
    if not user:
        user = User(id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
    await message.answer("Welcome to GPT Bot!", reply_markup=user_menu_kb())
    USER_STATE[message.from_user.id] = {}

@router.message(lambda message: message.text == "Select Model")
async def select_model(message: Message):
    user = session.get(User, message.from_user.id)
    models = user.models
    if not models:
        await message.answer("You have no models assigned. Please contact admin.")
        return
    kb = model_selection_kb(models)
    await message.answer("Select a model:", reply_markup=kb)
    USER_STATE[message.from_user.id]['state'] = UserStates.SELECTING_MODEL

@router.callback_query(lambda c: c.data.startswith('model_'))
async def model_selected(callback_query: CallbackQuery):
    model_id = int(callback_query.data.split('_')[1])
    model = session.query(Model).get(model_id)
    USER_STATE[callback_query.from_user.id]['model'] = model.name
    await callback_query.message.answer(f"Model '{model.name}' selected.", reply_markup=user_menu_kb())
    await callback_query.answer()

@router.message(lambda message: message.text == "Select Prompt")
async def select_prompt(message: Message):
    user = session.get(User, message.from_user.id)
    prompts = user.prompts
    if not prompts:
        await message.answer("You have no prompts assigned. Please contact admin.")
        return
    kb = prompt_selection_kb(prompts)
    await message.answer("Select a prompt:", reply_markup=kb)
    USER_STATE[message.from_user.id]['state'] = UserStates.SELECTING_PROMPT

@router.callback_query(lambda c: c.data.startswith('prompt_'))
async def prompt_selected(callback_query: CallbackQuery):
    prompt_id = int(callback_query.data.split('_')[1])
    prompt = session.query(Prompt).get(prompt_id)
    USER_STATE[callback_query.from_user.id]['prompt'] = prompt.text
    await callback_query.message.answer("Prompt selected.", reply_markup=user_menu_kb())
    await callback_query.answer()

@router.message(lambda message: message.text == "Keep Context")
async def keep_context(message: Message):
    user_id = message.from_user.id
    USER_STATE[user_id]['keep_context'] = True
    await message.answer("Context will be kept for this conversation.", reply_markup=user_menu_kb())

@router.message(lambda message: message.text == "View Stats")
async def view_stats(message: Message):
    # Implement stats retrieval (e.g., request count, token usage)
    await message.answer("Your stats: [Placeholder for stats]", reply_markup=user_menu_kb())

@router.message(lambda message: True)
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

# Reset context when user selects new model or prompt
@router.message(lambda message: message.text == "Select Model" or message.text == "Select Prompt")
async def reset_context(message: Message):
    USER_STATE[message.from_user.id]['conversation'] = []
