from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import json
import requests
from datetime import datetime
import pytz
# 한국 표준시 (KST) 타임존 가져오기
kst = pytz.timezone('Asia/Seoul')

API_KEY = st.secrets["OpenAI_key"]
client = OpenAI(api_key=API_KEY)
#thread id 를 하나로 관리하기 위함
if 'key' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.key = thread.id

thread_id = st.session_state.key
assistant_id = 'asst_q8c5crZIHLcWVMa59AH2QR4M'
my_assistant = client.beta.assistants.retrieve(assistant_id)
thread_messages = client.beta.threads.messages.list(thread_id,order="asc")

st.header('✨궁피티✨')
st.caption("설악고등학교 선생님들을 위한 인공지능입니다.")
msg = "안녕하세요? 😊✨"
with st.chat_message("assistant", avatar="seoli.png"):
    st.markdown(msg)

if "text_boxes" not in st.session_state:
    st.session_state.text_boxes = []

for msg in thread_messages.data:
    if msg.role == 'assistant':
        with st.chat_message(msg.role, avatar="seoli.png"):
            st.write(msg.content[0].text.value)
    else:
        with st.chat_message(msg.role):
            st.markdown(msg.content[0].text.value)

prompt = st.chat_input("질문해보세요")

if prompt:
  st.chat_message("user").write(prompt)
  with st.chat_message('assistant', avatar="seoli.png"):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    res_box = st.empty()
    report=[]
    stream = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        stream = True
    )
    with st.spinner("..생각중.."):
        for event in stream:
            print(event.data.object)
            if event.data.object == 'thread.message.delta':
                for content in event.data.delta.content:
                    if content.type == 'text':
                        report.append(content.text.value)
                        result = "".join(report).strip()
                        res_box.markdown(f'*{result}*')
                        success = True
        print("야호" + event.data.id)
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=event.data.id
        )
        print(run.status)
