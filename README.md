# Clipcopy

A simple Windows command-line utility that copies standard input to the Windows clipboard.

## Features

- Copy text from standard input directly to the Windows clipboard.
- Supports Unicode text.
- Reads until end-of-file (EOF).
- Works well in command pipelines.

## Installation

## From release

Download the latest release from the [Releases page](https://github.com/Hoang-Long2012/Clipcopy/releases/latest), extract it, and run Clipcopy.exe.

### From source

```
git clone https://github.com/Hoang-Long2012/clipcopy.git
cd clipcopy\src
python clipcopy.py
```

### Build a standalone executable

```
pip install pyinstaller
pyinstaller --onefile clipcopy.py
```

## Usage

```
Clipcopy [-h] [-v]
```

The program reads all text from standard input and places it into the Windows clipboard.

## Examples

Copy the output of a command:

```
dir | Clipcopy
```

Copy the contents of a file:

```
Clipcopy < readme.txt
```

Type text manually and finish with EOF:

```
Clipcopy
Hello, world!
This text will be copied.
```

Press **Ctrl+Z**, then **Enter** to finish input.

## Exit Code

| Code | Meaning |
|------|---------|
| 0 | Success. |
| 2 | Failed to access or modify the clipboard. |

## Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show the help message and exit. |
| `-v`, `--version` | Show the program version and exit. |

## Notes

- Existing clipboard text will be replaced.
- Only Unicode text (`CF_UNICODETEXT`) is supported.
- Binary data and other clipboard formats are not supported.
- This utility is intended for Windows only.

## License

This project is licensed under the [MIT License](LICENSE).