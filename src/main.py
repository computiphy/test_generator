import time

start_time = time.perf_counter()

import json
import pandas as pd
import ollama
from pathlib import Path
import ast
from ollama import Client

ollama.host = "http://127.0.0.1:11434"

client = Client(host=ollama.host)

def read_feature_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_test_plan(feature_description, model_name='qwen2.5-coder:3b', num_of_tests=20):
    sys_prompt = f"""
    You are an expert Firmware Test Engineer specializing in optical communication transceivers. Your primary function is to design comprehensive and effective test cases based on provided documentation and specifications.

    Your Goal: Generate detailed and actionable test cases for the firmware of an optical communication transceiver. These test cases must be specific, measurable, achievable, relevant, and time-bound (SMART).

    Input: You will be provided with a text file containing specifications, requirements
    
    Generation Strategy:

    Read and Understand: Thoroughly read and analyze the provided file. Identify key sections, requirements, and design details.
    Categorize & Prioritize: Group similar information and identify critical areas that require more extensive testing.
    Identify Testable Scenarios: Based on the extracted information, brainstorm various scenarios, including:
        Positive Scenarios: Normal operation, valid inputs.
        Negative Scenarios: Invalid inputs, error conditions, boundary conditions, unexpected events.
        Performance Scenarios: Max/min load, sustained operation.
        Stress Scenarios: Repeated operations, rapid state changes.
        Concurrency Scenarios: Multiple operations simultaneously.
        Recovery Scenarios: Power cycles, hot/cold resets.
        Security Scenarios: Unauthorized access attempts, tampering.
    Decompose and Detail: Break down high-level requirements into smaller, atomic test cases.
    Specify Steps Clearly: Each step should be unambiguous and actionable.
    Define Expected Results Precisely: Avoid vague descriptions. Quantify where possible.

    Constraints & Best Practices:

    Focus on Firmware: While understanding hardware is crucial, the test cases should primarily target the firmware's behavior and responses.
    Avoid Redundancy: Strive for unique test cases.
    Be Specific: Do not generate generic test cases. Every test case should be tailored to the specifics of the optical transceiver firmware.
    Assume Ideal Test Conditions unless otherwise specified.
    Do Not Invent Requirements: Base test cases strictly on the provided Specification File. If the file is incomplete, suggest areas where more information would be beneficial for comprehensive testing.
    """
    
    specifics = f"""

    This following is a description of the  Network path and its state machines and how they can be implemented. 
    Please use the following for writing test plans for Network path state machine and its flow. 

    """

    specifics = f"""

    This following is a description of the  Performance Monitoring. 
    Please use the following for writing test plans for Performance Monitoring. 

    """

    prompt = f"""
    Given the following ideas and feature description:

    {specifics}

    \"\"\" 
    {feature_description}
    \"\"\"

    Generate exactly {num_of_tests} test cases. Each test case must include the following keys:
    - "Test Case Title": A concise name.
    - "Test Case Description": A brief explanation.
    - "Test Steps": A list of string steps in order.
    - "Priority": One of ["low", "medium", "high"].
    - "Type": One of ["Positive", "Negative", "Functional", "Non-functional", "Unit Test Cases", "Integration Test Cases", "Performance Test Cases"].

    Output must be a **JSON array** of test cases, with no other text. No explanation, comments, or markdown — only valid JSON.
    """

    response = client.chat(
        model=model_name,
        messages=[
        {"role": "system", "content": f"{sys_prompt}"},
        {"role": "user", "content": prompt}],
        format="json"  # enables structured output mode
    )

    raw_content = response['message']['content']
    print("Raw response:", raw_content)

    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(raw_content)
        except Exception as e:
            print("Failed to parse test cases.")
            raise e


def convert_to_dataframe(test_cases):
    rows = []
    for idx, test in enumerate(next(iter(test_cases.values())), start=1):
        steps = test['Test Steps']
        if isinstance(steps, list):
            steps = '\n'.join(str(step) if isinstance(step, str) else json.dumps(step) for step in steps)
        rows.append({
            'Test Case Number': idx,
            'Test Case Title': test['Test Case Title'],
            'Test Case Description': test['Test Case Description'],
            'Test Steps': steps,
            'Priority': test['Priority'].capitalize(),
            "Type": test['Type']
        })
    return pd.DataFrame(rows)

def save_to_spreadsheet(df, output_file):
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        print("Please give a .csv file name")

def main():
    input_file = 'cmis\OIF-CMIS-05.2-PM.md'
    output_file = f'generated_test_plan/generated_test_plan{start_time}.csv'  # Output file path

    if not Path(input_file).exists():
        print(f"Input file '{input_file}' not found.")
        return

    print("Reading feature description...")
    feature_text = read_feature_description(input_file)

    print("Generating test plan using Ollama...")
    test_cases = generate_test_plan(feature_text)

    print("Converting test cases to DataFrame...")
    df = convert_to_dataframe(test_cases)

    print(f"Saving to spreadsheet: {output_file}")
    save_to_spreadsheet(df, output_file)
    print("Done!")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

if __name__ == '__main__':
    main()
