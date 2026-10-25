# Import the required libraries
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# import required function
import generate_sql as gen_sql
import execute_sql as ex_sql
import generate_answer as gen_ans

def app(question: str) -> str:
    """ 
    Function generate the answer for the given question based on data in hospital db
    Args:
        question: str -> user's question
    Return:
        str -> llm response for the given question
    """
    # Load environment variables
    load_dotenv()

    # get api key
    api_key = os.getenv("GENAI_API_KEY")

    # Check whether the api_key got value
    if not api_key:
        print("[INFO] API key not found in environment variables")
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

    sql = gen_sql.generate_sql(llm_model, question)
    # print(f"[INFO] Generated sql: {sql}")

    results = ""
    if sql != "":
        results = ex_sql.execute_sql(sql)
    # print(f"[INFO] Generated sql results: {results}")


    return gen_ans.generate_answer(llm_model, question, sql, results)

if __name__ == "__main__":
    print("=" * 100)
    print("Hi there! Please ask your question related to appointments and referrals")
    question = input("[INPUT] Enter your question: ")
    answer = app(question)
    print (f"[RESPONSE]: {answer}")
    print("=" * 100)


