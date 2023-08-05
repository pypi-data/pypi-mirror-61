# Backend Framework - Generator

Wekan's [Backend Framework](https://bitbucket.org/We-Kan-Code/python-backend-framework/) project and model generators

The CLI tool helps you initialize and develop applications. It assists in scaffolding the project and generating new modules.

The generated project is built on top of flask-restful, sqlalchemy and provides authentication, access control (RBAC) endpoints out of the box. Generated modules have built-in endpoints for basic CRUD operations.

## Prerequisites

- **python3-venv** - Required to automatically setup venv and install required packages
- **mysql, postgres client libs** - If mysql and postgres client libs are not installed, setup auto install will fail

## Getting started

Install the generator with

`pip install wekan`

and then `wekan` to get started

_Keep the model names singular, the generator converts the name to its plural form where requried._

_**Make sure the user script directory is added to the path if you cannot run it after the install**_