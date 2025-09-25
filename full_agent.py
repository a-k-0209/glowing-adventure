from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool

calculator = CalculatorTool()
translator = TranslatorTool()


tools = [calculator, translator]


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyBjKb2Gz5FSez_DE5QTLGV3pviAAfpg4io")
    # tools = load_tools("calculator", "translator", "wolframealpha")
prompt_template = PromptTemplate.from_template(
    f"""
You are a helpful AI agent. Follow these rules strictly:

1. Always think step-by-step and explain in a clear numbered list.
2. For "why" or "how" questions → provide a logical step-by-step explanation.
3. For "which" or "what" questions → reason briefly, then give the final answer.
4. If the user asks for any mathematical calculations or mathematical questions, you must use the 'calculator' tool. 
If the calculator tool cannot solve an math question, politely refuse.
5. If the user asks for any translation from one language to other, use the 'translator' tool.
If you cannot translate further using 'translator' tool, politely refuse
6. Keep answers concise, structured, and easy to read.

""")

agent = initialize_agent(
    tools, llm, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

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
            response = agent.run(user_input)
            print("AI:", response)
        except ValueError:
            print("The agent does not have a response. Please try again.")

if __name__ == "__main__":
    main()