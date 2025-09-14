#!/usr/bin/env python3
"""
File Renaming Automation Script

This script provides various methods to automatically rename files in a folder:
1. Add prefix/suffix to filenames
2. Sequential numbering
3. Replace text in filenames
4. Change case (uppercase/lowercase)
5. Remove unwanted characters
6. Format with date/time

select the file renaming method and options via command line prompts.
It also includes a preview of changes before execution.

"""

import os
import re
from datetime import datetime
from pathlib import Path

class FileRenamer:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        if not self.folder_path.exists():
            raise ValueError(f"Folder does not exist: {folder_path}")
    
    def get_files(self, extensions=None):
        """Get list of files in folder, optionally filtered by extensions."""
        files = []
        for file in self.folder_path.iterdir():
            if file.is_file():
                if extensions is None or file.suffix.lower() in extensions:
                    files.append(file)
        return sorted(files)
    
    def add_prefix_suffix(self, prefix="", suffix="", extensions=None, preview=True):
        """Add prefix and/or suffix to filenames."""
        files = self.get_files(extensions)
        changes = []
        
        for file in files:
            name_without_ext = file.stem
            extension = file.suffix
            new_name = f"{prefix}{name_without_ext}{suffix}{extension}"
            new_path = file.parent / new_name
            
            changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def sequential_rename(self, base_name="file", start_num=1, padding=3, extensions=None, preview=True):
        """Rename files with sequential numbers."""
        files = self.get_files(extensions)
        changes = []
        
        for i, file in enumerate(files):
            extension = file.suffix
            number = str(start_num + i).zfill(padding)
            new_name = f"{base_name}_{number}{extension}"
            new_path = file.parent / new_name
            
            changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def replace_text(self, old_text, new_text, case_sensitive=True, extensions=None, preview=True):
        """Replace text in filenames."""
        files = self.get_files(extensions)
        changes = []
        
        for file in files:
            name_without_ext = file.stem
            extension = file.suffix
            
            if case_sensitive:
                new_name_stem = name_without_ext.replace(old_text, new_text)
            else:
                new_name_stem = re.sub(re.escape(old_text), new_text, name_without_ext, flags=re.IGNORECASE)
            
            if new_name_stem != name_without_ext:  # Only if there was a change
                new_name = f"{new_name_stem}{extension}"
                new_path = file.parent / new_name
                changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def change_case(self, case_type="lower", extensions=None, preview=True):
        """Change case of filenames. Options: 'lower', 'upper', 'title', 'capitalize'"""
        files = self.get_files(extensions)
        changes = []
        
        for file in files:
            name_without_ext = file.stem
            extension = file.suffix
            
            if case_type == "lower":
                new_name_stem = name_without_ext.lower()
            elif case_type == "upper":
                new_name_stem = name_without_ext.upper()
            elif case_type == "title":
                new_name_stem = name_without_ext.title()
            elif case_type == "capitalize":
                new_name_stem = name_without_ext.capitalize()
            else:
                continue
            
            if new_name_stem != name_without_ext:
                new_name = f"{new_name_stem}{extension}"
                new_path = file.parent / new_name
                changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def remove_characters(self, chars_to_remove="", remove_spaces=False, remove_special=False, extensions=None, preview=True):
        """Remove specified characters from filenames."""
        files = self.get_files(extensions)
        changes = []
        
        for file in files:
            name_without_ext = file.stem
            extension = file.suffix
            new_name_stem = name_without_ext
            
            # Remove specific characters
            if chars_to_remove:
                for char in chars_to_remove:
                    new_name_stem = new_name_stem.replace(char, "")
            
            # Remove spaces
            if remove_spaces:
                new_name_stem = new_name_stem.replace(" ", "_")
            
            # Remove special characters (keep only alphanumeric, spaces, hyphens, underscores)
            if remove_special:
                new_name_stem = re.sub(r'[^a-zA-Z0-9\s\-_]', '', new_name_stem)
            
            if new_name_stem != name_without_ext:
                new_name = f"{new_name_stem}{extension}"
                new_path = file.parent / new_name
                changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def add_timestamp(self, timestamp_format="%Y%m%d", position="prefix", extensions=None, preview=True):
        """Add timestamp to filenames."""
        files = self.get_files(extensions)
        changes = []
        timestamp = datetime.now().strftime(timestamp_format)
        
        for file in files:
            name_without_ext = file.stem
            extension = file.suffix
            
            if position == "prefix":
                new_name = f"{timestamp}_{name_without_ext}{extension}"
            else:  # suffix
                new_name = f"{name_without_ext}_{timestamp}{extension}"
            
            new_path = file.parent / new_name
            changes.append((file, new_path))
        
        if preview:
            self._preview_changes(changes)
            return changes
        else:
            return self._execute_changes(changes)
    
    def _preview_changes(self, changes):
        """Preview the changes that would be made."""
        if not changes:
            print("No files match the criteria or no changes needed.")
            return
        
        print(f"\nPreview of changes ({len(changes)} files):")
        print("-" * 80)
        for old_path, new_path in changes:
            print(f"'{old_path.name}' → '{new_path.name}'")
        print("-" * 80)
    
    def _execute_changes(self, changes):
        """Execute the renaming changes."""
        if not changes:
            print("No files to rename.")
            return []
        
        successful = []
        failed = []
        
        for old_path, new_path in changes:
            try:
                if new_path.exists():
                    print(f"Warning: '{new_path.name}' already exists, skipping '{old_path.name}'")
                    failed.append((old_path, new_path, "Target file already exists"))
                else:
                    old_path.rename(new_path)
                    successful.append((old_path, new_path))
            except Exception as e:
                failed.append((old_path, new_path, str(e)))
        
        print(f"\nRenaming complete:")
        print(f"✓ Successfully renamed: {len(successful)} files")
        if failed:
            print(f"✗ Failed to rename: {len(failed)} files")
            for old_path, new_path, error in failed:
                print(f"  '{old_path.name}' → '{new_path.name}': {error}")
        
        return successful

def main():
    """Example usage of the FileRenamer class."""
    
    # Get folder path from user
    folder_path = input("Enter the folder path: ").strip().strip('"')
    
    try:
        renamer = FileRenamer(folder_path)
        
        while True:
            print("\n" + "="*50)
            print("File Renaming Options:")
            print("1. Add prefix/suffix")
            print("2. Sequential numbering")
            print("3. Replace text")
            print("4. Change case")
            print("5. Remove characters")
            print("6. Add timestamp")
            print("7. List files in folder")
            print("0. Exit")
            
            choice = input("\nSelect an option (0-7): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                prefix = input("Enter prefix (or press Enter for none): ").strip()
                suffix = input("Enter suffix (or press Enter for none): ").strip()
                changes = renamer.add_prefix_suffix(prefix=prefix, suffix=suffix, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.add_prefix_suffix(prefix=prefix, suffix=suffix, preview=False)
                    
            elif choice == "2":
                base_name = input("Enter base name (default: 'file'): ").strip() or "file"
                start_num = int(input("Enter starting number (default: 1): ").strip() or "1")
                padding = int(input("Enter number padding (default: 3): ").strip() or "3")
                changes = renamer.sequential_rename(base_name=base_name, start_num=start_num, padding=padding, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.sequential_rename(base_name=base_name, start_num=start_num, padding=padding, preview=False)
                    
            elif choice == "3":
                old_text = input("Enter text to replace: ").strip()
                new_text = input("Enter replacement text: ").strip()
                case_sensitive = input("Case sensitive? (Y/n): ").lower() != 'n'
                changes = renamer.replace_text(old_text, new_text, case_sensitive=case_sensitive, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.replace_text(old_text, new_text, case_sensitive=case_sensitive, preview=False)
                    
            elif choice == "4":
                print("Case options: lower, upper, title, capitalize")
                case_type = input("Enter case type: ").strip().lower()
                changes = renamer.change_case(case_type=case_type, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.change_case(case_type=case_type, preview=False)
                    
            elif choice == "5":
                chars_to_remove = input("Enter characters to remove: ").strip()
                remove_spaces = input("Replace spaces with underscores? (y/N): ").lower() == 'y'
                remove_special = input("Remove special characters? (y/N): ").lower() == 'y'
                changes = renamer.remove_characters(chars_to_remove=chars_to_remove, 
                                                 remove_spaces=remove_spaces, 
                                                 remove_special=remove_special, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.remove_characters(chars_to_remove=chars_to_remove, 
                                            remove_spaces=remove_spaces, 
                                            remove_special=remove_special, preview=False)
                    
            elif choice == "6":
                print("Format examples: %Y%m%d (20231215), %Y-%m-%d (2023-12-15), %H%M%S (143052)")
                timestamp_format = input("Enter timestamp format (default: %Y%m%d): ").strip() or "%Y%m%d"
                position = input("Position - prefix or suffix? (default: prefix): ").strip().lower() or "prefix"
                changes = renamer.add_timestamp(timestamp_format=timestamp_format, position=position, preview=True)
                if changes and input("\nExecute these changes? (y/N): ").lower() == 'y':
                    renamer.add_timestamp(timestamp_format=timestamp_format, position=position, preview=False)
                    
            elif choice == "7":
                files = renamer.get_files()
                print(f"\nFiles in '{folder_path}' ({len(files)} total):")
                for i, file in enumerate(files, 1):
                    print(f"{i:3d}. {file.name}")
            
            else:
                print("Invalid option. Please try again.")
    
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
