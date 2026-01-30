from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# ...

response = await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Қазақша қысқа, пайдалы жауап бер."},
        {"role": "user", "content": user_text},
    ],
    temperature=0.5,
)
answer = response.choices[0].message.content
