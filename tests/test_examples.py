"""Offline validation plus opt-in live tests for the migrated teaching material."""
import ast
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ('tutorials', 'moocs', 'workshops')


class DocumentationTests(unittest.TestCase):
    def test_python_syntax(self):
        for directory in CONTENT:
            for path in (ROOT / directory).rglob('*.py'):
                with self.subTest(path=path.relative_to(ROOT)):
                    tree = ast.parse(path.read_text(), filename=str(path))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            self.assertFalse((node.module or '').startswith('IPython'))

    def test_local_documentation_links(self):
        pages = [ROOT / 'README.md', ROOT / 'MIGRATION.md']
        for directory in CONTENT:
            pages.extend((ROOT / directory).rglob('*.md'))
        for page in pages:
            for link in re.findall(r'\]\(([^)]+)\)', page.read_text()):
                if link.startswith(('https:', 'http:', '#', 'mailto:', 'data:')):
                    continue
                with self.subTest(page=page.relative_to(ROOT), link=link):
                    target = unquote(link.split('#')[0])
                    self.assertTrue((page.parent / target).exists())

    def test_documented_steps_match_scripts(self):
        for directory in CONTENT:
            for page in (ROOT / directory).rglob('*.md'):
                steps = re.findall(r'### Step \d+\n\n```python\n(.*?)\n```', page.read_text(), re.S)
                if not steps:
                    continue
                script = page.with_suffix('.py')
                with self.subTest(page=page.relative_to(ROOT)):
                    self.assertTrue(script.exists())
                    source = script.read_text()
                    for step in steps:
                        indented = '\n'.join('    ' + line if line else '' for line in step.splitlines())
                        self.assertIn(indented, source)

    def test_dependency_lists_agree(self):
        project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
        requirements = (ROOT / 'requirements.txt').read_text().splitlines()
        self.assertEqual(project['project']['dependencies'], requirements)
        self.assertFalse(any(re.match(r'(jupyter|testbook|nbconvert|uv)\b', item) for item in requirements))


@unittest.skipUnless(os.environ.get('DES_RUN_INTEGRATION') == '1', 'Set DES_RUN_INTEGRATION=1 to use the live DES service')
class IntegrationTests(unittest.TestCase):
    def test_tutorial_scripts(self):
        # Same coverage as the former integration suite. Other examples include
        # batch reruns, historical services, or known backend limitations.
        examples = [
            '020_DATA_010-Loading-DataCubes',
            '020_DATA_020-Property_Filtering',
            '030_GEOM_010-Bounding-box',
            '030_GEOM_020-Polygons-Intro',
            '030_GEOM_030-Polygons-Areas',
            '040_VIZ_010-RGB',
            '040_VIZ_020-Drawing-Images-On-Base-Map',
            '050_PROC_010-Processes-intro',
            '050_PROC_020-Operators',
            '060_EO_020-Reductions',
            '060_EO_030-Spatial-Filtering',
        ]
        for name in examples:
            with self.subTest(example=name):
                subprocess.run([sys.executable, str(ROOT / 'tutorials' / (name + '.py'))],
                               cwd=ROOT, check=True, timeout=360)
