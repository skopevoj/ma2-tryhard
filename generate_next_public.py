#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import random
import re

def collect_all_questions(src_questions_dir: Path):
    """Collect questions from ./questions similar to generate.py (keeps math processing)."""
    questions = []
    # helper: add \displaystyle in inline math that contains \int (skip $$...$$)
    def process_math_inline(text: str) -> str:
        if not text:
            return text
        pattern = re.compile(r'(\$\$.*?\$\$)|(\$.*?\$)|\\\((?:.|\n)*?\\\)', re.DOTALL)
        def repl(m):
            s = m.group(0)
            if s.startswith('$$'):
                return s
            if s.startswith('$') and s.endswith('$'):
                inner = s[1:-1]
                if '\\int' in inner and '\\displaystyle' not in inner:
                    return '$' + '\\displaystyle ' + inner + '$'
                return s
            if s.startswith('\\(') and s.endswith('\\)'):
                inner = s[2:-2]
                if '\\int' in inner and '\\displaystyle' not in inner:
                    return '\\(' + '\\displaystyle ' + inner + '\\)'
                return s
            return s
        return pattern.sub(repl, text)

    if not src_questions_dir.exists():
        return questions

    for folder in sorted(src_questions_dir.iterdir()):
        if not folder.is_dir():
            continue
        json_file = folder / "quiz_data.json"
        if not json_file.exists():
            continue
        data = json.loads(json_file.read_text(encoding='utf-8'))
        quiz_id = data.get('id')
        for question in data.get('questions', []):
            # find first image file in folder
            image_file = next((f for f in folder.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}), None)
            q_text = question.get('question', '')
            question['question'] = process_math_inline(q_text)
            for ans in question.get('answers', []):
                ans_text = ans.get('text', '')
                ans['text'] = process_math_inline(ans_text)
            question['image_src'] = f"images/{folder.name}/{image_file.name}" if image_file else None
            question['source_folder'] = folder.name
            question['quiz_id'] = str(quiz_id) if quiz_id is not None else folder.name
            questions.append(question)
    return questions

def build_next_public(out_public_dir: Path, src_questions_dir: Path):
    """Create public/questions.json and copy images into public/images/*"""
    out_public_dir.mkdir(parents=True, exist_ok=True)
    images_out = out_public_dir / "images"
    if images_out.exists():
        shutil.rmtree(images_out)
    images_out.mkdir(parents=True, exist_ok=True)

    questions = collect_all_questions(src_questions_dir)
    # shuffle for variety
    random.shuffle(questions)

    # copy images per folder
    for folder in sorted(src_questions_dir.iterdir()):
        if not folder.is_dir():
            continue
        dest = images_out / folder.name
        dest.mkdir(parents=True, exist_ok=True)
        for file in folder.iterdir():
            if file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}:
                shutil.copy2(file, dest / file.name)

    # write questions.json to public
    out_file = out_public_dir / "questions.json"
    out_file.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote {len(questions)} questions to {out_file}")
    print(f"Copied images to {images_out}")

def main():
    repo_root = Path(__file__).resolve().parent  # .../ma2/ma2
    src_questions = repo_root / "questions"
    next_public = repo_root / "nextjs" / "public"
    build_next_public(next_public, src_questions)

if __name__ == "__main__":
    main()
