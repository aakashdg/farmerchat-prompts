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


<!-- # FarmerChat Prompts

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
**Last Updated**: December 202
**Maintainer**: Aakash (AI/ML Engineer) -->


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

Or install from GitHub:

```bash
pip install git+https://github.com/YOUR_USERNAME/farmerchat-prompts.git
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
from openai import OpenAI
client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
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

**Why These Prompts Matter:**

When building AI-powered agricultural chatbots, ensuring response quality is critical. Farmers depend on accurate, specific, and actionable information. The prompt evaluation domain provides a comprehensive framework to:

- **Validate Response Quality**: Automatically assess if AI-generated advice is specific and actionable
- **Extract Structured Knowledge**: Convert conversational responses into verifiable atomic facts
- **Ensure Consistency**: Detect contradictions between generated facts and ground truth
- **Measure Relevance**: Evaluate how well responses address farmer queries
- **Build Trust**: Provide transparent quality metrics for AI-generated agricultural advice

**Use Cases:**

#### 1. **Specificity Evaluation** (`specificity_evaluation`)

**Purpose**: Classify agricultural facts as "Specific" or "Not Specific" based on contextual anchors (location, time, quantity, entity) and actionability.

**Why It Matters**: Generic advice like "water your plants" is unhelpful. Farmers need specific guidance like "water tomato plants with 2 liters per plant every morning in summer." This prompt ensures facts contain enough detail for real-world application.

**Expected Input**:
```python
{
    "fact_text": "Apply neem oil at 3ml per liter for aphid control",
    "query_context": "User asked about organic pest control for tomatoes",
    "additional_params": "Focus on Bihar farming context"
}
```

**Expected Output**:
```json
{
    "text": "Apply neem oil at 3ml per liter for aphid control",
    "label": "Specific",
    "flags": [
        "entity_specificity",
        "quantity_measurement",
        "actionability"
    ],
    "justification": "Contains specific crop (tomatoes), precise measurement (3ml/L), and clear action (apply for aphid control), enabling farmers to implement directly."
}
```

**When to Use**: After generating facts, before storing them in a knowledge base or presenting to users.

---

#### 2. **Fact Generation** (`fact_generation`)

**Purpose**: Extract atomic, verifiable facts from conversational chatbot responses, filtering out greetings, disclaimers, and non-agricultural content.

**Why It Matters**: Chatbot responses often contain multiple claims mixed with conversational elements. This prompt isolates actionable agricultural knowledge, making it easier to validate, store, and reuse. Each fact becomes a standalone, verifiable unit.

**Expected Input**:
```python
{
    "chatbot_response": "Hello! For aphid control, apply neem oil at 3ml per liter. Spray in early morning. Repeat every 7 days. Hope this helps!",
    "user_query": "How to control aphids organically?",
    "regional_context": "Bihar-specific practices",
    "additional_params": "Extract only organic pest control methods"
}
```

**Expected Output**:
```json
{
    "facts": [
        {
            "fact": "Apply neem oil at 3ml per liter concentration for aphid control",
            "category": "pest_disease",
            "location_dependency": "universal",
            "bihar_relevance": "high",
            "confidence": 0.9
        },
        {
            "fact": "Apply neem oil spray in early morning for optimal effectiveness",
            "category": "pest_disease",
            "location_dependency": "universal",
            "bihar_relevance": "high",
            "confidence": 0.85
        },
        {
            "fact": "Repeat neem oil application every 7 days for persistent aphid control",
            "category": "pest_disease",
            "location_dependency": "universal",
            "bihar_relevance": "high",
            "confidence": 0.9
        }
    ]
}
```

**When to Use**: Immediately after receiving chatbot responses, before any downstream processing.

---

#### 3. **Fact Matching** (`fact_recall`)

**Purpose**: Find semantic matches between predicted facts and ground truth facts, accounting for different wording but equivalent agricultural meaning.

**Why It Matters**: The same agricultural advice can be expressed many ways. "Apply 3ml neem oil per liter" and "Mix neem oil at 3ml/L concentration" convey the same information. This prompt identifies equivalent facts for evaluation metrics like precision and recall.

**Expected Input**:
```python
{
    "category": "pest_disease",
    "gold_fact": "Apply neem oil at 3ml per liter for aphid control",
    "pred_facts": [
        "Use neem oil spray for pest management",
        "Mix 3ml neem oil in 1 liter water for aphids",
        "Water plants regularly"
    ]
}
```

**Expected Output**:
```json
{
    "best_match": "Mix 3ml neem oil in 1 liter water for aphids",
    "reason": "Both facts specify the same concentration (3ml per liter), same pest (aphids), and same treatment method (neem oil), representing equivalent agricultural advice despite different wording.",
    "confidence": 0.92
}
```

**When to Use**: During evaluation pipelines, after extracting facts from model outputs and comparing against ground truth.

---

#### 4. **Contradiction Detection** (`contradiction_detection`)

**Purpose**: Identify contradictions between generated facts and ground truth, with component-level analysis (temperature, humidity, timing, quantity, etc.).

**Why It Matters**: Contradictory advice can harm crops and farmer livelihoods. If ground truth says "water daily in summer" but the model says "avoid daily watering in summer," farmers receive conflicting guidance. This prompt catches such contradictions before they reach users.

**Expected Input**:
```python
{
    "category": "irrigation",
    "gold_fact": "Water tomato plants daily during summer months",
    "pred_facts": [
        "Avoid daily watering in summer to prevent root rot",
        "Water every 2-3 days for optimal growth",
        "Apply mulch to retain moisture"
    ],
    "additional_context": "Focus on tomato cultivation in Bihar"
}
```

**Expected Output**:
```json
{
    "contradictions": [
        {
            "contradicting_fact": "Avoid daily watering in summer to prevent root rot",
            "reference_fact": "Water tomato plants daily during summer months",
            "reason": "Direct opposition on watering frequency: reference recommends daily watering while candidate advises avoiding it.",
            "confidence": "High",
            "components_compared": [
                {
                    "component": "timing",
                    "reference_value": "daily",
                    "candidate_value": "avoid daily",
                    "status": "conflict"
                },
                {
                    "component": "season",
                    "reference_value": "summer",
                    "candidate_value": "summer",
                    "status": "compatible"
                }
            ],
            "structured_justification": [
                "Step 1: Decomposed facts into watering frequency and seasonal components",
                "Step 2: Identified opposite recommendations for frequency (daily vs. avoid daily)",
                "Step 3: Confirmed genuine contradiction in core watering guidance"
            ]
        }
    ]
}
```

**When to Use**: After fact matching, to identify generated facts that conflict with established knowledge.

---

#### 5. **Relevance Evaluation** (`relevance_evaluation`)

**Purpose**: Evaluate unmatched facts for relevance, quality, practical value, and farmer applicability, providing detailed scoring across multiple dimensions.

**Why It Matters**: Not all unmatched facts are bad—some provide valuable complementary information. Others are off-topic. This prompt distinguishes between high-quality additional advice and irrelevant content, helping you decide what to keep, improve, or discard.

**Expected Input**:
```python
{
    "question": "How to control aphids on tomato plants organically?",
    "ground_facts": [
        "Apply neem oil at 3ml per liter",
        "Use yellow sticky traps"
    ],
    "unmatched_facts": [
        "Water plants regularly in morning",
        "Introduce parasitic wasps for biological control",
        "Harvest tomatoes when fully red"
    ],
    "additional_evaluation_criteria": "Prioritize organic pest control methods"
}
```

**Expected Output**:
```json
{
    "question": "How to control aphids on tomato plants organically?",
    "ground_facts": ["Apply neem oil at 3ml per liter", "Use yellow sticky traps"],
    "predicted_facts_analysis": [
        {
            "predicted_fact": "Water plants regularly in morning",
            "relevance_score": 3,
            "ground_truth_alignment_score": 2,
            "practical_value_score": 5,
            "specificity_score": 4,
            "agricultural_soundness_score": 7,
            "overall_score": 4,
            "explanation": "While proper watering is important for plant health, this fact doesn't directly address aphid control, which is the core question.",
            "gaps_identified": [
                "No connection to pest management",
                "Doesn't complement existing organic control methods"
            ],
            "farmer_applicability": "Easy to implement but not relevant to the aphid problem"
        },
        {
            "predicted_fact": "Introduce parasitic wasps for biological control",
            "relevance_score": 9,
            "ground_truth_alignment_score": 8,
            "practical_value_score": 8,
            "specificity_score": 7,
            "agricultural_soundness_score": 9,
            "overall_score": 8,
            "explanation": "Highly relevant organic pest control method that complements neem oil and sticky traps. Parasitic wasps are effective natural predators of aphids.",
            "gaps_identified": [
                "Could specify wasp species (e.g., Aphidius colemani)",
                "Release timing not mentioned"
            ],
            "farmer_applicability": "Moderate implementation - requires sourcing beneficial insects, but highly effective for organic farming"
        }
    ],
    "summary": {
        "total_predicted_facts": 3,
        "average_overall_score": 6.3,
        "key_insights": [
            "One fact (parasitic wasps) provides valuable complementary pest control",
            "Two facts are tangential to the core aphid control question"
        ],
        "recommendations": [
            "Keep parasitic wasp fact as additional organic control option",
            "Consider removing or rephrasing watering and harvest facts"
        ]
    }
}
```

**When to Use**: At the end of the evaluation pipeline, to assess facts that didn't match ground truth but might still be valuable.

#### 6. **fact_stitching**: Synthesize atomic facts into natural, conversational farmer-friendly responses

**Example**

```python
# Synthesize structured facts into natural response
stitching = manager.get_prompt("openai", "fact_stitching", "prompt_evals")

facts = [
    {
        "fact": "Apply neem oil at 3ml per liter for aphid control",
        "category": "pest_disease",
        "confidence": 0.9,
        "bihar_relevance": "high"
    },
    {
        "fact": "Spray in early morning for best effectiveness",
        "category": "pest_disease",
        "confidence": 0.85,
        "bihar_relevance": "high"
    }
]

formatted = stitching.user_prompt_template.format(
    original_query="How to control aphids organically?",
    facts_json=json.dumps(facts),
    additional_context=""
)

# Returns natural, conversational synthesis of facts
```
---

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

- **Total Prompts**: 22 (15 crop advisory + 7 prompt evals for OpenAI)
- **Providers**: 3 (OpenAI, Claude, Llama)
- **Domains**: 2 (crop_advisory, prompt_evals)
- **Use Cases**: 12: 5 (crop_advisory) + 7 (prompt_evals)
- **Code Lines**: 3,500+
- **Test Coverage**: 33+ test cases

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
- **Colab Testing**: See `COLAB_TESTING_GUIDE.md`
- **GitHub Publishing**: See `GITHUB_PUBLISHING_GUIDE.md`
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
  url = {https://github.com/aakashdg/farmerchat-prompts}
}
```

## Acknowledgments

- Built for Farmer.Chat agricultural AI platform
- Optimized for Indian farming contexts
- Follows prompt engineering best practices from OpenAI, Anthropic, and Meta
- Includes comprehensive prompt evaluation framework for quality assessment

---

**Version**: 0.2.0  
**Last Updated**: December 2025 