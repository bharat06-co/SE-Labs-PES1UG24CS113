"""Print actual fault examples from untouched instructor starter code."""
from pathlib import Path
import importlib.util
p = Path(__file__).resolve().parents[1] / 'baseline' / 'processor.py'
spec = importlib.util.spec_from_file_location('original_processor', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
examples = [('parse_rental', None), ('parse_rental','medium:abc'),('parse_rental', 'small:-2'),
            ('duration_average', ''), ('duration_average', '3,,6'), ('duration_average', '-1,2'),
            ('payable_rent', 'abc|200'), ('payable_rent', '100|-1'), ('payable_rent', 'NaN|0')]
print('Lab 7 - Original application: discovered invalid-input behavior')
for func, value in examples:
    try:
        out = getattr(mod,func)(value)
        print(f'{func}({value!r}) -> {out!r}  [INVALID ACCEPTED]')
    except Exception as exc:
        print(f'{func}({value!r}) -> {type(exc).__name__}: {exc}  [CRASH]')
