# NoPM

As an individual contributor, I hate performance management. I want to build new stuff, not be a hype man for stuff I already built. 

In an ideal world, people leaders would just advocate on our behalf, but we need to support them in that role. We need to provide them with ammunition.

That's the rationale behind NoPM, a suite of tools for automating performance management so that we can go back to doing what we love: building stuff.

## Installation

```
python -m pip install git+https://github.com/droctothorpe/nopm.git
```

## Usage

For usage, you will need to define a model configuration file. Here is an example one using an Ollama cloud model, you can see more example configs [below](#model-configuration-files).

```yaml
provider: ollama
model: gpt-oss:120b-cloud
# https://docs.ollama.com/api/generate
method: generate
```

Since this is using an [Ollama](https://github.com/ollama/ollama) cloud model we will need to do three things:
1. Install the ollama python sdk: `python -m pip install ollama`.
2. Start an ollama server via `ollama serve` or starting the desktop application.
3. Sign into an Ollama account via `ollama signin`.

Then we can run our tooling

```bash
nopm figure model.yml description.md --output-file nopm_figure.svg
```

## Usage

```bash
export GITHUB_TOKEN=<your-github-token>
export ANTHROPIC_API_KEY=<your-anthropic-api-key>
nopm --gh-user droctothorpe --name "Alexander Perlman" --start-date 01/01/2025
```

The resulting markdown file is available in the nopm-output directory.

## Model configuration files

### Ollama

- [Models](https://ollama.com/search)

```bash
python -m pip install ollama

# For pulling local models
ollama pull codellama:7b
ollama pull codegemma:2b
```

```yaml
provider: ollama
model: gpt-oss:120b-cloud
# https://docs.ollama.com/api/generate
method: generate
```

```bash
python -m pip install openai
```

### OpenAI

```yaml
provider: openai
client:
    api_key: <your-openai-api-key>
model: gpt-4o
```

## Development setup

Create an environment and install this package:

```bash
# Via uv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Via conda
conda create --name nopm python
conda activate nopm
python -m pip install -e ".[dev]"
```

Run tests

```bash
# Currently most tests use ollama cloud models, so login
ollama signin

# Run tests
python -m pytest tests
# Run tests with cli (will repeat same queries through a subprocess)
python -m pytest tests --cli
```

## References
- Ollama
    - Models: https://ollama.com/search
    - Cloud Usage: https://ollama.com/settings