# Agentic AI Frictionless Parking System

A production-ready multi-agent AI system for intelligent parking management based on the research paper 'Agentic AI Systems: Architecture and Evaluation Using a Frictionless Parking Scenario'.

## Overview

This project implements a comprehensive agentic AI architecture for frictionless urban parking using OpenAI Agents SDK, featuring:

- **Multi-Agent Architecture**: 7 specialized AI agents working collaboratively
- **Interaction Agent**: Primary orchestration and user interface
- **Informative Search Agent**: Intelligent parking spot optimization
- **On-Route Guidance Agent**: Real-time navigation and routing
- **Access Agent**: Seamless parking facility entry
- **Micro-Routing Agent**: In-facility navigation
- **On-Spot Agent**: Vehicle monitoring and services
- **Departure Agent**: Exit management and payment processing

## Features

- 🤖 **Advanced Agent Cooperation**: Augmentative, integrative, and debative patterns
- 🔄 **Handoff & Cueing Mechanisms**: Seamless agent-to-agent task delegation
- 🛡️ **Guardrails System**: Input/output validation and safety checks
- 🎯 **Chain-of-Thought Reasoning**: Transparent decision-making process
- 📊 **Performance Optimization**: Based on research findings for latency and consistency
- 🌐 **Web Interface**: User-friendly parking assistance
- 🐳 **Docker Support**: Containerized deployment
- ☁️ **AWS Lambda Ready**: Serverless deployment support

## Installation

```bash
git clone https://github.com/salmansk858/agentic-ai-parking-system.git
cd agentic-ai-parking-system
pip install -r requirements.txt
cp .env.example .env
# Configure your API keys in .env
```

## Quick Start

```python
from src.agents import InteractionAgent, InformativeSearchAgent
from src.runner import ParkingSystem

# Initialize the parking system
system = ParkingSystem()

# Find parking near Toronto City Hall
result = system.find_parking(
    destination="Toronto City Hall",
    preferences={"price_tier": "affordable", "ev_charging": True}
)

print(result)
```

## Architecture

Based on the IEEE research paper, this system implements:

### Agent Cooperation Patterns
- **Augmentative**: Multiple agents working on parallelizable tasks
- **Integrative**: Complementary agents contributing specialized knowledge
- **Debative**: Multiple solutions evaluated for optimal outcomes

### Interaction Mechanisms
- **Handoff**: Transfer of control between agents
- **Cueing**: Early context sharing for task preparedness

### Performance Optimizations
- GPT-4o-mini backbone for optimal latency/consistency balance
- Concise verbosity settings
- Medium prompt specificity
- Chain-of-thought reasoning for reliability

## Documentation

- [API Reference](docs/api.md)
- [Agent Architecture](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Research Paper](docs/research-paper.pdf)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this system in your research, please cite:

```bibtex
@article{khamis2025agentic,
  title={Agentic AI Systems: Architecture and Evaluation Using a Frictionless Parking Scenario},
  author={Khamis, Alaa},
  journal={IEEE Access},
  volume={13},
  pages={126052--126069},
  year={2025},
  publisher={IEEE}
}
```

## Research Implementation

This implementation follows the experimental configuration from the research:
- 5 user profiles (commuter_saver, efficient_multitasker, creative_wanderer, independent_elder, green_professional)
- Optimized for gpt-4o-mini backbone
- Low entropy settings for consistency
- Short verbosity for minimal latency
- Medium prompt specificity for optimal performance

Built by [Mohammad Salman Aziz Siddiqui](https://github.com/salmansk858) for M.Tech Data Science research.