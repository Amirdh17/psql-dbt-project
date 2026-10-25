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
Answer the user's question using only the database results below.

User question:
{question}

SQL executed:
{sql}

Query results:
{json.dumps(results, default=str, indent=2)}

Instructions:
- Explain the results clearly and concisely.
- If no sql and query results are provided, then assume user's question do not has answer in our hospital db.
- If we have sql query but don't have query results, then assume we don't have relevant data for user's question.
- Do not invent facts that are not present in the results.
- Do not show the following patient related sensitive informations - patient_id, name, first_name, last_name, date_of_birth, phone, zip.
"""

    messages=[
                {
                    "role": "system",
                    "content": "You provide appropriate answer to the user's question based only on provided prompt"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
    response = llm_model.invoke(messages)

    return response.content.strip()
