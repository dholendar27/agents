from langgraph.graph import END, START, StateGraph

from agent.nodes import (
    anonymize_email,
    classify_email_node,
    deanonymize_email,
    filtered_email_reply,
    generate_email_reply,
)
from agent.schema import EmailSchema

builder = StateGraph(EmailSchema)


builder.add_node("classify_email", classify_email_node)
builder.add_node("generate_email", generate_email_reply)
builder.add_node("anonymize_email", anonymize_email)
builder.add_node("deanonymize_email", deanonymize_email)
builder.add_edge(START, "anonymize_email")
builder.add_edge("anonymize_email", "classify_email")
builder.add_conditional_edges(
    "classify_email",
    filtered_email_reply,
    {"generate": "generate_email", "stop": END},
)
builder.add_edge("generate_email", "deanonymize_email")
builder.add_edge("deanonymize_email", END)

graph = builder.compile()

# email = """
# Hello John,

# Thank you for contacting the Customer Support Team at ABC Online Store.

# We’re sorry to hear that you experienced an issue with your recent order (#45821). Our team is here to help resolve the problem as quickly as possible.

# To assist you better, could you please provide the following details:

# • A brief description of the issue you encountered
# • Photos or screenshots of the product (if damaged or incorrect)
# • Confirmation of your shipping address

# Once we receive the requested information, our support team will review your case and provide a resolution within 24–48 hours.

# If the item arrived damaged or incorrect, we will gladly arrange either a replacement or a full refund based on your preference.

# Thank you for your patience and for shopping with ABC Online Store. We appreciate your business and look forward to resolving this for you.

# Best regards,
# Emily Carter
# Customer Support Specialist
# ABC Online Store

# Email: [support@abconlinestore.com](mailto:support@abconlinestore.com)
# Phone: +1 (800) 555‑0199
# Support Hours: Monday – Friday, 9:00 AM – 6:00 PM (EST)

# """

# input_schema = EmailSchema(email=email)
# response = graph.invoke(input_schema)
# print(response.get("email_response"))
