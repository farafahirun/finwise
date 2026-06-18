from langchain_service import ask_langchain

result = ask_langchain(
    "Debt Ratio: 0.5",
    "Debt ratio ideal di bawah 0.3",
    "Bagaimana kondisi saya?"
)

print(result)