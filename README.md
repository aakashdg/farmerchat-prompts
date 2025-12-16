<!-- # FarmerChat Prompts

A Python library for managing AI prompts across multiple providers (OpenAI, Claude, Llama) with use-case specific templates optimized for agricultural applications.

## Features

- 🤖 **Multi-Provider Support**: OpenAI GPT, Anthropic Claude, and Meta Llama
- 🌾 **Agricultural Use Cases**: Crop recommendations, pest management, soil analysis, weather advisories, and market insights
- 🎯 **Optimized Prompts**: Each prompt follows provider-specific best practices
- 🔧 **Easy Integration**: Simple API to access prompts by provider and use case
- 📦 **Type Safe**: Built with Pydantic for runtime validation

## Installation

```bash
pip install farmerchat-prompts
```

## Quick Start

```python
from farmerchat_prompts import PromptManager

# Initialize the prompt manager
manager = PromptManager()

# Get a specific prompt
prompt = manager.get_prompt(
    provider="openai",
    use_case="crop_recommendation"
)

# Use with your AI client
response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": "I have sandy soil in Bihar, what should I grow?"}
    ]
)
```

## Supported Providers

- **OpenAI** (`openai`): GPT-3.5, GPT-4
- **Anthropic** (`claude`): Claude 3.5 Sonnet, Claude 3 Opus
- **Meta** (`llama`): Llama 3.1, Llama 3.2

## Use Cases

1. **crop_recommendation**: Get crop suggestions based on soil, climate, and location
2. **pest_management**: Identify pests and get treatment recommendations
3. **soil_analysis**: Analyze soil properties and get improvement suggestions
4. **weather_advisory**: Provide farming advice based on weather conditions
5. **market_insights**: Get market prices and selling recommendations

## Advanced Usage

### List All Available Prompts

```python
# Get all prompts for a provider
openai_prompts = manager.get_prompts_by_provider("openai")

# Get all prompts for a use case
crop_prompts = manager.get_prompts_by_use_case("crop_recommendation")

# Get all available combinations
all_prompts = manager.list_all_prompts()
print(f"Total prompts: {len(all_prompts)}")  # 15 (3 providers × 5 use cases)
```

### Custom Variables

```python
prompt = manager.get_prompt("claude", "weather_advisory")

# Format with custom variables
formatted = prompt.format(
    location="Araria, Bihar",
    current_weather="Heavy rainfall expected",
    crops="Rice, Wheat"
)
```

### Validation

```python
# Check if a combination exists
exists = manager.validate_combination("openai", "crop_recommendation")

# Get metadata
metadata = prompt.metadata
print(f"Provider: {metadata.provider}")
print(f"Use Case: {metadata.use_case}")
print(f"Version: {metadata.version}")
```

## Prompt Engineering Details

Each provider has specific optimizations:

- **OpenAI**: Structured with clear system/user roles, concise instructions
- **Claude**: XML-tagged sections, detailed context, step-by-step reasoning
- **Llama**: Direct instructions, example-based learning, clear formatting

## Development

### Setup

```bash
git clone https://github.com/yourusername/farmerchat-prompts
cd farmerchat-prompts
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black farmerchat_prompts/
flake8 farmerchat_prompts/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Aakash - AI/ML Engineer specializing in agricultural AI systems -->


# FarmerChat Prompts

A Python library for managing AI prompts across multiple providers (OpenAI, Claude, Llama) with domain-specific templates optimized for agricultural applications and prompt evaluation.

## Features

- 🤖 **Multi-Provider Support**: OpenAI GPT, Anthropic Claude, and Meta Llama
- 🌾 **Multi-Domain Architecture**: Organized by use case domains
  - **Crop Advisory**: Agricultural guidance and farming practices
  - **Prompt Evaluation**: Fact extraction, validation, and quality assessment
- 🎯 **Optimized Prompts**: Each prompt follows provider-specific best practices
- 🔧 **Easy Integration**: Simple API to access prompts by provider, use case, and domain
- 📦 **Type Safe**: Built with Pydantic for runtime validation
- 🔄 **Backward Compatible**: Existing code works without changes

## Installation

```bash
pip install farmerchat-prompts
```

## Quick Start

### Basic Usage

```python
from farmerchat_prompts import PromptManager

# Initialize the prompt manager
manager = PromptManager()

# Get a crop advisory prompt (defaults to crop_advisory domain)
prompt = manager.get_prompt("openai", "crop_recommendation")

# Use with your AI client
import openai
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": "I have sandy soil in Bihar, what should I grow?"}
    ]
)
```

### Using Multiple Domains

```python
# Crop advisory prompts
crop_prompt = manager.get_prompt(
    provider="openai",
    use_case="crop_recommendation",
    domain="crop_advisory"
)

# Prompt evaluation prompts
eval_prompt = manager.get_prompt(
    provider="openai",
    use_case="specificity_evaluation",
    domain="prompt_evals"
)
```

## Supported Providers

- **OpenAI** (`openai`): GPT-3.5, GPT-4
- **Anthropic** (`claude`): Claude 3.5 Sonnet, Claude 3 Opus
- **Meta** (`llama`): Llama 3.1, Llama 3.2

## Domains & Use Cases

### 1. Crop Advisory Domain (`crop_advisory`)

Agricultural guidance for Indian farming contexts:

1. **crop_recommendation**: Crop suggestions based on soil, climate, and location
2. **pest_management**: Pest identification and treatment recommendations
3. **soil_analysis**: Soil test interpretation and improvement suggestions
4. **weather_advisory**: Weather-based farming guidance
5. **market_insights**: Market prices and selling recommendations

### 2. Prompt Evaluation Domain (`prompt_evals`)

Fact extraction and quality assessment tools:

1. **specificity_evaluation**: Classify facts as Specific or Not Specific
2. **fact_generation**: Extract atomic facts from chatbot responses
3. **fact_matching**: Find semantic matches between facts
4. **contradiction_detection**: Detect contradictions with component analysis
5. **relevance_evaluation**: Evaluate unmatched facts for quality and relevance

## Advanced Usage

### Crop Advisory Example

```python
from farmerchat_prompts import PromptManager

manager = PromptManager()

# Get pest management prompt
prompt = manager.get_prompt("claude", "pest_management", "crop_advisory")

# Format with farmer's data
user_input = """
My tomato plants have yellow spots on leaves.
About 30% of plants affected.
Noticed 5 days ago in Patna, Bihar.
"""

# Get full prompt for API
full_prompt = prompt.get_full_prompt(user_input)

# Call Claude API
from anthropic import Anthropic
client = Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=full_prompt["system"],
    messages=full_prompt["messages"],
    max_tokens=2000
)
```

### Prompt Evaluation Example

```python
# Extract facts from chatbot response
fact_gen_prompt = manager.get_prompt(
    provider="openai",
    use_case="fact_generation",
    domain="prompt_evals"
)

# Format with response text
formatted = fact_gen_prompt.user_prompt_template.format(
    chatbot_response="Apply neem oil at 3ml per liter in early morning...",
    user_query="How to control aphids organically?",
    regional_context="Bihar-specific practices",
    additional_params="Extract only actionable facts"
)

# Evaluate fact specificity
specificity_prompt = manager.get_prompt(
    provider="openai",
    use_case="specificity_evaluation",
    domain="prompt_evals"
)

formatted = specificity_prompt.user_prompt_template.format(
    fact_text="Apply neem oil at 3ml per liter for aphid control",
    query_context="User asked about organic pest control",
    additional_params=""
)
```

### Exploring Available Prompts

```python
# List all domains
domains = manager.get_available_domains()
# ['crop_advisory', 'prompt_evals']

# Get all prompts in a domain
crop_prompts = manager.get_prompts_by_domain("crop_advisory")
eval_prompts = manager.get_prompts_by_domain("prompt_evals")

# Get statistics
stats = manager.get_stats()
print(f"Total prompts: {stats['total_prompts']}")
print(f"Providers: {stats['providers']}")
print(f"Use cases: {stats['use_cases']}")
```

### Custom Variables

```python
prompt = manager.get_prompt("openai", "weather_advisory", "crop_advisory")

# Format with custom variables
formatted = prompt.format(
    location="Araria, Bihar",
    current_weather="Heavy rainfall expected",
    crops="Rice, Wheat",
    growth_stage="Flowering",
    planned_activities="Pesticide spraying",
    concerns="Rain damage"
)
```

### Validation

```python
# Check if a combination exists
exists = manager.validate_combination("openai", "crop_recommendation", "crop_advisory")

# Get metadata
metadata = prompt.metadata
print(f"Provider: {metadata.provider}")
print(f"Use Case: {metadata.use_case}")
print(f"Domain: {metadata.domain}")
print(f"Version: {metadata.version}")
```

## Prompt Engineering Details

Each provider has specific optimizations:

### OpenAI Prompts
- **Style**: Structured with clear system/user roles, concise instructions
- **Length**: 200-500 words for system prompts
- **Format**: Bulleted lists, numbered steps, clear JSON output schemas
- **Best for**: Fast responses, structured outputs, function calling

### Claude Prompts
- **Style**: XML-tagged sections, detailed context, step-by-step reasoning
- **Length**: 500-1000+ words for comprehensive guidance
- **Format**: `<role>`, `<instructions>`, `<examples>` tags
- **Best for**: Complex analysis, detailed explanations, multi-step reasoning

### Llama Prompts
- **Style**: Direct instructions, example-driven learning
- **Length**: 300-800 words with extensive examples
- **Format**: ALL CAPS headers (ROLE, INSTRUCTIONS, EXAMPLES)
- **Best for**: Local deployment, cost-effective, privacy-focused

## Real-World Example: Evaluation Pipeline

```python
manager = PromptManager()

# Step 1: Generate facts from chatbot response
fact_gen = manager.get_prompt("openai", "fact_generation", "prompt_evals")

# Step 2: Evaluate specificity of each fact
specificity = manager.get_prompt("openai", "specificity_evaluation", "prompt_evals")

# Step 3: Match generated facts with ground truth
matcher = manager.get_prompt("openai", "fact_matching", "prompt_evals")

# Step 4: Check for contradictions
contradiction = manager.get_prompt("openai", "contradiction_detection", "prompt_evals")

# Step 5: Evaluate relevance of unmatched facts
relevance = manager.get_prompt("openai", "relevance_evaluation", "prompt_evals")
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/farmerchat-prompts
cd farmerchat-prompts
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black farmerchat_prompts/
flake8 farmerchat_prompts/
```

## Package Statistics

- **Total Prompts**: 20 (15 crop advisory + 5 prompt evals for OpenAI)
- **Providers**: 3 (OpenAI, Claude, Llama)
- **Domains**: 2 (crop_advisory, prompt_evals)
- **Use Cases**: 10 (5 per domain)
- **Code Lines**: 3,500+
- **Test Coverage**: 25+ test cases

## Architecture

```
farmerchat_prompts/
├── models.py           # Pydantic models with Domain support
├── manager.py          # PromptManager with domain parameter
└── prompts/
    ├── crop_advisory/  # Agricultural guidance prompts
    │   ├── openai.py   # 5 prompts
    │   ├── claude.py   # 5 prompts
    │   └── llama.py    # 5 prompts
    └── prompt_evals/   # Evaluation & extraction prompts
        ├── openai.py   # 5 prompts (complete)
        ├── claude.py   # Placeholder
        └── llama.py    # Placeholder
```

## Backward Compatibility

Existing code works without changes - domain parameter defaults to `crop_advisory`:

```python
# Old code (still works)
prompt = manager.get_prompt("openai", "crop_recommendation")

# Equivalent to new code
prompt = manager.get_prompt("openai", "crop_recommendation", "crop_advisory")
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

### Adding a New Domain

1. Create new directory: `prompts/your_domain/`
2. Add provider files: `openai.py`, `claude.py`, `llama.py`
3. Update `Domain` enum in `models.py`
4. Update `UseCase` enum with new use cases
5. Update `manager.py` to load new domain
6. Add tests for new domain

## Support & Resources

- **Documentation**: Full docs in this README
- **Examples**: See `examples/usage_examples.py`
- **Migration Guide**: See `MULTI_DOMAIN_MIGRATION.md`
- **Issues**: GitHub Issues
- **Email**: your.email@example.com

## License

MIT License - see LICENSE file for details

## Citation

If you use this package in your research or production system, please cite:

```bibtex
@software{farmerchat_prompts,
  author = {Aakash},
  title = {FarmerChat Prompts: Multi-Domain AI Prompt Management for Agriculture},
  year = {2024},
  url = {https://github.com/yourusername/farmerchat-prompts}
}
```

## Acknowledgments

- Built for Farmer.Chat agricultural AI platform
- Optimized for Indian farming contexts
- Follows prompt engineering best practices from OpenAI, Anthropic, and Meta
- Includes prompt evaluation framework for quality assessment

---

**Project Status**: Production Ready ✅  
**Version**: 0.2.0  
**Last Updated**: December 2024  
**Maintainer**: Aakash (AI/ML Engineer)