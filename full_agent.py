from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool




calculator = CalculatorTool()
translator = TranslatorTool()


tools = [calculator, translator]

model = ChatOpenAI(model="gpt-4o-mini")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are a helpful AI agent. Follow these rules strictly:

        1. Always think step-by-step and explain in a clear numbered list.
        2. For "why" or "how" questions → provide a logical step-by-step explanation.
        3. For "which" or "what" questions → reason briefly, then give the final answer.
        4. If the user asks for any mathematical calculations or mathematical questions, you must use the 'calculator' tool. 
        If the calculator tool cannot solve an math question, politely refuse.
        5. If the user asks for any translation from one language to other, use the 'translator' tool.
        If you cannot translate further using 'translator' tool, politely refuse
        6. Keep answers concise, structured, and easy to read.

        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# agent_executor.invoke({"input": query})




    # tools = load_tools("calculator", "translator", "wolframealpha")
# prompt_template = PromptTemplate.from_template(
#     f"""
# You are a helpful AI agent. Follow these rules strictly:

# 1. Always think step-by-step and explain in a clear numbered list.
# 2. For "why" or "how" questions → provide a logical step-by-step explanation.
# 3. For "which" or "what" questions → reason briefly, then give the final answer.
# 4. If the user asks for any mathematical calculations or mathematical questions, you must use the 'calculator' tool. 
# If the calculator tool cannot solve an math question, politely refuse.
# 5. If the user asks for any translation from one language to other, use the 'translator' tool.
# If you cannot translate further using 'translator' tool, politely refuse
# 6. Keep answers concise, structured, and easy to read.

# """)
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful assistant. Respond only in Spanish."),
#         ("human", "{input}"),
#         # Placeholders fill up a **list** of messages
#         ("placeholder", "{agent_scratchpad}"),
#     ]
# )

# agent = initialize_agent(
#     tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
#     )

def main():
    print("Level 3 Gemini Agent. Type 'exit' to exit chat.")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        try:
            response = agent_executor.invoke({'input': user_input})
            print("AI:", response)
        except ValueError:
            print("The agent does not have a response. Please try again.")

if __name__ == "__main__":
    main()