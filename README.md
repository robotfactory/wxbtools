# wxbtools
Tools for playing Weather Battle (wxbattle)

## Disclaimer
These tools are intended to be helpful, but you still need to make your own decisions about how you play Weather Battle. Don't make a wager based solely on what these tools might or might not tell you.

## mxbparse.py
Takes plain text copy/pasted from a WeatherBattle.com battle page and turns it into something useful. Produces either json or csv output which you can then use in your favorite tools.

### Usage:
`mxbparse.py -f OUTPUT_FORMAT INPUT_FILE`

### Example:
`mxbparse.py -f json input.txt`
