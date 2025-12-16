"""
Llama-optimized prompts for prompt evaluation use cases
Following Meta's Llama prompt engineering guidelines with example-driven approach

TODO: Implement Llama-optimized versions of:
- Specificity Evaluator
- Fact Generator
- Fact Matcher
- Contradiction Detector
- Relevance Evaluator
"""

from ...models import Prompt, PromptMetadata, Provider, UseCase, Domain

# Placeholder - to be implemented with Llama's example-driven structure
LLAMA_SPECIFICITY_EVALUATOR = None
LLAMA_FACT_GENERATOR = None
LLAMA_FACT_MATCHER = None
LLAMA_CONTRADICTION_DETECTOR = None
LLAMA_RELEVANCE_EVALUATOR = None

# Export all prompts (when implemented)
LLAMA_PROMPT_EVALS_PROMPTS = []

"""
Implementation notes for Llama prompts:
- Use clear ROLE and INSTRUCTIONS sections
- Provide extensive EXAMPLES with expected outputs
- Use ALL CAPS for section headers
- Direct, example-driven approach (300-800 words)
- Include complete input/output examples for each use case
"""