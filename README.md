# tools
Some tools scripts for every things

# update_version.py
A python 3 script to read a version.cfg and update version numbers.
No check on compatibility are made.

See the code at src/update_versions.py

## Dependencies
```bash
pip install requests
pip install packaging
```

## Usage
```bash
Usage: update_versions.py [options]

This script update package version from version.cfg file if passed or from
stdin.                       The output is written to stdout by default or to
the file passed as argument.

Options:
  -h, --help            show this help message and exit
  -f VERSION_FILE_PATH, --file=VERSION_FILE_PATH
                        Path to the version.cfg file, default is stdin.
  -v, --verbose         Verbose mode.
  -o OUTPUT_FILE_PATH, --output=OUTPUT_FILE_PATH
                        Path to the output file, default is stdout.
```

## Tests 
move to the cloned directory and set the sources path as
```bash
export PYTHONPATH=$PYTHONPATH:`pwd`/src
```

move to src and launch :

python3 -m unittest discover

Or install pytest and pytest-cov :

python3 -m pytest
python3 -m pytest --cov=update_versions
