import tiktoken

with open("transcription.txt", "r") as f:
    text = f.read()

encoding = tiktoken.encoding_for_model("gpt-4-0125-preview")

result = encoding.encode(text)

print(len(result))
