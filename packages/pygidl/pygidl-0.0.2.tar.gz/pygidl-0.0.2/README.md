# Python Google Images Downloader

This tool lets you download results from Google Images pretty fast. It uses
[aiohttp](https://docs.aiohttp.org/en/stable/) under the hood. It is essentially
a Python 3.7 rewrite of
[google-images-downloader](https://github.com/hardikvasa/google-images-download)
without the restriction of not using external dependencies.

## Installation

The following should work to install the utility and check that it will run:

```bash
pip install pygidl
pygidl -h
```

## Basic Usage

From the command line:

basic usage is something like `pygidl "cats and dogs"`. This will create an
output directory in your current working directory named for the timestamp that
the command was run. Underneath that directory will be another directory with
the slugified version of your query string. Underneath that directory will be
the downloaded images, named by their sha256 hashes and file type extensions:

```bash
pygidl "cats and dogs"
tree .
.
└── 2020-01-21-17-57-34
    └── cats-and-dogs
        ├── 01d2dde343a45e3a1fcc5e7cd3cace33398c9b06a97e494d4329f264e57d5f57.jpg
        ├── 026cef34db26cbd5fa246bc720c1234b39ffa07737e43523b160390c13d5d3e6.jpeg
        ├── 03a0f2ebeed5d91acaed73ad303bd724767e101688e33d1a5557cca9139972d7.webp
        ├── 0affcf3198b40063e9302c4515380d6796946098c7c1c3c043072815e29e2770.jpeg
        ...
```


## Advanced Usage

The command can be configured to support several more complex query scenarios:

### Verbose Output

Use the `-v/--verbose` flag to change the log level to show more messages. The
log level is "WARNING" by default. Supplying `-v` once sets it to "INFO", and
two or more times sets it to "DEBUG".

### Prefixes and Suffixes

The `-p/--prefix` and `-s/--suffix` flags can be used to run multiple copies of
the same Google Images query with extra prefix or suffix strings. For example:

```bash
pygidl -p Andorra -p Angola -s "on a ship" -s "on a plane" flag
tree -d .
.
└── 2020-01-21-18-15-59
    ├── andorra-flag-on-a-plane
    ├── andorra-flag-on-a-ship
    ├── angola-flag-on-a-plane
    └── angola-flag-on-a-ship

5 directories
```

### Output Groups

You can override the name of the directory that contains the results of each
query with the `-g/--group` flag. For example:


```bash
pygidl -g "Cute Animals" -p fluffy -p adorable -s dog -s cat "" -v
tree . -d
.
└── cute-animals
    ├── adorable-cat
    ├── adorable-dog
    ├── fluffy-cat
    └── fluffy-dog

5 directories
```

### Face Search

You can tell Google Images to find faces with the `-f/--face` flag. For example:

```bash
pygidl -g "Tom Hanks" -p "" -p young "Tom Hanks" -s "" -s "Oscars" -f -v
tree -d .
.
└── tom-hanks
    ├── tom-hanks
    ├── tom-hanks-oscars
    ├── young-tom-hanks
    └── young-tom-hanks-oscars

5 directories
```

## Programmatic Usage

Something like the following should work (assuming you have `opencv-python`
installed in your environment):

```python
import asyncio
import os

import cv2

from pygidl import scrape_google_images


downloaded_image_paths = asyncio.run(
    scrape_google_images(
        base_query="cats and dogs",
        prefixes=["cute", "adorable"],
        suffixes=["playing", "running"],
        group="cute-animals",
        output_dir=os.getcwd(),
        face=False,
    )
)
for path in downloaded_image_paths:
    image = cv2.imread(path)
    if image is None:
        print(f"could not load image {path}")
        continue
    height, width = image.shape[:2]
    print(f"image {path} has size {width}x{height}")
```

## Known Issues and Limitations

- Only returns max of 100 results per query
- Doesn't support full range of advanced search options
- No tests
- No retries
- No report on results/metadata output option
- Sometimes Google returns results from a different template without
  easily-parseable metadata


## Contributing

I don't think anyone will ever get this far, but if you want to open a pull
request (or even better, take over ownership of the project for me!), go for it.
At a minimum, new code should have type hints, docstrings, and be auto-formatted
with `black` with an 80-character max line length. Even better would be some
tests and Sphinx documentation!
