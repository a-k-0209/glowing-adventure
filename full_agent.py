import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool
import streamlit as st

load_dotenv()
st.set_page_config(page_title="Agent", page_icon="🤖")

calculator = CalculatorTool()
translator = TranslatorTool()

tools = [calculator, translator]

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set. Please set it in your environment or .env file.")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=API_KEY)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are a helpful AI agent. Follow these rules strictly:

        1. Always think step-by-step and explain in a clear numbered list.
        2. For "why" or "how" questions → provide a logical step-by-step explanation.
        3. For "which" or "what" questions → reason briefly, then give the final answer.
        4. If the user asks for any mathematical calculations or mathematical questions, you must use the 'calculator' tool and don't elaborate. 
        If the calculator tool cannot solve an math question, politely refuse.
        5. If the user asks for any translation from one language to other, use the 'translator' tool and don't elaborate.
        If you cannot translate further using 'translator' tool, politely refuse
        6. Keep answers concise, structured, and easy to read.

        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)


def main():
    st.title("Level 3 Full Agent")
     
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Your Message")

    if user_input is not None and user_input != "":
        st.session_state.chat_history.append({"role": "Human", "content": user_input})

        with st.chat_message("Human"):
            st.markdown(user_input)

        try:
            if user_input.lower() in {"exit", "quit"}:
                response = "Bye!"
            else:
                response = agent_executor.invoke({'input': user_input})["output"]
        except ValueError:
            response = "The agent does not have a response. Please try again."

        st.session_state.chat_history.append({"role": "AI", "content": response})

        with st.chat_message("AI"):
            st.markdown(response)

if __name__ == "__main__":
    main()

