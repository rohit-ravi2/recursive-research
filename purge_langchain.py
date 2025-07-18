import os
import re

PROJECT_ROOT = "."  # Set to '.' assuming you're in the repo root
LANGCHAIN_PATTERNS = [
    r"langchain\..*",
]

REPLACEMENTS = {
    # Replace LLM calls using LangChain with invoke_invoke_llm(prompt)
    r"llm\(.*\)": 'invoke_invoke_llm(prompt)',
}

def clean_file(path):
    with open(path, "r") as f:
        lines = f.readlines()

    original = lines[:]
    lines = [line for line in lines if not any(re.search(p, line) for p in LANGCHAIN_PATTERNS)]

    code = "".join(lines)
    for pattern, repl in REPLACEMENTS.items():
        code = re.sub(pattern, repl, code)

    if code != "".join(original):
        with open(path, "w") as f:
            f.write(code)
        print(f"✅ Cleaned: {path}")

def purge_langchain_code():
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                clean_file(path)

if __name__ == "__main__":
    print("🚫 Purging all LangChain-related code...")
    purge_langchain_code()
    print("🎉 Done.")
