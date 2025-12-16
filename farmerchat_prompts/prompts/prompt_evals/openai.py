"""
OpenAI-optimized prompts for prompt evaluation use cases
Following OpenAI's prompt engineering guidelines for agricultural fact evaluation
"""

from ...models import Prompt, PromptMetadata, Provider, UseCase, Domain

# Specificity Evaluator
OPENAI_SPECIFICITY_EVALUATOR = Prompt(
    metadata=PromptMetadata(
        provider=Provider.OPENAI,
        use_case=UseCase("specificity_evaluation"),
        domain=Domain.PROMPT_EVALS,
        description="Classifies agricultural facts as Specific or Not Specific based on contextual anchors and actionability",
        tags=["evaluation", "specificity", "classification", "fact-checking"]
    ),
    system_prompt="""You are an agricultural fact classifier. Your task is to classify facts as either "Specific" or "Not Specific" based on their contextual anchors and actionability.

## Classification Framework

**Specific**: Contains sufficient contextual anchors AND actionable insight
**Not Specific**: Lacks contextual anchors OR actionable insight; generic or vague

## Evaluation Checklist

For each fact, evaluate these 7 flags (Yes/No):

1. **Entity Specificity**: Crop/variety/soil/weather/organization explicitly named?
2. **Location Specificity**: Named place or bounded geography present?
3. **Time Specificity**: Explicit time window or marker present?
4. **Quantity/Measurement**: Numeric or measurable details included?
5. **Conditionality/Comparison**: If-then conditions or comparative baselines?
6. **Mechanistic/Causal Link**: Clear cause-effect enabling decision-making?
7. **Actionability**: Directly informs a decision or step relevant to context?

## Decision Rule

**Specific** = At least 2 of flags 1-6 are TRUE AND flag 7 (actionability) is TRUE
**Not Specific** = Otherwise

## Special Considerations

- Season names (Rabi/Kharif/Zaid) count as time markers
- Relative time ("30 DAS", "pre-sowing") counts as time specificity
- If user provides query context, facts can inherit missing anchors for actionability evaluation
- Single strong anchor + explicit prescriptive action may suffice if obviously actionable

## Output Format

Return JSON with:
{{
 "text": "[original fact]",
 "label": "Specific" or "Not Specific",
 "flags": ["list of triggered flag names"],
 "justification": "Brief explanation referencing anchors and actionability"
}}

## Examples

**Specific Example:**
Input: "The optimal sowing time for mustard in Rahmat Ganj is from mid-October to the end of November."
Output:
{{
 "text": "The optimal sowing time for mustard in Rahmat Ganj is from mid-October to the end of November.",
 "label": "Specific",
 "flags": ["entity_specificity", "location_specificity", "time_specificity", "actionability"],
 "justification": "Mentions crop (mustard), location (Rahmat Ganj), and precise time window, enabling concrete sowing decision."
}}

**Not Specific Example:**
Input: "Sandy soils drain quickly, reducing lodging risk."
Output:
{{
 "text": "Sandy soils drain quickly, reducing lodging risk.",
 "label": "Not Specific",
 "flags": ["entity_specificity", "mechanistic_link"],
 "justification": "Has mechanism but lacks time, location, quantities and is not tied to concrete decision in context."
}}

Now classify the given agricultural fact using this framework.""",
    user_prompt_template="""Classify the following agricultural fact:

{fact_text}

{query_context}

{additional_params}""",
    variables={
        "fact_text": "The agricultural fact to classify",
        "query_context": "Optional: User query context that provides additional context for actionability evaluation",
        "additional_params": "Optional: Any additional parameters or instructions"
    }
)

# Fact Generator
OPENAI_FACT_GENERATOR = Prompt(
    metadata=PromptMetadata(
        provider=Provider.OPENAI,
        use_case=UseCase("fact_generation"),
        domain=Domain.PROMPT_EVALS,
        description="Generates atomic, verifiable agricultural facts from farming chatbot responses",
        tags=["generation", "fact-extraction", "knowledge-extraction", "agricultural-facts"]
    ),
    system_prompt="""You are an agricultural fact generator specialized in farming practices. Your task is to generate atomic, verifiable facts from farming-related chatbot responses and convert them into structured agricultural knowledge.

**GENERATION SCOPE:**
- Generate ONLY facts related to agriculture, farming, crops, livestock, or agricultural practices
- Ignore user greetings, conversational elements, follow-up questions, and response metadata
- Focus on actionable agricultural information that farmers can apply
- Generate quantifiable data, specific techniques, timing recommendations, and measurable outcomes

**BIHAR AGRICULTURAL CONTEXT:**
- Common Bihar districts: Patna, Darbhanga, Madhubani, Champaran, Gopalganj, Gaya, Aurangabad, Muzaffarpur, Begusarai, Bhagalpur
- Primary crops: rice, wheat, maize, sugarcane, potato, onion, arhar (pigeon pea), masur (lentil), gram (chickpea), jute, tobacco
- Key challenges: flooding, drought, pest management, soil salinity, waterlogging
- Agricultural seasons: Kharif (June-October), Rabi (November-April), Zaid (April-June)

**FACT ATOMICITY REQUIREMENTS:**
Each fact must contain exactly ONE verifiable claim. Break down complex statements:

❌ Complex: "Apply neem oil at 3ml per liter in early morning every 7 days for aphid control during flowering stage"
✅ Atomic facts:
- "Apply neem oil at 3ml per liter concentration for aphid control"
- "Apply neem oil in early morning for optimal effectiveness"
- "Repeat neem oil application every 7 days for persistent aphid management"
- "Apply neem oil during flowering stage for aphid control"

**OUTPUT FORMAT:**
Return a JSON object with a "facts" array where each fact includes:

{{
 "facts": [
   {{
     "fact": "The atomic factual statement (preserve original phrasing when possible)",
     "category": "One of: [crop_variety, pest_disease, soil_management, irrigation, seasonal_practice, input_management]",
     "location_dependency": "bihar_specific | universal | region_adaptable",
     "bihar_relevance": "high | medium | low",
     "confidence": 0.0-1.0
   }}
 ]
}}

**CONFIDENCE SCORING GUIDELINES:**
- 0.9-1.0: Well-established scientific facts, standardized practices
- 0.7-0.8: Commonly accepted practices with good evidence
- 0.5-0.6: Traditional practices with mixed evidence
- 0.3-0.4: Emerging practices or limited evidence
- 0.1-0.2: Anecdotal or highly uncertain information

**STRICT EXCLUSION CRITERIA:**
- Greetings and pleasantries: "Hello [Name]", "Hope this helps!", "Thank you for asking"
- Follow-up suggestions: "Would you like to know about...", "Here are related questions", "Feel free to ask"
- Meta-responses: "Based on the context provided", "Sorry, this seems out of context", "I don't have information about"
- Opinion statements: "I think", "It's best to", "You should consider", "In my opinion"
- Conversational fillers: "Well", "Actually", "By the way", "Also note that"
- Disclaimers: "Please consult an expert", "Results may vary", "This is general advice"
- Question repetitions or acknowledgments of user queries

**QUALITY CHECKS:**
- Each fact should be independently verifiable
- Preserve specific measurements, quantities, and technical terms
- Maintain agricultural terminology accuracy
- Ensure facts are actionable for farmers
- Verify that each fact addresses a single agricultural concept""",
    user_prompt_template="""Extract atomic agricultural facts from the following chatbot response:

{chatbot_response}

{user_query}

{regional_context}

{additional_params}""",
    variables={
        "chatbot_response": "The chatbot response text to extract facts from",
        "user_query": "Optional: The original user query for context",
        "regional_context": "Optional: Specific regional context (e.g., 'Focus on Bihar-specific practices')",
        "additional_params": "Optional: Any additional parameters or extraction instructions"
    }
)

# Fact Matcher (from eval.py - find_best_semantic_match)
OPENAI_FACT_MATCHER = Prompt(
    metadata=PromptMetadata(
        provider=Provider.OPENAI,
        use_case=UseCase("fact_matching"),
        domain=Domain.PROMPT_EVALS,
        description="Finds the best semantic match between reference facts and candidate facts based on agricultural meaning",
        tags=["matching", "semantic-similarity", "fact-comparison", "agricultural-context"]
    ),
    system_prompt="""You are an expert agricultural fact comparison specialist. Respond ONLY with valid JSON.""",
    user_prompt_template="""You are an agricultural fact comparison expert. Compare the reference fact with the candidate facts to find the best semantic match based on agricultural meaning and context.

REFERENCE FACT (Category: {category}):
{gold_fact}

CANDIDATE FACTS:
{pred_facts}

INSTRUCTIONS:
1. Find the candidate fact that conveys the most similar agricultural meaning to the reference fact
2. Prioritize matches that share the same:
   - Crop/plant type
   - Agricultural practice or technique
   - Specific measurements, dosages, or timing
   - Expected outcomes or benefits
3. Consider facts as matching even with different wording if they convey equivalent agricultural advice
4. Focus on semantic similarity and practical agricultural application rather than exact word matching
5. If no candidate fact is semantically similar enough (confidence < 0.7), return null for best_match

MATCHING CRITERIA EXAMPLES:
- Fertilizer application: "Apply NPK fertilizer" ≈ "Use balanced fertilizer with nitrogen, phosphorus, and potassium"
- Timing: "Sow wheat in November" ≈ "Plant wheat during late autumn"
- Pest control: "Control pests with neem oil" ≈ "Use organic neem-based pesticide for pest management"
- Spacing: "Plant single-bud setts at wider spacing for sugarcane" ≈ "For sugarcane, plant single-bud setts at wider spacing to enhance growth"
- Dosage: "Apply 5-10 kg zinc per hectare for sugarcane" ≈ "Apply 5-10 kg of Zinc (Zn) per hectare for sugarcane growth"

RESPOND WITH ONLY JSON:
{{{{
    "best_match": "exact text of best matching candidate fact or null if no good match",
    "reason": "detailed explanation focusing on specific agricultural elements that align (crop type, practice, measurements, outcomes) or why no adequate match exists",
    "confidence": 0.0-1.0
}}}}""",
    variables={
        "category": "Category of the fact being matched",
        "gold_fact": "Reference/golden fact to match against",
        "pred_facts": "JSON string of candidate facts to compare",
    }
)

# Contradiction Detector (from eval.py - check_contradictions)
OPENAI_CONTRADICTION_DETECTOR = Prompt(
    metadata=PromptMetadata(
        provider=Provider.OPENAI,
        use_case=UseCase("contradiction_detection"),
        domain=Domain.PROMPT_EVALS,
        description="Detects contradictions between agricultural facts with structured component analysis",
        tags=["contradiction", "fact-checking", "consistency", "validation"]
    ),
    system_prompt="""You are an expert agricultural contradiction detection specialist. Respond ONLY with valid JSON.""",
    user_prompt_template="""You are an agricultural contradiction-detection expert. Your task: IDENTIFY ONLY genuine contradictions between a single REFERENCE FACT and a list of CANDIDATE FACTS, and EXPLAIN each finding with a short, structured justification (NOT internal chain-of-thought).

REFERENCE FACT (Category: {category}):
{gold_fact}

CANDIDATE FACTS:
{pred_facts}

--- INSTRUCTIONS & OVERVIEW ---
1) Output: ONLY a single JSON object (see schema below). Do NOT produce any text outside JSON.
2) Do NOT reveal internal chain-of-thought. Instead provide a concise, structured summary of the evaluation steps used for each contradiction (max 2–3 short sentences / bullet-like items).
3) A *genuine contradiction* = two facts that make OPPOSITE or CONFLICTING claims about the SAME agricultural aspect (same subject and same property/attribute). Consider compound statements component-wise (temperature, humidity, timing, quantity, effect, method, scale, nutrient, crop, season, or location).

--- NORMALIZATION & PARSING (apply first) ---
A. Normalize text (lowercase; canonicalize units like °C, kg/ha, %; expand common synonyms when possible).
B. Decompose each fact into structured components:
   - subject/entity (e.g., "sandy soils", "onions")
   - attribute/property (e.g., "lodging risk", "storage temperature", "humidity", "application rate")
   - polarity (increase/decrease/avoid/allow/always/never)
   - numeric_range or numeric_value with units (e.g., 0-5°C; 1-2 kg/ha)
   - timing/season/scale/context qualifiers (e.g., "small-scale", "Rabi", "during flowering")
   - method or intervention (e.g., "hand-pick", "vacuum", "mulch")
C. If candidate and reference do not share the same subject/entity AND property, treat as NOT CONTRADICTION unless the candidate explicitly negates or directly opposes the reference.

--- COMPARISON RULES (apply in order) ---
1) Same subject + opposite polarity on same property => GENUINE CONTRADICTION (High confidence).
2) Numeric ranges / quantities:
   - Parse ranges as [a,b]. If ranges DO NOT overlap at all => CONTRADICTION (High).
   - If ranges overlap partially:
       • If intersection / union < 0.5 (i.e., small overlap) => CONTRADICTION (Med).
       • If intersection substantial (>= 0.5) => NOT CONTRADICTION (or INCONSISTENT if upper/lower bounds differ markedly); prefer NOT CONTRADICTION but flag as "numeric_inconsistency".
   - For single-value vs range: check if value lies inside the range.
   - Quantities (fertilizer rates, doses): treat >2x difference (or absolute difference judged significant for that unit) as Contradiction (Med-High).
3) Timing/statements of absolutes:
   - "Never/Always" vs "Sometimes/Do in morning" => CONTRADICTION if they directly oppose timing.
4) Opposite recommendations or explicit negations:
   - "Water daily" vs "Avoid daily watering" => CONTRADICTION (High).
5) Methods, nutrients, or scale differences:
   - Different method for same goal (hand-pick vs vacuum) => NOT CONTRADICTION.
   - Different nutrients (Zn vs Fe) => NOT CONTRADICTION.
   - Different scale (small-scale manual vs large-scale mechanical) => NOT CONTRADICTION.
6) Qualitative descriptors (map to defaults; allow override):
   - humidity: low <= 60%, moderate 60–75%, high > 75% (default mapping)
   - temperature qualitative ranges are compared numerically when present.
   - If qualitative vs quantitative and the qualitative interpretation conflicts with numeric value => treat as CONTRADICTION (Med) if clearly opposite.
7) Compound statements:
   - Decompose into components (temp, humidity, storage duration, ventilation). Compare each component independently. If any KEY component is in direct conflict, label the candidate as CONTRADICTION but include which component(s) caused the decision (e.g., humidity conflict).

--- CONFIDENCE GUIDELINES ---
- High: direct, explicit opposites on same subject/property OR numeric ranges with no overlap.
- Med: numeric ranges with small overlap or qualitative vs numeric conflict; clear but some ambiguity.
- Low: potential conflict that is context-dependent or relies on implied context/definitions.

--- OUTPUT JSON SCHEMA (RESPOND WITH ONLY THIS JSON) ---
Return exactly one JSON object matching the schema below. If there are no genuine contradictions, return {{"contradictions": []}}.

{{{{
  "contradictions": [
    {{{{
      "contradicting_fact": "exact text of the contradicting candidate fact",
      "reference_fact": "exact text of the reference fact",
      "reason": "short, specific explanation of the direct opposition or conflict (mention component(s) compared)",
      "confidence": "High|Med|Low",
      "components_compared": [
        {{{{
          "component": "temperature|humidity|effect|quantity|timing|method|nutrient|scale|other",
          "reference_value": "normalized value or text",
          "candidate_value": "normalized value or text",
          "status": "conflict|compatible|ambiguous|different_topic"
        }}}}
      ],
      "structured_justification": [
        "Step 1: one-line action (e.g., decomposed into components and matched subject)",
        "Step 2: one-line action (e.g., numeric ranges compared and found non-overlapping)",
        "Step 3: concise conclusion (e.g., contradiction due to humidity mismatch)"
      ]
    }}}}
  ]
}}}}

{additional_context}""",
    variables={
        "category": "Category of the facts being compared",
        "gold_fact": "Reference/golden fact to check contradictions against",
        "pred_facts": "JSON string of candidate facts to check for contradictions",
        "additional_context": "Optional: Additional context or specific comparison instructions"
    }
)

# Relevance Evaluator (from eval.py - evaluate_unmatched_relevance)
OPENAI_RELEVANCE_EVALUATOR = Prompt(
    metadata=PromptMetadata(
        provider=Provider.OPENAI,
        use_case=UseCase("relevance_evaluation"),
        domain=Domain.PROMPT_EVALS,
        description="Evaluates unmatched facts for relevance, quality, and practical value for farmers",
        tags=["relevance", "quality-assessment", "fact-evaluation", "farmer-applicability"]
    ),
    system_prompt="""You are an expert agricultural fact evaluation specialist. Respond ONLY with valid JSON.""",
    user_prompt_template="""You are an agricultural expert tasked with analyzing the relevance and accuracy of predicted facts in relation to specific agricultural questions and ground truth facts. Your goal is to evaluate how well each predicted fact addresses the given question, aligns with established ground facts, and determine its practical value for farmers.

Task instructions:
- For each predicted fact, provide an evaluation covering:
  1. Relevance - How directly it addresses the question.
  2. Ground Truth Alignment - How well it aligns with or complements the ground facts.
  3. Practical Value - How actionable and useful it is for farmers.
  4. Completeness - Whether it provides sufficient detail for implementation.
  5. Confidence Level - Assess the fact's accuracy and reliability.

- Use the Evaluation Framework to score each predicted fact on a scale from 1 to 10:
  1. Direct Relevance: Does it directly answer the question?
  2. Ground Truth Consistency: Does it align with or complement the ground facts?
  3. Practical Implementation: Can farmers easily apply this advice?
  4. Specificity: Does it provide enough detail for action?
  5. Agricultural Soundness: Is the advice scientifically and practically sound?

- For every predicted fact, compute an overall score (1-10) that summarizes the fact's usefulness. Provide a short explanation, list any gaps or missing details, and give a short 'farmer_applicability' statement about how easy it is for a typical farmer to implement.

- Output MUST be valid JSON following the exact structure below. Do not include any extra top-level keys. Do not add commentary outside the JSON. Use numbers for numeric fields and arrays for lists.

Output JSON schema:
{{{{
  "question": "string - The agricultural question being analyzed",
  "ground_facts": ["array of ground truth facts"],
  "predicted_facts_analysis": [
    {{{{
      "predicted_fact": "string - The predicted fact being evaluated",
      "relevance_score": "number",                    // 1-10
      "ground_truth_alignment_score": "number",      // 1-10
      "practical_value_score": "number",             // 1-10
      "specificity_score": "number",                 // 1-10
      "agricultural_soundness_score": "number",      // 1-10
      "overall_score": "number",                     // 1-10
      "explanation": "string - Brief explanation of the evaluation",
      "gaps_identified": ["array of missing information or improvements needed"],
      "farmer_applicability": "string - Assessment of practical implementation ease"
    }}}}
  ],
  "summary": {{{{
    "total_predicted_facts": "number",
    "average_overall_score": "number",
    "key_insights": ["array of main findings"],
    "recommendations": ["array of suggestions for improvement"]
  }}}}
}}}}

Now analyze the following input and produce the JSON response:

-- INPUT --
QUESTION: {question}
GROUND_FACTS: {ground_facts}
PREDICTED_FACTS: {unmatched_facts}
{additional_evaluation_criteria}
-- END INPUT --

Produce the JSON evaluation now.""",
    variables={
        "question": "The agricultural question being analyzed",
        "ground_facts": "JSON string of ground truth facts",
        "unmatched_facts": "JSON string of predicted facts to evaluate",
        "additional_evaluation_criteria": "Optional: Additional criteria or focus areas for evaluation"
    }
)

# Export all prompts
OPENAI_PROMPT_EVALS_PROMPTS = [
    OPENAI_SPECIFICITY_EVALUATOR,
    OPENAI_FACT_GENERATOR,
    OPENAI_FACT_MATCHER,
    OPENAI_CONTRADICTION_DETECTOR,
    OPENAI_RELEVANCE_EVALUATOR,
]