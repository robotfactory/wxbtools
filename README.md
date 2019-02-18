# wxbtools
Tools for playing Weather Battle (wxbattle)

## Disclaimer
These tools are intended to be helpful, but you still need to make your own decisions about how you play Weather Battle. Don't make a wager based solely on what these tools might or might not tell you.

## wxbparse.py
Takes plain text copy/pasted from a WeatherBattle.com battle page and turns it into something useful. Produces either json or csv output which you can then use in your favorite tools.

### Usage:
Select all the text (CTL+A) on a battle page, copy it (CTL+C), then paste it into a plain old text file (CTL+V). Save that text file. Then, run the script on it.

```
$ ./wxbparse.py -h
usage: wxbparse.py [-h] [-f FORMAT] input_file

Injests plain text from WXBattle and spits out pretty stuff

positional arguments:
  input_file            The file to injest

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Output to csv or json. (Default: csv)
```

### Example:
`wxbparse.py -f json input.txt`
