from pathlib import Path

def load_knowledge():

    knowledge_dir = Path("knowledge")

    texts = []

    for file in knowledge_dir.glob("*.txt"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            texts.append(f.read())

    return "\n\n".join(texts)