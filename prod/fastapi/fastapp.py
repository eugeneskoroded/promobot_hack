import sys
from inference import *
from entites import *
import warnings
# from transformers import AutoTokenizer, AutoModel
# import torch
from warnings import filterwarnings
from typing import Union
from fastapi import FastAPI, Request, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
import base64
import numpy as np
from tqdm import tqdm
import torch
from transformers import AutoModel, AutoTokenizer, Trainer, TrainingArguments, default_data_collator, DebertaV2Tokenizer, PegasusForConditionalGeneration, PegasusTokenizer
import re
import json
import requests
filterwarnings("ignore")
gpt_url = 'http://gpt_server:8082/ai_answer'

model = Model(embed_dim=1024, num_classes=221, n_layers=1, hidden_dim=1024)
if torch.cuda.is_available():
    model = model.cuda()
model.load_state_dict(torch.load("model/final_model_for_deploying"))
model.eval()

tree = pickle.load(open("model/tree", "rb"))
reversed_mapping = pickle.load(open("model/reversed_mapping", "rb"))

encoder = AutoModel.from_pretrained("sberbank-ai/sbert_large_mt_nlu_ru")
if torch.cuda.is_available():
    encoder = encoder.cuda()
tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/sbert_large_mt_nlu_ru")


def text_cleaner_for_bert(input_text):
    """ Функция, которая выполняет очистку текста от лишних символов """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', input_text)
    rem_url = re.sub(r'http\S+', '', cleantext)
    rem_url = re.sub(r'([a-z]{2}\d+[a-z]{2})', ' ', rem_url)
    rem_url = re.sub(r'!+', '.', rem_url)
    text = re.sub(
        r"[-—()\"#/@;:<>{}=~|€«»$\+'_–\*°“”\\√&×•ó÷≈„()‽\+]+", " ", rem_url)
    text = re.sub("!", ".", text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r"\[.+\]", '', text)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)

    text = emoji_pattern.sub('', text)
    return text


def create_prompt(text):
    prompt = f'''Анализируйте следующий текст сообщения пользователя из социальной сети и найдите все сущности, ограничиваясь списком: номера телефонов, фамилии, имена, отчества, адреса, даты, названия организаций. Формируйте результат в виде JSON, включая только те типы сущностей, которые присутствуют в тексте. Если определённого типа сущностей нет в тексте, их не следует включать в итоговый JSON.\n\nТекст сообщения:\n{text}\n\nОтвет:'''
    return prompt


# FASTAPI
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/send_message")
async def send_message(message: Request):
    data = await message.json()
    message = data["message"]
    ai_assistant = data["withAiAssistant"]
    cleaned_message = text_cleaner_for_bert(message)
    inputs = make_embeddings(encoder, tokenizer, [cleaned_message])
    predictions = make_predict(model, inputs, tree, reversed_mapping)

    print(f"[LOG] Income message: {text_cleaner_for_bert(message)}")

    return_json = \
        {
            "group": predictions[0]["group"],
            "theme": predictions[0]["theme"]
        }
    if ai_assistant:
        try:
            prompt = create_prompt(cleaned_message)
            response = requests.get(
                gpt_url, json={"prompt": prompt}).json()["answer"]
            return_json.update({"description": response})
        except Exception as e:
            print(e)
    print(f"[LOG] Outcome message: {return_json}")
    print(f"[LOG] Ai assistant: {ai_assistant}")
    return return_json
