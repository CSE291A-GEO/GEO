# GEO - Multi-Agent Content Optimization

A multi-agent pipeline for **Generative Engine Optimization (GEO)** that iteratively improves content visibility in AI-powered search engines.

## Overview

This project implements a MACO-style pipeline using LangGraph to optimize documents for better citation and prominence in generative search engine responses.

## Pipeline Architecture

The system uses four specialized agents:

1. **Query Agent** - Generates realistic user queries related to the target document
2. **Evaluator Agent** - Scores documents using 6 metrics (CP, AA, FA, KC, SC, AD)
3. **Analyst Agent** - Identifies weaknesses and proposes improvement strategies
4. **Editor Agent** - Applies targeted edits to optimize content

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| CP | Citation Prominence |
| AA | Attribution Accuracy |
| FA | Faithfulness |
| KC | Key Information Coverage |
| SC | Semantic Contribution |
| AD | Answer Dominance |

## Tech Stack

- **LangGraph** - Multi-agent orchestration
- **Google Gemini** - LLM backbone (gemini-2.5-flash/flash-lite)
- **Gensee AI** - Context retrieval
- **LangSmith** - Tracing & monitoring

## Setup

1. Clone the repository
2. Install dependencies
3. Set environment variables in `.env`:
   ```
   GOOGLE_API_KEY=your_key
   GENSEE_API_KEY=your_key
   LANGSMITH_API_KEY=your_key
   ```

## Usage

See `demo.ipynb` for a quick start or `notebooks/MACO_pipeline_v2.ipynb` for the full implementation.

## Project Structure

```
├── demo.ipynb                  # Quick start demo
├── data_analysis.ipynb         # Results analysis
├── notebooks/
│   ├── MACO_pipeline.ipynb     # Base pipeline
│   ├── MACO_pipeline_v2.ipynb  # Paper-aligned implementation
│   └── data/                   # Output articles & metrics
└── data/
    ├── queries/                # Benchmark queries
    └── corpus/                 # Document corpus
```