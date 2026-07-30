# welcome to `learn_lang`!

[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff) 
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/connorwilloughby/learn_lang/checks.yml)
![Static Badge](https://img.shields.io/badge/%20https%3A%2F%2Fimg.shields.io%2Fbadge%2Fcoverage-5%25-red?label=coverage)
![Static Badge](https://img.shields.io/badge/~5.1GB-red?label=proj-size)

---

Want to learn a language? Hate paying for subscription services? Are you a nerd?

This repo can solve two of your three problems. This repo is a mid weight terminal application which lets you drill translations within your [target language](#active-development). The repo depends on some heavy models ~4GB which enable you to use this project locally, no API calls, no 3rd parties. 

As you can see from the activity on this project I have lots of free time so if youd like to hire me please get in touch [@connor-willougyby](https://www.linkedin.com/in/connor-willoughby/)


## getting started

If you have UV installed on your system then you can get stuck in with `sync` then running the entry point below.

```bash
uv sync
uv run src/main.py
```

## supported languages

| Source Language | Target Language | 
|----|---|
|English (🏴󠁧󠁢󠁥󠁮󠁧󠁿️) | Spanish(🇪🇸️)|

## language roadmap

Currently the main challenge with language support is the sourcing of standardized data for the various problem types. For the long term the source language will be English.

### active development

1. Español

### next up

1. Pусский

## credits

- [sentence_transformers](https://huggingface.co/sentence-transformers)
- [Tatoeba.org](https://tatoeba.org/en/downloads)
