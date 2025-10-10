import itertools
import random
import re
import sys
from typing import Dict, List, Set

# ANSI Colors
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Banner
BANNER = f"""
{CYAN}                                                      /$$   /$$     /$$      
                                                     |__/  | $$    | $$      
  /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$$ /$$$$$$/$$$$  /$$ /$$$$$$  | $$$$$$$ 
 /$$__  $$ |____  $$ /$$_____//$$_____/| $$_  $$_  $$| $$|_  $$_/  | $$__  $$
| $$  \ $$  /$$$$$$$|  $$$$$$|  $$$$$$ | $$ \ $$ \ $$| $$  | $$    | $$  \ $$
| $$  | $$ /$$__  $$ \____  $$\____  $$| $$ | $$ | $$| $$  | $$ /$$| $$  | $$
| $$$$$$$/|  $$$$$$$ /$$$$$$$//$$$$$$$/| $$ | $$ | $$| $$  |  $$$$/| $$  | $$
| $$____/  \_______/|_______/|_______/ |__/ |__/ |__/|__/   \___/  |__/  |__/{RESET}
{MAGENTA}MADE BY: PWIMAWY{RESET}
"""

# ---------------- Helpers -------------------------------------------------

def normalize_date(value: str) -> List[str]:
    digits = re.sub(r"\D", "", value or '')
    variants = set()
    if len(digits) == 8:
        yyyy, mm, dd = digits[0:4], digits[4:6], digits[6:8]
        variants.update([yyyy, yyyy[2:], mm+dd, dd+mm, mm+yyyy, dd+mm+yyyy, yyyy+mm+dd])
    elif len(digits) == 6:
        y2, mm, dd = digits[0:2], digits[2:4], digits[4:6]
        variants.update([y2, mm+dd, dd+mm, y2+mm+dd])
    elif len(digits) in (4,2):
        variants.add(digits)
    else:
        if digits:
            variants.add(digits)
            if len(digits) >= 4:
                variants.add(digits[-4:])
            if len(digits) >= 2:
                variants.add(digits[-2:])
    return sorted(v for v in variants if v)


def casing_variants(s: str) -> Set[str]:
    if not s:
        return set()
    vals = {s, s.lower(), s.upper(), s.capitalize()}
    parts = [p for p in re.split(r"\s+", s) if p]
    if parts:
        initials = ''.join([p[0] for p in parts])
        vals.add(initials)
        vals.add(initials.lower())
    return vals


def leet_variants(s: str) -> Set[str]:
    subs = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    out = {s}
    for i, ch in enumerate(s.lower()):
        if ch in subs:
            out.add(s[:i] + subs[ch] + s[i+1:])
    return out


def field_variants(field_name: str, value: str, enable_leet: bool=False) -> Set[str]:
    if not value:
        return set()
    key = (field_name or '').lower()
    vals = set()
    if key in ('birthdate', 'anniversary', 'dob', 'date'):
        vals.update(normalize_date(value))
    elif key == 'age':
        vals.add(re.sub(r"\D", "", value))
    else:
        clean = re.sub(r"[^A-Za-z0-9 ]+", '', value)
        parts = [p for p in re.split(r"\s+", clean) if p]
        if not parts:
            return set()
        vals.add(''.join(parts))
        for p in parts:
            vals.add(p)
        if len(parts) > 1:
            vals.add(''.join([p[0] for p in parts]))
    final = set()
    for v in vals:
        for c in casing_variants(v):
            final.add(c)
            if enable_leet:
                final.update(leet_variants(c))
    return final


def generate_two_combinations(fields: Dict[str, str], separators: List[str], order_matters: bool=True, enable_leet: bool=False) -> List[str]:
    items = [(k, v) for k, v in fields.items() if v]
    pairs = itertools.permutations(items, 2) if order_matters else itertools.combinations(items, 2)
    out = []
    for (k1, v1), (k2, v2) in pairs:
        vars1 = field_variants(k1, v1, enable_leet=enable_leet)
        vars2 = field_variants(k2, v2, enable_leet=enable_leet)
        for a in vars1:
            for b in vars2:
                for sep in separators:
                    out.append(f"{a}{sep}{b}")
                    if not order_matters:
                        out.append(f"{b}{sep}{a}")
    return out


def filter_by_length(candidates: List[str], exact: int=None, min_len: int=None, max_len: int=None) -> List[str]:
    out = []
    for c in candidates:
        L = len(c)
        if exact is not None:
            if L == exact:
                out.append(c)
        else:
            if min_len is not None and L < min_len:
                continue
            if max_len is not None and L > max_len:
                continue
            out.append(c)
    return out

# ----------------- UI components -----------------------------------------

def prompt_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}Interrupted. Returning to menu.{RESET}")
        return ''


def show_menu():
    print(BANNER)
    print(f"{CYAN}1{RESET}) Create value")
    print(f"{CYAN}2{RESET}) Review values")
    print(f"{CYAN}3{RESET}) Execute Wordlist")
    print(f"{CYAN}4{RESET}) Edit settings (leet/separators/length)")
    print(f"{CYAN}5{RESET}) Preview generated results")
    print(f"{CYAN}6{RESET}) Export to file")
    print(f"{CYAN}0{RESET}) Exit")

# ----------------- menu flows -------------------------------------------

def create_value_flow(fields: Dict[str, str]):
    print(f"\n{CYAN}Create values — enter key=value pairs. Type 'done' when finished.{RESET}")
    print(f"{YELLOW}Example: name=Peter, surname=Parker, birthdate=19900115{RESET}")
    while True:
        line = prompt_input(f"{CYAN}> {RESET}").strip()
        if not line:
            continue
        if line.lower() == 'done':
            break
        if line.lower().startswith('del '):
            k = line[4:].strip().lower()
            if k in fields:
                del fields[k]
                print(f"{GREEN}Removed {k}{RESET}")
            else:
                print(f"{RED}Key not found: {k}{RESET}")
            continue
        if '=' not in line:
            print(f"{RED}Invalid format — use key=value or 'del key' or 'done'.{RESET}")
            continue
        k, v = line.split('=', 1)
        fields[k.strip().lower()] = v.strip()
        print(f"{GREEN}Added{RESET}: {k.strip().lower()} = {v.strip()}")


def review_values_flow(fields: Dict[str, str]):
    if not fields:
        print(f"{YELLOW}No fields yet. Use Create value first.{RESET}")
        return
    print(f"\n{CYAN}Current fields:{RESET}")
    for idx, (k, v) in enumerate(fields.items(), 1):
        print(f"{idx}. {k} = {v}")
    cmd = prompt_input(f"{CYAN}Type 'del key' to delete or Enter to return: {RESET}").strip()
    if cmd.lower().startswith('del '):
        k = cmd[4:].strip().lower()
        if k in fields:
            del fields[k]
            print(f"{GREEN}Removed {k}{RESET}")
        else:
            print(f"{RED}Key not found: {k}{RESET}")


def edit_settings_flow(settings: Dict):
    print(f"\n{CYAN}Edit settings{RESET}")
    print(f"Current separators: {settings['separators']}")
    print(f"Order matters: {settings['order_matters']}")
    print(f"Enable leet: {settings['enable_leet']}")
    print(f"Exact length: {settings['exact_length']}")
    print(f"Min length: {settings['min_length']}")
    print(f"Max length: {settings['max_length']}")

    s = prompt_input(f"{CYAN}Set separators (comma-separated e.g. '',_,-) or Enter to keep: {RESET}").strip()
    if s:
        settings['separators'] = [p if p.lower() != 'none' else '' for p in [x.strip() for x in s.split(',')]]
    o = prompt_input(f"{CYAN}Order matters? (y/n) or Enter to keep: {RESET}").strip().lower()
    if o in ('y','n'):
        settings['order_matters'] = (o == 'y')
    l = prompt_input(f"{CYAN}Enable leet? (y/n) or Enter to keep: {RESET}").strip().lower()
    if l in ('y','n'):
        settings['enable_leet'] = (l == 'y')
    ex = prompt_input(f"{CYAN}Exact length (number) or Enter to keep/unset: {RESET}").strip()
    settings['exact_length'] = int(ex) if ex.isdigit() else None
    mn = prompt_input(f"{CYAN}Min length or Enter to keep: {RESET}").strip()
    settings['min_length'] = int(mn) if mn.isdigit() else None
    mx = prompt_input(f"{CYAN}Max length or Enter to keep: {RESET}").strip()
    settings['max_length'] = int(mx) if mx.isdigit() else None
    print(f"{GREEN}Settings updated.{RESET}")


def execute_wordlist_flow(fields: Dict[str, str], settings: Dict) -> List[str]:
    if len(fields) < 2:
        print(f"{RED}At least two fields required to generate.{RESET}")
        return []
    candidates = generate_two_combinations(fields, settings['separators'], settings['order_matters'], settings['enable_leet'])
    # dedupe preserving order
    seen = set(); unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c); unique.append(c)
    filtered = filter_by_length(unique, settings['exact_length'], settings['min_length'], settings['max_length'])
    print(f"{GREEN}Generated {len(filtered)} candidates.{RESET}")
    return filtered


def preview_flow(words: List[str], n: int=50):
    if not words:
        print(f"{YELLOW}No generated words to preview. Run Execute Wordlist first.{RESET}")
        return
    print(f"\n{CYAN}Preview (first {n}):{RESET}")
    for i, w in enumerate(words[:n], 1):
        print(f"{i:3}: {MAGENTA}{w}{RESET}")


def export_flow(words: List[str]):
    if not words:
        print(f"{YELLOW}No words to export.{RESET}")
        return
    fname = prompt_input(f"{CYAN}Enter filename to save (default wordlist.txt): {RESET}").strip() or 'wordlist.txt'
    try:
        with open(fname, 'w', encoding='utf-8') as f:
            for w in words:
                f.write(w + '\n')
        print(f"{GREEN}Saved {len(words)} words to {fname}{RESET}")
    except Exception as e:
        print(f"{RED}Error writing file:{RESET} {e}")

# ----------------- Main loop -------------------------------------------

def main_loop():
    fields: Dict[str, str] = {}
    settings = {
        'separators': ['', '.', '_', '-'],
        'order_matters': True,
        'enable_leet': False,
        'exact_length': None,
        'min_length': None,
        'max_length': None,
    }
    generated: List[str] = []

    while True:
        show_menu()
        cmd = prompt_input(f"\n{YELLOW}Select option (0-6): {RESET}").strip()
        if cmd == '1':
            create_value_flow(fields)
        elif cmd == '2':
            review_values_flow(fields)
        elif cmd == '3':
            generated = execute_wordlist_flow(fields, settings)
        elif cmd == '4':
            edit_settings_flow(settings)
        elif cmd == '5':
            if not generated:
                print(f"{YELLOW}No generated list in memory. Run Execute Wordlist first.{RESET}")
            else:
                n = prompt_input(f"{CYAN}How many to preview? (default 50): {RESET}").strip()
                n_val = int(n) if n.isdigit() else 50
                preview_flow(generated, n_val)
        elif cmd == '6':
            export_flow(generated)
        elif cmd == '0':
            print(f"{MAGENTA}Goodbye!{RESET}")
            return
        else:
            print(f"{RED}Unknown option. Choose 0-6.{RESET}")

# ----------------- Entry point -----------------------------------------

def main():
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted. Exiting.{RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()
