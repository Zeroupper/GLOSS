# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GLOSS (Group of LLMs for Open-Ended Sensemaking) is a multi-agent system that answers natural language queries about passive sensing data from mobile and wearable devices. It uses coordinated LLM agents to iteratively gather, analyze, and synthesize data from multiple sources (phone sensors, Garmin wearables, etc.).

## Commands

### Environment Setup
```bash
# Create conda environment (use appropriate yml for your OS)
conda env create -f environment_linux.yml  # or environment_mac.yml
conda activate gloss-sensemaking

# Clone stress detection algorithm inside repo (required dependency)
git clone https://github.com/UbiWell/stress-detection-algorithm-code-python.git
```

### Docker Setup (required for code execution)
```bash
docker build -f Dockerfile -t gloss-sensemaking-code .
```

### Running GLOSS
```bash
# Command-line interface
python sensemaking_process.py

# Web UI (Streamlit)
streamlit run sensemaking_ui.py
```

### Testing the Database Registry
```bash
python test_registry.py
```

## Architecture

### Multi-Agent Pipeline

The sensemaking process flows through these stages (max 3 iterations):

1. **ActionPlanGenerationAgent** - Creates initial strategy for answering the query
2. **NextStepAgent** - Decides: seek more info (INF) or done (END)
3. **InformationSeekingAgent** - Identifies which databases to query and what data to request
4. **GenericDatabaseManager** - Routes queries to specific databases, generates and executes code
5. **SenseMakingAgent** - Local sense (summarize raw results) → Global sense (update overall understanding)
6. **PresentationAgent** - Formats final answer per user instructions

Entry point: `SenseMaker` class in `sensemaking_process.py` orchestrates this flow.

### Database Registry System

`agents/database_registry.py` auto-discovers data sources from:
- `data_streams/*_database.py` - Phone/wearable sensor databases
- `models/*.py` - ML models (e.g., stress prediction)

Each database module must expose:
- `database_info`: dict with name, info, device, additional_instructions
- `functions`: dict of function metadata for LLM prompts (params, returns, examples)
- `function_refs`: dict mapping function names to actual implementations

### Key Configuration

`agents/config.py`:
- `USE_OPENROUTER` / `OPENROUTER_MODEL` - LLM provider settings
- `ONLY_CODE_FUNCTIONS` - True for code generation mode, False for function calling
- `DOCKER_NAME` - Docker image name for sandboxed code execution
- `USE_CSV` - True if using CSV data files

Environment variables: `OPENROUTER_API_KEY`

### Code Execution

`agents/coding_agent.py` uses AutoGen with Docker for sandboxed execution of LLM-generated code. The `work_dir` path (line 34) must be updated to your local repo path.

### Adding New Data Sources

1. Copy `data_streams/database_template.py` to `data_streams/my_database.py`
2. Uncomment and fill in `database_info`, `functions`, `function_refs`
3. The registry auto-discovers files ending in `_database.py`

## Data Sources

Available databases (auto-registered):
- **Phone**: location, activity, app_usage, wifi, battery, brightness, call_log, lock_unlock, phone_steps
- **Garmin**: garmin_hr, garmin_steps, garmin_ibi, garmin_stress
- **Models**: stress_prediction_model
