# NoPM

As an individual contributor, I hate performance management. I want to build new stuff, not be a hype man for stuff I already built. 

In an ideal world, people leaders would just advocate on our behalf, but we need to support them in that role. We need to provide them with ammunition.

That's the rationale behind NoPM, a suite of tools for automating performance management so that we can go back to doing what we love: building stuff.


## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
export GITHUB_TOKEN=<your-github-token>
export ANTHROPIC_API_KEY=<your-anthropic-api-key>
nopm --gh-user droctothorpe --name "Alexander Perlman" --start-date 01/01/2025
```

The resulting markdown file is available in the nopm-output directory.