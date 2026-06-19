def fix_syntax_again():
    with open("app.py", "r") as f:
        content = f.read()
    
    # We replace the problematic line with a cleaner version using a local variable to avoid any quote/escape issues.
    old_line = 'reply = ask_langchain(ga["context_str"] + f"\\n\\nAI Summary: {ga[\\"ai_summary\\"]}", "", prompt)'
    new_line = "                            ai_summ = ga['ai_summary']\n                            reply = ask_langchain(ga['context_str'] + f'\\n\\nAI Summary: {ai_summ}', '', prompt)"
    
    content = content.replace(old_line, new_line)
    
    with open("app.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix_syntax_again()
