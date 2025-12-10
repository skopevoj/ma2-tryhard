import os
import json
import google.generativeai as genai
from pathlib import Path
from PIL import Image

# Configure the API key (set your API key as environment variable)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Use Gemini 1.5 Pro for best image understanding
model = genai.GenerativeModel('gemini-2.5-flash')

def process_quiz_image(image_path):
    """Process a single quiz image and extract structured data."""
    
    # Load the image
    img = Image.open(image_path)
    
    # Create a detailed prompt for the AI
    prompt = """
    Analyze this math quiz image and extract all information in a structured format.
    
    IMPORTANT: This is a multiple-choice quiz where ONE question has FOUR answer options.
    Do NOT create separate questions for each answer option.
    Do NOT use generic "True"/"False" as answer text.
    
    For the question in the image:
    1. Extract the MAIN question text (the header/instruction text)
    2. Transcribe ALL FOUR answer options exactly as they appear in the image
    3. Each answer option should contain the full text with proper LaTeX notation
    4. Use LaTeX syntax (e.g., $x^2$, \\frac{a}{b}, \\sqrt{x}$, etc.) for all math
    5. Identify which answers are marked as correct (checked/selected) in the image
    6. Assign the most appropriate category from this list:
       - Neurčitý integrál a primitivní funkce
       - Určitý integrál
       - Číselné a mocninné řady
       - Taylorovy polynomy, řady a věta
       - Lineární rekurentní rovnice
       - Diferenciální počet funkcí více proměnných
    
    CRITICAL - LaTeX Escaping Rules:
    - In JSON strings, backslashes MUST be escaped
    - Greek letters: \\alpha, \\beta, \\gamma, \\varphi, \\phi, \\theta, etc.
    - Operators: \\int, \\sum, \\prod, \\frac, \\sqrt, \\operatorname, etc.
    - ALWAYS use double backslash in JSON: "\\varphi" NOT "\varphi"
    
    EXAMPLE of CORRECT JSON format:
    {
        "question": "Nechť $F$ je primitivní funkcí k funkci $f$ na intervalu $(a, b)$, $\\varphi$ je na intervalu $(\\alpha, \\beta)$ diferencovatelná.",
        "answers": [
            {"text": "$F(\\varphi(x))$ je primitivní funkcí k $f(\\varphi(x))\\varphi'(x)$ na $(\\alpha, \\beta)$.", "correct": true}
        ]
    }
    
    WRONG - Single backslash (will break JSON):
    {"text": "$F(\varphi(x))$"}
    
    CORRECT - Double backslash in JSON:
    {"text": "$F(\\varphi(x))$"}
    
    Return ONLY valid JSON in this exact format:
    {
        "questions": [
            {
                "question": "The main question text with $LaTeX$ math notation",
                "category": "One of the categories from the list above",
                "answers": [
                    {"text": "Full text of answer option 1 with $LaTeX$", "correct": true},
                    {"text": "Full text of answer option 2 with $LaTeX$", "correct": false},
                    {"text": "Full text of answer option 3 with $LaTeX$", "correct": false},
                    {"text": "Full text of answer option 4 with $LaTeX$", "correct": true}
                ]
            }
        ]
    }
    
    Make sure:
    - There is exactly ONE question object in the "questions" array
    - The question has exactly FOUR answer objects
    - Each answer contains the full mathematical expression or statement
    - All mathematical notation is properly formatted in LaTeX with DOUBLE backslashes in JSON
    - Greek letters like \\alpha, \\beta, \\varphi MUST have double backslashes
    """
    
    # Generate content with the image
    response = model.generate_content([prompt, img])
    
    return response.text

def extract_json_from_response(response_text):
    """Extract and parse JSON from AI response."""
    # Remove markdown code blocks if present
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    # Try to parse, if it fails due to escape sequences, try to fix them
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  JSON decode error: {e}")
        print(f"  Attempting to fix escape sequences...")
        # Replace single backslashes with double backslashes for LaTeX
        # But be careful not to double-escape already escaped sequences
        import re
        # This regex finds backslashes that aren't already escaped
        text = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', text)
        try:
            return json.loads(text)
        except json.JSONDecodeError as e2:
            print(f"  Still failed after fix: {e2}")
            print(f"  Response text sample: {text[:500]}...")
            raise

def main():
    # Define paths
    quiz_folder = Path("./quiz")
    output_base = Path("./output")
    output_base.mkdir(exist_ok=True)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_files = [f for f in quiz_folder.iterdir() 
                   if f.suffix.lower() in image_extensions]
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    for idx, image_path in enumerate(image_files, 1):
        print(f"\nProcessing {idx}/{len(image_files)}: {image_path.name}")
        
        try:
            # Create output folder for this image
            folder_name = image_path.stem  # filename without extension
            output_folder = output_base / folder_name
            output_folder.mkdir(exist_ok=True)
            
            # Copy original image to output folder
            import shutil
            shutil.copy2(image_path, output_folder / image_path.name)
            
            # Process the image
            response_text = process_quiz_image(image_path)
            
            # Save raw response for debugging
            with open(output_folder / "raw_response.txt", 'w', encoding='utf-8') as f:
                f.write(response_text)
            
            # Extract and parse JSON
            quiz_data = extract_json_from_response(response_text)
            
            # Save JSON to output folder
            json_path = output_folder / "quiz_data.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Saved to {output_folder}")
            print(f"  Found {len(quiz_data.get('questions', []))} questions")
            
            # Remove the original image from quiz folder after successful processing
            os.remove(image_path)
            print(f"  Removed original from quiz folder")
            
        except Exception as e:
            print(f"✗ Error processing {image_path.name}: {str(e)}")
            import traceback
            traceback.print_exc()
            # Don't remove the image if there was an error
            continue

if __name__ == "__main__":
    main()
