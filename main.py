import time
from pathlib import Path
from src.config_loader import load_config
from src.test_plan_generator import TestPlanGenerator
from src.test_script_generator import TestScriptGenerator

def main():
    start_time = time.perf_counter()
    config = load_config()
    timestamp = int(start_time)

    input_file = Path("requirement_documents/OIF-CMIS-05.2-PM.md")
    output_folder = Path(f"output/generated_test_plan_{timestamp}")
    output_folder.mkdir(parents=True, exist_ok=True)

    csv_path = output_folder / "generated_test_plan.csv"

    if not input_file.exists():
        print(f"Input file '{input_file}' not found.")
        return

    generator = TestPlanGenerator(config)
    print("📄 Reading feature description...")
    feature_text = generator.read_feature_description(input_file)

    print("🧪 Generating test cases...")
    test_cases = generator.generate_test_plan(feature_text)

    print("📊 Converting to DataFrame...")
    df = generator.convert_to_dataframe(test_cases)

    print(f"💾 Saving test plan to: {csv_path}")
    df.to_csv(csv_path, index=False)

    print("💻 Generating individual test scripts...")
    output_dir = csv_path.parent
    script_gen = TestScriptGenerator()
    script_gen.generate_scripts_from_csv(csv_path, output_dir)

    print("✅ All done!")
    print(f"🗂️ Output Folder: {output_folder.resolve()}")
    print(f"⏱️ Elapsed Time: {time.perf_counter() - start_time:.2f}s")

if __name__ == '__main__':
    main()
