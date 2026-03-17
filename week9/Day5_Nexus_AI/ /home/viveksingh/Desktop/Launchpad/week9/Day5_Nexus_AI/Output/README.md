# Name Repeater Script

This project contains a small Python utility that writes a provided name to a file five times.

## Usage

```bash
python main.py <name>
```

After running the command, an `output.txt` file will be created (or overwritten) in the current directory with the name repeated on separate lines.

## Example

```bash
$ python main.py Alice
Created output.txt with 'Alice' repeated five times.
$ cat output.txt
1. Alice
2. Alice
3. Alice
4. Alice
5. Alice
```

No external dependencies are required beyond the Python standard library.
