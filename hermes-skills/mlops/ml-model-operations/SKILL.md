---
name: ml-model-operations
description: Class-level MLOps workflow for finding models, serving LLMs, local inference, benchmarking, experiment tracking, and model artifact management.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, huggingface, llm-serving, llama.cpp, vllm, evaluation, wandb, benchmarks, model-hub]
---

# ML Model Operations

Use this umbrella for operational work around ML/LLM models: discovering or downloading model artifacts, serving LLMs, running local GGUF inference, benchmarking with standard harnesses, tracking experiments, and managing model outputs.

## Default workflow

1. Identify the operational objective: acquire, convert/quantize, serve, benchmark, track, or publish.
2. Capture constraints: hardware/VRAM/CPU, target latency/throughput, model format, license, context length, quantization, and deployment surface.
3. Choose the tool path:
   - Hugging Face Hub for search/download/upload and model metadata;
   - llama.cpp/GGUF for CPU/edge/local single-user inference;
   - vLLM for high-throughput GPU serving and OpenAI-compatible APIs;
   - lm-evaluation-harness for standardized benchmarks;
   - W&B for experiment tracking, sweeps, artifacts, and dashboards.
4. Run the smallest verification first, then scale.
5. Report exact commands, model IDs, artifact paths, benchmark config, and observed results.

## Labeled playbooks

### Hugging Face Hub operations

Use `hf`/API workflows for login, search, metadata inspection, download, upload, and dataset/model repo management. Always verify license/gated access and disk space before large downloads.

### llama.cpp and GGUF local inference

Use for local CPU/Metal/CUDA inference, quantized GGUFs, prompt testing, and lightweight OpenAI-compatible servers. Match quantization to RAM/VRAM; verify model loads before extended benchmarking.

### vLLM serving

Use for production or batch serving on GPUs. Tune `--gpu-memory-utilization`, context length, tensor parallelism, prefix caching, quantization, and metrics. Verify with a real OpenAI-compatible request and watch logs for OOM or slow TTFT.

### Evaluation harness benchmarking

Use EleutherAI lm-evaluation-harness for MMLU, GSM8K, HellaSwag, HumanEval, and other standardized tasks. Pin model args, task names, few-shot counts, seeds, output paths, and hardware. Prefer vLLM backend for speed when available.

### Weights & Biases tracking

Use W&B for training/eval metrics, sweep management, artifact versioning, model registry, and dashboard reports. Log config and environment details so runs are reproducible.

### Vision model operations and SAM segmentation

Use computer-vision model playbooks for zero-shot segmentation, model checkpoint selection, batching, ONNX export, and pipeline integration. For Segment Anything, choose ViT-B/L/H based on speed/accuracy/VRAM, compute image embeddings once per image, use point/box/mask prompts for interactive refinement, filter automatic masks by predicted IoU/stability/area, and verify outputs with saved masks or overlays. The archived `segment-anything-model` package preserves detailed code examples and troubleshooting.

## Verification

- For hub work: list the downloaded/uploaded path or repo URL.
- For serving: issue a real request to the endpoint and include status/result snippet.
- For local inference: run a short prompt and include timing/load notes.
- For benchmarks: preserve output JSON and summarize primary metrics.
- For tracking: provide run/project/artifact IDs or URLs.

## Archived source packages

Detailed former skills for individual tools were consolidated here. Their archived packages retain long command examples and references for recovery when a narrow tool-specific appendix is needed.
