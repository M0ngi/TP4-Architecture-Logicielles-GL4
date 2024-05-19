# TP 4 Architecture Logicielles - GL4 INSAT 2024

Group:

- Salma Seddik
- Naima Attia
- Med Mongi Saidane

## Description

A simulation of microservices architecture, using RabbitMQ for reactive communication between services.

Link of problem: [TP4](https://insatunisia.github.io/TP-ArchLog/tp4/)

## Architecture

<p align="center">
    <img src="https://i.imgur.com/8HoNmc4.png" />
</p>

## How to run?

Start docker services using:

```bash
docker compose up --build
```

As a client to submit a new application, use

```bash
nc 0.0.0.0 1337
```

## Screenshots

- Starting up services:

<p align="center">
    <img src="https://i.imgur.com/oS7ORLY.png" />
</p>

<p align="center">
    <img src="https://i.imgur.com/GQ66X9f.png" />
</p>

- Client connection

<p align="center">
    <img src="https://i.imgur.com/EM1S0pN.png" />
</p>

- Micro-Services tracelog

<p align="center">
    <img src="https://i.imgur.com/SaMVBHB.png" />
</p>
