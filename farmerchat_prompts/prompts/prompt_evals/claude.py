"""
Claude-optimized prompts for prompt evaluation use cases
Following Anthropic's prompt engineering guidelines with XML structure

TODO: Implement Claude-optimized versions of:
- Specificity Evaluator
- Fact Generator
- Fact Matcher
- Contradiction Detector
- Relevance Evaluator
"""

from ...models import Prompt, PromptMetadata, Provider, UseCase, Domain

# Placeholder - to be implemented with Claude's XML-based structure
CLAUDE_SPECIFICITY_EVALUATOR = None
CLAUDE_FACT_GENERATOR = None
CLAUDE_FACT_MATCHER = None
CLAUDE_CONTRADICTION_DETECTOR = None
CLAUDE_RELEVANCE_EVALUATOR = None

# Export all prompts (when implemented)
CLAUDE_PROMPT_EVALS_PROMPTS = []

"""
Implementation notes for Claude prompts:
- Use XML tags for structure (<role>, <instructions>, <examples>)
- Include detailed context and reasoning steps
- Use <think> tags for complex evaluations
- Provide comprehensive examples in <example> tags
- Maintain 500-1000+ word system prompts with detailed guidance
"""