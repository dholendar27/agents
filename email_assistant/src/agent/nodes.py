import json

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from pydantic import EmailStr

from agent.llm import model
from agent.schema import EmailSchema
from agent.util import convert_response_to_json


def classify_email_node(state: EmailSchema):
    classifier_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
    You are an email classification assistant.

    Your task is to analyze the given email and classify it into one of the following categories:

    Categories:
    1. Work / Business
    2. Personal
    3. Spam / Marketing
    4. Finance / Billing
    5. Support / Customer Service
    6. Notifications / Alerts
    7. Promotions / Offers
    8. Other

    Instructions:
    - Read the email subject and body carefully.
    - Choose the single most appropriate category.
    - If the email contains advertisements, sales offers, or marketing content, classify it as "Spam / Marketing" or "Promotions / Offers".
    - If the email relates to payments, invoices, receipts, or banking, classify it as "Finance / Billing".
    - If it relates to a work task, meeting, or business communication, classify it as "Work / Business".
    - If none of the categories fit clearly, classify it as "Other".

    Return ONLY valid JSON in this format:

    {{
      "category": "<category_name>",
      "confidence": "<low | medium | high>",
      "reason": "<short explanation>",
      "tone": <tone_of_email>
    }}
    """,
            ),
            (
                "human",
                """
    Email to classify:
    {email}
    """,
            ),
        ]
    )
    messages = classifier_prompt.format_messages(email=state.masked_email)
    response = model.invoke(messages)
    response_dict = convert_response_to_json(response.content)
    return {
        "messages": state.messages + [("ai", response.content)],
        "email_category": response_dict["category"],
        "email_tone": response_dict["tone"],
    }


def filtered_email_reply(state: EmailSchema):
    filtered_email_types = [
        "Spam / Marketing",
        "Promotions / Offers",
        "Notifications / Alerts",
    ]
    if not state.email_category in filtered_email_types:
        return "generate"
    return "stop"


def generate_email_reply(state: EmailSchema):
    email_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert email writer. Read the email below carefully and draft a professional,
                polite, and concise reply. Make sure your response addresses all key points,
                maintains a courteous tone, and includes any necessary follow-up questions or actions.
                Keep the response clear and structured.
                When providing the reply please use the same entities as mentioned in the mail. Don't add any extra characters
                """,
            ),
            (
                "human",
                """
                The original email is:"

                {email}

                "Now, draft the reply email
                """,
            ),
        ]
    )
    messages = email_prompt.format_messages(email=state.masked_email)
    response = model.invoke(messages)
    return {
        "messages": state.messages + [("ai", response.content)],
        "masked_email_response": response.content,
    }


def anonymize_email(state: EmailSchema):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    text = state.email

    # Detect PII
    results = analyzer.analyze(text=text, language="en")
    entities = []
    for r in results:
        value = text[r.start : r.end]
        entities.append(
            {
                "entity": r.entity_type,
                "original_value": value,
                "start": r.start,
                "end": r.end,
            }
        )
    # Anonymize
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    return {"masked_email": anonymized_text.text, "masked_email_entites": entities}


def deanonymize_email(state: EmailSchema):
    text = state.masked_email_response
    entities = state.masked_email_entites

    for entity in entities:
        text = text.replace(f"<{entity['entity']}>", entity["original_value"])

    return {"email_response": text}
