def fix_syntax_error():
    with open("app.py", "r") as f:
        lines = f.readlines()

    with open("app.py", "w") as f:
        for i, line in enumerate(lines):
            # We are looking for the broken f-string
            if "reply = ask_langchain(ga['context_str'] + f\"" in line and not line.strip().endswith(')'):
                # The next lines are probably:
                # 
                # AI Summary: {ga['ai_summary']}\", \"\", prompt)
                pass # skip writing this broken line, we will write it fixed
            elif "AI Summary:" in line and "prompt)" in line:
                # We found the end of the broken statement, write the fixed one
                f.write('                            reply = ask_langchain(ga["context_str"] + f"\\n\\nAI Summary: {ga[\\"ai_summary\\"]}", "", prompt)\n')
            else:
                f.write(line)

if __name__ == "__main__":
    fix_syntax_error()
