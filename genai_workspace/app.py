# Import the required libraries
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

# import required function
import generate_sql as gen_sql
import execute_sql as ex_sql
import generate_answer as gen_ans

# set up LLM model
# Load environment variables
load_dotenv()

# get api key
api_key = os.getenv("GENAI_API_KEY")

# Check whether the api_key got value
if not api_key:
    # print("[INFO] API key not found in environment variables")
    raise
else:
    print("[INFO] API key is successfully loaded!")

try:    
    llm_model = ChatOpenAI(
            model="cohere/north-mini-code:free",  # The specific model name from OpenRouter
            base_url="https://openrouter.ai/api/v1", # OpenRouter's API endpoint
            api_key=api_key,
            temperature=0.2
        )

except Exception as e:
        print(f"[ERROR] Failed while initialize the llm model : {e}")


def app(user_input: str, chat_history: str) -> str:
    """ clea
    Function generate the answer for the given question based on data in hospital db
    Args:
        question: str -> user's question
    Return:
        str -> llm response for the given question
    """
    # Format the prompt with history and current input
    formatted_prompt = prompt.format_messages(
        history=chat_history,
        input=user_input
    )
    
    sql = gen_sql.generate_sql(llm_model, formatted_prompt)
    # print(f"[INFO] Generated sql: {sql}")

    results = ""
    if sql != "":
        results = ex_sql.execute_sql(sql)
    # print(f"[INFO] Generated sql results: {results}")


    return gen_ans.generate_answer(llm_model, formatted_prompt, sql, results)

if __name__ == "__main__":
    print("=" * 100)
    print("Hi there! Please ask your question related to appointments and referrals")
    print("[INFO] Type 'exit' or 'quit' to stop.\n")

    # Define the prompt
    prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ])

    # To store human and ai messages
    chat_history = []

    while True:
        user_input = input("You: ").strip()
        print()

        if user_input.lower() in ["exit", "quit"]:
            print("[INFO] Chat ended.")
            break

        if not user_input:
            continue
        
        response = app(user_input, chat_history)
        
        print(f"AI: {response}\n")

        # Save the current conversation turn
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        # Keep the system message and the latest 5 turns
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]
    
    print("=" * 100)


