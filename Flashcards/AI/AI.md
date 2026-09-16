Front: What is the core mechanism of the Transformer architecture?
Back: Self-attention, which allows the model to weigh relationships between all tokens in a sequence simultaneously instead of processing them sequentially like RNNs.

---

Front: What is tokenization and why does it affect LLM costs and behavior?
Back: Tokenization breaks text into subword units (e.g., BPE). Non-English languages take more tokens per word (costing more), and models process text by token chunks, explaining why letter-counting tasks often fail.

---

Front: What is the "lost in the middle" effect in long-context models?
Back: LLMs attend less reliably to information located in the middle of a massive context window compared to information at the beginning or end.

---

Front: How does autoregressive generation enable techniques like Chain-of-Thought (CoT)?
Back: Models predict one token at a time based on all prior tokens. CoT forces the model to generate intermediate reasoning tokens, giving it more context to condition on before producing the final answer.

---

Front: How do Temperature, Top-p, and Top-k sampling parameters control LLM output?
Back: They adjust randomness during token selection. Low values produce deterministic, factual outputs, while higher values yield more creative outputs.

---

Front: Why do LLMs hallucinate?
Back: LLMs are next-token predictors optimized for plausibility rather than retrieved facts, lacking a built-in mechanism to verify truth or admit missing knowledge.

---

Front: Zero-Shot vs. Few-Shot Prompting
Back:

* Zero-Shot: Prompting without examples.
* Few-Shot: Providing 2–5 examples within the prompt to improve consistency in formatting and style at the cost of context space.

---

Front: System Prompts vs. User Prompts
Back:

* System Prompt: Sets persistent rules, behavior, persona, and output constraints.
* User Prompt: Represents the specific task or input submitted for execution.

---

Front: Asking for JSON vs. Constrained Decoding / Schemas
Back: Requesting JSON in plain text is unreliable. Enforcing JSON via function-calling schemas, Pydantic validation, or constrained decoding guarantees downstream parseability.

---

Front: What is prompt injection and how is it mitigated?
Back: Untrusted external content Hijacks model instructions.
Mitigations:

* Input/output sanitization
* Enforcing instruction hierarchy (System > User > Tool)
* Privilege separation for sensitive actions

---

Front: Prompt Versioning Best Practices
Back: Treat prompts like code: version, diff, and run automated regression tests against a golden eval set before deployment.

---

Front: Key components of a basic RAG pipeline
Back:

1. Ingest & Chunk documents
2. Generate Embeddings & store in Vector DB
3. Retrieve top-k relevant chunks based on query embedding
4. Inject chunks into the prompt context to Generate answer

---

Front: Dense Vector Search vs. Hybrid Search
Back:

* Dense Vector: Captures semantic meaning via cosine/dot similarity.
* Hybrid Search: Combines vector search with keyword search (e.g., BM25) for better precision on exact terms like IDs or names.

---

Front: What is Reranking in RAG?
Back: A secondary scoring model that re-orders the retrieved chunks by relevance before they are inserted into the final context window.

---

Front: Primary rule for choosing between Fine-Tuning and RAG
Back: Fine-tuning is for teaching **behavior/style**, whereas RAG is for providing **knowledge/facts**.

---

Front: Trade-offs: Prompting vs. RAG vs. Fine-Tuning vs. Long Context
Back:

* Prompting: Fast iteration; limited context capacity.
* RAG: Fresh/large knowledge; retrieval complexity.
* Long Context: Simple integration; expensive and prone to context degradation.
* Fine-Tuning: Custom behavior/style; costly and unreliable for static facts.

---

Front: Definition of an AI Agent
Back: A loop-based system where an LLM observes state, decides on an action (such as calling a tool), executes it, and repeats until a goal or stop condition is met.

---

Front: ReAct Pattern
Back: Reasoning + Acting: An agent pattern interleaving explicit reasoning steps ("Thought") with execution steps ("Action") based on dynamic tool outputs.

---

Front: How do LLM tools/function calls execute?
Back: The LLM does **not** run code. It outputs structured arguments adhering to a schema, which the host application executes before returning the result back to the model context.

---

Front: Short-Term vs. Long-Term Agent Memory
Back:

* Short-Term: Active conversation and intermediate scratchpad tokens within the context window.
* Long-Term: Context persisted across sessions using databases or vector search.

---

Front: Key techniques for Agent safety and guardrails
Back:

* Human-in-the-loop approvals for sensitive actions
* Scoped least-privilege tool permissions
* Action allowlists and max step/cost limits
* Isolated execution sandboxes

---

Front: Single-Agent vs. Multi-Agent Systems
Back: Multi-agent systems delegate specialized roles across agents, improving separation of concerns at the expense of higher latency, token cost, and orchestration complexity.

---

Front: What is the Model Context Protocol (MCP)?
Back: An open standard designed to simplify tool and data integrations by providing a unified protocol between AI client applications and external tools.

---

Front: Reference-based Evals vs. LLM-as-a-Judge vs. Human Eval
Back:

* Reference-based: Exact/similarity match for deterministic tasks.
* LLM-as-a-Judge: Scalable evaluation using strong models with rubrics; prone to verbosity and self-preference bias.
* Human Eval: High-quality ground truth; costly and difficult to scale.

---

Front: Public Benchmarks vs. Production Evals
Back: Public benchmarks (e.g., MMLU) measure broad model abilities, whereas task-specific production evals measure performance on your specific system domain and data.

---

Front: Open-Weight vs. Closed/API Models
Back:

* Open-Weight: Full control, self-hosting capability, and private fine-tuning; higher operational cost.
* Closed API: Simpler setup and access to cutting-edge models; relies on third-party infrastructure and pricing.

---

Front: Model Cascading / Routing
Back: Directing simpler or routing queries to cheaper/faster models and reserving large frontier models for complex tasks to optimize cost and latency.

---

Front: Prompt Caching
Back: Storing and reusing static prompt prefixes (like system prompts or large static documents) to cut API latency and token costs on repetitive calls.

---

Front: Context Window vs. Agent Memory
Back: The context window is the hard token limit per model call; memory is the application design strategy determining what historical information fits into that window.