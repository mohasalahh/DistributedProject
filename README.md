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


## Screenshots

<img width="1512" alt="Screenshot 2024-05-17 at 11 47 33 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/6d9b7fbe-b9b6-48e0-a228-2853b169466b">
<img width="1512" alt="Screenshot 2024-05-17 at 11 46 26 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/f8222d47-78fd-467f-ae98-b583ecf505d0">
<img width="1512" alt="Screenshot 2024-05-17 at 11 46 20 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/366465e9-be39-48e6-8f41-41d7d689d364">
<img width="1512" alt="Screenshot 2024-05-17 at 11 46 15 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/35e58138-21a0-46bb-bb0a-ce349c3e3fb7">
<img width="1512" alt="Screenshot 2024-05-17 at 11 46 11 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/41c182f1-5333-43d4-bb68-baa43e7a3403">
<img width="1512" alt="Screenshot 2024-05-17 at 11 45 57 PM" src="https://github.com/mohasalahh/DistributedProject/assets/10936011/6f73d9ac-d6fc-407c-94c7-917dff793c75">
