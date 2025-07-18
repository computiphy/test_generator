import os
import pandas as pd
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import ollama
from src.registry_matcher import match_step_to_function
from mdextractor import extract_md_blocks  # your existing markdown code extractor

class TestScriptGenerator:
    def __init__(self, template_dir="src/templates", model_name="qwen2.5-coder:3b"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("pytest_case.jinja2")
        self.model = model_name

    def generate_scripts_from_csv(self, csv_path: Path, output_dir: Path):
        df = pd.read_csv(csv_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        if 'Test Steps' not in df.columns:
            raise Exception("CSV must contain a 'Test Steps' column.")

        for index, row in df.iterrows():
            test_title = row.get("Test Case Title", f"Test_{index+1}").replace(" ", "_").lower()
            test_step = row['Test Steps']
            match_suggestions = match_step_to_function(test_step, top_k=3)

            prompt = self._build_prompt(test_step, match_suggestions)
            response = ollama.chat(model=self.model, messages=prompt)

            code_md = response['message']['content']
            try:
                code = extract_md_blocks(code_md)[0]
            except:
                code = code_md  # fallback if not markdown-wrapped

            test_filename = f"test_{index + 1:03}_{test_title}.py"
            with open(output_dir / test_filename, 'w', encoding='utf-8') as f:
                f.write(code)

            print(f"✅ Generated: {output_dir / test_filename}")

    def _build_prompt(self, test_step: str, function_suggestions: list[str]):
        suggestions = "\n".join(function_suggestions)
        user_prompt = f"""
Write a Python program using pytest based on the following test step.

Test Step:
{test_step}

You may use any of the following predefined firmware functions:
{suggestions}

Please structure the output as an executable pytest script.
Respond with only valid Python code.
        """.strip()

        sys_prompt = """
You are a Python developer writing pytest-based test scripts.
Only respond with correct, syntax-valid code. No explanations or markdown.
        """.strip()

        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
