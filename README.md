# Obsidian Markdown organizer

## Overview

This tool automatically sorts Markdown (.md) files in the current directory into folders based on the tag information described in the YAML header at the beginning of each file, according to user-defined rules in `rules.yaml`.

## Features
- Flexible sorting of .md files based on tags in the YAML header
- Rules are written in YAML format and support logical expressions (and/or/not, parentheses)
- Actual file moving is performed using the `obsidian-cli` command
- Shows a summary of planned moves and asks for user confirmation before execution
- Written in Python, dependencies managed with venv

## rules.yaml Syntax

Write rules in `rules.yaml` as follows:

```yaml
rules:
  - name: rule-1
    when: tag:Ai and not tag:Business
    then: move to software/AI
  - name: rule-2
    when: tag:Graphics and not tag:Business
    then: move to software/CG
  - name: rule-3
    when: tag:Business
    then: move to business
  # ...
```

### Field Descriptions
- `name`: Rule identifier (any string)
- `when`: Condition. Write a logical expression (and, or, not, parentheses) to check for tags.
    - Example: `tag:Ai and not tag:Business`
    - Example: `tag:Software or tag:Electronics`
    - Example: `tag:Crafts and (tag:Art or tag:Handmade)`
- `then`: Action when matched. Write in the format `move to <folder name>`.

### Syntax for `when` Expressions
- Use `tag:<tagname>` to check for the presence of a tag
- Use `and`, `or`, `not` for logical operations
- Use parentheses `()` for grouping

#### Examples
- `tag:Ai and not tag:Business`
- `tag:Graphics or tag:Software`
- `tag:Crafts and (tag:Art or tag:Handmade)`

## Usage
1. Install required packages
   ```sh
   pip install -r requirements.txt
   ```
2. Edit the rule file (`rules.yaml`)
3. Place .md files in the current directory
4. Run the tool
   ```sh
   python obsidian-folder-organizer.py
   ```
5. Review the planned moves and enter `y` to execute

## Dependencies
- pyyaml
- lark

## Notes
- The [obsidian-cli](https://github.com/Yakitrak/obsidian-cli) command is required for file moving. Please install it in advance.

## License
- MIT license.
