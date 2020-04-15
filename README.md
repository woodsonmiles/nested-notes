### Capabilities
Nestingnote is a platform-independent terminal-based text-editor for outlining. It's capable of creating collapsable nested lists and matrices ideal for organizing notes and data.

### Installation
- Windows
  1. [Download](https://github.com/woodsonmiles/nestingnote/raw/master/executable/Windows/nestingnote.exe)
- Linux (varies per distro)
  1. [Download](https://github.com/woodsonmiles/nestingnote/raw/master/executable/Linux/nestingnote)
  1. `chmod +x nestingnote`

### Controls
Most controls are intuitive, e.g., all printable keys insert that character, arrow keys, home, end, page up, and page down all move the cursor appropriately. However, there are a few special controls introduced by nestingnote:
- **Tab**: at the beginning of a line will indent the line, starting an inner nested list. Within the line, tab will split the line into fields similar to columns in a matrix.
- **Ctrl+k**: toggles whether the current item in the nested list is collapsed, meaning that all items nested beneath it are hidden.
- **Ctrl+w**: save the edits

### Pip alternative
  1. install nestingnote<br>
    `python3 -m pip install nestingnote`
  1. create alias (for convenience)<br>
    ```
    echo "alias nestingnote='python3 -m nestingnote'" >> ~/.bash_aliases
    source ~/.bash_aliasees
    ```    
  1. Execution
     ```python3 -m nestingnote \path\to\my\notes```
