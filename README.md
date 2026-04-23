# Task Manager with Intelligent Scheduling

## Overview

This project started as a basic CLI task manager and was later refined into a system that not only stores tasks but also **makes decisions on task execution order**.

The focus of the refinement was to move from simple CRUD operations to a **decision-making model based on task attributes**.

---

## Original Features (Baseline System)

The initial version supported:

* Add tasks via CLI or interactive input
* Edit, delete, and mark tasks as complete
* Store tasks persistently in a CSV file
* View all tasks

Each task contained:

* Description
* Due date
* Priority
* Duration
* Optional tag

This version functioned purely as a **data management system**.

---

## Refinements and Improvements

### 1. Separation of Data and Computation

Originally, all task attributes were static.

Refinement:

* Introduced **derived attributes** (urgency, score)
* Avoided storing computed values in CSV
* Computation is done dynamically during scheduling

**Impact:**
Ensures consistency and prevents stale or incorrect stored values.

---

### 2. Introduction of a Scoring Model

Added a scoring function to evaluate task importance:

score = 0.4 * urgency + 0.4 * priority - 0.2 * duration

Where urgency is derived from time to deadline.

**Impact:**
Shifted the system from passive storage → active decision-making.

---

### 3. Dynamic Scheduling Simulation

Instead of ranking tasks once, the system:

* Selects the highest-scoring task
* Advances current time based on task duration
* Recomputes scores for remaining tasks

**Impact:**
Models real-world execution instead of static prioritization.

---

### 4. Input Validation and Error Handling

Refinements include:

* Validation of date format (`dd-mm-yyyy`)
* Priority range enforcement (1–5)
* Duration type and positivity checks
* Safer handling of user input during editing

**Impact:**
Improves robustness and prevents invalid state.

---

### 5. Improved CLI Design

* Switched CLI arguments (`-e`, `-d`, `-c`) to integer types
* Reduced runtime errors by enforcing input at parsing level

**Impact:**
Cleaner and more predictable user interaction.

---

## Scheduling Logic

Urgency is calculated as:

urgency = 1 / (days_to_deadline + 1)        if task not overdue
urgency = 1 + (overdue_days * 0.1)         if overdue

Tasks are then selected iteratively based on score.

---

## Design Philosophy

This project demonstrates a transition from:

* Static data management
  → to
* Heuristic-based decision systems

The goal is not optimal scheduling, but a **reasonable and explainable prioritization strategy**.

---

## Limitations

* Uses a heuristic model, not guaranteed optimal
* Time precision is limited to days (not hours/minutes)
* No task dependencies
* CLI-based interaction only

---

## Future Work

* Introduce task dependencies (graph-based scheduling)
* Improve time granularity
* Replace heuristic scoring with learned models
* Extend into a neural decision system

---

## Author Note

This project reflects an iterative refinement process, focusing on improving system design, validation, and decision-making logic rather than just adding features.
