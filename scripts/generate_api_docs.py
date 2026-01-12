#!/usr/bin/env python3
"""
Automatic API documentation generator for Trace Python library.
Generates MDX files from Python docstrings with proper structure.

Usage:
    python scripts/generate_api_docs.py
    
This will scan the opto package and generate API reference documentation.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import importlib.util


class APIDocGenerator:
    """Generate API documentation from Python source code."""
    
    def __init__(self, source_dir: Path, output_dir: Path):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_python_files(self, package_path: Path) -> List[Path]:
        """Recursively get all Python files in a package."""
        python_files = []
        for file in package_path.rglob("*.py"):
            # Skip __pycache__, tests, and private modules
            if "__pycache__" in str(file) or "test" in str(file).lower():
                continue
            python_files.append(file)
        return python_files
    
    def parse_module(self, file_path: Path) -> Dict[str, Any]:
        """Parse a Python module and extract classes, functions, and docstrings."""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError as e:
                print(f"⚠️  Syntax error in {file_path}: {e}")
                return {}
        
        module_info = {
            'docstring': ast.get_docstring(tree),
            'classes': [],
            'functions': [],
            'path': file_path
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'methods': [],
                    'is_private': node.name.startswith('_')
                }
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if not item.name.startswith('__'):  # Skip magic methods for now
                            class_info['methods'].append({
                                'name': item.name,
                                'docstring': ast.get_docstring(item),
                                'args': [arg.arg for arg in item.args.args],
                                'is_private': item.name.startswith('_')
                            })
                
                if not class_info['is_private']:
                    module_info['classes'].append(class_info)
            
            elif isinstance(node, ast.FunctionDef) and not isinstance(node, ast.AsyncFunctionDef):
                # Only top-level functions
                if node.col_offset == 0 and not node.name.startswith('_'):
                    module_info['functions'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'args': [arg.arg for arg in node.args.args],
                    })
        
        return module_info
    
    def format_docstring(self, docstring: str) -> str:
        """Format docstring for MDX output."""
        if not docstring:
            return "*No documentation available.*"
        
        # Basic formatting - you can enhance this
        lines = docstring.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Convert common docstring sections to headers
            if stripped in ['Args:', 'Arguments:', 'Parameters:', 'Returns:', 'Raises:', 'Examples:', 'Example:', 'Note:', 'Notes:']:
                formatted_lines.append(f'\n**{stripped}**\n')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def generate_module_mdx(self, module_info: Dict[str, Any], relative_path: str) -> str:
        """Generate MDX content for a module."""
        file_path = module_info['path']
        module_name = relative_path.replace('/', '.').replace('.py', '')
        
        lines = [
            "---",
            f"title: {module_name}",
            f"description: API reference for {module_name}",
            "---",
            "",
            f"# {module_name}",
            ""
        ]
        
        # Module docstring
        if module_info['docstring']:
            lines.append(self.format_docstring(module_info['docstring']))
            lines.append("")
        
        # Classes
        if module_info['classes']:
            lines.append("## Classes")
            lines.append("")
            
            for cls in module_info['classes']:
                lines.append(f"### `{cls['name']}`")
                lines.append("")
                
                if cls['docstring']:
                    lines.append(self.format_docstring(cls['docstring']))
                else:
                    lines.append("*No documentation available.*")
                lines.append("")
                
                # Methods
                if cls['methods']:
                    lines.append("#### Methods")
                    lines.append("")
                    
                    for method in cls['methods']:
                        if method['is_private']:
                            continue
                        
                        args_str = ', '.join(method['args'])
                        lines.append(f"##### `{method['name']}({args_str})`")
                        lines.append("")
                        
                        if method['docstring']:
                            lines.append(self.format_docstring(method['docstring']))
                        else:
                            lines.append("*No documentation available.*")
                        lines.append("")
        
        # Functions
        if module_info['functions']:
            lines.append("## Functions")
            lines.append("")
            
            for func in module_info['functions']:
                args_str = ', '.join(func['args'])
                lines.append(f"### `{func['name']}({args_str})`")
                lines.append("")
                
                if func['docstring']:
                    lines.append(self.format_docstring(func['docstring']))
                else:
                    lines.append("*No documentation available.*")
                lines.append("")
        
        return '\n'.join(lines)
    
    def generate_index_mdx(self, modules: List[str], category: str) -> str:
        """Generate an index page for a category."""
        lines = [
            "---",
            f"title: {category.title()}",
            f"description: API reference for {category}",
            "---",
            "",
            f"# {category.title()} API Reference",
            "",
            "This section contains the API reference for the `" + category + "` module.",
            "",
            "## Modules",
            ""
        ]
        
        for module in modules:
            module_name = module.replace('.mdx', '')
            lines.append(f"- [{module_name}](./{module})")
        
        return '\n'.join(lines)
    
    def generate_docs(self):
        """Main function to generate all documentation."""
        print("🚀 Starting API documentation generation...")
        print(f"📂 Source: {self.source_dir}")
        print(f"📝 Output: {self.output_dir}")
        
        # Define main packages to document
        packages = {
            'trace': self.source_dir / 'trace',
            'optimizers': self.source_dir / 'optimizers',
            'trainer': self.source_dir / 'trainer',
            'utils': self.source_dir / 'utils',
        }
        
        for package_name, package_path in packages.items():
            if not package_path.exists():
                print(f"⚠️  Package {package_name} not found at {package_path}")
                continue
            
            print(f"\n📦 Processing package: {package_name}")
            
            # Create output directory for this package
            package_output_dir = self.output_dir / package_name
            package_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Get all Python files
            python_files = self.get_python_files(package_path)
            print(f"   Found {len(python_files)} Python files")
            
            generated_modules = []
            
            for py_file in python_files:
                # Skip __init__.py for now (can be handled separately)
                if py_file.name == '__init__.py':
                    continue
                
                # Parse the module
                module_info = self.parse_module(py_file)
                
                if not module_info.get('classes') and not module_info.get('functions'):
                    continue  # Skip empty modules
                
                # Get relative path
                relative_path = py_file.relative_to(package_path)
                
                # Generate MDX content
                mdx_content = self.generate_module_mdx(module_info, str(relative_path))
                
                # Write to output
                output_file = package_output_dir / relative_path.with_suffix('.mdx')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(mdx_content)
                
                generated_modules.append(str(relative_path.with_suffix('.mdx')))
                print(f"   ✅ {relative_path}")
            
            # Generate index page for this package
            if generated_modules:
                index_content = self.generate_index_mdx(generated_modules, package_name)
                index_file = package_output_dir / 'index.mdx'
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)
                print(f"   ✅ Created index.mdx")
        
        print("\n✨ API documentation generation complete!")


def main():
    """Main entry point."""
    # Get paths relative to script location
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent
    
    # Source directory is the Trace repo (one level up)
    trace_repo = docs_dir.parent / 'Trace'
    source_dir = trace_repo / 'opto'
    
    # Output directory
    output_dir = docs_dir / 'content' / 'docs' / 'api-reference'
    
    if not source_dir.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        print(f"   Please ensure the Trace repository is at: {trace_repo}")
        sys.exit(1)
    
    generator = APIDocGenerator(source_dir, output_dir)
    generator.generate_docs()


if __name__ == '__main__':
    main()

