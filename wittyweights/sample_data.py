"""
Candidate raw intelligence pool spanning all three beats:
1. Systems & Architecture
2. Insurance & FinTech (Top Priority)
3. Model Dev & Optimization
"""

from typing import List
from wittyweights.schemas import RawItem

SAMPLE_MULTI_BEAT_ITEMS: List[RawItem] = [
    # --- BEAT 1: SYSTEMS & ARCHITECTURE ---
    RawItem(
        id="sys-github-01",
        target_beat="systems_architecture",
        source_name="GitHub Engineering",
        source_category="Developer Tooling & Copilot Architecture",
        reputation_weight=0.98,
        title="Copilot Workspace: Compiler-Guided Speculative Agent Loops",
        url="https://github.blog/engineering/copilot-workspace-compiler-loops",
        published_date="2026-11-25",
        media_type="case_study",
        summary="GitHub details the production agent architecture behind Copilot Workspace, replacing single-turn generation with compiler-guided execution loops that cut hallucinated API calls by 46%.",
        raw_content="Instead of relying on LLMs to self-correct in a vacuum, the workspace architecture pipes intermediate AST diffs through language servers (LSP) and incremental typecheckers. When a syntax or type error is encountered, the compiler diagnostics feed back into the prompt context, reducing hallucinated symbol errors by 46% across Python and TypeScript codebases."
    ),
    RawItem(
        id="sys-cursor-02",
        target_beat="systems_architecture",
        source_name="Cursor / Anysphere Blog",
        source_category="Applied Coding Agents & Codebase Indexing",
        reputation_weight=0.96,
        title="Sub-Second Semantic Search Across 10M-Line Repositories",
        url="https://www.cursor.com/blog/instant-codebase-indexing-merkle",
        published_date="2026-11-22",
        media_type="blog",
        summary="Cursor shares their production indexing pipeline using Merkle trees and shadow git branches, enabling sub-second hybrid dense-sparse code retrieval across multi-million line enterprise monorepos.",
        raw_content="Full-codebase agent context requires continuously indexing file mutations as developers type. Cursor implements an incremental Merkle-tree chunking cache coupled with local sqlite vector indices and tree-sitter AST parsing, ensuring repo context lookups complete in under 80ms even in 10M+ line codebases without spinning up heavy cloud infrastructure."
    ),
    RawItem(
        id="sys-netflix-03",
        target_beat="systems_architecture",
        source_name="Netflix Technology Blog",
        source_category="Large-Scale Multimodal Retrieval & Systems",
        reputation_weight=0.94,
        title="Multimodal Video Search: Sub-50ms Frame Retrieval Across 100M Assets",
        url="https://netflixtechblog.com/multimodal-video-frame-search-scale",
        published_date="2026-11-20",
        media_type="blog",
        summary="Netflix engineering explains their dual-encoder frame embedding architecture that lets creative editors search petabytes of video footage using natural language queries with sub-50ms p95 latency.",
        raw_content="To index millions of hours of studio masters, Netflix combines temporal pooling with product quantization (PQ) vector indices. Editors can query 'close-up shot of car headlights in rainy night' and retrieve exact timecodes instantly, replacing hours of manual tagging."
    ),
    RawItem(
        id="sys-karpathy-04",
        target_beat="systems_architecture",
        source_name="Andrej Karpathy Tech Dives",
        source_category="Production Agent Architecture Breakdowns",
        reputation_weight=0.99,
        title="Video Breakdown: The Anatomy of a Production Autonomous Coding Agent",
        url="https://www.youtube.com/watch?v=agent-architecture-deep-dive",
        published_date="2026-11-24",
        media_type="video_talk",
        summary="Karpathy releases a 45-minute architectural masterclass breaking down why naive tool-calling loops diverge in production, and how deterministic state-machine fences keep agents on rails.",
        raw_content="In this 45-minute technical session, Karpathy deconstructs production coding agents. Key insights: why prompt engineering is the weakest guardrail, why deterministic file diff validators are mandatory, and how token-budgeted planning trees prevent infinite looping on edge cases."
    ),

    # --- BEAT 2: INSURANCE & FINTECH (PRIORITY) ---
    RawItem(
        id="ins-lemonade-01",
        target_beat="insurance_fintech",
        source_name="Lemonade AI & Tech Blog",
        source_category="InsurTech, Vision Claims & Autonomous FNOL",
        reputation_weight=0.97,
        title="Automating FNOL: Vision Agents Cut Auto Collision Appraisal from 5 Days to 90 Seconds",
        url="https://lemonade.com/blog/autonomous-damage-appraisal-vision-agents",
        published_date="2026-11-24",
        media_type="case_study",
        summary="Lemonade details their production vision-agent pipeline that analyzes smartphone crash photos, cross-checks vehicle parts databases, and auto-settles sub-$2,500 claims in 90 seconds with 84% straight-through processing.",
        raw_content="First Notice of Loss (FNOL) traditionally takes days of human adjuster reviews. Lemonade's pipeline couples fine-tuned segmentation models for metal tear and dent volume estimation with deterministic Mitchell parts catalog lookups and onboard vehicle telematics verification. When photo EXIF data and onboard telematics match impact dynamics, the agent authorizes immediate payout without human intervention, maintaining a sub-1.2% fraud false-positive rate."
    ),
    RawItem(
        id="ins-munichre-02",
        target_beat="insurance_fintech",
        source_name="Munich Re Tech Insights",
        source_category="Underwriting Risk Models & Reinsurance AI",
        reputation_weight=0.95,
        title="Commercial Property Underwriting: Ingesting 200-Page Loss Runs in 45 Minutes",
        url="https://munichre.com/tech/commercial-underwriting-agentic-loss-runs",
        published_date="2026-11-23",
        media_type="case_study",
        summary="Munich Re deploys a multimodal underwriting agent that extracts unstructured loss-run schedules, building sensor telemetry, and aerial roof inspections, cutting commercial underwriting triage from 4 days to 45 minutes.",
        raw_content="Commercial insurance underwriting requires parsing hundreds of pages of disparate broker PDFs, building inspection imagery, and historical loss runs. Using vision-augmented schema extractors coupled with deterministic actuarial rating tables, underwriters process submissions 6x faster while identifying unpriced roof wear and wild-fire boundary risks with 94% precision."
    ),
    RawItem(
        id="ins-root-05",
        target_beat="insurance_fintech",
        source_name="Root Insurance Tech Blog",
        source_category="InsurTech Telematics & Edge Risk Models",
        reputation_weight=0.95,
        title="Edge Telematics: Continuous Driving Risk Modeling on Mobile Neural Engines",
        url="https://root.engineering/edge-telematics-mobile-risk-models",
        published_date="2026-11-25",
        media_type="case_study",
        summary="Root details their on-device quantized neural net evaluating accelerometer and braking telemetry locally, improving auto loss ratio predictability by 18% while cutting server bandwidth costs by 85%.",
        raw_content="Instead of streaming gigabytes of raw phone sensor data to cloud clusters, Root deployed a quantized 1.5MB ConvNet directly onto iOS and Android Neural Engines. The model classifies distracted driving and sudden braking events locally, transmitting only cryptographic risk summaries. This reduced battery consumption to under 1% per trip and improved loss ratio pricing accuracy by 18%."
    ),
    RawItem(
        id="ins-zurich-06",
        target_beat="insurance_fintech",
        source_name="Zurich Commercial AI Labs",
        source_category="Parametric Insurance & Catastrophe Underwriting",
        reputation_weight=0.94,
        title="Parametric Flood Claims: Automating Payouts via Synthetic Aperture Radar",
        url="https://zurich.com/tech/parametric-flood-radar-claims",
        published_date="2026-11-25",
        media_type="case_study",
        summary="Zurich rolled out automated parametric flood coverage that ingests European Space Agency Sentinel-1 radar feeds to verify inundation depths, disbursing commercial claims in 4 hours without on-site loss adjusters.",
        raw_content="Physical adjusters often take weeks to safely access flooded commercial properties. Zurich pairs synthetic aperture radar (SAR) water backscatter measurements with local elevation digital elevation models (DEM) to calculate precise water level penetration. When water levels exceed policy triggers for more than 6 hours, bank payouts trigger automatically with zero claims paperwork."
    ),
    RawItem(
        id="ins-stripe-03",
        target_beat="insurance_fintech",
        source_name="Stripe Engineering",
        source_category="Financial Dispute State Machines & Fraud Agents",
        reputation_weight=0.96,
        title="Automating $50M in Merchant Chargeback Disputes with State Machine Agents",
        url="https://stripe.com/blog/automating-chargeback-disputes-agentic-systems",
        published_date="2026-11-21",
        media_type="case_study",
        summary="Stripe outlines their hybrid agentic system that ingests messy payment receipts and shipping logs to generate dispute evidence packs, lifting merchant dispute win-rates by 28%.",
        raw_content="Processing cardholder disputes requires extracting unstructured invoices, tracking carrier webhook events, and formatting bank-specific evidence. Stripe deployed a LangGraph-style state machine where LLM extractors operate under strict PII-redaction filters and deterministic rule verifiers, processing over $50M in dispute volume with zero unvetted API calls."
    ),
    RawItem(
        id="ins-janestreet-04",
        target_beat="insurance_fintech",
        source_name="Jane Street Tech Blog",
        source_category="High-Throughput Algorithmic Systems",
        reputation_weight=0.95,
        title="Zero-Allocation ML Inference in Production OCaml Systems",
        url="https://blog.janestreet.com/zero-allocation-inference-ocaml",
        published_date="2026-11-20",
        media_type="blog",
        summary="Jane Street details their bespoke compiler extensions and SIMD vectorization pass that enable microsecond-level neural net evaluation inside latency-critical trading loops without garbage collection pauses.",
        raw_content="Evaluating modern transformer layers within sub-10-microsecond market response windows requires eliminating runtime memory allocation. We introduce custom unboxed floating-point arrays and compiler intrinsics targeting AVX-512 and Apple Silicon NEON."
    ),

    # --- BEAT 3: MODEL DEV & OPTIMIZATION ---
    RawItem(
        id="model-deepmind-01",
        target_beat="model_dev_optimization",
        source_name="Google DeepMind",
        source_category="RL from Verifiable Rewards & Test-Time Search",
        reputation_weight=0.99,
        title="Scaling Test-Time Compute in Large Language Models for Mathematical Reasoning",
        url="https://deepmind.google/discover/blog/scaling-test-time-compute",
        published_date="2026-11-25",
        media_type="research_paper",
        summary="DeepMind researchers demonstrate that allocating dynamic search and verifier compute at inference time yields greater accuracy gains per FLOP than 10x pre-training parameter scaling on complex reasoning benchmarks.",
        raw_content="In this paper, we explore trade-offs between pre-training compute and test-time search. By employing Monte Carlo Tree Search paired with learned process reward models (PRMs), a 7B parameter model surpasses an 8x larger model on MATH500 while reducing total inference cost when budgeted adaptively."
    ),
    RawItem(
        id="model-nvidia-02",
        target_beat="model_dev_optimization",
        source_name="NVIDIA Technical Blog",
        source_category="FP4/FP8 Quantization & TensorRT-LLM",
        reputation_weight=0.96,
        title="Production FP4 Quantization: Slashing Memory Bandwidth on Blackwell GPUs",
        url="https://developer.nvidia.com/blog/production-fp4-quantization-blackwell",
        published_date="2026-11-23",
        media_type="blog",
        summary="NVIDIA engineering shares benchmark results demonstrating a 3.2x throughput increase for 70B parameter models using 4-bit floating point (FP4) Tensor Cores with less than 0.8% perplexity degradation on MMLU.",
        raw_content="The NVLink 5 interconnect and dual-die Blackwell architecture introduce native FP4 tensor execution. We present microbenchmarks comparing FP8 vs FP4 GEMM kernels across varying batch sizes and context lengths up to 128k tokens."
    ),
    RawItem(
        id="model-mistral-03",
        target_beat="model_dev_optimization",
        source_name="Mistral AI News",
        source_category="Efficient MoE Architectures & Open Weights",
        reputation_weight=0.94,
        title="Mistral-Large-3: Fully Open Apache 2.0 Weights with Native Function Calling",
        url="https://mistral.ai/news/mistral-large-3",
        published_date="2026-11-25",
        media_type="blog",
        summary="Mistral releases weights for Mistral Large 3 under Apache 2.0 license, featuring an 8x22B Mixture-of-Experts architecture with 128k context and state-of-the-art multilingual code synthesis.",
        raw_content="By activating only 39B parameters per token during forward pass, Mistral Large 3 matches proprietary frontier models on HumanEval and GSM8k while remaining hostable on a single 8xH100 node without multi-node tensor parallelism."
    ),
    RawItem(
        id="model-twosigma-04",
        target_beat="model_dev_optimization",
        source_name="Two Sigma Research",
        source_category="State Space Models (SSMs) & Continuous-Time AI",
        reputation_weight=0.92,
        title="State Space Models for Irregularly Sampled Financial Time Series",
        url="https://www.twosigma.com/articles/state-space-models-financial-time-series",
        published_date="2026-11-19",
        media_type="research_paper",
        summary="Two Sigma researchers benchmark Mamba and continuous-time SSMs against Transformers for high-frequency tick data, finding a 6x speedup during sequence rollout with superior resistance to attention saturation.",
        raw_content="Financial tick feeds arrive at non-uniform intervals. While standard self-attention incurs quadratic complexity with respect to history length, continuous-time SSM formulations maintain O(1) state update cost."
    ),

    # --- REJECTED FLUFF (FILTER DEMO) ---
    RawItem(
        id="spam-buzz-01",
        target_beat="systems_architecture",
        source_name="Viral Growth Labs",
        source_category="Consumer Tech",
        reputation_weight=0.40,
        title="We Built an AI Agent that Auto-Comments on LinkedIn Posts to Grow Followers",
        url="https://growthhacks.example.com/linkedin-auto-reply-bot",
        published_date="2026-11-25",
        media_type="tooling_release",
        summary="A startup built a Chrome extension that scrapes your feed and generates generic 'Great insights!' AI comments to game the engagement algorithm.",
        raw_content="Our bot runs in your browser, uses OpenAI API with basic prompts, and leaves 50 comments per hour automatically."
    )
]
