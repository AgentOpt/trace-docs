#!/usr/bin/env python3
"""
Convert Jupyter notebooks to MDX format for Fumadocs.
Preserves code cells, outputs, and markdown cells with proper formatting.

Usage:
    python scripts/convert_notebooks.py [notebook_path] [output_path]
    
    Or to convert all notebooks in the examples directory:
    python scripts/convert_notebooks.py --all
    
Features:
- Converts code cells to MDX code blocks
- Preserves markdown formatting
- Adds "Open in Colab" badges
- Extracts title from first heading or filename
- Handles images and outputs
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse


class NotebookConverter:
    """Convert Jupyter notebooks to MDX format."""
    
    def __init__(self, trace_repo_url: str = "https://github.com/AgentOpt/OpenTrace"):
        self.trace_repo_url = trace_repo_url
    
    def extract_title(self, cells: List[Dict[str, Any]]) -> str:
        """Extract title from first markdown heading or use filename."""
        for cell in cells:
            if cell.get('cell_type') == 'markdown':
                for line in cell.get('source', []):
                    if line.startswith('# '):
                        return line[2:].strip()
        return "Untitled Notebook"
    
    def convert_markdown_cell(self, cell: Dict[str, Any]) -> str:
        """Convert a markdown cell to MDX."""
        source = cell.get('source', [])
        if isinstance(source, list):
            content = ''.join(source)
        else:
            content = source
        
        # Handle image paths (convert relative paths)
        content = re.sub(
            r'!\[(.*?)\]\(((?!http)[^\)]+)\)',
            r'![\1](/images/\2)',
            content
        )
        
        return content
    
    def convert_code_cell(self, cell: Dict[str, Any], show_output: bool = True) -> str:
        """Convert a code cell to MDX code block."""
        source = cell.get('source', [])
        if isinstance(source, list):
            code = ''.join(source)
        else:
            code = source
        
        # Remove trailing newlines
        code = code.rstrip('\n')
        
        lines = [
            "```python",
            code,
            "```"
        ]
        
        # Handle outputs if requested
        if show_output and cell.get('outputs'):
            output_text = self.extract_output(cell['outputs'])
            if output_text:
                lines.extend([
                    "",
                    "<Callout type=\"info\" title=\"Output\">",
                    "",
                    "```",
                    output_text,
                    "```",
                    "",
                    "</Callout>"
                ])
        
        return '\n'.join(lines)
    
    def extract_output(self, outputs: List[Dict[str, Any]]) -> str:
        """Extract text output from cell outputs."""
        output_lines = []
        
        for output in outputs:
            if output.get('output_type') == 'stream':
                text = output.get('text', [])
                if isinstance(text, list):
                    output_lines.extend(text)
                else:
                    output_lines.append(text)
            
            elif output.get('output_type') in ['execute_result', 'display_data']:
                data = output.get('data', {})
                if 'text/plain' in data:
                    text = data['text/plain']
                    if isinstance(text, list):
                        output_lines.extend(text)
                    else:
                        output_lines.append(text)
            
            elif output.get('output_type') == 'error':
                # Include error information
                output_lines.append(f"Error: {output.get('ename', 'Unknown')}")
                output_lines.append(output.get('evalue', ''))
        
        return ''.join(output_lines).strip()
    
    def generate_frontmatter(
        self, 
        title: str, 
        description: Optional[str] = None,
        colab_path: Optional[str] = None
    ) -> str:
        """Generate MDX frontmatter."""
        lines = ["---", f"title: {title}"]
        
        if description:
            lines.append(f"description: {description}")
        else:
            lines.append(f"description: Tutorial notebook - {title}")
        
        lines.append("---")
        lines.append("")
        
        # Add note about editing
        lines.extend([
            "{/* This file was auto-generated from a Jupyter notebook. */}",
            "{/* You can edit it, but changes may be overwritten if the notebook is regenerated. */}",
            ""
        ])
        
        # Add Colab badge if path provided
        if colab_path:
            lines.extend([
                "<Callout type=\"tip\">",
                f"  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_path})",
                "</Callout>",
                ""
            ])
        
        return '\n'.join(lines)
    
    def convert_notebook(
        self, 
        notebook_path: Path, 
        output_path: Path,
        relative_notebook_path: Optional[str] = None,
        show_outputs: bool = False
    ) -> None:
        """Convert a Jupyter notebook to MDX format."""
        print(f"📓 Converting: {notebook_path.name}")
        
        # Read notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        cells = notebook.get('cells', [])
        
        # Extract title
        title = self.extract_title(cells)
        
        # Generate Colab link
        colab_path = None
        if relative_notebook_path:
            colab_path = f"https://colab.research.google.com/github/AgentOpt/Trace/blob/main/{relative_notebook_path}"
        
        # Generate MDX content
        mdx_lines = []
        
        # Add frontmatter
        frontmatter = self.generate_frontmatter(title, colab_path=colab_path)
        mdx_lines.append(frontmatter)
        
        # Convert cells
        for i, cell in enumerate(cells):
            cell_type = cell.get('cell_type')
            
            if cell_type == 'markdown':
                content = self.convert_markdown_cell(cell)
                # Skip the first h1 if it matches the title (already in frontmatter)
                if i == 0 and content.strip().startswith(f"# {title}"):
                    continue
                mdx_lines.append(content)
                mdx_lines.append("")
            
            elif cell_type == 'code':
                # Skip empty code cells
                source = cell.get('source', [])
                if not source or (isinstance(source, list) and not ''.join(source).strip()):
                    continue
                
                code_block = self.convert_code_cell(cell, show_output=show_outputs)
                mdx_lines.append(code_block)
                mdx_lines.append("")
        
        # Write MDX file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(mdx_lines))
        
        print(f"   ✅ Saved to: {output_path.relative_to(output_path.parent.parent.parent)}")
    
    def convert_all_notebooks(self, examples_dir: Path, output_base: Path) -> None:
        """Convert all notebooks in the examples directory."""
        print("🚀 Converting all notebooks in examples directory...")
        
        notebook_files = list(examples_dir.rglob("*.ipynb"))
        
        if not notebook_files:
            print("⚠️  No notebook files found")
            return
        
        print(f"📚 Found {len(notebook_files)} notebooks")
        
        for notebook_path in notebook_files:
            # Skip checkpoints
            if '.ipynb_checkpoints' in str(notebook_path):
                continue
            
            # Get relative path from examples dir
            relative_path = notebook_path.relative_to(examples_dir.parent)
            
            # Create output path in tutorials directory
            # Group by subdirectory
            parts = notebook_path.relative_to(examples_dir).parts
            if len(parts) > 1:
                # Has subdirectory (e.g., textgrad_examples/notebooks/file.ipynb)
                category = parts[0]
            else:
                category = 'general'
            
            output_path = output_base / category / notebook_path.with_suffix('.mdx').name
            
            try:
                self.convert_notebook(
                    notebook_path, 
                    output_path,
                    relative_notebook_path=str(relative_path),
                    show_outputs=False  # Can be customized
                )
            except Exception as e:
                print(f"   ❌ Error converting {notebook_path.name}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to MDX format for Fumadocs"
    )
    parser.add_argument(
        'notebook_path',
        nargs='?',
        help='Path to notebook file to convert'
    )
    parser.add_argument(
        'output_path',
        nargs='?',
        help='Output MDX file path'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all notebooks in examples directory'
    )
    parser.add_argument(
        '--show-outputs',
        action='store_true',
        help='Include cell outputs in the MDX'
    )
    
    args = parser.parse_args()
    
    converter = NotebookConverter()
    
    # Get paths
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent
    trace_repo = docs_dir.parent / 'Trace'
    
    if args.all:
        # Convert all notebooks
        examples_dir = trace_repo / 'examples'
        output_base = docs_dir / 'content' / 'docs' / 'tutorials'
        
        if not examples_dir.exists():
            print(f"❌ Error: Examples directory not found: {examples_dir}")
            sys.exit(1)
        
        converter.convert_all_notebooks(examples_dir, output_base)
        print("\n✨ All notebooks converted!")
    
    elif args.notebook_path and args.output_path:
        # Convert single notebook
        notebook_path = Path(args.notebook_path)
        output_path = Path(args.output_path)
        
        if not notebook_path.exists():
            print(f"❌ Error: Notebook not found: {notebook_path}")
            sys.exit(1)
        
        converter.convert_notebook(notebook_path, output_path, show_outputs=args.show_outputs)
        print("✨ Conversion complete!")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

