# Distributed Image Processing System

This repository hosts a distributed image processing system that utilizes MPI, RabbitMQ, Redis, and Flask to process images by distributing tasks across multiple nodes. This system is designed to efficiently handle large-scale image processing tasks by leveraging distributed computing resources.

## Project Structure

- **src/**: Source code directory for the system's core functionalities.
  - **mpi/**: MPI-related modules managing worker nodes and task distribution.
    - **worker.py**: Implements the worker node process.
    - **task_manager.py**: Manages task distribution among worker nodes.
    - **processing.py**: Contains the core image processing logic.
  - **rmq_helpers/**: Helper modules for RabbitMQ message handling.
    - **rmq_receiver.py**: Module for receiving messages from RabbitMQ queues.
    - **rmq_sender.py**: Module for sending messages to RabbitMQ queues.
  - **redis_access/**: Access layer for Redis operations.
    - **redis_access.py**: Provides functions for interacting with Redis.
  - **web_server/**: Flask-based web server for system interaction.
    - **app.py**: Flask application entry point.
    - **static/**: Stores static files (CSS, JS) for the web interface.
    - **templates/**: HTML templates for rendering web pages.
  - **models/**: Defines data models used across the system.
    - **image_processing_task.py**: Model representing an image processing task.
  - **tests/**: Scripts for testing system components.
- **uploaded_imgs/**: Directory for storing images uploaded by users.
- **processed_imgs/**: Directory for storing images processed by the system.
- **.gitignore**: Specifies intentionally untracked files to ignore.
- **requirements.txt**: Lists all Python dependencies.

## System Overview

### Architecture

The system integrates the following components:
- **Flask Web Server**: Serves as the interface for users to upload images and view processed results.
- **MPI**: Manages distribution of image processing tasks across multiple worker nodes.
- **RabbitMQ**: Handles message queuing between different system components.
- **Redis**: Utilized for caching and quick data retrieval.

### Functionality

- **Image Upload**: Users can upload images through the web interface.
- **Image Processing**: Uploaded images are split into parts, processed in parallel, and recombined.
- **Result Retrieval**: Users can download or view the processed images.


## RabbitMQ Docker command

docker run -d --hostname rmq --name rabbit-server -p 15672:15672 -p 5672:5672 rabbitmq:3-management


## Redis Docker command

docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest