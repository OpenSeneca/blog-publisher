# Blog Publisher

Formats blog post outlines from blog-assistant into publication-ready markdown for Substack, Obsidian, and other platforms.

## Features

- **Multi-platform support**: Format for Substack, Obsidian, or standard markdown
- **Automatic parsing**: Extracts title, date, word count, and sections from blog outlines
- **Clean output**: Platform-specific formatting with appropriate metadata and styling
- **Batch-friendly**: Can be integrated into automated publishing workflows
- **Stdout mode**: Print to stdout for piping to other tools

## Installation

```bash
# From GitHub
pip install git+https://github.com/OpenSeneca/blog-publisher.git

# From local directory
cd ~/.openclaw/workspace/tools/blog-publisher
pip install -e .
```

## Usage

### Format for Substack
```bash
blog-publisher <outline_file> --format substack
```

### Format for Obsidian
```bash
blog-publisher <outline_file> --format obsidian
```

### Format as standard markdown
```bash
blog-publisher <outline_file> --format markdown
```

### Print to stdout
```bash
blog-publisher <outline_file> --format substack --stdout
```

### Custom output path
```bash
blog-publisher <outline_file> -o /path/to/output.md
```

## Workflow

1. Generate blog outline using blog-assistant:
   ```bash
   blog-assistant --topic "AI for Drug Discovery"
   ```

2. Review the generated outline in `~/workspace/outputs/blog-outline-YYYY-MM-DD.md`

3. Format for publication:
   ```bash
   blog-publisher ~/workspace/outputs/blog-outline-2026-05-09.md --format substack
   ```

4. The formatted post is saved to `~/workspace/outputs/blog-posts/substack-<topic>-<timestamp>.md`

5. Copy to Substack, Obsidian, or your publishing platform

## Output Structure

### Substack Format
- Title with publication date and target word count
- Clean markdown formatting
- Research citations as footnotes
- Substack-style footer with subscribe call-to-action

### Obsidian Format
- YAML frontmatter with tags, date, and metadata
- Wiki-link friendly structure
- Separate research sources section
- Obsidian-specific properties

### Markdown Format
- Standard markdown without platform-specific features
- Clean, portable format
- Includes generation timestamp

## Dependencies

- Python 3.8+
- No external dependencies (uses Python stdlib only)

## Integration

Works seamlessly with:
- **Blog Assistant**: Generates the outlines that this tool formats
- **Substack**: Direct copy-paste ready formatting
- **Obsidian**: Supports tags and metadata
- **Other markdown platforms**: Standard markdown output

## Status

**Tool Status:** ✅ Built, packaged, ready for publishing
**Published:** 📋 Pending GitHub push
**Last Updated:** 2026-05-09

## License

MIT
