# issue-resolution-system
Here is a `README.md` file that provides an overview of the system, including the functions, classes, design patterns, and strategies used in the project.

---

# Customer Issue Resolution System

## Overview

The Customer Issue Resolution System is designed to manage and resolve customer issues efficiently by assigning them to appropriate customer service agents. The system includes functionalities for creating issues, assigning them to agents based on their expertise, resolving issues, and reassigning waiting issues if no agents are available.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Classes and Components](#classes-and-components)
  - [IssueType](#issuetype)
  - [Issue](#issue)
  - [Agent](#agent)
  - [User](#user)
  - [AgentManager](#agentmanager)
  - [IssueManager](#issuemanager)
  - [AgentAssignmentStrategy](#agentassignmentstrategy)
  - [Factories](#factories)
- [Design Patterns](#design-patterns)
  - [Factory Pattern](#factory-pattern)
  - [Strategy Pattern](#strategy-pattern)
  - [Dependency Injection](#dependency-injection)
- [Functions](#functions)
  - [createIssue](#createissue)
  - [addAgent](#addagent)
  - [assignIssue](#assignissue)
  - [getIssues](#getissues)
  - [updateIssue](#updateissue)
  - [resolveIssue](#resolveissue)
  - [viewAgentsWorkHistory](#viewagentsworkhistory)
- [Execution](#execution)
- [Initial Data](#initial-data)
- [Contributing](#contributing)

## System Architecture

The system is composed of several key components, each responsible for a specific part of the customer issue resolution process:

- **Issue Creation**: Customers can raise issues that are stored in the system.
- **Agent Assignment**: Issues are assigned to agents based on their expertise.
- **Issue Resolution**: Agents work on resolving the issues assigned to them.
- **Issue Reassignment**: If an issue cannot be assigned immediately, it is placed in a waiting queue and reassigned when possible.

## Classes and Components

### `IssueType`

The `IssueType` class defines various types of issues that can be raised by customers. It includes:
- `PAYMENT_RELATED`
- `MUTUAL_FUND_RELATED`
- `GOLD_RELATED`
- `INSURANCE_RELATED`

### `Issue`

The `Issue` class represents a customer issue. Each issue has the following properties:
- `issue_id`: Unique identifier for the issue.
- `transaction_id`: ID of the related transaction.
- `issue_type`: Type of the issue (`IssueType`).
- `subject`: Brief description of the issue.
- `description`: Detailed description of the issue.
- `email`: Email of the user who raised the issue.
- `status`: Current status of the issue (`IssueStatus`).
- `resolution`: Resolution details, if the issue is resolved.
- `assigned_agent`: Agent assigned to the issue.

### `Agent`

The `Agent` class represents a customer service agent. Agents have the following properties:
- `agent_id`: Unique identifier for the agent.
- `name`: Name of the agent.
- `email`: Email address of the agent.
- `expertise`: List of `IssueType` instances representing the agent's expertise.
- `current_issue`: The issue currently assigned to the agent.
- `work_history`: List of issues that the agent has worked on.
- `status`: Current status of the agent (`AgentStatus`).

### `User`

The `User` class represents a customer who can raise issues in the system. It has the following properties:
- `email`: Email address of the user.
- `name`: Name of the user.

### `AgentManager`

The `AgentManager` class manages the collection of agents in the system. Key functions include:
- `add_agent`: Adds a new agent to the system.
- `get_free_agents`: Retrieves a list of free agents with the required expertise.
- `get_agent_by_id`: Retrieves an agent by their ID.

### `IssueManager`

The `IssueManager` class manages the collection of issues in the system. Key functions include:
- `create_issue`: Creates and stores a new issue.
- `update_issue`: Updates the status and resolution of an issue.
- `resolve_issue`: Marks an issue as resolved.
- `add_to_waitlist`: Adds an issue to the waitlist if no agents are available.
- `get_next_waiting_issue`: Retrieves the next issue from the waitlist.
- `try_assign_issue`: Attempts to assign an issue to an agent with retry logic.
- `get_issues_by_status`: Retrieves issues based on their current status.

### `AgentAssignmentStrategy`

The `AgentAssignmentStrategy` class handles the assignment of issues to agents based on their availability and expertise. It includes:
- `assign_issue`: Assigns an issue to a free agent or adds it to the waitlist if no agent is available.
- `reassign_waiting_issues`: Periodically checks and reassigns issues from the waitlist.

### Factories

- **`IssueFactory`**: Creates instances of the `Issue` class.
- **`AgentFactory`**: Creates instances of the `Agent` class.
- **`UserFactory`**: Creates instances of the `User` class.

## Design Patterns

### Factory Pattern

The Factory Pattern is used to create instances of `Issue`, `Agent`, and `User` classes. This pattern encapsulates the creation logic and ensures consistency in object creation.

### Strategy Pattern

The Strategy Pattern is used in the `AgentAssignmentStrategy` class to handle different assignment strategies. This allows the system to easily swap out the assignment logic without modifying the core logic.

### Dependency Injection

Dependency Injection is used to pass dependencies (like `AgentManager` and `IssueManager`) to the `AgentAssignmentStrategy` class. This reduces coupling and makes the code more maintainable and testable.

## Functions

### `createIssue`

```python
def createIssue(transactionId, issueType, subject, description, email):
    issue = IssueFactory.create_issue(transactionId, issueType, subject, description, email)
    issue_manager.create_issue(issue.transaction_id, issue.issue_type, issue.subject, issue.description, issue.email)
```

Creates a new issue in the system.

### `addAgent`

```python
def addAgent(agentEmail, agentName, expertise):
    agent = AgentFactory.create_agent(agentEmail, agentName, expertise)
    agent_manager.add_agent(agent.email, agent.name, agent.expertise)
```

Adds a new agent to the system.

### `assignIssue`

```python
def assignIssue(issueId):
    issue = issue_manager.get_issue_by_id(issueId)
    if issue:
        strategy.assign_issue(issue)
```

Assigns an issue to an available agent.

### `getIssues`

```python
def getIssues(filter):
    issues = issue_manager.get_issues_by_status(filter)
    return issues
```

Retrieves issues based on the provided filter (status).

### `updateIssue`

```python
def updateIssue(issueId, status, resolution):
    issue_manager.update_issue(issueId, status, resolution)
```

Updates the status and resolution of an issue.

### `resolveIssue`

```python
def resolveIssue(issueId, resolution):
    issue_manager.resolve_issue(issueId, resolution)
```

Marks an issue as resolved.

### `viewAgentsWorkHistory`

```python
def viewAgentsWorkHistory():
    history = {}
    for agent in agent_manager.agents.values():
        history[agent.name] = [issue.issue_id for issue in agent.work_history]
    return history
```

Returns a list of issues that each agent has worked on.

## Execution

To execute the system:

1. Ensure the `initial_data.json` file is populated with agents and users.
2. Run the `main.py` file to start the simulation.

```bash
python main.py
```

## Initial Data

The `initial_data.json` file contains initial data for agents and users. Example:

```json
{
    "agents": [
        {
            "email": "agent1@test.com",
            "name": "Agent 1",
            "expertise": ["Payment Related", "Gold Related"]
        },
        ...
    ],
    "users": [
        {
            "email": "testUser1@test.com",
            "name": "Test User 1"
        },
        ...
    ]
}
```
