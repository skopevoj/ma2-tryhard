import os
from pathlib import Path

def rename_folders_sequentially():
    questions_dir = Path(__file__).parent / "questions"
    
    if not questions_dir.exists():
        print(f"Error: Questions directory not found at {questions_dir}")
        return
    
    # Get all subdirectories
    folders = [f for f in questions_dir.iterdir() if f.is_dir()]
    
    if not folders:
        print("No folders found in questions directory")
        return
    
    # Sort folders by name to maintain consistent order
    folders.sort(key=lambda x: x.name)
    
    print(f"Found {len(folders)} folders to rename:")
    for i, folder in enumerate(folders, start=1):
        print(f"  {folder.name} -> {i}")
    
    # Confirm before renaming
    response = input("\nProceed with renaming? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Rename folders (use temporary names to avoid conflicts)
    temp_prefix = "_temp_"
    temp_mappings = []
    
    # First pass: rename to temporary names
    for i, folder in enumerate(folders, start=1):
        temp_name = questions_dir / f"{temp_prefix}{i}"
        temp_mappings.append((folder, temp_name, i))
        folder.rename(temp_name)
    
    # Second pass: rename to final names
    for _, temp_folder, final_num in temp_mappings:
        final_name = questions_dir / str(final_num)
        temp_folder.rename(final_name)
        print(f"Renamed: {final_name.name}")
    
    print(f"\nSuccessfully renamed {len(folders)} folders!")

if __name__ == "__main__":
    rename_folders_sequentially()
