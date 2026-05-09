#!/usr/bin/env python3
"""
Blog Publisher - Formats blog posts for publication

Formats blog post outlines from blog-assistant into publication-ready markdown
for Substack, Obsidian, and other platforms.

Usage:
    python3 main.py <outline_file> --format substack
    python3 main.py <outline_file> --format obsidian
"""

import sys
import re
from pathlib import Path
from datetime import datetime
import argparse

def parse_outline(outline_path: Path) -> dict:
    """Parse a blog outline file into structured data"""
    content = outline_path.read_text()

    # Extract metadata
    title_match = re.search(r'^# Blog Outline: (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Untitled'

    date_match = re.search(r'\*\*Date:\*\* (\d{4}-\d{2}-\d{2})', content)
    date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')

    word_count_match = re.search(r'\*\*Target Word Count:\*\* ([\d,]+) words', content)
    word_count = word_count_match.group(1) if word_count_match else '1800-2000'

    # Extract sections
    sections = {}
    current_section = None
    current_content = []

    # Skip header up to first section
    lines = content.split('\n')
    in_sections = False

    for line in lines:
        if line.startswith('## ') or line.startswith('### '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()

            # Start new section
            current_section = line.strip()
            current_content = []
            in_sections = True
        elif in_sections and current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return {
        'title': title,
        'date': date,
        'word_count': word_count,
        'sections': sections,
        'raw': content
    }

def format_for_substack(outline: dict) -> str:
    """Format blog post for Substack publication"""
    md = f"# {outline['title']}\n\n"
    md += f"**Published:** {outline['date']}\n"
    md += f"**Target Length:** {outline['word_count']} words\n\n"
    md += "---\n\n"

    # Add selected title if present
    if '## Selected Title' in outline['sections']:
        md += outline['sections']['## Selected Title'] + "\n\n"
        md += "---\n\n"

    # Add all sections
    for section_name, section_content in outline['sections'].items():
        # Skip metadata sections
        if section_name in ['## Title Suggestions', '## Selected Title',
                           '## Outline Structure', '## Research Sources Used',
                           '## Hook / Lede', '## Background Context']:
            # Include these sections but remove markdown headers
            if section_name.startswith('## '):
                clean_name = section_name[3:]
                md += f"## {clean_name}\n\n"
            elif section_name.startswith('### '):
                clean_name = section_name[4:]
                md += f"### {clean_name}\n\n"
        else:
            # Keep section headers for research sections
            md += f"{section_name}\n\n"

        # Add section content, converting bullet points to Substack style
        for line in section_content.split('\n'):
            if line.strip().startswith('- '):
                md += line + "\n"
            elif line.strip().startswith('*Research:'):
                # Research citations - add as footnote-style
                md += f"_{line}_\n"
            elif line.strip():
                md += line + "\n"

        md += "\n"

    # Add footer
    md += "---\n\n"
    md += "*Thanks for reading Run Data Run! If you enjoyed this post, subscribe for more AI agent research and practical insights.*\n"

    return md

def format_for_obsidian(outline: dict) -> str:
    """Format blog post for Obsidian publication"""
    md = f"# {outline['title']}\n\n"
    md += f"tags: [blog, published]\n"
    md += f"date: {outline['date']}\n"
    md += f"word-count: {outline['word_count']}\n\n"
    md += "---\n\n"

    # Add metadata in Obsidian YAML frontmatter style
    md += f"**Type:** Blog Post\n"
    md += f"**Status:** Published\n"
    md += f"**Platform:** Substack\n"
    md += f"**Target Length:** {outline['word_count']} words\n\n"
    md += "---\n\n"

    # Add selected title if present
    if '## Selected Title' in outline['sections']:
        md += outline['sections']['## Selected Title'] + "\n\n"

    # Add all sections
    for section_name, section_content in outline['sections'].items():
        # Skip metadata sections
        if section_name not in ['## Title Suggestions', '## Outline Structure',
                                '## Research Sources Used']:
            # Keep section headers
            if section_name.startswith('## '):
                clean_name = section_name[3:]
                md += f"## {clean_name}\n\n"
            elif section_name.startswith('### '):
                clean_name = section_name[4:]
                md += f"### {clean_name}\n\n"

            # Add section content
            md += section_content + "\n\n"

    # Add research sources as separate section
    if '## Research Sources Used' in outline['sections']:
        md += "---\n\n"
        md += outline['sections']['## Research Sources Used'] + "\n\n"

    return md

def format_for_markdown(outline: dict) -> str:
    """Format blog post as standard markdown (no platform-specific formatting)"""
    md = f"# {outline['title']}\n\n"
    md += f"**Date:** {outline['date']}\n"
    md += f"**Target Length:** {outline['word_count']} words\n\n"
    md += "---\n\n"

    # Add all sections
    for section_name, section_content in outline['sections'].items():
        # Skip metadata sections
        if section_name not in ['## Title Suggestions', '## Outline Structure',
                                '## Research Sources Used']:
            # Keep section headers
            md += f"{section_name}\n\n"
            md += section_content + "\n\n"

    # Add research sources
    if '## Research Sources Used' in outline['sections']:
        md += "---\n\n"
        md += outline['sections']['## Research Sources Used'] + "\n\n"

    # Add footer
    md += "---\n\n"
    md += f"*Generated by Blog Publisher on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return md

def save_formatted(formatted: str, outline_path: Path, format_type: str) -> Path:
    """Save formatted blog post to file"""
    output_dir = Path.home() / ".openclaw" / "workspace" / "outputs" / "blog-posts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract topic name from outline filename
    topic = outline_path.stem.replace('blog-outline-', '').replace(f'-{datetime.now().strftime("%Y-%m-%d")}', '')

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    if format_type == 'substack':
        filename = f"substack-{topic}-{timestamp}.md"
    elif format_type == 'obsidian':
        filename = f"obsidian-{topic}-{timestamp}.md"
    else:
        filename = f"{format_type}-{topic}-{timestamp}.md"

    output_path = output_dir / filename
    output_path.write_text(formatted)

    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="Blog Publisher - Format blog posts for publication",
        epilog="Formats blog outlines from blog-assistant for Substack, Obsidian, etc."
    )
    parser.add_argument(
        "outline",
        help="Path to blog outline file (output from blog-assistant)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=['substack', 'obsidian', 'markdown'],
        default='substack',
        help="Output format (default: substack)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: outputs/blog-posts/<format>-<topic>-<timestamp>.md)"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of saving to file"
    )

    args = parser.parse_args()

    # Parse outline file
    outline_path = Path(args.outline)
    if not outline_path.exists():
        print(f"[ERROR] Outline file not found: {args.outline}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Reading outline: {args.outline}")
    outline = parse_outline(outline_path)

    # Format for requested platform
    print(f"[INFO] Formatting for: {args.format}")
    if args.format == 'substack':
        formatted = format_for_substack(outline)
    elif args.format == 'obsidian':
        formatted = format_for_obsidian(outline)
    else:
        formatted = format_for_markdown(outline)

    # Output
    if args.stdout:
        print(formatted)
    else:
        output_path = args.output
        if not output_path:
            output_path = save_formatted(formatted, outline_path, args.format)

        print(f"[SUCCESS] Saved to: {output_path}")
        print(f"[INFO] Format: {args.format}")
        print(f"[INFO] Topic: {outline['title']}")

if __name__ == "__main__":
    main()
