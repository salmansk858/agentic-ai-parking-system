# Architecture Documentation

## Overview

The Agentic AI Frictionless Parking System implements a multi-agent architecture based on the IEEE research paper "Agentic AI Systems: Architecture and Evaluation Using a Frictionless Parking Scenario" (2025).

## System Architecture

### Core Components

1. **Agent Layer**: Specialized AI agents for different parking tasks
2. **Orchestration Layer**: Agent coordination and handoff mechanisms  
3. **Tool Layer**: External APIs and service integrations
4. **Data Layer**: User preferences, session management, and caching

### Agent Specifications

#### 1. Interaction Agent
- **Role**: Primary user interface and orchestration
- **Responsibilities**:
  - Handle user queries via natural language
  - Retrieve and update user preferences
  - Coordinate other agents (Search, Routing, Access)
  - Collect feedback for post-trip learning
- **Optimization**: Chain-of-Thought reasoning, medium prompt specificity

#### 2. Informative Search Agent  
- **Role**: Parking spot optimization and search
- **Responsibilities**:
  - Multi-criteria constrained optimization 
  - Apply hard constraints (duration, accessibility, EV charging)
  - Incorporate soft constraints (preferences)
  - Query real-time parking APIs
  - Return ranked optimal parking options
- **Tools**: Web search, Parking APIs, Google Maps, optimization solvers

#### 3. On-Route Guidance Agent
- **Role**: Navigation and trip coordination
- **Responsibilities**:
  - Real-time navigation using Google Maps
  - ETA prediction with live traffic data
  - Dynamic route adaptation (traffic, weather, events)
  - Reservation management and booking confirmation
- **Tools**: Google Maps API, Traffic APIs, Weather APIs, Booking systems

#### 4. Access Agent
- **Role**: Seamless parking facility entry
- **Responsibilities**:
  - License plate recognition systems
  - QR code and digital token validation
  - Valet service coordination
  - Parking infrastructure integration
- **Tools**: LPR systems, QR scanners, Digital tokens, Gate control

#### 5. Micro-Routing Agent
- **Role**: In-facility navigation
- **Responsibilities**:
  - Indoor spot localization
  - Micro-routing to designated spaces
  - Real-time occupancy monitoring
  - Multi-level structure navigation
- **Tools**: Facility layouts, Occupancy sensors, Indoor navigation

#### 6. On-Spot Agent
- **Role**: Vehicle monitoring and services
- **Responsibilities**:
  - EV charging activation and monitoring
  - Security system integration
  - Advanced alerting (intrusion, proximity)
  - Service continuity during parking
- **Tools**: Charging systems, Security monitoring, Alert systems

#### 7. Departure Agent
- **Role**: Exit management and payment
- **Responsibilities**:
  - Session duration tracking and notifications
  - Extension request handling
  - Walking directions to vehicle
  - Payment processing (subscriptions, cards, tokens)
  - Violation risk alerts
- **Tools**: Session timers, Payment systems, Navigation, Violation checkers

## Cooperation Patterns

### 1. Augmentative Cooperation
Multiple agents with similar capabilities work on parallelizable sub-tasks.

**Formula**: ∑(i=1 to n) Ai(τi) → Action(τ)

**Example**: Multiple Search Agents covering different geographic zones

### 2. Integrative Cooperation  
Agents with complementary expertise collaborate on complex tasks.

**Formula**: F(A1(τ1), A2(τ2), ..., An(τn)) → Action(τ)

**Example**: Search Agent finds spots + Routing Agent provides navigation

### 3. Debative Cooperation
Multiple agents independently solve the same task, then compare solutions.

**Formula**: Best({Ai(τ)}n i=1) → Action(τ)

**Example**: Multiple Search Agents with different optimization strategies

## Interaction Mechanisms

### Handoff
Transfer of control and responsibility between agents.

**Formula**: Handoff(Ai, Aj, τ) → Aj.takeover(τ)

**Examples**:
- Interaction Agent → Search Agent (parking search task)
- Search Agent → Routing Agent (navigation task)
- Routing Agent → Access Agent (facility entry)

### Cueing
Early context sharing without control transfer.

**Formula**: Cue(Ai, Aj, d) → Aj.prepare(d)

**Examples**:
- Search Agent cues Routing Agent with destination info
- Routing Agent cues Access Agent with arrival time
- Access Agent cues Micro-Routing Agent with entry point

## Performance Optimizations

Based on research findings from 6-factor factorial experiment:

### Model Configuration
- **Backbone**: GPT-4o-mini (optimal latency/consistency: 3.7s, 0.66)
- **Temperature**: 0.2 (low entropy for consistency)
- **Max Tokens**: 150 (short verbosity for speed)
- **Top-p**: 0.8 (nucleus sampling optimization)

### Prompt Engineering
- **Specificity**: Medium (optimal balance)
- **Complexity**: Moderate (best performance) 
- **Chain-of-Thought**: Enabled for all agents
- **Guardrails**: Input/output validation

### User Profiles (Research-Based)
1. **Commuter Saver**: Budget-focused EV driver
2. **Efficient Multitasker**: Time-prioritized professional  
3. **Creative Wanderer**: Atmosphere-seeking explorer
4. **Independent Elder**: Accessibility-requiring senior
5. **Green Professional**: Business EV user

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Agents**: OpenAI Agents SDK
- **Models**: GPT-4o-mini (optimized)
- **Database**: SQLite/PostgreSQL + Redis
- **APIs**: Google Maps, Parking APIs, Weather APIs

### Frontend  
- **Web Interface**: Streamlit
- **API Documentation**: FastAPI auto-generated
- **Monitoring**: Prometheus + Grafana

### Deployment
- **Containers**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)
- **Serverless**: AWS Lambda (alternative)
- **CI/CD**: GitHub Actions
- **Registry**: GitHub Container Registry

## Security & Compliance

### Data Protection
- Environment-based secrets management
- No plaintext API keys in code
- User data encryption at rest/transit
- GDPR compliance for EU users

### Agent Security
- Input/output guardrails on all agents
- Content filtering and validation
- Rate limiting and abuse protection
- Audit logging for all agent actions

## Monitoring & Observability

### Metrics
- **Latency**: Agent response times (target: <4s)
- **Consistency**: Response stability (target: >0.65)
- **Success Rate**: Task completion rates
- **User Satisfaction**: Feedback scores

### Logging
- Structured JSON logging
- Chain-of-Thought reasoning capture
- Agent handoff tracking
- Performance metrics collection

## Scalability Considerations

### Horizontal Scaling
- Stateless agent design
- Redis-based session management  
- Load balancer distribution
- Database connection pooling

### Performance Optimization
- Response caching (Redis)
- Database query optimization
- Async/await throughout
- Connection reuse

This architecture provides a robust, scalable foundation for intelligent parking management while maintaining the research-based optimizations for optimal performance.
