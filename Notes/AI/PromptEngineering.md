---
title: Prompt Engineering
nav_order: 3
parent: AI
layout: default
---

# Prompt Engineering

1. ## Fundamentals of Generative AI
    - LLM Mechanics:
        - Large Language Models (LLMs) predict the next most likely token in a sequence based on patterns learned during
          training.
        - Prioritize plausibility over objective truth.
    - Tokens vs. Words:
        - LLMs process tokens, which are chunks of characters, rather than individual words
    - The Prompt:
        - The specific input (instruction, context, data) provided to the AI to elicit a response.
    - Prompt Engineering:
        - The systematic process of structuring text to influence the model's latent space, maximizing the relevance,
          accuracy, and consistency of the output.
2. ### Components:
    1. Instructions:
        - The specific task you want model to perform
        - Example: Summarize
    2. Context: External information, background, or target audience details the model needs to guide its response.
    3. Input Data: : The specific piece of content or data provided for processing..
    4. Output Indicator: Target format or style.
    5.
        * Persona: Optional but provides context to thinking by using Act as
    6.
        * Constraints: Telling model what not to do
3. ### Mechanics of LLM:
    - Models just predict the next token (sub-word unit) based on probability distributions.
4. ## Strategies
    1. ## Zero-shot vs Few Shot:
        1. ### Zero-shot: Direct instruction without examples.
            - Example:
                - Prompt: "Translate 'The library is closed on Sundays' into French."
                - Output: "La bibliothèque est fermée le dimanche."
        2. ### Few-shot: Using examples to establish patterns.
            - Prompt:
                - "Great movie! // Positive"
                - "That was a waste of time. // Negative"
                - "The acting was mediocre. // Neutral"
                - "I’ve never seen anything better! //"
            - Output: "Positive"
    2. ### Chain-of-Thought (CoT):
        - Forcing step-by-step reasoning.
        - This forces the AI to break down complex reasoning into intermediate steps, significantly reducing logical
          errors in math or symbolic tasks.
        - Prompt: "A cafeteria has 23 apples. If they use 20 to make lunch and buy 6 more, how many apples do they
          have?
          Think through this step-by-step."
        - Output:
            1. The cafeteria started with 23 apples.
            2. They used 20, so $23 - 20 = 3$
            3. They bought 6 more, so $3 + 6 = 9$
            4. They have 9 apples.
    3. ### Tree of Thoughts (ToT):
        - Encouraging the model to explore and evaluate multiple reasoning paths simultaneously to find an optimal
          solution.
        - Example:
            - Prompt:
                - Goal: Solve this puzzle: "I have 4 liters of water, a 3-liter jug, and a 5-liter jug. How do I get
                  exactly 4 liters into the 5-liter jug?"
                - Instructions:
                    - Phase 1: Brainstorming. Create three distinct initial steps (Thoughts A, B, and C).
                    - Phase 2: Evaluation. Analyze the viability of each step. Which one leads to a dead end? Which one
                      is most efficient?
                    - Phase 3: Expansion. Take the most promising thought and develop the next two steps.
                    - Phase 4: Decision. Provide the final sequence of actions.
            - Model Execution:
                - Phase 1: Brainstorming
                    - Thought A: Fill the 3L jug first and pour it into the 5L jug.
                    - Thought B: Fill the 5L jug first and pour it into the 3L jug.
                    - Thought C: Fill both jugs halfway.
                - Phase 2: Evaluation
                    - Eval A: Leads to 3L in the 5L jug. Useful, but requires more steps to reach exactly 4L.
                    - Eval B: Filling the 5L first allows you to immediately subtract 3L (leaving 2L). This is a strong
                      mathematical starting point for reaching 4L.
                    - Eval C: Discard. Standard jugs do not have measurement markings; "halfway" is an imprecise guess.
                - Phase 3: Expansion (Following Thought B)
                    - Step 1: Fill the 5L jug. Pour it into the 3L jug. (Result: 2L remains in the 5L jug).
                    - Step 2: Empty the 3L jug. Pour the 2L from the 5L jug into the 3L jug. (Result: 3L jug now has 2L;
                      1L
                      of space remains).
                    - Phase 4: Final Decision/Solution
                    - Step 3: Fill the 5L jug again.
                    - Step 4: Pour water from the 5L jug into the 3L jug until it is full. Since the 3L jug already had
                      2L,
                      it only takes 1L from the 5L jug.
                - Final Result: The 5L jug now contains exactly 4 liters.
    4. ### Self-Consistency:
        - Running the same prompt multiple times and selecting the most frequent answer (the "majority vote" method) to
          increase reliability.
    5. ### Generated Knowledge: model first generates relevant facts or information about a topic, then uses that specific
       knowledge to produce a more accurate final response.
        - Prompt 1: "List three key physical requirements for growing orchids."
        - Prompt 2 (Using output from 1): "Based on the need for high humidity, indirect light, and airflow, explain
          why
          a bathroom windowsill might be a good or bad location for an orchid."
        - Output: An analysis explaining that while the bathroom provides the necessary humidity, the windowsill
          must be
          checked for direct sun exposure (which could scorch leaves) and adequate ventilation to prevent mold.'
    6. ### Act as technique
        - Using persona-driven prompting (e.g., "Act as a Senior DevOps Engineer") to narrow the model's focus and
          vocabulary.
    7. ### ReAct (Reasoning + Acting) Framework
       - ReAct addresses the limitations of standard LLMs—specifically their tendency to hallucinate and their lack of access to real-time data.
       - The framework structures the AI's output into a repeatable loop:
         - Thought: The model verbalizes its reasoning about the task (e.g., "I need to find the current weather in Paris, so I should use a search tool").
         - Action: The model executes a specific command or calls a tool (e.g., Google Search("weather in Paris")).
         - Observation: The system feeds the result of the action back into the model (e.g., "Paris is currently 18°C with light rain").
5. ## Refinement and Parameters
    - Metrics:
        - Accuracy, formatting, and tone.
    - ## Parameters:
    - ### Temperature:
      Controls randomness. Lower values (0.0–0.3) produce deterministic, factual outputs; higher values (0.7+) increase
      creativity.
    - ### Top-P/Top-K:
      Sampling methods to limit the vocabulary considered for the next token.
    - ### Max Tokens:
        - Sets the limit on the length of the generated response.
    - ### Context Window:
        - Managing the limit of tokens an LLM can process to prevent the model from "forgetting" earlier instructions.
        - Basic models often lose context as time goes on
        - More advanced models summarize past content to maintain context but summarization also loses some context
6. ## Debugging And Refinement
    - ### System Messages:
        - Setting permanent behavioral constraints that override user-level instructions (e.g., "You are a Python expert
          who never uses external libraries").
    - ### Instruction Drift
        - To prevent "instruction drift," use distinct delimiters (e.g., ###, """, ---) to separate instructions from
          the primary data source
    - ## Completion Paradigm:
        - Modern LLMs function best when provided with a logical starting point to complete, rather than just a
          question.
    - ## Grounding:
        - Instructing the model to answer only based on a provided text
            - (e.g., "If the answer is not in the document, state that you do not know")
        - Prevents Hallucination by allowing model to accept ignorance
    - ## Negative Constraints:
      - 
7. ## Evaluation:
    - todo: Expand
    - Using objective and subjective metrics to determine if an AI response is accurate, coherent, and unbiased.
8. ## Debugging Prompts:
    - Identifying why a prompt failed and applying iterative refinement to fix it.
