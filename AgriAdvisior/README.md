# AgriAdvisor

An intelligent agricultural assistant powered by Google ADK that helps farmers, agronomists, and gardeners make informed decisions about crop management, plant health, and weather-based farming strategies.

## Overview

AgriAdvisor combines computer vision and real-time weather data to provide comprehensive agricultural guidance. The system uses specialized AI agents to analyze plant images for disease detection and fetch location-based weather information to deliver actionable farming recommendations.

## Features

- Plant species identification from images
- Disease and deficiency detection with severity assessment
- Treatment recommendations for plant health issues
- Real-time weather data retrieval for any location
- Weather-aware farming advice for irrigation, spraying, and harvesting
- Multi-agent architecture for specialized task handling

## Architecture

The system uses a hierarchical agent structure:

- **Root Agent (AgriAdvisor)**: Main orchestrator that coordinates between specialized agents
- **Vision Agent**: Analyzes plant images to identify species and diagnose health issues
- **Weather Agent**: Retrieves current weather conditions for location-based recommendations

## Prerequisites

- Python 3.12 or higher
- Google Maps API key
- Google ADK access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dholendar27/agents.git
cd agriadvisior
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp AgriAdivisor/sample.env AgriAdivisor/.env
```

4. Add your Google Maps API key to `AgriAdivisor/.env`:
```
GOOGLE_MAPS_KEY=your_api_key_here
```

## Usage

### Running the Application

```bash
adk web
```

### Using the Vision Agent

Upload or provide a plant image to receive:
- Plant identification (common and scientific names)
- Health status assessment
- Disease or deficiency diagnosis
- Symptom description
- Severity rating
- Treatment recommendations

### Using the Weather Agent

Request weather information by providing a location to get:
- Current temperature
- Weather conditions
- Humidity levels
- Wind speed
- 7-day forecast data

## Dependencies

- google-adk: Google Agent Development Kit for building AI agents
- googlemaps: Google Maps API client for geocoding
- requests: HTTP library for API calls
- python-dotenv: Environment variable management

## API Keys

This project requires a Google Maps API key with the following APIs enabled:
- Geocoding API
- Weather API

Get your API key from the [Google Cloud Console](https://console.cloud.google.com/).

## Development

The project uses uv for dependency management. To add new dependencies:

```bash
uv add <package-name>
```