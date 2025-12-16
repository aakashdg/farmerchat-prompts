# Quick Start Guide

Get started with `farmerchat-prompts` in 5 minutes with multi-domain support!

## Installation

```bash
pip install farmerchat-prompts
```

## Basic Usage

### 1. Import and Initialize

```python
from farmerchat_prompts import PromptManager

manager = PromptManager()
```

### 2. Get a Prompt (Crop Advisory)

```python
# Get crop recommendation prompt (defaults to crop_advisory domain)
prompt = manager.get_prompt("openai", "crop_recommendation")
```

### 3. Use with OpenAI

```python
import openai

# Get the prompt
prompt = manager.get_prompt("openai", "crop_recommendation")

# Create the API call
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": "I have sandy soil in Bihar, what should I grow?"}
    ]
)

print(response.choices[0].message.content)
```

## Multi-Domain Usage

### Crop Advisory Domain

```python
# Pest management
prompt = manager.get_prompt(
    provider="claude",
    use_case="pest_management",
    domain="crop_advisory"  # Explicit domain
)

from anthropic import Anthropic
client = Anthropic(api_key="your-key")

full_prompt = prompt.get_full_prompt(
    "My tomato plants have yellow spots. Help me identify the problem."
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=full_prompt["system"],
    messages=full_prompt["messages"],
    max_tokens=2000
)
```

### Prompt Evaluation Domain

```python
# Evaluate fact specificity
specificity_prompt = manager.get_prompt(
    provider="openai",
    use_case="specificity_evaluation",
    domain="prompt_evals"  # Different domain
)

formatted = specificity_prompt.user_prompt_template.format(
    fact_text="Apply neem oil at 3ml per liter for aphid control",
    query_context="User asked about organic pest control for tomatoes",
    additional_params=""
)

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": specificity_prompt.system_prompt},
        {"role": "user", "content": formatted}
    ],
    response_format={"type": "json_object"}
)

result = json.loads(response.choices[0].message.content)
print(f"Classification: {result['label']}")
print(f"Justification: {result['justification']}")
```

## Available Domains

### 1. Crop Advisory (`crop_advisory`)

```python
# List all crop advisory use cases
use_cases = [
    "crop_recommendation",  # Crop selection guidance
    "pest_management",      # Pest identification & treatment
    "soil_analysis",        # Soil improvement recommendations
    "weather_advisory",     # Weather-based farming advice
    "market_insights"       # Market prices & selling strategy
]
```

### 2. Prompt Evaluation (`prompt_evals`)

```python
# List all prompt evaluation use cases
use_cases = [
    "specificity_evaluation",   # Classify fact specificity
    "fact_generation",          # Extract atomic facts
    "fact_matching",            # Semantic fact matching
    "contradiction_detection",  # Detect contradictions
    "relevance_evaluation"      # Evaluate fact relevance
]
```

## Common Workflows

### Workflow 1: Crop Advisory

```python
manager = PromptManager()

# Get weather advisory
prompt = manager.get_prompt("openai", "weather_advisory", "crop_advisory")

# Format with farmer's data
formatted = prompt.format(
    location="Patna, Bihar",
    current_weather="32°C, Cloudy",
    forecast="Heavy rain tomorrow",
    crops="Rice",
    growth_stage="Flowering",
    planned_activities="Harvesting",
    concerns="Rain damage"
)

# Use with API
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": formatted}
    ]
)
```

### Workflow 2: Fact Extraction & Validation

```python
import json

# Step 1: Extract facts from chatbot response
fact_gen = manager.get_prompt("openai", "fact_generation", "prompt_evals")

chatbot_response = """
Apply neem oil spray at 3ml per liter.
Spray in early morning for best results.
Repeat every 7 days during flowering stage.
"""

formatted = fact_gen.user_prompt_template.format(
    chatbot_response=chatbot_response,
    user_query="How to control aphids organically?",
    regional_context="Bihar farming practices",
    additional_params=""
)

# Call API to extract facts
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": fact_gen.system_prompt},
        {"role": "user", "content": formatted}
    ],
    response_format={"type": "json_object"}
)

facts = json.loads(response.choices[0].message.content)

# Step 2: Evaluate each fact's specificity
specificity = manager.get_prompt("openai", "specificity_evaluation", "prompt_evals")

for fact_item in facts['facts']:
    formatted = specificity.user_prompt_template.format(
        fact_text=fact_item['fact'],
        query_context="",
        additional_params=""
    )
    
    # Evaluate
    result = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": specificity.system_prompt},
            {"role": "user", "content": formatted}
        ],
        response_format={"type": "json_object"}
    )
    
    evaluation = json.loads(result.choices[0].message.content)
    print(f"Fact: {fact_item['fact']}")
    print(f"Specificity: {evaluation['label']}")
    print()
```

### Workflow 3: Fact Matching

```python
# Match predicted facts with ground truth
matcher = manager.get_prompt("openai", "fact_matching", "prompt_evals")

gold_fact = "Apply neem oil at 3ml per liter for aphid control"
candidate_facts = [
    "Use neem oil spray for pest management",
    "Mix 3ml neem oil in 1 liter water for aphids",
    "Water plants in morning"
]

formatted = matcher.user_prompt_template.format(
    category="pest_disease",
    gold_fact=gold_fact,
    pred_facts=json.dumps(candidate_facts)
)

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": matcher.system_prompt},
        {"role": "user", "content": formatted}
    ],
    response_format={"type": "json_object"}
)

match_result = json.loads(response.choices[0].message.content)
print(f"Best match: {match_result['best_match']}")
print(f"Confidence: {match_result['confidence']}")
print(f"Reason: {match_result['reason']}")
```

## Exploring Prompts

```python
# Get all domains
domains = manager.get_available_domains()
print(f"Domains: {domains}")
# Output: ['crop_advisory', 'prompt_evals']

# Get prompts in a domain
eval_prompts = manager.get_prompts_by_domain("prompt_evals")
print(f"Prompt evals: {len(eval_prompts)} prompts")

# Get all providers
providers = manager.get_available_providers()
# Output: ['openai', 'claude', 'llama']

# Get statistics
stats = manager.get_stats()
print(f"Total: {stats['total_prompts']} prompts")
print(f"Providers: {stats['providers']}")
print(f"Use cases: {stats['use_cases']}")
```

## Formatting Prompts

All prompts support custom variables:

```python
# Get prompt
prompt = manager.get_prompt("openai", "soil_analysis", "crop_advisory")

# Check available variables
print(f"Variables: {list(prompt.variables.keys())}")

# Format with your data
formatted = prompt.format(
    location="Araria, Bihar",
    soil_type="Sandy loam",
    ph="6.5",
    organic_carbon="0.8",
    nitrogen="150",
    phosphorus="12",
    potassium="180",
    # ... other variables
)

# Use formatted prompt
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": formatted}
    ]
)
```

## Backward Compatibility

Old code works without changes:

```python
# OLD WAY (still works) - defaults to crop_advisory
prompt = manager.get_prompt("openai", "crop_recommendation")

# NEW WAY (explicit domain)
prompt = manager.get_prompt("openai", "crop_recommendation", "crop_advisory")

# Both return the same prompt
```

## Complete Example: Evaluation Pipeline

```python
from farmerchat_prompts import PromptManager
import openai
import json

manager = PromptManager()

# Simulated chatbot response
chatbot_response = """
For aphid control, apply neem oil at 3ml per liter.
Spray in early morning for best effectiveness.
Repeat application every 7 days during flowering.
Make sure plants are well-watered before spraying.
"""

# Step 1: Extract facts
fact_gen = manager.get_prompt("openai", "fact_generation", "prompt_evals")
formatted = fact_gen.user_prompt_template.format(
    chatbot_response=chatbot_response,
    user_query="How to control aphids?",
    regional_context="",
    additional_params=""
)

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": fact_gen.system_prompt},
        {"role": "user", "content": formatted}
    ],
    response_format={"type": "json_object"}
)

facts = json.loads(response.choices[0].message.content)
print(f"Extracted {len(facts['facts'])} facts")

# Step 2: Evaluate specificity
specificity = manager.get_prompt("openai", "specificity_evaluation", "prompt_evals")

specific_facts = []
for fact_item in facts['facts']:
    formatted = specificity.user_prompt_template.format(
        fact_text=fact_item['fact'],
        query_context="",
        additional_params=""
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": specificity.system_prompt},
            {"role": "user", "content": formatted}
        ],
        response_format={"type": "json_object"}
    )
    
    eval_result = json.loads(response.choices[0].message.content)
    if eval_result['label'] == 'Specific':
        specific_facts.append(fact_item['fact'])

print(f"Found {len(specific_facts)} specific facts")

# Step 3: Match with ground truth
matcher = manager.get_prompt("openai", "fact_matching", "prompt_evals")

ground_truth = ["Apply neem oil at 3ml/L for aphids"]

for gt_fact in ground_truth:
    formatted = matcher.user_prompt_template.format(
        category="pest_disease",
        gold_fact=gt_fact,
        pred_facts=json.dumps(specific_facts)
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": matcher.system_prompt},
            {"role": "user", "content": formatted}
        ],
        response_format={"type": "json_object"}
    )
    
    match = json.loads(response.choices[0].message.content)
    if match['best_match']:
        print(f"✓ Matched: {match['best_match']}")
        print(f"  Confidence: {match['confidence']}")
```

## Next Steps

- Check out `examples/usage_examples.py` for 13 detailed examples
- Read the full documentation in `README.md`
- Try different providers (OpenAI, Claude, Llama)
- Experiment with both domains (crop_advisory, prompt_evals)

**Happy Prompting! 🌾🤖**