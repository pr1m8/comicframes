#!/usr/bin/env python3
"""
Migration script for converting old main.py/main2.py usage to the new package structure.

This script helps users migrate their existing code to use the new comics package.
"""

import os
import sys


def show_migration_guide():
    """Display migration guide for users."""
    print("ComicFrames Package Migration Guide")
    print("=" * 40)
    print()
    
    print("OLD CODE (main.py/main2.py):")
    print("-" * 25)
    print("from main import pdf_to_images, detect_frames")
    print("pdf_to_images('comic.pdf')")
    print("detect_frames('page.png')")
    print()
    
    print("NEW CODE (comicframes package):")
    print("-" * 25)
    print("from comicframes import pdf_to_images, detect_frames")
    print("pdf_to_images('comic.pdf')")
    print("detect_frames('page.png')")
    print()
    
    print("COMMAND LINE USAGE:")
    print("-" * 18)
    print("# Convert PDF to images")
    print("comicframes-pdf comic.pdf")
    print()
    print("# Extract frames from directory")
    print("comicframes-extract ./pages ./output")
    print()
    
    print("KEY CHANGES:")
    print("-" * 12)
    print("✓ Better error handling")
    print("✓ Configurable output directories")
    print("✓ Command-line interface")
    print("✓ Proper Python packaging")
    print("✓ Fixed dependency issues (fitz -> pymupdf)")
    print("✓ Modular code structure")
    print("✓ Unit tests included")
    print()
    
    print("INSTALLATION:")
    print("-" * 12)
    print("uv pip install -e .")
    print("# or")
    print("pip install -e .")


def check_old_files():
    """Check if old files exist and suggest cleanup."""
    old_files = ['main.py', 'main2.py']
    found_files = [f for f in old_files if os.path.exists(f)]
    
    if found_files:
        print(f"\nFound old files: {', '.join(found_files)}")
        print("These files have been replaced by the new package structure.")
        print("You can safely remove them after migrating your code.")
        return True
    return False


def main():
    """Main migration helper."""
    show_migration_guide()
    
    if check_old_files():
        print("\nIMPORTANT: Update any import statements in your code!")
        print("Change 'from main import ...' to 'from comicframes import ...'")


if __name__ == "__main__":
    main()
