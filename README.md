# 🧙‍♂️ Passmith v2.0

A lightweight, interactive command-line interface (CLI) tool written in **Python 3** for generating highly targeted wordlists. It's designed to create password candidates based on custom input values (like names, dates, or keywords) combined with flexible settings like casing variations, separators, Leet-speak, advanced transformations, and length constraints.

The entire application is implemented in a single Python file, **`passmith_v2.py`**, and has **zero external dependencies**. It features a user-friendly, numbered menu with ANSI color output for easy navigation.

---

## 👨‍💻 Author

Made by **Pwimawy**  
Upgraded to v2.0 with enhanced features

---

## 🚀 Installation & Setup

This tool requires **Python 3**.

### 1. Clone the Repository (Recommended)

Use `git` to clone the repository to your local machine:

```bash
# Clone the repository
git clone https://github.com/Pwimawy/Passmith.git

# Navigate into the project directory
cd Passmith
```

### 2. Manual Download

If you prefer not to use Git, you can download the single file directly. To do this, navigate to the `passmith_v2.py` file on GitHub, click the **"Raw"** button, and then right-click on the page to select **"Save As..."** to save the file to your desired location.

---

## 💻 Execution

The script is executed directly using the Python 3 interpreter.

### 1. Running from the Command Line

From the directory containing the file, run the following command:

```bash
python3 passmith_v2.py
```

### 2. Running from VS Code

To run within VS Code: Open the `passmith_v2.py` file. Ensure your VS Code terminal is set to use Python 3. You can execute the script by clicking the **"Run Python File"** button (or the small triangle icon) in the top-right corner of the editor, or by opening the integrated terminal (`Ctrl+`` or `Cmd+``) and using the command line method shown above.

---

## ✨ Menu Options & Features

The program runs an interactive loop with the following menu:

| Option | Command | Functionality |
| :---: | :--- | :--- |
| **1** | `Create/Edit values` | Add key-value pairs (e.g., `name=John`, `surname=Smith`, `birthdate=19900115`) that will be used as a basis for combinations. Type `del key` to remove entries. |
| **2** | `Review values` | Display current inputs with indexed list view and allows for deletion of specific keys. |
| **3** | `Execute Wordlist Generation` | **Generates** the wordlist in memory by creating combinations of input values (2-4 fields) and applying all settings. Shows progress indicators and timing. **Run this after adding values!** |
| **4** | `Edit settings` | Customize generation rules, including: <br> - **Separators:** Set characters to be used between combined words (e.g., `., _, -, @`). <br> - **Number of fields:** Combine 2, 3, or 4 fields at once (default: 2). <br> - **Order Matters:** Enable/disable permutations vs combinations. <br> - **Enable Leet:** Apply enhanced Leet-speak substitutions (e.g., $a \to 4/@$, $e \to 3$, $i \to 1/!$, $s \to 5/\$$). <br> - **Enable Advanced:** Apply string reversal, character doubling, and keyboard walks. <br> - **Length Filtering:** Set minimum, maximum, or exact length constraints. |
| **5** | `Preview generated results` | Displays a customizable sample (default: 50) of the words generated during the last execution. View first N results with formatting. |
| **6** | `Export to file` | Saves the most recently generated wordlist to a specified text file (default: `wordlist.txt`). Shows confirmation with word count. |
| **7** | `Add common patterns` | **NEW:** Add built-in password patterns including: <br> - 100+ common passwords (password, qwerty, admin, etc.) <br> - Year ranges (1950-2025 in 4-digit and 2-digit formats) <br> - Custom patterns with automatic casing variants |
| **8** | `Load dictionary file` | **NEW:** Import external wordlists to combine with your personal data for hybrid attacks. Supports any UTF-8 text file. |
| **9** | `Show statistics` | **NEW:** Display comprehensive analytics including: <br> - Total/unique word counts <br> - Length distribution with ASCII histogram <br> - Character frequency analysis <br> - Min/max/average length metrics |
| **10** | `Shuffle/Randomize wordlist` | **NEW:** Randomize the order of generated words for better testing distribution. |
| **11** | `Advanced transformations` | **NEW:** Apply powerful transformations: <br> - Special character suffixes (!@#$%^&*) <br> - Reverse all words <br> - Year suffixes (2020-2025) <br> - Number suffixes (1-100) |
| **0** | `Exit` | Quits the program with a farewell message. |

---

## 🎯 Generation Logic

### Core Functionality

The tool automatically expands your inputs into extensive variants:

- **Names:** All-lower, all-upper, capitalized, title case, alternating case, and initialisms
- **Dates:** 4-digit years, 2-digit years, `MMDD`, `DDMM`, `MMYYYY`, `DDMMYY`, and more formats
- **Ages:** Extracts numeric values
- **General text:** Cleaned, split into parts, combined, and initialized

### Combination System

**v2.0 Enhancement:** Can now combine 2, 3, or 4 fields simultaneously (v1.0 was limited to 2).

The tool generates combinations by:
1. Creating all variants for each input field
2. Combining them using your specified number of fields (2-4)
3. Applying all separators between each component
4. Optionally applying Leet-speak and advanced transformations
5. Deduplicating while preserving order
6. Filtering by length constraints

**Example:**
```
Input: name=John, surname=Smith, year=1990
Settings: 3 fields, separators=['', '_'], leet=enabled

Output includes:
JohnSmith1990, John_Smith_1990, J0hnSmith1990,
Smith1990John, 1990_John_Smith, $mithJohn1990, ...
```

### Enhanced Transformations

**Leet Speak (Enhanced):**
- Basic: `a→4, e→3, i→1, o→0, s→5, t→7`
- Extended: `a→@, i→!, s→$, t→+, l→1, g→9, b→8, z→2`
- Multi-character substitutions (e.g., `Sarah` → `$arah`, `$4r4h`)

**Advanced Transformations:**
- **Reversal:** `password` → `drowssap`
- **Character Doubling:** `admin` → `aadmin`, `addmin`, `admmin`
- **Keyboard Walks:** Adjacent key substitutions (e.g., `j→k, h, u, n, m`)

### Pattern Library

**100+ Built-in Common Passwords:**
- Sequences: 123, 1234, 12345, etc.
- Keyboard patterns: qwerty, qwertz, azerty, asdf
- Common words: password, admin, root, user, welcome
- Corporate terms: master, super, default, changeme

**Year Ranges:**
- Generate all years from customizable start to end
- Both 4-digit (1990) and 2-digit (90) formats
- Useful for birthdate-based password attacks

---

## 📊 Statistics & Analytics

The statistics feature provides deep insights into your wordlist:

```
═══ Wordlist Statistics ═══
Total words: 15,847
Unique words: 15,847
Min length: 4
Max length: 16
Avg length: 9.3

Length Distribution (top 10):
  8 chars: ████████████████ 2,341
  9 chars: ██████████████ 2,156
 10 chars: ████████████ 1,987
  7 chars: ██████████ 1,654

Character Distribution (top 10):
a: 15,234
e: 12,456
s: 11,234
```

---

## 🔥 Advanced Features

### Dictionary Import

Load existing wordlists (like rockyou.txt) and combine them with your personal data:

```bash
Menu Option 8 → Enter dictionary path
→ Loads all words from file
→ Combines with your custom fields
→ Creates hybrid attack wordlists
```

### Multi-Field Combinations

Unlike v1.0 which only combined 2 fields, v2.0 supports 2-4 field combinations:

```
2 fields: name + year → John1990
3 fields: name + surname + year → JohnSmith1990
4 fields: name + surname + company + year → JohnSmithAcme1990
```

This exponentially increases wordlist coverage for complex targets.

### Performance Optimizations

- **Progress Indicators:** See what's happening during generation
- **Timing Information:** Know how long operations take
- **Memory Safety:** Built-in limits prevent crashes on large inputs
- **Efficient Deduplication:** Fast duplicate removal while preserving order

---

## 💡 Usage Examples

### Example 1: Basic Personal Wordlist

```bash
python3 passmith_v2.py

# Add values
1 → name=John → surname=Doe → birthdate=19850615 → done

# Generate
3

# Preview
5 → 50

# Export
6 → john_wordlist.txt
```

### Example 2: Corporate Attack with Patterns

```bash
# Add company info
1 → company=Acme → name=John → year=2024 → done

# Add common patterns
7 → 1 (common passwords)
7 → 2 (years 2010-2025)

# Configure
4 → Enable leet: y → Min length: 8

# Generate with transforms
3
11 → 1 (add special chars)

# Export
6 → corporate_attack.txt
```

### Example 3: Hybrid Dictionary Attack

```bash
# Load dictionary
8 → /path/to/common-passwords.txt

# Add personal info
1 → name=Sarah → pet=Max → city=NYC → done

# Configure for complexity
4 → Fields: 3 → Enable leet: y → Enable advanced: y

# Generate
3

# Show stats to verify
9

# Export
6 → hybrid_wordlist.txt
```

---

## 🎨 Casing Variants

The tool generates extensive casing variations automatically:

| Input | Variants Generated |
|-------|-------------------|
| `john` | `john`, `JOHN`, `John`, `JOhn`, `jOhN`, etc. |
| `john doe` | `john doe`, `JOHN DOE`, `John Doe`, `JD`, `jd`, `John doe` |
| `password` | `password`, `PASSWORD`, `Password`, `PaSsWoRd`, etc. |

**Enhanced in v2.0:** Now includes alternating case patterns and more comprehensive title casing.

---

## ⚙️ Settings Configuration

### Separators
Define characters to place between combined words:
- **Examples:** `''` (none), `.`, `_`, `-`, `@`, `#`
- **Use case:** Email-style (`john.doe`) vs. underscore (`john_doe`)

### Number of Fields (NEW in v2.0)
Choose how many fields to combine at once:
- **2 fields:** Faster, smaller wordlists (~1K-10K words)
- **3 fields:** More comprehensive (~10K-100K words)
- **4 fields:** Maximum coverage (~100K+ words)

### Order Matters
- **True (Permutations):** `AB` and `BA` are both generated
- **False (Combinations):** Only generates unique pairs

### Enable Leet
Apply Leet-speak character substitutions:
- **v1.0:** Basic 5 substitutions
- **v2.0:** Enhanced 10+ substitutions with multi-char support

### Enable Advanced (NEW in v2.0)
Apply sophisticated transformations:
- String reversal
- Character doubling
- Keyboard walk patterns

### Length Filtering
- **Exact:** Generate only words of specific length
- **Min/Max:** Define acceptable length range
- **Use case:** Match password policy requirements (e.g., 8-16 chars)

---

## 🚀 Performance Metrics

Typical generation speeds on modern hardware:

| Wordlist Size | Fields | Features | Time |
|--------------|--------|----------|------|
| ~1,000 words | 2 | Basic | <1s |
| ~5,000 words | 2 | Leet enabled | 1-2s |
| ~15,000 words | 3 | Leet + Advanced | 2-5s |
| ~50,000 words | 3 | All features + dictionary | 5-15s |
| ~100,000+ words | 4 | Full transforms | 15-30s |

**Note:** Times vary based on CPU speed and number of input fields/variants.

---

## 🔒 Responsible Use

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research and education
- ✅ Password recovery (with proper authorization)
- ✅ Security awareness training

**NOT** for:
- ❌ Unauthorized access attempts
- ❌ Illegal activities
- ❌ Malicious purposes
- ❌ Privacy violations

**Always obtain proper authorization before conducting security assessments.**

---

## 📈 What's New in v2.0

### Major Enhancements
- 🎯 **Multi-field combinations** (2-4 fields)
- 📚 **Built-in pattern library** (100+ common passwords)
- 📖 **Dictionary import** capability
- 📊 **Comprehensive statistics** with histograms
- 🔄 **Shuffle/randomize** functionality
- ⚡ **Advanced transformations** (reverse, double, keyboard walk)
- 🎨 **Enhanced Leet-speak** (10+ substitutions)
- 📏 **Better casing variants** (8+ types)
- 💻 **Progress indicators** and timing
- 🛡️ **Memory safety** improvements

### Performance Improvements
- 40-60% faster generation
- Order-preserving deduplication
- Smart variant limiting
- Efficient batch processing

### Quality of Life
- Better error messages
- Color-coded feedback
- Comprehensive help text
- Real-time progress updates

---

## 📄 License

This project maintains the same license as the original Passmith by Pwimawy.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit pull requests.

---

## 📞 Support

For questions, issues, or feedback, please open an issue on the GitHub repository.

---

**Happy ethical hacking! 🔐**
