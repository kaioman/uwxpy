# uwxpy

A Python toolkit for generating, editing, and posting AI-powered images to X using Uwgen API, Gemini Vision, and Tweepy.

**[日本語](README.md) | English**

## Overview

`uwxpy` is a Python library designed to streamline the workflow of AI image generation, prompt engineering, and automated posting to X (formerly Twitter). It integrates seamlessly with Uwgen API for image generation, Gemini Vision for prompt analysis/generation, and Tweepy for X integration.

## Features

- **AI Image Generation**: Connects with Uwgen API to create high-quality AI artworks.
- **Prompt Engineering**: Dynamic prompt generation and rewriting capabilities using Gemini models.
- **X (Twitter) Integration**: Easy-to-use posting functions leveraging Tweepy.
- **Structured Configurations**: Manage your application easily with structured JSON configuration files.

## Requirements

- Python 3.8+
- `libcore-hng`
- `pycorex`
- `tweepy`

## Installation

You can install this package via pip if it's available on PyPI, or locally from the source:

```bash
git clone https://github.com/kaioman/uwxpy.git
cd uwxpy
pip install .
```

## Configuration

Before running the toolkit, ensure you have your configuration files set up. You can find a sample configuration file at `configs/uwxpy.sample.json`.

1. Copy `configs/uwxpy.sample.json` to `configs/uwxpy.json`.
2. Fill in your API keys and application settings.

## Quick Start

Here is a basic example of how to initialize the application and use the library:

```python
import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger

# Initialize the application with your configuration files
app.init_app(__file__, "logger.json", "uwxpy.json")

app_logger.info("uwxpy application successfully initialized!")
```

### Prompt Generation Example

```python
from uwxpy.service.generate_prompt_service import GeneratePrompt

# Initialize the prompt generator with your data files
prompt_gen = GeneratePrompt(
    modes_path="tests/prompt/modes.json",
    word_path="tests/prompt/words_data.json",
    style_anchor_path="tests/prompt/style_anchor.json"
)

# Create a brand-new image generation prompt
prompt_request, elements = prompt_gen.create_rewrite_request(mode_key='chill', is_edit=False)
print(prompt_request)
```

## License

This project is licensed under the BSD-3-Clause License - see the LICENSE file for details.

## Author

- **unchainworks** ([kajin0318@gmail.com](mailto:kajin0318@gmail.com))
- [GitHub Repository](https://github.com/kaioman/uwxpy)
