import itertools
import random
import re
import sys
import os
from typing import Dict, List, Set, Tuple
from collections import Counter
import time

# ANSI Colors
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
BLUE = "\033[94m"
RESET = "\033[0m"

BANNER = rf"""
{CYAN}                                                /$$   /$$     /$$      
                                                     |__/  | $$    | $$      
  /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$$ /$$$$$$/$$$$  /$$ /$$$$$$  | $$$$$$$ 
 /$$__  $$ |____  $$ /$$_____//$$_____/| $$_  $$_  $$| $$|_  $$_/  | $$__  $$
| $$  \ $$  /$$$$$$$|  $$$$$$|  $$$$$$ | $$ \ $$ \ $$| $$  | $$    | $$  \ $$
| $$  | $$ /$$__  $$ \____  $$\____  $$| $$ | $$ | $$| $$  | $$ /$$| $$  | $$
| $$$$$$$/|  $$$$$$$ /$$$$$$$//$$$$$$$/| $$ | $$ | $$| $$  |  $$$$/| $$  | $$
| $$____/  \_______/|_______/|_______/ |__/ |__/ |__/|__/   \___/  |__/  |__/{RESET}
{MAGENTA}MADE BY: PWIMAWY | v2.0{RESET}
"""

# ---------------- Helpers -------------------------------------------------

def normalize_date(value: str) -> List[str]:
    """Enhanced date normalization with more formats"""
    digits = re.sub(r"\D", "", value or '')
    variants = set()
    if len(digits) == 8:
        yyyy, mm, dd = digits[0:4], digits[4:6], digits[6:8]
        variants.update([
            yyyy, yyyy[2:], mm+dd, dd+mm, mm+yyyy, dd+mm+yyyy, yyyy+mm+dd,
            dd+mm+yyyy[2:], yyyy[2:]+mm+dd, mm+dd+yyyy, mm+dd+yyyy[2:]
        ])
    elif len(digits) == 6:
        y2, mm, dd = digits[0:2], digits[2:4], digits[4:6]
        variants.update([y2, mm+dd, dd+mm, y2+mm+dd, dd+mm+y2, mm+dd+y2])
    elif len(digits) in (4,2):
        variants.add(digits)
    else:
        if digits:
            variants.add(digits)
            if len(digits) >= 4:
                variants.add(digits[-4:])
                variants.add(digits[:4])
            if len(digits) >= 2:
                variants.add(digits[-2:])
                variants.add(digits[:2])
    return sorted(v for v in variants if v)


def casing_variants(s: str) -> Set[str]:
    """Enhanced casing with more variations"""
    if not s:
        return set()
    vals = {s, s.lower(), s.upper(), s.capitalize()}
    
    # Title case
    vals.add(s.title())
    
    # Alternating case
    if len(s) > 1:
        vals.add(''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)]))
        vals.add(''.join([c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(s)]))
    
    # First letter upper, rest lower
    if len(s) > 0:
        vals.add(s[0].upper() + s[1:].lower())
    
    parts = [p for p in re.split(r"\s+", s) if p]
    if parts:
        initials = ''.join([p[0] for p in parts])
        vals.add(initials)
        vals.add(initials.lower())
        vals.add(initials.upper())
    return vals


def leet_variants(s: str) -> Set[str]:
    """Enhanced leet speak with more substitutions"""
    subs = {
        'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
        's': ['5', '$'], 't': ['7', '+'], 'l': ['1'], 'g': ['9'],
        'b': ['8'], 'z': ['2']
    }
    out = {s}
    
    # Single character substitutions
    for i, ch in enumerate(s.lower()):
        if ch in subs:
            for sub in subs[ch]:
                out.add(s[:i] + sub + s[i+1:])
    
    # Multiple substitutions (up to 3)
    positions = [(i, ch) for i, ch in enumerate(s.lower()) if ch in subs]
    if len(positions) >= 2:
        for combo in itertools.combinations(positions[:4], min(2, len(positions))):
            temp = list(s)
            for idx, ch in combo:
                temp[idx] = subs[ch][0]
            out.add(''.join(temp))
    
    return out


def reverse_string(s: str) -> str:
    """Reverse a string"""
    return s[::-1]


def double_chars(s: str) -> Set[str]:
    """Double certain characters"""
    out = set()
    for i in range(len(s)):
        out.add(s[:i] + s[i] + s[i:])
    return out


def keyboard_walk(s: str) -> Set[str]:
    """Generate keyboard walk patterns"""
    keyboard_map = {
        'q': 'wa', 'w': 'qeas', 'e': 'wdsr', 'r': 'etf', 't': 'rgy', 'y': 'tuh', 'u': 'yij', 'i': 'uok', 'o': 'ipl', 'p': 'ol',
        'a': 'qwsz', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'huikmn', 'k': 'jiolm', 'l': 'kop',
        'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
    }
    out = set()
    for i, ch in enumerate(s.lower()):
        if ch in keyboard_map:
            for neighbor in keyboard_map[ch]:
                out.add(s[:i] + neighbor + s[i+1:])
    return out


def field_variants(field_name: str, value: str, enable_leet: bool=False, enable_advanced: bool=False) -> Set[str]:
    """Enhanced field variants with more transformations"""
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
            # Add reversed initials
            vals.add(''.join([p[0] for p in reversed(parts)]))
    
    final = set()
    for v in vals:
        for c in casing_variants(v):
            final.add(c)
            if enable_leet:
                final.update(leet_variants(c))
            if enable_advanced:
                final.add(reverse_string(c))
                # Limit double_chars to shorter strings to avoid explosion
                if len(c) <= 6:
                    final.update(list(double_chars(c))[:5])
    
    return final


def generate_common_patterns() -> List[str]:
    """Generate common password patterns"""
    patterns = []
    
    # Common sequences
    patterns.extend(['123', '1234', '12345', '123456', '1234567', '12345678'])
    patterns.extend(['qwerty', 'qwertz', 'azerty', 'asdf', 'asdfgh'])
    patterns.extend(['password', 'pass', 'passwd', 'letmein', 'welcome'])
    patterns.extend(['admin', 'root', 'user', 'test', 'guest'])
    patterns.extend(['master', 'super', 'default', 'changeme'])
    
    # Years
    for year in range(1950, 2026):
        patterns.append(str(year))
        patterns.append(str(year)[2:])
    
    # Common suffixes/prefixes
    suffixes = ['!', '!!', '!!!', '123', '1', '01', '2024', '2025', '@', '#']
    prefixes = ['!', '@', '#', '$']
    
    return patterns


def generate_year_range(start: int, end: int) -> List[str]:
    """Generate year range"""
    years = []
    for year in range(start, end + 1):
        years.append(str(year))
        years.append(str(year)[2:])
    return years


def add_special_char_variants(base: str) -> Set[str]:
    """Add special character variations"""
    special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    variants = {base}
    
    for char in special_chars[:8]:  # Limit to prevent explosion
        variants.add(base + char)
        variants.add(char + base)
    
    # Common patterns
    variants.add(base + '!')
    variants.add(base + '!!')
    variants.add(base + '123')
    variants.add(base + '@')
    variants.add(base + '#')
    
    return variants


def generate_combinations(fields: Dict[str, str], separators: List[str], 
                         num_fields: int = 2, order_matters: bool = True, 
                         enable_leet: bool = False, enable_advanced: bool = False) -> List[str]:
    """Generate combinations with configurable number of fields"""
    items = [(k, v) for k, v in fields.items() if v]
    
    if len(items) < num_fields:
        return []
    
    if order_matters:
        combos = itertools.permutations(items, num_fields)
    else:
        combos = itertools.combinations(items, num_fields)
    
    out = []
    total_combos = 0
    
    for combo in combos:
        total_combos += 1
        if total_combos > 10000:  # Safety limit for memory
            break
            
        # Get variants for each field
        variant_lists = []
        for k, v in combo:
            variants = field_variants(k, v, enable_leet=enable_leet, enable_advanced=enable_advanced)
            # Limit variants per field to prevent explosion
            variant_lists.append(list(variants)[:20])
        
        # Generate all combinations
        for variant_combo in itertools.product(*variant_lists):
            for sep in separators:
                out.append(sep.join(variant_combo))
    
    return out


def filter_by_length(candidates: List[str], exact: int=None, min_len: int=None, max_len: int=None) -> List[str]:
    """Filter candidates by length"""
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


def calculate_statistics(words: List[str]) -> Dict:
    """Calculate statistics about generated wordlist"""
    if not words:
        return {}
    
    lengths = [len(w) for w in words]
    char_counter = Counter()
    for w in words:
        char_counter.update(w.lower())
    
    return {
        'total': len(words),
        'unique': len(set(words)),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'avg_length': sum(lengths) / len(lengths),
        'length_distribution': Counter(lengths),
        'char_distribution': char_counter.most_common(10)
    }


def load_dictionary(filepath: str) -> List[str]:
    """Load words from a dictionary file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}Error loading dictionary: {e}{RESET}")
        return []


# ----------------- UI components -----------------------------------------

def prompt_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}Interrupted. Returning to menu.{RESET}")
        return ''


def show_menu():
    print(BANNER)
    print(f"{CYAN}═══════════════════ MAIN MENU ═══════════════════{RESET}")
    print(f"{CYAN}1{RESET})  Create/Edit values")
    print(f"{CYAN}2{RESET})  Review values")
    print(f"{CYAN}3{RESET})  Execute Wordlist Generation")
    print(f"{CYAN}4{RESET})  Edit settings (leet/separators/length/advanced)")
    print(f"{CYAN}5{RESET})  Preview generated results")
    print(f"{CYAN}6{RESET})  Export to file")
    print(f"{CYAN}7{RESET})  Add common patterns")
    print(f"{CYAN}8{RESET})  Load dictionary file")
    print(f"{CYAN}9{RESET})  Show statistics")
    print(f"{CYAN}10{RESET}) Shuffle/Randomize wordlist")
    print(f"{CYAN}11{RESET}) Advanced transformations")
    print(f"{CYAN}0{RESET})  Exit")
    print(f"{CYAN}═════════════════════════════════════════════════{RESET}")


# ----------------- menu flows -------------------------------------------

def create_value_flow(fields: Dict[str, str]):
    print(f"\n{CYAN}Create values — enter key=value pairs. Type 'done' when finished.{RESET}")
    print(f"{YELLOW}Example: name=Peter, surname=Parker, birthdate=19900115{RESET}")
    print(f"{YELLOW}Common keys: name, surname, nickname, birthdate, age, city, company, pet{RESET}")
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
    print(f"\n{CYAN}═══ Current fields ═══{RESET}")
    for idx, (k, v) in enumerate(fields.items(), 1):
        print(f"{idx}. {MAGENTA}{k}{RESET} = {WHITE}{v}{RESET}")
    cmd = prompt_input(f"{CYAN}Type 'del key' to delete or Enter to return: {RESET}").strip()
    if cmd.lower().startswith('del '):
        k = cmd[4:].strip().lower()
        if k in fields:
            del fields[k]
            print(f"{GREEN}Removed {k}{RESET}")
        else:
            print(f"{RED}Key not found: {k}{RESET}")


def edit_settings_flow(settings: Dict):
    print(f"\n{CYAN}═══ Edit settings ═══{RESET}")
    print(f"Current separators: {YELLOW}{settings['separators']}{RESET}")
    print(f"Number of fields to combine: {YELLOW}{settings['num_fields']}{RESET}")
    print(f"Order matters: {YELLOW}{settings['order_matters']}{RESET}")
    print(f"Enable leet: {YELLOW}{settings['enable_leet']}{RESET}")
    print(f"Enable advanced transforms: {YELLOW}{settings['enable_advanced']}{RESET}")
    print(f"Exact length: {YELLOW}{settings['exact_length']}{RESET}")
    print(f"Min length: {YELLOW}{settings['min_length']}{RESET}")
    print(f"Max length: {YELLOW}{settings['max_length']}{RESET}")

    s = prompt_input(f"{CYAN}Set separators (comma-separated e.g. '',_,-,@) or Enter to keep: {RESET}").strip()
    if s:
        settings['separators'] = [p if p.lower() != 'none' else '' for p in [x.strip() for x in s.split(',')]]
    
    n = prompt_input(f"{CYAN}Number of fields to combine (2-4) or Enter to keep: {RESET}").strip()
    if n.isdigit() and 2 <= int(n) <= 4:
        settings['num_fields'] = int(n)
    
    o = prompt_input(f"{CYAN}Order matters? (y/n) or Enter to keep: {RESET}").strip().lower()
    if o in ('y','n'):
        settings['order_matters'] = (o == 'y')
    
    l = prompt_input(f"{CYAN}Enable leet? (y/n) or Enter to keep: {RESET}").strip().lower()
    if l in ('y','n'):
        settings['enable_leet'] = (l == 'y')
    
    a = prompt_input(f"{CYAN}Enable advanced transforms (reverse, double, etc)? (y/n) or Enter to keep: {RESET}").strip().lower()
    if a in ('y','n'):
        settings['enable_advanced'] = (a == 'y')
    
    ex = prompt_input(f"{CYAN}Exact length (number) or Enter to keep/unset: {RESET}").strip()
    settings['exact_length'] = int(ex) if ex.isdigit() else None
    
    mn = prompt_input(f"{CYAN}Min length or Enter to keep: {RESET}").strip()
    settings['min_length'] = int(mn) if mn.isdigit() else None
    
    mx = prompt_input(f"{CYAN}Max length or Enter to keep: {RESET}").strip()
    settings['max_length'] = int(mx) if mx.isdigit() else None
    
    print(f"{GREEN}Settings updated.{RESET}")


def execute_wordlist_flow(fields: Dict[str, str], settings: Dict, extra_words: List[str]) -> List[str]:
    if len(fields) < settings['num_fields']:
        print(f"{RED}At least {settings['num_fields']} fields required to generate with current settings.{RESET}")
        return []
    
    print(f"{CYAN}Generating wordlist...{RESET}")
    start_time = time.time()
    
    candidates = []
    
    # Generate combinations
    print(f"{YELLOW}→ Generating {settings['num_fields']}-field combinations...{RESET}")
    combos = generate_combinations(
        fields, 
        settings['separators'], 
        settings['num_fields'],
        settings['order_matters'], 
        settings['enable_leet'],
        settings['enable_advanced']
    )
    candidates.extend(combos)
    
    # Add extra words (patterns, dictionary)
    if extra_words:
        print(f"{YELLOW}→ Adding {len(extra_words)} extra patterns/dictionary words...{RESET}")
        candidates.extend(extra_words)
    
    # Dedupe preserving order
    print(f"{YELLOW}→ Removing duplicates...{RESET}")
    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    
    # Filter by length
    print(f"{YELLOW}→ Filtering by length...{RESET}")
    filtered = filter_by_length(unique, settings['exact_length'], settings['min_length'], settings['max_length'])
    
    elapsed = time.time() - start_time
    print(f"{GREEN}✓ Generated {len(filtered)} unique candidates in {elapsed:.2f}s{RESET}")
    print(f"{YELLOW}  (Removed {len(unique) - len(filtered)} duplicates/filtered){RESET}")
    
    return filtered


def preview_flow(words: List[str], n: int=50):
    if not words:
        print(f"{YELLOW}No generated words to preview. Run Execute Wordlist first.{RESET}")
        return
    print(f"\n{CYAN}═══ Preview (first {n}) ═══{RESET}")
    for i, w in enumerate(words[:n], 1):
        print(f"{i:4}: {MAGENTA}{w}{RESET}")
    if len(words) > n:
        print(f"{YELLOW}... and {len(words) - n} more{RESET}")


def export_flow(words: List[str]):
    if not words:
        print(f"{YELLOW}No words to export.{RESET}")
        return
    fname = prompt_input(f"{CYAN}Enter filename to save (default wordlist.txt): {RESET}").strip() or 'wordlist.txt'
    try:
        with open(fname, 'w', encoding='utf-8') as f:
            for w in words:
                f.write(w + '\n')
        print(f"{GREEN}✓ Saved {len(words)} words to {fname}{RESET}")
    except Exception as e:
        print(f"{RED}Error writing file:{RESET} {e}")


def add_patterns_flow(extra_words: List[str]):
    print(f"\n{CYAN}═══ Add Common Patterns ═══{RESET}")
    print(f"{CYAN}1{RESET}) Add common passwords (123, qwerty, password, etc)")
    print(f"{CYAN}2{RESET}) Add year range")
    print(f"{CYAN}3{RESET}) Add custom pattern")
    print(f"{CYAN}0{RESET}) Back")
    
    choice = prompt_input(f"{YELLOW}Select option: {RESET}").strip()
    
    if choice == '1':
        patterns = generate_common_patterns()
        extra_words.extend(patterns)
        print(f"{GREEN}✓ Added {len(patterns)} common patterns{RESET}")
    elif choice == '2':
        start = prompt_input(f"{CYAN}Start year (default 1950): {RESET}").strip()
        end = prompt_input(f"{CYAN}End year (default 2025): {RESET}").strip()
        start = int(start) if start.isdigit() else 1950
        end = int(end) if end.isdigit() else 2025
        years = generate_year_range(start, end)
        extra_words.extend(years)
        print(f"{GREEN}✓ Added {len(years)} year variations{RESET}")
    elif choice == '3':
        pattern = prompt_input(f"{CYAN}Enter pattern: {RESET}").strip()
        if pattern:
            extra_words.append(pattern)
            # Add some variants
            extra_words.extend(list(casing_variants(pattern)))
            print(f"{GREEN}✓ Added pattern and variants{RESET}")


def load_dictionary_flow(extra_words: List[str]):
    filepath = prompt_input(f"{CYAN}Enter dictionary file path: {RESET}").strip()
    if not filepath:
        return
    
    if not os.path.exists(filepath):
        print(f"{RED}File not found: {filepath}{RESET}")
        return
    
    words = load_dictionary(filepath)
    if words:
        extra_words.extend(words)
        print(f"{GREEN}✓ Loaded {len(words)} words from dictionary{RESET}")


def show_statistics_flow(words: List[str]):
    if not words:
        print(f"{YELLOW}No words generated yet.{RESET}")
        return
    
    stats = calculate_statistics(words)
    
    print(f"\n{CYAN}═══ Wordlist Statistics ═══{RESET}")
    print(f"Total words: {YELLOW}{stats['total']}{RESET}")
    print(f"Unique words: {YELLOW}{stats['unique']}{RESET}")
    print(f"Min length: {YELLOW}{stats['min_length']}{RESET}")
    print(f"Max length: {YELLOW}{stats['max_length']}{RESET}")
    print(f"Avg length: {YELLOW}{stats['avg_length']:.1f}{RESET}")
    
    print(f"\n{CYAN}Length Distribution (top 10):{RESET}")
    for length, count in stats['length_distribution'].most_common(10):
        bar = '█' * min(50, count // max(1, stats['total'] // 50))
        print(f"{length:3} chars: {bar} {count}")
    
    print(f"\n{CYAN}Character Distribution (top 10):{RESET}")
    for char, count in stats['char_distribution']:
        print(f"{char}: {count}")


def shuffle_flow(words: List[str]) -> List[str]:
    if not words:
        print(f"{YELLOW}No words to shuffle.{RESET}")
        return words
    
    shuffled = words.copy()
    random.shuffle(shuffled)
    print(f"{GREEN}✓ Shuffled {len(shuffled)} words{RESET}")
    return shuffled


def advanced_transforms_flow(words: List[str]) -> List[str]:
    if not words:
        print(f"{YELLOW}No words to transform.{RESET}")
        return words
    
    print(f"\n{CYAN}═══ Advanced Transformations ═══{RESET}")
    print(f"{CYAN}1{RESET}) Add special character suffixes (!@#$)")
    print(f"{CYAN}2{RESET}) Reverse all words")
    print(f"{CYAN}3{RESET}) Add year suffixes (2020-2025)")
    print(f"{CYAN}4{RESET}) Add number suffixes (1-100)")
    print(f"{CYAN}0{RESET}) Back")
    
    choice = prompt_input(f"{YELLOW}Select option: {RESET}").strip()
    
    result = words.copy()
    
    if choice == '1':
        print(f"{YELLOW}Adding special character variants...{RESET}")
        new_words = []
        for w in words[:1000]:  # Limit to prevent explosion
            new_words.extend(list(add_special_char_variants(w)))
        result.extend(new_words)
        print(f"{GREEN}✓ Added {len(new_words)} variants{RESET}")
    
    elif choice == '2':
        reversed_words = [reverse_string(w) for w in words]
        result.extend(reversed_words)
        print(f"{GREEN}✓ Added {len(reversed_words)} reversed words{RESET}")
    
    elif choice == '3':
        new_words = []
        for w in words[:500]:  # Limit
            for year in range(2020, 2026):
                new_words.append(w + str(year))
                new_words.append(w + str(year)[2:])
        result.extend(new_words)
        print(f"{GREEN}✓ Added {len(new_words)} year variants{RESET}")
    
    elif choice == '4':
        new_words = []
        for w in words[:200]:  # Limit
            for num in range(1, 101):
                new_words.append(w + str(num))
        result.extend(new_words)
        print(f"{GREEN}✓ Added {len(new_words)} number variants{RESET}")
    
    # Dedupe
    seen = set()
    unique = []
    for w in result:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    
    return unique


# ----------------- Main loop -------------------------------------------

def main_loop():
    fields: Dict[str, str] = {}
    settings = {
        'separators': ['', '.', '_', '-'],
        'num_fields': 2,
        'order_matters': True,
        'enable_leet': False,
        'enable_advanced': False,
        'exact_length': None,
        'min_length': None,
        'max_length': None,
    }
    generated: List[str] = []
    extra_words: List[str] = []

    while True:
        show_menu()
        cmd = prompt_input(f"\n{YELLOW}Select option (0-11): {RESET}").strip()
        
        if cmd == '1':
            create_value_flow(fields)
        elif cmd == '2':
            review_values_flow(fields)
        elif cmd == '3':
            generated = execute_wordlist_flow(fields, settings, extra_words)
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
        elif cmd == '7':
            add_patterns_flow(extra_words)
        elif cmd == '8':
            load_dictionary_flow(extra_words)
        elif cmd == '9':
            show_statistics_flow(generated)
        elif cmd == '10':
            generated = shuffle_flow(generated)
        elif cmd == '11':
            generated = advanced_transforms_flow(generated)
        elif cmd == '0':
            print(f"{MAGENTA}Goodbye! Happy pentesting!{RESET}")
            return
        else:
            print(f"{RED}Unknown option. Choose 0-11.{RESET}")

# ----------------- Entry point -----------------------------------------

def main():
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted. Exiting.{RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()
