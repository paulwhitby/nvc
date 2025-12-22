#!/usr/bin/env python3
"""Automated script to fix Priority 1 PEP-8 issues.

This script fixes critical PEP-8 violations:
1. Remove trailing whitespace
2. Fix bare except clause
3. Document protected member access with pylint disable
4. Add proper spacing around inline comments

Usage:
    python fix_pep8_priority1.py

Creates backups with .bak extension before modifying files.
"""

import os
import re
import shutil
from pathlib import Path


def create_backup(filepath: Path) -> Path:
    """Create a backup of the file before modifying.

    Args:
        filepath: Path to file to backup

    Returns:
        Path to backup file
    """
    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
    shutil.copy2(filepath, backup_path)
    print(f"✓ Created backup: {backup_path}")
    return backup_path


def remove_trailing_whitespace(content: str) -> tuple[str, int]:
    """Remove trailing whitespace from all lines.

    Args:
        content: File content as string

    Returns:
        Tuple of (modified_content, number_of_fixes)
    """
    lines = content.split('\n')
    fixed_lines = []
    fixes = 0

    for line in lines:
        original_line = line
        line = line.rstrip()
        if line != original_line:
            fixes += 1
        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fixes


def fix_bare_except(content: str) -> tuple[str, int]:
    """Fix bare except clauses.

    Args:
        content: File content as string

    Returns:
        Tuple of (modified_content, number_of_fixes)
    """
    fixes = 0

    # Pattern: except: followed by newline and indent
    # Replace with: except Exception as e:
    pattern = r'^(\s*)except:\s*$'

    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        if re.match(pattern, line):
            indent = re.match(r'^(\s*)', line).group(1)
            # Check if next line has a comment about why broad except is needed
            next_line = lines[i + 1] if i + 1 < len(lines) else ''
            if 'pylint: disable=broad-exception-caught' not in next_line:
                fixed_lines.append(f'{indent}except Exception as e:  # pylint: disable=broad-exception-caught')
                fixes += 1
                # Add logging line if return None is next
                if i + 1 < len(lines) and 'return None' in lines[i + 1]:
                    # Add a print statement before return
                    fixed_lines.append(f'{indent}    print(f"[ERROR] Exception occurred: {{e}}")')
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), fixes


def add_protected_access_comments(content: str) -> tuple[str, int]:
    """Add pylint disable comments for protected member access.

    Args:
        content: File content as string

    Returns:
        Tuple of (modified_content, number_of_fixes)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []

    # Pattern: accessing ._dict or other protected members
    protected_pattern = r'\._dict|\._\w+'

    for i, line in enumerate(lines):
        if re.search(protected_pattern, line):
            # Check if pylint disable already present
            if 'pylint: disable=protected-access' not in line:
                # Check if this is a docstore._dict access (FAISS specific)
                if '._dict' in line and 'docstore' in line:
                    # Add inline disable comment
                    if '#' in line:
                        # Comment already exists, append to it
                        line = line.replace('#', '# pylint: disable=protected-access;')
                    else:
                        # Add new comment
                        line = line.rstrip() + '  # pylint: disable=protected-access'
                    fixes += 1

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fixes


def fix_inline_comment_spacing(content: str) -> tuple[str, int]:
    """Fix spacing around inline comments.

    PEP-8 requires at least two spaces before inline comments.

    Args:
        content: File content as string

    Returns:
        Tuple of (modified_content, number_of_fixes)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Pattern: code followed by single space and comment
        # But not if it's a shebang or in a string
        if '#' in line and not line.strip().startswith('#'):
            # Find the first # that's not in a string
            in_string = False
            quote_char = None

            for i, char in enumerate(line):
                if char in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                    if in_string and char == quote_char:
                        in_string = False
                        quote_char = None
                    elif not in_string:
                        in_string = True
                        quote_char = char
                elif char == '#' and not in_string:
                    # Check spacing before #
                    if i > 0:
                        spaces_before = 0
                        j = i - 1
                        while j >= 0 and line[j] == ' ':
                            spaces_before += 1
                            j -= 1

                        # Need at least 2 spaces before inline comment
                        if 0 < spaces_before < 2:
                            # Add missing space
                            line = line[:i] + ' ' + line[i:]
                            fixes += 1
                    break

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), fixes


def fix_inconsistent_blank_lines(content: str) -> tuple[str, int]:
    """Fix blank lines around class definitions.

    PEP-8 requires 2 blank lines before class definitions at module level.

    Args:
        content: File content as string

    Returns:
        Tuple of (modified_content, number_of_fixes)
    """
    fixes = 0
    lines = content.split('\n')
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a class definition
        if line.strip().startswith('class ') and ':' in line:
            # Count blank lines before this
            blank_before = 0
            j = i - 1
            while j >= 0 and lines[j].strip() == '':
                blank_before += 1
                j -= 1

            # Check if previous non-blank line is also a class (then 2 is ok)
            # Otherwise, need 2 blank lines
            if j >= 0:
                prev_line = lines[j].strip()
                # If previous line is module-level code, need 2 blank lines
                if not prev_line.startswith('class ') and blank_before < 2:
                    # Add missing blank lines
                    needed = 2 - blank_before
                    for _ in range(needed):
                        fixed_lines.append('')
                        fixes += 1

        fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines), fixes


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single file to fix PEP-8 issues.

    Args:
        filepath: Path to file to process
        dry_run: If True, don't write changes, just report

    Returns:
        Dictionary with fix statistics
    """
    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    print(f"{'='*60}")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content
    stats = {
        'file': str(filepath),
        'trailing_whitespace': 0,
        'bare_except': 0,
        'protected_access': 0,
        'inline_comments': 0,
        'blank_lines': 0,
        'total_fixes': 0
    }

    # Apply fixes in order
    fixes = [
        ('Trailing whitespace', remove_trailing_whitespace),
        ('Bare except clauses', fix_bare_except),
        ('Protected member access', add_protected_access_comments),
        ('Inline comment spacing', fix_inline_comment_spacing),
        ('Blank lines around classes', fix_inconsistent_blank_lines),
    ]

    for fix_name, fix_func in fixes:
        content, count = fix_func(content)
        key = fix_name.lower().replace(' ', '_').replace('clauses', '').replace('around_classes', '').strip()
        if key in stats:
            stats[key] = count
        stats['total_fixes'] += count

        if count > 0:
            print(f"✓ Fixed {count} instance(s) of: {fix_name}")

    # Write changes if not dry run
    if not dry_run and content != original_content:
        # Create backup
        create_backup(filepath)

        # Write fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✓ File updated: {filepath}")
        print(f"  Total fixes: {stats['total_fixes']}")
    elif content == original_content:
        print("\n✓ No changes needed")
    else:
        print(f"\n[DRY RUN] Would apply {stats['total_fixes']} fixes")

    return stats


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Fix Priority 1 PEP-8 issues in Python files'
    )
    parser.add_argument(
        'files',
        nargs='*',
        default=[
            'claude_multi_pdf_analyzer.py',
            'claude_nvc_chatbot.py'
        ],
        help='Files to process (default: claude_multi_pdf_analyzer.py claude_nvc_chatbot.py)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes'
    )

    args = parser.parse_args()

    print("PEP-8 Priority 1 Fixer")
    print("="*60)
    print("This script fixes:")
    print("  1. Trailing whitespace")
    print("  2. Bare except clauses")
    print("  3. Protected member access (adds pylint comments)")
    print("  4. Inline comment spacing")
    print("  5. Blank lines around class definitions")
    print()

    if args.dry_run:
        print("*** DRY RUN MODE - No files will be modified ***\n")

    # Get script directory
    script_dir = Path(__file__).parent

    # Process each file
    all_stats = []
    for filename in args.files:
        filepath = script_dir / filename

        if not filepath.exists():
            print(f"\n⚠ Warning: File not found: {filepath}")
            continue

        stats = process_file(filepath, dry_run=args.dry_run)
        all_stats.append(stats)

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    total_files = len(all_stats)
    total_fixes = sum(s['total_fixes'] for s in all_stats)

    print(f"Files processed: {total_files}")
    print(f"Total fixes applied: {total_fixes}")

    if total_fixes > 0:
        print("\nFixes by type:")
        fix_types = [
            'trailing_whitespace',
            'bare_except',
            'protected_access',
            'inline_comments',
            'blank_lines'
        ]
        for fix_type in fix_types:
            count = sum(s.get(fix_type, 0) for s in all_stats)
            if count > 0:
                label = fix_type.replace('_', ' ').title()
                print(f"  {label}: {count}")

    if not args.dry_run and total_fixes > 0:
        print("\n✓ All fixes applied successfully!")
        print("  Backup files created with .bak extension")
        print("\nNext steps:")
        print("  1. Review the changes")
        print("  2. Test your code")
        print("  3. Run: python -m flake8 --max-line-length=99 *.py")
        print("  4. If satisfied, delete .bak files")
    elif args.dry_run:
        print("\nRun without --dry-run to apply fixes")


if __name__ == '__main__':
    main()
