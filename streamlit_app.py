from openai import OpenAI
import streamlit as st

##########################################
## 슬라이드 바
##########################################
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    thread_id = st.text_input("Thread ID")
    st.button("Create net thread")

##########################################
## 채팅 방
##########################################
st.title("💬 파일 업로드 어시스턴트 테스트")
st.caption("성경파일을 업로드하고 그 파일에서만 성경 내용을 찾도록 테스트")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

##########################################
##              Assistants              ##
##########################################

client = OpenAI(api_key = openai_api_key)

file = "file/easy_bible.pdf"

## 1) 파일 업로드
def file_upload(file):
    file = client.file.create(
        file = open(file, "rb"), 
        purpose = "assistnats"
        )
    return file.id

## Step 1) Create an Assistant
def assistant_creator():
    assistant = client.beta.assistants.create(
          name="Math Tutor",
          instructions="You are a personal math tutor. Write and run code to answer math questions.",
          tools=[{"type": "code_interpreter"}],
          model="gpt-4o",
          )
    return assistant
    
## Step 2) Create a Thread
def create_thread():
    thread = client.beta.threads.create()
    return thread

## Step 3) Add a Message to the Thread
def add_message_to_thread():
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
        )
    return message


## Step 4-1) Create a Run - without Streaming
def run_api():
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
        )


## Step 4-2) Create a Run - with Streaming



##########################################
##             Completions              ##
##########################################
# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)


