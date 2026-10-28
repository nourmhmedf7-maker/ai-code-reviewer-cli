import sys
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_APIKEY"),
    base_url="https://api.groq.com/openai/v1",
)
try:
    with open(sys.argv[1],"r",encoding="utf-8") as f :
        file = f.read()
    print("loading....")
    prompt = f"""
    You are a skilled code reviewer. Your task is to thoroughly review and analyze the project's code, evaluate the project/code out of 10, and identify any potential issues in the code.

    You must return **ONLY** the following sections to the user, using a calm, friendly, and respectful tone:

    1. **Rating (out of 10)**
    2. **Code Issues and Their Solutions** (if any; if there are no issues, explicitly state that the code is free of issues).
    3. **Improvements** (suggestions for improving the code, such as making it more concise or reducing unnecessary lines).

    ### Important Instructions

    **Regarding code issues:**
    By "code issues," we mean problems that could cause programming errors, unexpected behavior, or prevent the program from functioning as intended. After thoroughly analyzing the code and identifying such issues, explain each problem to the user and provide a solution.

    **Strict Output Restrictions:**
    - Do not include any text outside the required sections.
    - Do not deviate from the specified format or section order.
    - Always follow this exact order:
    1. Rating
    2. Code Issues and Their Solutions
    3. Improvements

    **Code Review Process:**
    Do not review all lines of code at once. Instead, review the code **line by line**, carefully analyzing each line before moving to the next. Pay close attention to potential errors, logical flaws, edge cases, and opportunities for improvement.

    ### Required Output Format

    **Rating:** 6/10

    **Code Issues:**
    - **Line 5:** A division-by-zero error may occur.
    - **Solution:** Check that the divisor is not zero before performing the division.

    **Improvements:**
    - Consider replacing multiple lines of repetitive code with a reusable function to reduce duplication and improve maintainability.
    - Use Python's built-in `sum()` function instead of manually adding numbers in a loop when appropriate.


    """
    

    response = client.responses.create(
        model = "openai/gpt-oss-20b",
        instructions = prompt,
        input= [{"role":"user","content":file}],
        stream= True,
        temperature= 0,
        
    )

    for event in response:
        if hasattr(event,"type") and "reasoning_text.delta" in event.type:
            continue

        if hasattr(event,"type") and "output_text.delta" in event.type:
            print(event.delta,end="",flush=True)

except IndexError :
    print("please enter your file name")
except FileNotFoundError :
    print("file not found")
except UnicodeDecodeError :
    print("file")
except openai.AuthenticationError :
    print("Check your API key or token ")
except openai.APIConnectionError :
    print("check your network")




