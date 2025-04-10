# Nexla MCP Proof of Concept: Wine Review Demo

## Overview

This repository contains a proof-of-concept implementation of a MCP (Model Context Protocol) server that interfaces with the Nexla platform. It demonstrates how to query a vector database Nexset containing wine review data to retrieve relevant wines based on natural language queries.

## Disclaimer

This implementation is intended for demonstration purposes only and is not intended as the official Nexla MCP implementation. It serves as a reference and starting point for understanding how to build integrations with Nexla and MCP. This implementation is also well suited for the specific example of Nexset 113071 (a vector DB containing wine reviews). If you'd like to try this with other vector DB Nexsets, you can modify the prompt in the MCP tool function.

## Features

- Semantic search of wine reviews using natural language queries
- Integration with Nexla Nexset vector database 
- Return of wine details including flavor profiles, ratings, and pricing


## Getting Started

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/abhijit914/nexset-mcp-poc.git
   ```

2. Configure mcp.json
    - Modify the directory in the run command to include the corect path to the cloned repository
    - Add your environment variables for OPENAI_API_KEY and NEXLA_SERVICE_KEY
    - Copy the mcp.json and paste it into the configuration of an MCP Client of your choosing (Claude Desktop, Cursor IDE, etc.)


## Usage

Once configured in your MCP client, you can query the wine review database using natural language. Examples:

- "Find wines with citrus flavors"
- "What are some good Chardonnays with floral or earthy notes"
- "Recommend a wine with high ratings that pairs well with seafood"
