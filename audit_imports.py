import importlib
import os
import sys

sys.path.insert(0, '.')

errors = []
for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root or '.agents' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            rel_path = os.path.relpath(os.path.join(root, file), '.')
            mod_name = rel_path.replace(os.sep, '.').removesuffix('.py')
            if mod_name.endswith('.__init__'):
                mod_name = mod_name.removesuffix('.__init__')
            try:
                importlib.import_module(mod_name)
                print(f"✅ {mod_name}")
            except Exception as e:
                print(f"❌ {mod_name}: {type(e).__name__}: {e}")
                errors.append((mod_name, e))

if errors:
    print(f"\n❌ FOUND {len(errors)} IMPORT ERRORS!")
    sys.exit(1)
else:
    print("\n✅ ALL MODULE IMPORTS VERIFIED CLEANLY!")
