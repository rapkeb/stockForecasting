# Stock Forecasting

## Overview

This project is a comprehensive stock forecasting system that utilizes multiple services to predict future stock prices. The application is composed of several microservices, including a frontend (Nginx), backend (Flask), Kafka for messaging, and a chat service for user interaction. The entire system is containerized and can be deployed on Kubernetes using Minikube.

## Features

- **Modular Architecture**: Divided into separate services for frontend, backend, Kafka, and chat.
- **Stock Data Ingestion**: Fetches and processes historical stock data using the backend service.
- **Real-time Predictions**: Uses machine learning models in the backend to forecast stock prices.
- **User Interaction**: The chat service allows users to interact with the system and get insights.
- **Scalable Deployment**: The system is designed to be deployed on Kubernetes, making it scalable and resilient.

## Project Structure

```plaintext
.
├── frontend/                   # Nginx server for user interaction with static files
├── backend/                    # Flask application for data processing and model serving
├── db/                         # Flask application for interactions with the data base
├── kafka/                      # Kafka setup for messaging between services
├── chat/                       # Chat service for user interaction
├── consumer/                   # consume from kafka
├── kubernetes/                 # Kubernetes deployment files
│   ├── frontend.yaml
│   ├── backend.yaml
|   ├── db.yaml
|   ├── consumer.yaml
│   ├── kafka.yaml
│   ├── chat.yaml
|   ├── mongo.yaml
│   ├── zookeeper.yaml
│   └── ingress.yaml
└── README.md                   # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Kubernetes with Minikube
- Docker (for building images)
- Financial API key (e.g., Finnhub)
- Chat API key (chatgpt)

### Step-by-Step Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rapkeb/stockForecasting.git
   cd stockForecasting
   ```

2. **Set up environment variables:**

   - Create a `.env` file in the `backend/` directory with your API key:

     ```
     FINNHUB_API_KEY=your_api_key_here
     ```

   - Create a `.env` file in the `chat/` directory with your API keys:

     ```
     API_KEY=your_api_key_here
     SECRET_KEY=your_api_key_here
     ```

3. **Start Minikube:**

   ```bash
   minikube start
   ```

4. **Deploy the services to Kubernetes:**

   - Apply the Kubernetes configuration files:

     ```bash
     kubectl apply -f kubernetess/zookeeper.yaml
     kubectl apply -f kubernetess/kafka.yaml
     kubectl apply -f kubernetess/mongo.yaml
     kubectl apply -f kubernetess/chat.yaml
     kubectl apply -f kubernetess/consumer.yaml
     kubectl apply -f kubernetess/frontend.yaml
     kubectl apply -f kubernetess/backend.yaml
     kubectl apply -f kubernetess/db.yaml
     ```

   - If using Ingress, set up the Ingress controller:

     ```bash
     minikube addons enable ingress
     kubectl apply -f k8s/ingress.yaml
     minikube tunnel
     ```

5. **Access the application:**

   - Use local host to get into the app.

## Contributing

Contributions are welcome! Please adhere to the following guidelines:

- Fork the repository.
- Create a new branch (`git checkout -b feature/your-feature`).
- Commit your changes (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature/your-feature`).
- Create a pull request.

## Contact

For any issues, questions, or suggestions, feel free to reach out via GitHub Issues or contact [rapkeb](https://github.com/rapkeb).
