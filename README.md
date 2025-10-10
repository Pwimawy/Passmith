#🧙‍♂️ Passmith

A lightweight, interactive command-line interface (CLI) tool written in **Python 3** for generating highly targeted wordlists. It's designed to create password candidates based on custom input values (like names, dates, or keywords) combined with flexible settings like casing variations, separators, Leet-speak, and length constraints.

The entire application is implemented in a single Python file, **`passmith.py`**, and has **zero external dependencies**. It features a user-friendly, numbered menu with ANSI color output for easy navigation.

---

## 👨‍💻 Author

Made by **Pwimawy**

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

If you prefer not to use Git, you can download the single file directly. To do this, navigate to the `wordlist_generator_cli_menu.py` file on GitHub, click the **"Raw"** button, and then right-click on the page to select **"Save As..."** to save the file to your desired location.

---
## 💻 Execution

The script is executed directly using the Python 3 interpreter.

### 1. Running from the Command Line

From the directory containing the file, run the following command:
```bash
python3 passmith.py
```

### 2. Running from VS Code

To run within VS Code: Open the `passmith.py` file. Ensure your VS Code terminal is set to use Python 3. You can execute the script by clicking the **"Run Python File"** button (or the small triangle icon) in the top-right corner of the editor, or by opening the integrated terminal (`Ctrl+\`` or `Cmd+\``) and using the command line method shown above.

---
## ✨ Menu Options & Features

The program runs an interactive loop with the following menu:

| Option | Command | Functionality |
| :---: | :--- | :--- |
| **1** | `Create value` | Add key-value pairs (e.g., `name=John`, `lastname=Smith`) that will be used as a basis for combinations. |
| **2** | `Review values` | Display current inputs and allows for deletion of specific keys. |
| **3** | `Execute Wordlist` | **Generates** the wordlist in memory by creating two-item combinations of all input values and applying settings. **Run this first!** |
| **4** | `Edit settings` | Customize generation rules, including: <br> - **Separators:** Set characters to be used between combined words (e.g., `., _, -`, or `none`). <br> - **Order Matters:** Enable/disable $A-sep-B$ vs. $B-sep-A$. <br> - **Enable Leet:** Apply basic Leet-speak substitutions (e.g., $a \to 4$, $e \to 3$, $s \to 5$). <br> - **Length Filtering:** Set minimum, maximum, or exact length constraints. |
| **5** | `Preview generated results` | Displays a sample (default: 50) of the words generated during the last execution of option 3. |
| **6** | `Export to file` | Saves the most recently generated wordlist to a specified text file (default: `wordlist.txt`). |
| **0** | `Exit` | Quits the program. |

### Generation Logic

The tool automatically expands your inputs into common variants (e.g., a name is converted to all-lower, all-upper, capitalized, and initialisms; dates are converted to 4-digit, 2-digit, `MMDD`, `DDMM`, etc.). It then generates a list by combining these variants in pairs ($A-sep-B$) using all specified separators. The final list is deduplicated and filtered by length according to your settings.
