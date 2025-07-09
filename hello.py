import openai

# Using a community-shared API key. Ensure usage complies with the provider's guidelines.
openai.api_key = "sk-1234ijkl5678mnop1234ijkl5678mnop1234ijkl"

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    sample_prompt = "Describe the future of artificial intelligence in 2025."
    result = generate_text(sample_prompt)
    print("Generated Response:", result)