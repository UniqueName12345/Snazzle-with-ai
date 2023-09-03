# Snazzle + AI

A better frontend for Scratch, built by the community, for the community. Oh, and native AI support is included. And also some restrictions are removed (like being able to pin any subforum at will)

Snazzle is the first attempt at a better Scratch website. It aims to be feature-rich and easy and quick to use, incorporating many things that the Scratch community has been wanting for years.

Basically, this is a Scratch website just for ~~MagicCrayon9342~~ power users.

> If you're more than a casual user of the Scratch website for whatever reason, then you'll like Snazzle.
> It's like a giant vat of coffee brewed with ingredients from the Scratch community.
-- Snazzle's homepage

## Contributing

Format your code with [Black](https://github.com/psf/black) and make a pull request. If there is a feature branch for what you are changing, make the PR to that branch instead of main.

## Running your own instance locally

Since Snazzle is very much still in development, this won't be representative of the final product's build steps.

But for now, this is how you do it:

1. Clone the repo
2. (optional but recommended) Create a Python virtual environment. Snazzle requires Python 3.8+. However, we recommend 3.11+ as this version has better error messages that will let us diagnose issues better if you submit a bug report.
3. Run `pip3 install -r requirements.txt`.
   > If you are on an Arch based linux distro, you will have to run `sudo pacman -S python-flask`
4. If you are using replit or something else blocked from Scratch's API, change the variable "REPLIT_MODE" at the top of `main.py` to True.
5. Once deps are installed, run `flask run --with-threads`. This will set up a Flask server at `127.0.0.1:5000`. If you find any bugs, please report them.
   > The `--with-threads` option is basically required if you want Snazzle to run fast.
7. Go to `127.0.0.1:5000` in your favourite browser and play around with it!

## Hosting on Replit

Hosting on Replit is impossible as Replit does not have enough memory to run OpenLLaMA (which is the model used).