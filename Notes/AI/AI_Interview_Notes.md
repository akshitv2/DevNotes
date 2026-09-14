# AI Topics for Dev/Tech Leads

## 1. LLM Fundamentals

**What to know:**

- **Transformer architecture** — self-attention lets the model weigh relationships between all tokens in a sequence
  simultaneously, rather than processing sequentially like RNNs. Know the rough shape: embeddings → positional
  encoding → stacked attention + feed-forward blocks → output layer.
- **Tokenization** — text is broken into subword tokens (e.g., BPE). Explains why "strawberry" letter-counting fails,
  why non-English languages often cost more tokens, and why pricing/context limits are token-based, not word-based.
- **Context window** — the max tokens (input + output) a model can process at once. Bigger isn't free: "lost in the
  middle" effects mean models attend less reliably to content buried in a huge context, even within the stated limit.
- **Autoregressive generation** — models predict one token at a time based on everything before it. This is *why*
  techniques like chain-of-thought work: letting the model "think out loud" gives it more intermediate tokens to
  condition on before the final answer.
- **Temperature / top-p / top-k** — sampling parameters controlling randomness. Low temperature = deterministic/factual
  tasks; higher = creative tasks. A tech lead should know *when* to tune these, not just what they are.

**Likely interview angle:** "Why does an LLM hallucinate?" — because it's a next-token predictor optimized for
plausibility, not a database with retrieval guarantees. It has no built-in mechanism to say "I don't know" unless
trained/prompted to.

---

## 2. Prompt Engineering

This is the most "developer" of the classic topics — expect hands-on questions, not just definitions.

- **Zero-shot vs few-shot prompting** — few-shot (giving 2-5 examples in the prompt) reliably improves consistency of
  format and style for narrower tasks; costs context budget though.
- **Chain-of-thought (CoT)** — asking the model to reason step-by-step before answering improves accuracy on
  multi-step/logical tasks. Modern "reasoning models" (o-series, Claude extended thinking) internalize this rather than
  requiring explicit prompting.
- **System prompts vs user prompts** — system prompt sets persistent behavior/role/constraints; user prompt is the task.
  Interviewers may ask how you'd structure a system prompt for a production app (tone, guardrails, output format,
  refusal behavior).
- **Structured output** — forcing JSON/XML output via schema constraints (e.g., JSON mode, function-calling schemas,
  Pydantic validation) is critical for anything downstream-parseable. Know the difference between "asking nicely for
  JSON" (unreliable) and constrained decoding / tool-call schemas (reliable).
- **Prompt injection** — untrusted content (a webpage, a user-uploaded doc, a retrieved chunk) contains instructions
  that hijack the model's behavior. This is the #1 security concern for anything that feeds external content into a
  prompt. Mitigations: input/output sanitization, privilege separation (don't let the model take irreversible actions
  from untrusted-content-derived instructions without confirmation), instruction hierarchy (system > developer > user >
  tool output).
- **Prompt versioning/testing** — treat prompts like code: version them, diff them, regression-test them against a
  golden set before shipping changes. This is a strong signal of maturity to bring up unprompted.

**Likely interview angle:** "How would you make an LLM feature reliable in production?" — expect you to mention
structured outputs, eval sets, prompt versioning, and fallback/retry logic, not just "write a good prompt."

---

## 3. Retrieval-Augmented Generation (RAG)

- **Why it exists** — grounds model responses in your own data without retraining; reduces hallucination by giving the
  model source material to cite/quote from.
- **Pipeline**: ingest → chunk → embed → store in vector DB → at query time, embed the query → retrieve top-k similar
  chunks → stuff into context → generate.
- **Chunking strategy** matters a lot in practice — too small loses context, too large wastes tokens and dilutes
  relevance. Semantic/paragraph-aware chunking usually beats fixed-size splitting.
- **Embeddings & vector search** — dense vector similarity (cosine/dot product) captures semantic meaning, not just
  keyword overlap. Hybrid search (BM25 keyword + vector) often outperforms pure vector search in practice, especially
  for exact-match needs (IDs, names, codes).
- **Reranking** — a second-pass model that reorders retrieved candidates by relevance before they hit the final prompt;
  cheap way to meaningfully boost RAG quality.
- **Failure modes**: stale embeddings after data changes, retrieval returning irrelevant-but-similar chunks, context
  window overflow from too many retrieved chunks, no clear "not found" path when nothing relevant exists.

**Likely interview angle:** "When would you use RAG vs fine-tuning vs just a bigger context window?" — see comparison in
section 4.

---

## 4. RAG vs Fine-Tuning vs Long Context vs Prompting

A classic "trade-off" interview question. Framework to answer it:

| Approach                               | Best for                                                                                                                                    | Weakness                                                                                               |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Prompting/few-shot**                 | Quick iteration, small tasks, format control                                                                                                | Doesn't scale to large knowledge bases                                                                 |
| **RAG**                                | Frequently-changing or large external knowledge, need for citations/freshness                                                               | Retrieval quality bottleneck, added infra complexity                                                   |
| **Long context (stuff everything in)** | Simplicity, small-to-medium fixed knowledge bases                                                                                           | Cost, latency, "lost in the middle," doesn't scale indefinitely                                        |
| **Fine-tuning**                        | Teaching a *style*, *format*, or *behavior* the base model doesn't have; domain-specific tone; reducing prompt length for high-volume tasks | Doesn't reliably teach new *facts*; expensive, slower iteration, needs retraining as knowledge changes |

Key insight to voice out loud: **fine-tuning is for behavior, RAG is for knowledge.** Conflating these is a common
junior mistake and a good thing to explicitly call out.

---

## 5. AI Agents

Expect real depth here — this is where "tech lead" questions differentiate from generic AI trivia.

- **Definition** — a system where an LLM doesn't just respond once, but runs in a loop: observes state, decides an
  action (often a tool call), executes it, observes the result, and repeats until a goal is met or a stop condition is
  hit.
- **ReAct pattern** (Reason + Act) — the model interleaves reasoning traces with tool calls, using the tool output to
  inform the next reasoning step. Foundational pattern behind most agent frameworks.
- **Tool use / function calling** — the model is given a schema of available tools (name, description, parameters) and
  outputs a structured call rather than free text; the *application* (not the model) executes the actual function and
  feeds the result back in. Know that the model doesn't execute anything itself — this is a common misconception to
  correct in an interview.
- **Planning** — for multi-step tasks, agents may explicitly plan (decompose a goal into subtasks) before acting, either
  in one upfront plan or interleaved re-planning as new information arrives. Re-planning is more robust but costs more
  tokens/latency.
- **Memory** — short-term (conversation/scratchpad within a run) vs long-term (persisted across sessions, often via a
  vector store or key-value store). Distinguish this from context window — memory is a system design choice about *what
  gets fed back into* context, not an inherent model capability.
- **Guardrails & control** — the biggest real-world agent risk is *unbounded* or *irreversible* actions (e.g., an agent
  that can send emails or make purchases). Standard mitigations: human-in-the-loop confirmation for high-stakes actions,
  scoped/least-privilege tool permissions, action allowlists, spend/step limits, sandboxing.
- **Multi-agent systems** — splitting work across specialized agents (e.g., a planner, a coder, a reviewer) that
  communicate via a shared state or message passing. Trade-off: better separation of concerns and specialization vs
  added orchestration complexity, latency, and cost (more LLM calls). A good answer notes that multi-agent isn't
  automatically better — often a single well-prompted agent with good tools outperforms a complex multi-agent setup for
  simpler tasks.
- **Evaluating agents** — harder than evaluating single-turn LLM output because you need to judge trajectories (did it
  take a reasonable path?), not just final answers. Common approaches: task success rate on a held-out task suite,
  step-count/cost efficiency, and human or LLM-as-judge review of the reasoning trace.

**Likely interview angle:** "Design an agent that can [do X]." Expect to talk through: what tools it needs, what the
loop/stop condition looks like, where a human needs to be in the loop, and how you'd evaluate/monitor it in production —
not just "give it a prompt and some tools."

---

## 6. Model Context Protocol (MCP) & Tool Ecosystems

- MCP is an open standard (from Anthropic) for connecting LLM applications to external tools/data sources through a
  common protocol, instead of every app writing bespoke integrations for every tool. Worth knowing conceptually: it's
  the "USB-C for AI tools" analogy — a standard interface rather than N×M custom integrations.
- Relevant framing for a tech lead: this is an *integration/architecture* decision, similar to picking a standard API
  protocol. Interviewers may ask how you'd decide between building custom tool integrations vs adopting a protocol like
  MCP for a growing set of tools.

---

## 7. Evaluation & Observability for LLM Systems

- **Evals** — a curated set of test cases (inputs + expected properties of outputs) run against the system, ideally
  automatically, on every prompt/model change. Distinguish:
    - *Reference-based evals* (exact match, similarity to a golden answer) — good for structured/deterministic tasks.
    - *LLM-as-judge* — using a strong model to grade outputs against a rubric — useful for open-ended quality but has
      known biases (favors verbose answers, self-preference bias) and needs calibration against human judgment.
    - *Human eval* — the ground truth for subjective quality, but expensive/slow — usually sampled, not exhaustive.
- **Benchmarks vs production evals** — public benchmarks (MMLU, HumanEval, etc.) tell you about general model
  capability, not whether *your* prompt/pipeline works. Always build a task-specific eval set.
- **Observability** — logging prompts, outputs, latency, token usage, and (where applicable) tool calls/trajectories in
  production. Needed for debugging regressions, catching drift when providers update models silently, and cost tracking.
- **Hallucination detection** — no silver bullet; practical mitigations are grounding via RAG, requiring citations,
  self-consistency checks (sample multiple times, check agreement), and downstream verification steps for high-stakes
  outputs.

**Likely interview angle:** "How do you know if a prompt change made things better or worse?" — this is really asking
whether you have an eval-driven mindset, the LLM equivalent of "how do you know your code change didn't break anything."

---

## 8. Model Selection & Trade-offs

Interviewers like this because it's a genuine engineering trade-off question, not trivia:

- **Latency vs quality vs cost** — bigger/smarter models cost more and are slower; often the right architecture uses a
  cheap/fast model for routing or simple sub-tasks and a stronger model only where needed (model cascading/routing).
- **Context length** — needed for long-document or long-conversation use cases, but longer context increases cost and
  can degrade retrieval accuracy within the prompt.
- **Open-weight vs closed/API models** — open-weight models (Llama, Mistral, etc.) allow self-hosting, fine-tuning, and
  data control, at the cost of infra/ops burden; closed API models (Claude, GPT) trade control for ease of integration,
  managed scaling, and typically stronger frontier performance.
- **Multimodal capability** — whether you need image/audio/video input or just text — narrows model choice immediately.
- **Structured-output / tool-calling reliability** — not all models are equally good at reliable function calling; this
  matters a lot for agentic use cases specifically.

---

## 9. Cost & Performance Optimization

- **Prompt caching** — reusing a cached prefix (e.g., a long system prompt or document) across requests to cut
  cost/latency on repeated content.
- **Batching** — for non-realtime workloads, batch APIs offer meaningfully lower cost in exchange for higher latency.
- **Streaming** — returning tokens as they're generated rather than waiting for the full response; a UX necessity for
  chat interfaces, not a cost optimization per se.
- **Prompt compression / trimming context** — summarizing or pruning conversation history instead of sending the full
  transcript on every turn, especially in long agent loops where context otherwise grows unbounded.
- **Model right-sizing** — using the smallest/cheapest model that meets the quality bar for a given sub-task, reserving
  frontier models for the parts of a pipeline that actually need them.

---

## 10. Safety, Security & Responsible AI

- **Prompt injection** (see section 2) — the top security concern for anything ingesting untrusted content.
- **Data privacy** — what happens to data sent to a third-party model API (retention policies, zero-data-retention
  options, PII redaction before sending to external APIs).
- **Guardrails** — input/output filtering for disallowed content, PII leakage, or off-brand responses; can be
  rule-based, classifier-based, or a secondary LLM check.
- **Bias & fairness** — models can reflect biases in training data; relevant if the system makes consequential
  decisions (hiring, lending, moderation) — worth mentioning that such use cases need extra evaluation and human
  oversight.
- **Regulatory awareness** — high-level familiarity with the fact that regulations (EU AI Act, sector-specific rules)
  increasingly require risk categorization, transparency, and human oversight for certain AI use cases — you're not
  expected to be a lawyer, but awareness signals maturity.

---

## 11. LLMOps / Production Architecture Patterns

- **Common product architectures**: simple chat wrapper → RAG-augmented assistant → tool-using agent → multi-agent
  orchestration. Know how to place a given product requirement on this spectrum rather than jumping straight to the most
  complex option.
- **Versioning**: pin model versions explicitly in production (providers deprecate/update models); treat prompt + model
  version + tool schema as a single deployable unit.
- **Fallbacks & retries**: handle rate limits, timeouts, and malformed structured outputs gracefully — e.g., retry with
  a stricter schema reminder, or fall back to a smaller/more reliable model.
- **Human-in-the-loop design**: decide upfront which actions need confirmation, which can be fully automated, and how a
  human reviewer sees/overrides agent behavior when something looks wrong.
- **A/B testing prompts and models**: same discipline as feature-flagging any other product change, since model/prompt
  changes can shift behavior in non-obvious ways.

---

## Quick-Reference: Likely "Explain the difference" Questions

- **Fine-tuning vs prompting vs RAG** — behavior vs instruction vs knowledge (see section 4).
- **Agent vs chatbot** — chatbot responds once per turn; agent loops, calls tools, and pursues a goal across multiple
  steps autonomously.
- **Embedding vs fine-tuning** — embeddings are for *retrieval/similarity*, fine-tuning is for *changing model
  behavior*. Different tools, not interchangeable.
- **Hallucination vs bias** — hallucination is confidently generating false/unsupported content; bias is systematically
  skewed output reflecting patterns in training data. Different root causes, different mitigations.
- **Zero-shot vs one-shot vs few-shot** — number of in-prompt examples provided (0, 1, several) before the actual task.
- **Context window vs memory** — context window is a hard architectural token limit per call; memory is a system-level
  design choice about what gets carried forward into that window across turns/sessions.

---

*Tip for the interview itself: for almost any AI system-design question, structure your answer as: (1) what's the
simplest approach that could work, (2) what breaks it at scale, (3) what you'd add to fix that, and (4) how you'd know
it's working (evals/observability). That progression signals engineering judgment more than reciting the fanciest
architecture up front.*
