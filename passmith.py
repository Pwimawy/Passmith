import itertools
import random
import re
import sys
import os
from typing import Dict, List, Set, Optional
from collections import Counter
import time


# ── ANSI Colors ────────────────────────────────────────────────────────────────
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
WHITE   = "\033[97m"
RESET   = "\033[0m"

BANNER = f"""{CYAN}
██████╗  █████╗ ███████╗███████╗███╗   ███╗██╗████████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ████║██║╚══██╔══╝██║  ██║
██████╔╝███████║███████╗███████╗██╔████╔██║██║   ██║   ███████║
██╔═══╝ ██╔══██║╚════██║╚════██║██║╚██╔╝██║██║   ██║   ██╔══██║
██║     ██║  ██║███████║███████╗██║ ╚═╝ ██║██║   ██║   ██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
{RESET}{GREEN}                MADE BY: PWIMAWY | v2.1{RESET}"""

OUTPUT_DIR = "generated wordlist"


# ── Output folder ──────────────────────────────────────────────────────────────

def ensure_output_dir() -> str:
    """Create output folder if it doesn't exist. Returns the path to use."""
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            print(f"{GREEN}✓ Created output folder: '{OUTPUT_DIR}'{RESET}")
        except Exception as e:
            print(f"{RED}Could not create '{OUTPUT_DIR}': {e} — saving to current dir.{RESET}")
            return "."
    return OUTPUT_DIR


# ── Input helper ───────────────────────────────────────────────────────────────

def ask(prompt: str) -> str:
    """Prompt for input, always reading/writing from the real terminal."""
    try:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:          # EOF / closed pipe
            return ""
        return line.rstrip("\n").rstrip("\r")
    except (EOFError, KeyboardInterrupt):
        return ""


def pause() -> None:
    """Wait for the user to press Enter, always via the real terminal."""
    try:
        sys.stdout.write(f"\n{CYAN}  Press Enter to return to menu…{RESET}")
        sys.stdout.flush()
        sys.stdin.readline()
    except (EOFError, KeyboardInterrupt):
        pass


# ── Transform helpers ──────────────────────────────────────────────────────────

def normalize_date(value: str) -> List[str]:
    digits = re.sub(r"\D", "", value or "")
    variants: set = set()
    if len(digits) == 8:
        yyyy, mm, dd = digits[:4], digits[4:6], digits[6:]
        variants.update([
            yyyy, yyyy[2:], mm+dd, dd+mm,
            mm+yyyy, dd+mm+yyyy, yyyy+mm+dd,
            dd+mm+yyyy[2:], yyyy[2:]+mm+dd,
            mm+dd+yyyy, mm+dd+yyyy[2:],
        ])
    elif len(digits) == 6:
        y2, mm, dd = digits[:2], digits[2:4], digits[4:]
        variants.update([y2, mm+dd, dd+mm, y2+mm+dd, dd+mm+y2, mm+dd+y2])
    elif len(digits) in (4, 2):
        variants.add(digits)
    elif digits:
        variants.add(digits)
        if len(digits) >= 4:
            variants.update([digits[:4], digits[-4:]])
        if len(digits) >= 2:
            variants.update([digits[:2], digits[-2:]])
    return sorted(v for v in variants if v)


def casing_variants(s: str) -> Set[str]:
    if not s:
        return set()
    out = {s, s.lower(), s.upper(), s.capitalize(), s.title()}
    if len(s) > 1:
        out.add("".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)))
        out.add("".join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(s)))
    out.add(s[0].upper() + s[1:].lower())
    parts = s.split()
    if parts:
        initials = "".join(p[0] for p in parts)
        out.update([initials, initials.lower(), initials.upper()])
    return out


def leet_variants(s: str) -> Set[str]:
    subs = {
        "a": ["4", "@"], "e": ["3"], "i": ["1", "!"], "o": ["0"],
        "s": ["5", "$"], "t": ["7", "+"], "l": ["1"], "g": ["9"],
        "b": ["8"], "z": ["2"],
    }
    out = {s}
    for i, ch in enumerate(s.lower()):
        if ch in subs:
            for sub in subs[ch]:
                out.add(s[:i] + sub + s[i+1:])
    positions = [(i, ch) for i, ch in enumerate(s.lower()) if ch in subs]
    if len(positions) >= 2:
        for combo in itertools.combinations(positions[:4], 2):
            tmp = list(s)
            for idx, ch in combo:
                tmp[idx] = subs[ch][0]
            out.add("".join(tmp))
    return out


def double_chars(s: str) -> Set[str]:
    return {s[:i] + s[i] + s[i:] for i in range(len(s))}


def field_variants(field_name: str, value: str,
                   enable_leet: bool = False,
                   enable_advanced: bool = False) -> Set[str]:
    if not value:
        return set()
    key = field_name.lower()
    base: set = set()

    if key in ("birthdate", "anniversary", "dob", "date"):
        base.update(normalize_date(value))
    elif key == "age":
        base.add(re.sub(r"\D", "", value))
    else:
        clean = re.sub(r"[^A-Za-z0-9 ]+", "", value)
        parts = clean.split()
        if not parts:
            return set()
        base.add("".join(parts))
        base.update(parts)
        if len(parts) > 1:
            base.add("".join(p[0] for p in parts))
            base.add("".join(p[0] for p in reversed(parts)))

    final: set = set()
    for v in base:
        for c in casing_variants(v):
            final.add(c)
            if enable_leet:
                final.update(leet_variants(c))
            if enable_advanced:
                final.add(c[::-1])
                if len(c) <= 6:
                    final.update(list(double_chars(c))[:5])
    return final


# ── Generation core ────────────────────────────────────────────────────────────

def generate_single_field_variants(fields: Dict[str, str],
                                    enable_leet: bool,
                                    enable_advanced: bool) -> List[str]:
    out = []
    for k, v in fields.items():
        out.extend(field_variants(k, v, enable_leet, enable_advanced))
    return out


def generate_combinations(fields: Dict[str, str],
                           separators: List[str],
                           num_fields: int,
                           order_matters: bool,
                           enable_leet: bool,
                           enable_advanced: bool) -> List[str]:
    items = [(k, v) for k, v in fields.items() if v]
    if len(items) < num_fields:
        return []

    combos = (itertools.permutations(items, num_fields)
              if order_matters
              else itertools.combinations(items, num_fields))

    out = []
    for n, combo in enumerate(combos):
        if n >= 10000:
            break
        vlists = [list(field_variants(k, v, enable_leet, enable_advanced))[:20]
                  for k, v in combo]
        for vc in itertools.product(*vlists):
            for sep in separators:
                out.append(sep.join(vc))
    return out


def filter_by_length(candidates: List[str],
                     exact: Optional[int] = None,
                     min_len: Optional[int] = None,
                     max_len: Optional[int] = None) -> List[str]:
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


def dedup(lst: List[str]) -> List[str]:
    seen: set = set()
    out = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


# ── Patterns & extras ─────────────────────────────────────────────────────────

def generate_common_patterns() -> List[str]:
    patterns: List[str] = []
    patterns.extend(["123", "1234", "12345", "123456", "1234567", "12345678"])
    patterns.extend(["qwerty", "qwertz", "azerty", "asdf", "asdfgh"])
    patterns.extend(["password", "pass", "passwd", "letmein", "welcome"])
    patterns.extend(["admin", "root", "user", "test", "guest"])
    patterns.extend(["master", "super", "default", "changeme"])
    for year in range(1950, 2026):
        patterns.append(str(year))
        patterns.append(str(year)[2:])
    suffixes = ["!", "!!", "123", "1", "01", "2024", "2025", "@", "#"]
    prefixes = ["!", "@", "#", "$"]
    for w in ["password", "pass", "admin", "root", "user", "test"]:
        for s in suffixes:
            patterns.append(w + s)
        for p in prefixes:
            patterns.append(p + w)
    return patterns


def generate_year_range(start: int, end: int) -> List[str]:
    out = []
    for y in range(start, end + 1):
        out.append(str(y))
        out.append(str(y)[2:])
    return out


def add_special_char_variants(base: str) -> Set[str]:
    chars = ["!", "@", "#", "$", "%", "^", "&", "*"]
    out = {base}
    for c in chars:
        out.add(base + c)
        out.add(c + base)
    out.update([base + "!", base + "!!", base + "123"])
    return out


def load_dictionary(filepath: str) -> List[str]:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}Error loading dictionary: {e}{RESET}")
        return []


def calculate_statistics(words: List[str]) -> dict:
    if not words:
        return {}
    lengths = [len(w) for w in words]
    cc = Counter()
    for w in words:
        cc.update(w.lower())
    return {
        "total": len(words),
        "unique": len(set(words)),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "avg_length": sum(lengths) / len(lengths),
        "length_dist": Counter(lengths),
        "char_dist": cc.most_common(10),
    }


# ── Menu display ───────────────────────────────────────────────────────────────

def show_menu(fields: Dict[str, str], generated: List[str], extra_words: List[str]):
    print(BANNER)
    print(f"\n{CYAN}═══════════════════ MAIN MENU ═══════════════════{RESET}")
    print(f"{CYAN}─────────────────────────────────────────────────{RESET}")
    print(f"  {CYAN}1{RESET}  Add / edit fields")
    print(f"  {CYAN}2{RESET}  ► Execute wordlist generation")
    print(f"  {CYAN}3{RESET}  Settings  (leet / separators / length / advanced)")
    print(f"  {CYAN}4{RESET}  Preview results")
    print(f"  {CYAN}5{RESET}  Export to file")
    print(f"  {CYAN}6{RESET}  Add common patterns")
    print(f"  {CYAN}0{RESET}  Exit")
    print(f"{CYAN}═════════════════════════════════════════════════{RESET}")


# ── Flow functions ─────────────────────────────────────────────────────────────

def flow_add_fields(fields: Dict[str, str]):
    print(f"\n{CYAN}── Add / Edit Fields ──────────────────────────────{RESET}")
    print(f"{YELLOW}  add <value>   to add a field.")
    print(f"  del <value>   to remove a field.")
    print(f"  review        to see current fields.")
    print(f"  done          to return to menu.{RESET}\n")
    changed = False
    idx = max(fields.keys(), key=lambda k: int(k) if k.isdigit() else 0, default="0")
    counter = int(idx) + 1 if idx.isdigit() else len(fields) + 1
    while True:
        line = ask(f"{CYAN}  >{RESET} ").strip()
        if not line:
            continue
        low = line.lower()
        if low == "done":
            break
        if low == "review":
            if not fields:
                print(f"{YELLOW}  No fields yet.{RESET}")
            else:
                print(f"\n{CYAN}  Current fields:{RESET}")
                for v in fields.values():
                    print(f"    {MAGENTA}•{RESET} {WHITE}{v}{RESET}")
                print()
            continue
        if low.startswith("add "):
            v = line[4:].strip()
            if not v:
                print(f"{RED}  Nothing to add.{RESET}")
                continue
            k = str(counter)
            counter += 1
            fields[k] = v
            print(f"{GREEN}  Added:{RESET} {WHITE}{v}{RESET}")
            changed = True
            continue
        if low.startswith("del "):
            target = line[4:].strip().lower()
            match = next((k for k, val in fields.items() if val.lower() == target), None)
            if match:
                print(f"{GREEN}  Removed '{fields[match]}'{RESET}")
                del fields[match]
                changed = True
            else:
                print(f"{RED}  Not found: {target}{RESET}")
            continue
        print(f"{RED}  Unknown command. Use add, del, review, or done.{RESET}")
    return changed


def flow_review_fields(fields: Dict[str, str]):
    if not fields:
        print(f"{YELLOW}  No fields yet.{RESET}")
        return
    print(f"\n{CYAN}── Current Fields ─────────────────────────────────{RESET}")
    for i, (k, v) in enumerate(fields.items(), 1):
        print(f"  {i}. {MAGENTA}{k}{RESET} = {WHITE}{v}{RESET}")
    cmd = ask(f"\n{CYAN}  Type  del <key>  to remove, or Enter to go back: {RESET}").strip()
    if cmd.lower().startswith("del "):
        k = cmd[4:].strip().lower()
        if k in fields:
            del fields[k]
            print(f"{GREEN}  Removed '{k}'{RESET}")
        else:
            print(f"{RED}  Key not found: {k}{RESET}")


def flow_execute(fields: Dict[str, str],
                 settings: dict,
                 extra_words: List[str]) -> List[str]:
    if not fields:
        print(f"{RED}  No fields set — use option 1 to add values first.{RESET}")
        return []

    t0 = time.time()
    candidates: List[str] = []

    # Step 1 — single-field variants
    sv = generate_single_field_variants(fields,
                                        settings["enable_leet"],
                                        settings["enable_advanced"])
    candidates.extend(sv)

    # Step 2 — multi-field combinations (only if enabled and enough fields)
    if settings.get("combine_fields", True):
        if len(fields) >= settings["num_fields"]:
            cv = generate_combinations(fields,
                                       settings["separators"],
                                       settings["num_fields"],
                                       settings["order_matters"],
                                       settings["enable_leet"],
                                       settings["enable_advanced"])
            candidates.extend(cv)

    # Step 3 — extra patterns / dictionary
    if extra_words:
        candidates.extend(extra_words)

    # Step 4 — dedup + length filter
    unique = dedup(candidates)
    filtered = filter_by_length(unique,
                                settings["exact_length"],
                                settings["min_length"],
                                settings["max_length"])

    print(f"\n  {GREEN}✓ {len(filtered)} words generated.{RESET}")
    return filtered


def flow_settings(settings: dict):
    print(f"\n{CYAN}── Settings ───────────────────────────────────────{RESET}")
    print(f"  Combine fields   : {YELLOW}{settings['combine_fields']}{RESET}")
    print(f"  Separators       : {YELLOW}{settings['separators']}{RESET}")
    print(f"  Fields to combine: {YELLOW}{settings['num_fields']}{RESET}")
    print(f"  Order matters    : {YELLOW}{settings['order_matters']}{RESET}")
    print(f"  Leet speak       : {YELLOW}{settings['enable_leet']}{RESET}")
    print(f"  Advanced         : {YELLOW}{settings['enable_advanced']}{RESET}")
    print(f"  Exact length     : {YELLOW}{settings['exact_length']}{RESET}")
    print(f"  Min length       : {YELLOW}{settings['min_length']}{RESET}")
    print(f"  Max length       : {YELLOW}{settings['max_length']}{RESET}")
    print(f"{YELLOW}  (Press Enter on any prompt to keep current value){RESET}\n")

    cb = ask(f"  Combine fields? (y/n) — OFF = single-field variants only: ").strip().lower()
    if cb in ("y", "n"):
        settings["combine_fields"] = cb == "y"

    s = ask(f"  Separators (comma-sep, use '' for empty e.g. '',_,-): ").strip()
    if s:
        settings["separators"] = [
            ("" if p.strip().lower() in ("''", '""', "none", "") else p.strip())
            for p in s.split(",")
        ]

    n = ask(f"  Fields to combine (1-4): ").strip()
    if n.isdigit() and 1 <= int(n) <= 4:
        settings["num_fields"] = int(n)

    o = ask(f"  Order matters? (y/n): ").strip().lower()
    if o in ("y", "n"):
        settings["order_matters"] = o == "y"

    l = ask(f"  Enable leet speak? (y/n): ").strip().lower()
    if l in ("y", "n"):
        settings["enable_leet"] = l == "y"

    a = ask(f"  Enable advanced transforms? (y/n): ").strip().lower()
    if a in ("y", "n"):
        settings["enable_advanced"] = a == "y"

    ex = ask(f"  Exact length (number, or 'clear'): ").strip()
    if ex.isdigit():
        settings["exact_length"] = int(ex)
    elif ex.lower() in ("clear", "none", "reset"):
        settings["exact_length"] = None

    mn = ask(f"  Min length (number, or 'clear'): ").strip()
    if mn.isdigit():
        settings["min_length"] = int(mn)
    elif mn.lower() in ("clear", "none", "reset"):
        settings["min_length"] = None

    mx = ask(f"  Max length (number, or 'clear'): ").strip()
    if mx.isdigit():
        settings["max_length"] = int(mx)
    elif mx.lower() in ("clear", "none", "reset"):
        settings["max_length"] = None

    print(f"\n  {GREEN}✓ Settings saved.{RESET}")


def flow_preview(generated: List[str]):
    if not generated:
        print(f"{YELLOW}  Nothing generated yet — run option 3 first.{RESET}")
        return
    raw = ask(f"  How many to preview? (default 50): ").strip()
    n = int(raw) if raw.isdigit() else 50
    print(f"\n{CYAN}── Preview (first {n} of {len(generated)}) ────────────────{RESET}")
    for i, w in enumerate(generated[:n], 1):
        print(f"  {i:4}: {MAGENTA}{w}{RESET}")
    if len(generated) > n:
        print(f"  {YELLOW}... and {len(generated) - n} more{RESET}")


def flow_export(generated: List[str]):
    if not generated:
        print(f"{YELLOW}  Nothing to export — run option 3 first.{RESET}")
        return
    out_dir = ensure_output_dir()
    raw = ask(f"  Filename (default: wordlist.txt): ").strip()
    fname = os.path.basename(raw) if raw else "wordlist.txt"
    if not fname.endswith(".txt"):
        fname += ".txt"
    full = os.path.join(out_dir, fname)
    try:
        with open(full, "w", encoding="utf-8") as f:
            f.write("\n".join(generated) + "\n")
        print(f"  {GREEN}✓ Saved {len(generated)} words → '{full}'{RESET}")
    except Exception as e:
        print(f"  {RED}Error saving file: {e}{RESET}")


def flow_add_patterns(extra_words: List[str]):
    print(f"\n{CYAN}── Add Common Patterns ────────────────────────────{RESET}")
    print(f"  {CYAN}1{RESET}  Common passwords (123, qwerty, password…)")
    print(f"  {CYAN}2{RESET}  Year range")
    print(f"  {CYAN}3{RESET}  Custom pattern")
    print(f"  {CYAN}0{RESET}  Back")
    c = ask(f"\n  Choice: ").strip()
    if c == "1":
        p = generate_common_patterns()
        extra_words.extend(p)
        print(f"  {GREEN}✓ Added {len(p)} patterns{RESET}")
    elif c == "2":
        s = ask("  Start year (default 1950): ").strip()
        e = ask("  End year   (default 2025): ").strip()
        years = generate_year_range(
            int(s) if s.isdigit() else 1950,
            int(e) if e.isdigit() else 2025,
        )
        extra_words.extend(years)
        print(f"  {GREEN}✓ Added {len(years)} year entries{RESET}")
    elif c == "3":
        p = ask("  Enter pattern: ").strip()
        if p:
            extra_words.append(p)
            extra_words.extend(casing_variants(p))
            print(f"  {GREEN}✓ Added pattern + casing variants{RESET}")


def flow_load_dictionary(extra_words: List[str]):
    path = ask("  Dictionary file path: ").strip()
    if not path:
        return
    if not os.path.exists(path):
        print(f"  {RED}File not found: {path}{RESET}")
        return
    words = load_dictionary(path)
    if words:
        extra_words.extend(words)
        print(f"  {GREEN}✓ Loaded {len(words)} words{RESET}")


def flow_statistics(generated: List[str]):
    if not generated:
        print(f"{YELLOW}  No words generated yet.{RESET}")
        return
    s = calculate_statistics(generated)
    print(f"\n{CYAN}── Statistics ─────────────────────────────────────{RESET}")
    print(f"  Total  : {YELLOW}{s['total']}{RESET}")
    print(f"  Unique : {YELLOW}{s['unique']}{RESET}")
    print(f"  Min len: {YELLOW}{s['min_length']}{RESET}")
    print(f"  Max len: {YELLOW}{s['max_length']}{RESET}")
    print(f"  Avg len: {YELLOW}{s['avg_length']:.1f}{RESET}")
    print(f"\n{CYAN}  Length distribution (top 10):{RESET}")
    for length, count in s["length_dist"].most_common(10):
        bar = "█" * min(40, count // max(1, s["total"] // 40))
        print(f"    {length:3} chars: {bar} {count}")
    print(f"\n{CYAN}  Top characters:{RESET}")
    for ch, count in s["char_dist"]:
        print(f"    '{ch}': {count}")


def flow_shuffle(generated: List[str]) -> List[str]:
    if not generated:
        print(f"{YELLOW}  Nothing to shuffle.{RESET}")
        return generated
    result = generated.copy()
    random.shuffle(result)
    print(f"  {GREEN}✓ Shuffled {len(result)} words{RESET}")
    return result


def flow_advanced_transforms(generated: List[str]) -> List[str]:
    if not generated:
        print(f"{YELLOW}  Nothing to transform — run option 3 first.{RESET}")
        return generated
    print(f"\n{CYAN}── Advanced Transformations ───────────────────────{RESET}")
    print(f"  {CYAN}1{RESET}  Special char suffixes  (!@#$…)")
    print(f"  {CYAN}2{RESET}  Reverse all words")
    print(f"  {CYAN}3{RESET}  Year suffixes (2020-2025)")
    print(f"  {CYAN}4{RESET}  Number suffixes (1-100)")
    print(f"  {CYAN}0{RESET}  Back")
    c = ask("\n  Choice: ").strip()

    new: List[str] = []
    if c == "1":
        for w in generated[:1000]:
            new.extend(add_special_char_variants(w))
        print(f"  {GREEN}✓ Added {len(new)} special-char variants{RESET}")
    elif c == "2":
        new = [w[::-1] for w in generated]
        print(f"  {GREEN}✓ Added {len(new)} reversed words{RESET}")
    elif c == "3":
        for w in generated[:500]:
            for y in range(2020, 2026):
                new.append(w + str(y))
                new.append(w + str(y)[2:])
        print(f"  {GREEN}✓ Added {len(new)} year variants{RESET}")
    elif c == "4":
        for w in generated[:200]:
            for num in range(1, 101):
                new.append(w + str(num))
        print(f"  {GREEN}✓ Added {len(new)} number variants{RESET}")
    else:
        return generated

    return dedup(generated + new)


# ── Main loop ──────────────────────────────────────────────────────────────────

def main():
    fields: Dict[str, str] = {}
    settings = {
        "separators":      ["", ".", "_", "-"],
        "combine_fields":  True,
        "num_fields":      2,
        "order_matters":   True,
        "enable_leet":     False,
        "enable_advanced": False,
        "exact_length":    None,
        "min_length":      None,
        "max_length":      None,
    }
    generated: List[str] = []
    extra_words: List[str] = []

    ensure_output_dir()

    while True:
        show_menu(fields, generated, extra_words)
        cmd = ask(f"\n{YELLOW}  Select option (0-6): {RESET}").strip()

        if cmd == "1":
            changed = flow_add_fields(fields)
            if changed and fields:
                print(f"\n{CYAN}  ↻ Auto-updating wordlist…{RESET}")
                generated = flow_execute(fields, settings, extra_words)
        elif cmd == "2":  generated = flow_execute(fields, settings, extra_words)
        elif cmd == "3":  flow_settings(settings)
        elif cmd == "4":  flow_preview(generated)
        elif cmd == "5":  flow_export(generated)
        elif cmd == "6":  flow_add_patterns(extra_words)
        elif cmd == "0":
            print(f"\n{MAGENTA}  Goodbye! Happy pentesting!{RESET}\n")
            sys.exit(0)
        else:
            print(f"  {RED}Unknown option — choose 0 to 6.{RESET}")

        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}  Interrupted.{RESET}\n")
        sys.exit(0)
