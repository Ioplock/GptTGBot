from sqlalchemy.orm import joinedload

from .database import User, Prompt, Model, APIEndpoint, AccessToken, session

# CREATE operations

def create_user(user_id, username):
    user = User(user_id=user_id, username=username)
    session.add(user)
    session.commit()
    return user

def create_prompt(text, user_ids):
    prompt = Prompt(text=text)
    for user_id in user_ids:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            prompt.users.append(user)
    session.add(prompt)
    session.commit()
    return prompt

def create_model(name, endpoint_id, user_ids):
    model = Model(name=name, endpoint_id=endpoint_id)
    for user_id in user_ids:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            model.users.append(user)
    session.add(model)
    session.commit()
    return model

def create_api_endpoint(url):
    endpoint = APIEndpoint(url=url)
    session.add(endpoint)
    session.commit()
    return endpoint

def create_access_token(token, api_endpoint_id, user_id):
    access_token = AccessToken(token=token, api_endpoint=api_endpoint_id, user_id=user_id)
    session.add(access_token)
    session.commit()
    return access_token

# READ operations

def get_user(user_id):
    return session.query(User).filter_by(user_id=user_id).first()

def get_prompt(prompt_id):
    return session.query(Prompt).filter_by(prompt_id=prompt_id).options(joinedload(Prompt.users)).first()

def get_model(model_id):
    return session.query(Model).filter_by(model_id=model_id).options(joinedload(Model.users)).first()

def get_api_endpoint(endpoint_id):
    return session.query(APIEndpoint).filter_by(endpoint_id=endpoint_id).first()

def get_access_token(token_id):
    return session.query(AccessToken).filter_by(token_id=token_id).first()

# UPDATE operations

def update_user(user_id, new_username):
    user = get_user(user_id)
    if user:
        user.username = new_username
        session.commit()
    return user

def update_prompt(prompt_id, new_text, user_ids):
    prompt = get_prompt(prompt_id)
    if prompt:
        prompt.text = new_text
        prompt.users = []
        for user_id in user_ids:
            user = get_user(user_id)
            if user:
                prompt.users.append(user)
        session.commit()
    return prompt

def update_model(model_id, new_name, new_endpoint_id, user_ids):
    model = get_model(model_id)
    if model:
        model.name = new_name
        model.endpoint_id = new_endpoint_id
        model.users = []
        for user_id in user_ids:
            user = get_user(user_id)
            if user:
                model.users.append(user)
        session.commit()
    return model

def update_api_endpoint(endpoint_id, new_url):
    endpoint = get_api_endpoint(endpoint_id)
    if endpoint:
        endpoint.url = new_url
        session.commit()
    return endpoint

def update_access_token(token_id, new_token, new_api_endpoint_id, new_user_id):
    access_token = get_access_token(token_id)
    if access_token:
        access_token.token = new_token
        access_token.api_endpoint = new_api_endpoint_id
        access_token.user_id = new_user_id
        session.commit()
    return access_token

# DELETE operations

def delete_user(user_id):
    user = get_user(user_id)
    if user:
        session.delete(user)
        session.commit()

def delete_prompt(prompt_id):
    prompt = get_prompt(prompt_id)
    if prompt:
        session.delete(prompt)
        session.commit()

def delete_model(model_id):
    model = get_model(model_id)
    if model:
        session.delete(model)
        session.commit()

def delete_api_endpoint(endpoint_id):
    endpoint = get_api_endpoint(endpoint_id)
    if endpoint:
        session.delete(endpoint)
        session.commit()

def delete_access_token(token_id):
    access_token = get_access_token(token_id)
    if access_token:
        session.delete(access_token)
        session.commit()
