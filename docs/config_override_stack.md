# Config + CLI Override Stack

## Purpose

This document defines the project pattern for using config defaults together with per-run CLI overrides.

The goal is to keep project behavior visible, reviewable, reusable, and safe to change without editing source code for every experiment.

## Problem Solved

Hardcoded thresholds become hidden policy.

For example, a minimum utilization threshold controls which GPU samples count as active. If that value is buried inside a script, future reviewers cannot easily tell whether an analysis result came from the data or from an invisible threshold choice.

This stack separates:

- reusable implementation logic in `gpu_lab/`
- stable defaults in `config/`
- per-run overrides from CLI arguments
- generated outputs under `results/`

## Ownership Rules

Reusable config logic belongs in:

```text
gpu_lab/config.py