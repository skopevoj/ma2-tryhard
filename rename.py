import os
import json
import random
from pathlib import Path

def generate_unique_id(existing_names, used_ids):
    while True:
        num = random.randint(10_000_000, 99_999_999)
        s = str(num)
        if s not in existing_names and s not in used_ids:
            return s

def rename_folders_with_ids():
    questions_dir = Path(__file__).parent / "questions"
    
    if not questions_dir.exists():
        print(f"Error: Questions directory not found at {questions_dir}")
        return
    
    # Collect subdirectories that contain quiz_data.json
    all_folders = [f for f in questions_dir.iterdir() if f.is_dir()]
    target_folders = [f for f in all_folders if (f / "quiz_data.json").exists()]
    # Keep only folders that do NOT already have an 'id' in quiz_data.json
    folders_without_id = []
    for f in target_folders:
        json_file = f / "quiz_data.json"
        try:
            with open(json_file, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
            if 'id' not in data:
                folders_without_id.append(f)
        except Exception:
            # If file cannot be read or parsed, include it for processing
            folders_without_id.append(f)
    target_folders = folders_without_id

    if not target_folders:
        print("No folders with quiz_data.json found in questions directory")
        return
    
    # Build set of existing names to avoid collisions
    existing_names = set(p.name for p in all_folders)
    used_ids = set()
    mappings = []  # (orig_path, id_str)
    
    for folder in sorted(target_folders, key=lambda x: x.name):
        new_id = generate_unique_id(existing_names, used_ids)
        used_ids.add(new_id)
        existing_names.add(new_id)  # reserve the name
        mappings.append((folder, new_id))
    
    print("Planned renames (folder -> 8-digit id):")
    for orig, nid in mappings:
        print(f"  {orig.name} -> {nid}")
    
    resp = input("\nProceed with applying IDs and renaming? (y/n): ").strip().lower()
    if resp != 'y':
        print("Aborted.")
        return
    
    # First pass: rename originals to temporary names to avoid collisions
    temp_prefix = ".renametmp_"
    temp_paths = []
    try:
        for i, (orig, nid) in enumerate(mappings):
            temp_name = questions_dir / f"{temp_prefix}{i}"
            orig.rename(temp_name)
            temp_paths.append((temp_name, nid))
        
        # Second pass: rename temps to final numeric folder names and write id into quiz_data.json
        for temp_path, nid in temp_paths:
            final_path = questions_dir / nid
            # if final_path exists for any reason, abort to avoid clobbering
            if final_path.exists():
                raise FileExistsError(f"Target folder already exists: {final_path}")
            temp_path.rename(final_path)
            
            json_file = final_path / "quiz_data.json"
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = {}
                # write numeric id (int)
                data['id'] = int(nid)
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Renamed and wrote id: {final_path.name}")
        
        print(f"\nSuccessfully processed {len(temp_paths)} folders.")
    except Exception as e:
        print("Error during renaming:", e)
        print("Attempting best-effort rollback of any temporary renames...")
        # Try to rollback temp renames (best-effort)
        for temp_path, nid in temp_paths:
            try:
                if temp_path.exists():
                    # find original mapping by index in temp name
                    idx = int(temp_path.name.replace(temp_prefix, ""))
                    orig_folder = mappings[idx][0]
                    temp_path.rename(orig_folder)
            except Exception:
                pass
        print("Rollback attempted. Please check folders manually.")

if __name__ == "__main__":
    rename_folders_with_ids()
