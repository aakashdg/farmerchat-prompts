# Changelog

All notable changes to the farmerchat-prompts project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-15

### Added
- Initial release of farmerchat-prompts package
- Support for 3 AI providers: OpenAI, Claude (Anthropic), and Llama (Meta)
- 5 agricultural use cases:
  - Crop Recommendation
  - Pest Management
  - Soil Analysis
  - Weather Advisory
  - Market Insights
- PromptManager class for centralized prompt management
- Provider-specific prompt engineering optimizations:
  - OpenAI: Clear, structured instructions with role-based prompts
  - Claude: XML-tagged sections with detailed context
  - Llama: Direct instructions with example-based learning
- Pydantic models for type safety and validation
- Comprehensive test suite with 22 test cases
- Full documentation including:
  - README with usage examples
  - Quick Start guide
  - Publishing guide for PyPI
  - Example scripts
- Features:
  - Get prompts by provider and use case
  - Search prompts by keyword
  - List and validate prompt combinations
  - Format prompts with custom variables
  - Get provider-specific API structures

### Technical Details
- Python 3.8+ support
- Pydantic 2.0+ for data validation
- 15 total prompt variations (3 providers × 5 use cases)
- All prompts follow prompt engineering best practices for their respective models
- Agricultural domain expertise integrated into all prompts

[0.1.0]: https://github.com/yourusername/farmerchat-prompts/releases/tag/v0.1.0
