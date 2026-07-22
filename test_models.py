from google import genai

client = genai.Client(api_key="AQ.Ab8RN6KBrH_-gaG5-wBX2lR1gkfuOIo84oh3WHdqPgBgUEHnrw")

for model in client.models.list():
    print(model.name)
