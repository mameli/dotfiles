#!/usr/bin/env python3
"""Offline regression checks: real PyMuPDF/uv/ensurepip, fixture wrapper CLIs.
Run with a Python containing pymupdf and uv on PATH. No converter installs,
models, browser actions, or user documents; temporary files stay in this skill.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SKILL = Path(__file__).resolve().parent.parent


def run(args, env, ok=True):
    result = subprocess.run([str(x) for x in args], env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ok and result.returncode:
        raise AssertionError(f"{args}: {result.returncode}\n{result.stderr}")
    return result


# Explicit test doubles exercise wrapper I/O, NOT converter quality.
CONVERTER = '''#!/usr/bin/env python3
import os, pathlib, sys
args = sys.argv[1:]
output = pathlib.Path(args[args.index('-o') + 1])
if '-f' in args:
    output = output / (pathlib.Path(args[-1]).stem + '.md')
if os.environ.get('EXPECTED_PARENT'):
    expected = pathlib.Path(os.environ['EXPECTED_PARENT']).resolve()
    assert expected in output.resolve().parents, (expected, output)
mode = os.environ.get('FIXTURE_MODE', 'success')
output.write_text('partial' if mode == 'fail' else '' if mode == 'empty' else '# Fixture output\\n')
if mode == 'fail':
    sys.exit(17)
'''


def main():
    import pymupdf
    uv = shutil.which('uv')
    assert uv, 'uv is required for real unseeded-environment bootstrap checks'
    with tempfile.TemporaryDirectory(prefix='.offline-test-', dir=SKILL) as td:
        root = Path(td)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', UV_OFFLINE='1',
                   UV_PYTHON_DOWNLOADS='never', UV_CACHE_DIR=str(root / 'uv-cache'),
                   PIP_NO_INDEX='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
                   TMPDIR=str(root))
        scripts = root / 'scripts'
        scripts.mkdir()
        for name in ('run_document_to_markdown.sh', 'run_pdf_to_markdown.sh'):
            shutil.copy2(SKILL / 'scripts' / name, scripts / name)
            run(['bash', '-n', scripts / name], env)
        pdf = root / 'input.pdf'
        doc = pymupdf.open()
        doc.new_page().insert_text((72, 72), 'Offline extraction sentinel')
        doc.set_metadata({'title': 'Fixture title'})
        doc.save(pdf)
        doc.close()
        extractor = SKILL / 'scripts/extract_pymupdf.py'
        text = run([sys.executable, extractor, pdf], env).stdout
        metadata = run([sys.executable, extractor, pdf, '--metadata'], env).stdout
        assert 'Offline extraction sentinel' in text
        assert json.loads(metadata)['title'] == 'Fixture title'
        assert 'Offline extraction sentinel' not in metadata
        print('PASS real PDF text extraction; --metadata is metadata-only')
        office = root / 'input.docx'
        office.write_text('Wrapper fixture, not an Office conversion test')
        fakebin = root / 'fixture-bin'
        fakebin.mkdir()
        # No JVM is invoked by wrapper plumbing tests.
        java = fakebin / 'java'
        java.write_text('#!/bin/sh\nexit 0\n')
        java.chmod(0o755)
        env['PATH'] = str(fakebin) + os.pathsep + env['PATH']
        specs = {}
        for kind, wrapper, binary, spec, source in [
            ('office', 'run_document_to_markdown.sh', 'markitdown',
             'markitdown[docx,pptx,xlsx,xls]>=0.1.0,<0.2', office),
            ('pdf', 'run_pdf_to_markdown.sh', 'opendataloader-pdf',
             'opendataloader-pdf>=2.2.1,<3', pdf),
        ]:
            runtime = root / '.runtime' / kind
            venv = runtime / 'venv'
            run([uv, 'venv', '--python', '3.12', venv], env)
            python = venv / 'bin/python'
            assert run([python, '-m', 'pip', '--version'], env, ok=False).returncode != 0
            converter = venv / 'bin' / binary
            converter.write_text(CONVERTER)
            converter.chmod(0o755)
            (runtime / 'install-spec.txt').write_text(spec + '\n')
            specs[kind] = spec + '\n'
            output = root / 'destination with spaces' / (kind + '.md')
            e = dict(env, EXPECTED_PARENT=str(output.parent))
            result = run(['bash', scripts / wrapper, source, '--output', output], e)
            assert result.stdout.strip() == str(output)
            assert output.read_text() == '# Fixture output\n'
            assert 'pip ' in run([python, '-m', 'pip', '--version'], env).stdout
            assert not (runtime / 'bootstrap.lock').exists()
            print(f'PASS {kind}: real uv pipless venv repaired by ensurepip; adjacent output')
            for mode in ('fail', 'empty'):
                output.write_text('KEEP ORIGINAL')
                result = run(['bash', scripts / wrapper, source, '--output', output],
                             dict(e, FIXTURE_MODE=mode), ok=False)
                assert result.returncode != 0
                assert output.read_text() == 'KEEP ORIGINAL'
                assert not list(output.parent.glob('.*markdown.*'))
            result = run(['bash', scripts / wrapper, source], env)
            assert result.stdout == '# Fixture output\n'
            result = run(['bash', scripts / wrapper, source, '--output', output.parent], env, ok=False)
            assert result.returncode != 0 and 'is a directory' in result.stderr
            print(f'PASS {kind}: failure/empty preserves destination; temp cleanup; stdout; directory rejection')
        for kind, spec in specs.items():
            assert (root / '.runtime' / kind / 'install-spec.txt').read_text() == spec
        assert not (root / '.runtime/venv').exists()
        rejected = run(['bash', scripts / 'run_document_to_markdown.sh', pdf], env, ok=False)
        assert rejected.returncode != 0 and 'scripts/run_pdf_to_markdown.sh' in rejected.stderr
        print('PASS runtime/spec isolation and PDF routing')
    print('PASS isolated fixtures removed; no downloads or browser actions')


if __name__ == '__main__':
    main()
