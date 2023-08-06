# tridens_neptuni
A fork of Python-future that just provides py3 to py2 `pasteurize` with scalable fixer install/uninstall interface

## Why?
This is a lightweight fork of `python-future` that I tailored to my needs. When installed (`python -m setup.py bdist_wheel`)
it will expose a `neptunize` command which works almost exactly like `pasteurize`. Under the hood instead of using a
`set` to list the names of the `fixers` and requiring you to physically modify the file whenever you want to add or remove a fixer,
it looks for all fixer files in the `fixes` directory and uses them unless they are excluded on runtime (`--nofix` didn't work
for me as expected, so I fixed it). It also allows you to easily install new fixers (you can refer to the main project docs to see
how to make extra fixers) by exposing `--install` and `--uninstall` options (which under the hood simply copy the fixer files to
the package directory). The only requirement is that the file follows naming pattern: `fix_*.py`.

### But why tho?
I needed an extensible version of `pasteurize` to make sure differences to `IronPython` are handled and certain libraries
that don't work are replaced by something else. I didn't want the project I use this for to be written in old ugly 2.7 codebase,
but having to port stuff to `IronPython`, I decided to use a parser but some of the functionality didn't agree with `ipy`. Think of this
little fork as a way of fixing shortcomings of `pasteurize` regarding extensibility.

### Why this weird ugly name?
* *Tridens* -> Latin for *trident* -> like fork (lol) -> big thing made of steel -> steel is like better iron -> IronPython -> Illuminati Confirmed
* *Neptuni* -> Latin for *Neptune's* -> because someone has to hold the fork -> I myself prefer chopsticks

## What to look out for?
Be careful when installing this if you intend to use `pasteurize` along `neptunize`. It might not work because this project modifies
the `libpasteurize` package. I might provide a safer way to handle this in the future but that is the deal now.
Naturally, `future` itself is one of the dependencies listed in `setup.py` and many of the functionalities rely on `python-future`
(this specifically on version 0.18.2).

## Copyright notice
`python-future` is MIT-licensed. I left in the original LICENSE file, included only info about myself as the fork author.
If you wish to grab this specific copy and do something to it feel free to submit a pull request. If you fork it,
please consider licesing it under MIT, it helps the community of developers tremendously to be freely able to modify software
as they need. Many thanks to Ed Schofield and the team behind `python-future` for bringing these amazing features.
Believe it or not, some people still need to use them in 2020 and they are still very relevant.
