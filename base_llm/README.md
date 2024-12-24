# Base LLM

Base module for integrating Large Language Models (LLM) services in Odoo.

## Features

- Flexible LLM provider management
- Support for multiple LLM services (Groq, OpenAI, etc.)
- Model management with context lengths
- Configurable provider settings
- Easy integration with other modules

## Configuration

1. Go to Settings > Technical > LLM
2. Configure LLM provider settings:
   - API keys
   - Models
   - Default provider

## Usage

### LLM Provider Model

The module provides two main models:

1. `llm.provider` for managing providers:
```python
# Get default provider
provider = env["llm.provider"].get_default_provider()

# Process prompt
result = provider.process_prompt(
    prompt,
    response_format={"type": "json_object"},  # Optional for JSON output
    temperature=0.1,                          # Optional for response randomness
)
if result["success"]:
    content = result["content"]
else:
    error = result["error"]
```

2. `llm.model` for managing LLM models:
```python
# Get available models for provider type
models = env["llm.model"].search([
    ("provider_type", "=", "groq"),
    ("active", "=", True)
])
```

### Extend Provider Types

1. Create new provider model inheriting `llm.provider`
2. Implement `_process_[provider_type]` method
3. Add provider type to selection field

Example:
```python
class CustomProvider(models.Model):
    _inherit = "llm.provider"

    def _process_custom(self, prompt, **kwargs):
        # Implement custom LLM processing
        return {
            "success": True,
            "content": "Generated text",
        }
```

### Available Models

The module comes with pre-configured models for different providers:

#### Groq Models
- LLaMA 3.3 70B Versatile (128k context)
- Mixtral 8x7B (32k context)
- Gemma 2 9B Instruct (8k context)
- LLaMA 3 70B (8k context)
- LLaMA 3 8B (8k context)
- LLaMA 3.1 8B Instant (128k context)
- LLaMA Guard 3 8B (8k context)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please:
1. Check existing issues
2. Create a new issue with detailed information
3. Contact the maintainers
