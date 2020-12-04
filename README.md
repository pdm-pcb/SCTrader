## SCTrader
SCTrader is a _very_ simple Python script, in the scriptiest sense of the word.
Plainly, all this code is doing is reading commodity prices from the wonderful
https://gallog.co/ and accounts for travel distances/times between bodies as
well as buying and selling times. The calculations are extremely rough on
purpose, and there's no accounting for atmospheric density, etc. There's also no
route planning, as this is more about single-ended trips.

### Requirements
* Python 3.9
* TKInter
* requests
* bs4

### Usage
Provided you've got Python3 and TKInter, you should be able to just run
`sctrade.py` and go from there. The Refresh button makes all the requests
you'll need until a value changes on the page, so press that once to get going.

Then select your ship (for the SCU value) and twiddle the other three variables
to your liking. Whenever you want, click Calculate to account for the changed
values.

The UI freezes up while it's making the HTTP requests, and that's more or less
purposeful so I don't blast gallog on accident. =)

Don't expect this to be robust or accurate! It might help some of you, and I'd
love to hear if it does. For now, though, it's just a tool for me to make
quicker trade decisions.

### License
MIT - https://choosealicense.com/licenses/mit/
