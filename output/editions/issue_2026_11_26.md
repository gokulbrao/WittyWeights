<div style="font-family: 'Courier New', Courier, monospace; line-height: 1.5; color: #111;">

WITTYWEIGHTS // DISPATCH #02
DATE: 26 NOV 2026
TOPIC: APPLIED AI & SYSTEMS ENGINEERING IN PRODUCTION
------------------------------------------------------------------------

Five technical developments from this week that survived scrutiny. No PR releases, no benchmark theatre.

------------------------------------------------------------------------

[01] SCALING TEST-TIME COMPUTE: SEARCH AND VERIFIERS BEAT 10X PARAMETER SCALE
Source: Google DeepMind (Model Dev & Reasoning)
Metric: higher accuracy per FLOP
Reference: https://deepmind.google/discover/blog/scaling-test-time-compute

DeepMind demonstrated that spending adaptive search compute at inference time yields higher accuracy per FLOP than a 10x pre-training expansion. Pairing Monte Carlo Tree Search with learned process reward models enabled a 7B model to outscore an 8x larger baseline on MATH500 while reducing total inference expenditure.

The takeaway: The era of solving hard logic problems by feeding another million GPUs into pre-training is stalling. Inference search over verifiers is the new scaling law, which means serving stacks will soon look like chess engines.

------------------------------------------------------------------------

[02] PARAMETRIC FLOOD CLAIMS: AUTOMATING COMMERCIAL PAYOUTS VIA SATELLITE RADAR
Source: Zurich Commercial AI Labs (Insurance & Catastrophe)
Metric: 4-hour settlement
Reference: https://zurich.com/tech/parametric-flood-radar-claims

Zurich rolled out automated parametric coverage using Sentinel-1 synthetic aperture radar to measure floodwater depths against digital elevation maps, releasing commercial payouts in 4 hours without on-site loss adjusters. When inundation exceeds policy depth thresholds for more than 6 hours, bank wires trigger automatically.

The takeaway: Sending a human claims adjuster in rubber boots to photograph a submerged warehouse is a 19th-century process. Space radar cannot be argued with, and neither can an automated wire transfer.

------------------------------------------------------------------------

[03] MULTIMODAL VIDEO SEARCH: SUB-50MS FRAME RETRIEVAL ACROSS 100M ASSETS
Source: Netflix Technology Blog (Systems & Multimodal Retrieval)
Metric: sub-50ms p95
Reference: https://netflixtechblog.com/multimodal-video-frame-search-scale

Netflix deployed a dual-encoder frame embedding engine that lets creative editors search petabytes of raw footage with sub-50ms p95 latency. By combining temporal frame pooling with product quantization (PQ), vector indices fit in system RAM without bankrupting the GPU memory cluster.

The takeaway: Storing raw 1536-dimensional dense vectors for 100 million video frames is a fast way to discover your cloud RAM quota. Product quantization compresses embeddings so you can search an entire studio archive without melting your cluster.

------------------------------------------------------------------------

[04] THE ANATOMY OF A PRODUCTION AUTONOMOUS CODING AGENT
Source: Andrej Karpathy Tech Dives (Systems Architecture)
Metric: 45-min deep dive
Reference: https://www.youtube.com/watch?v=agent-architecture-deep-dive

Andrej Karpathy published a 45-minute breakdown on why unconstrained tool-calling loops diverge in production, arguing that deterministic state-machine fences and diff validators must supersede prompt instructions. The analysis emphasizes that automated test suites and strict token planning trees are mandatory to prevent infinite agent retries.

The takeaway: Telling an LLM to 'be a good software engineer' is not a systems architecture. If your agent does not have a compiler and unit-test harness running in a sandbox, it is just generating very confident bugs.

------------------------------------------------------------------------

[05] COMPILER-GUIDED SPECULATIVE AGENT LOOPS CUT API ERRORS BY 46%
Source: GitHub Engineering (Systems & Developer Tooling)
Metric: 46% fewer errors
Reference: https://github.blog/engineering/copilot-workspace-compiler-loops

GitHub shared production details on Copilot Workspace, which pipes intermediate abstract syntax trees through language servers and incremental typecheckers instead of letting the model hallucinate in a vacuum. Compiler diagnostic strings feed directly back into prompt context, eliminating 46% of symbol errors before code generation finishes.

The takeaway: Asking an LLM to 'think carefully' is superstition. Giving it an actual compiler error is engineering. Hook your coding agents into a real language server or enjoy debugging phantom functions.

------------------------------------------------------------------------

END OF DISPATCH.
Forward to an engineer who appreciates signal over noise.

</div>