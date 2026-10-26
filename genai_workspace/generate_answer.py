import json


def generate_answer(llm_model, question: str, sql: str, results: str):
    """
    Convert SQL results into a natural-language answer.
    Args:
        llm_model
        question: str -> user question
        sql: str -> executable sql query
        results: str -> query result
    Returns:
        answer: str -> llm's answer for the user question"""

    prompt = f"""
Answer the user's question using the query results and chat history.

User input with chat history:
{question}

SQL executed:
{sql}

Query results:
{json.dumps(results, default=str, indent=2)}

Instructions:
- Explain the results clearly and concisely.
- If we have sql query but don't have query results, answer based on chat history
- Answer based on query results. If query results not provided, answer based on user input and chat history.
- Use previous messages to understand the context of the current question.
- Resolve references such as "it", "that", "this", and "the previous one" using relevant information from the conversation history.
- If the current question depends on previous context, use that context when generating your answer.
"""

    messages=[
                {
                    "role": "system",
                    "content": "You provide appropriate and concise answer to the user's question based only on provided prompt"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
    response = llm_model.invoke(messages)

    return response.content.strip()
