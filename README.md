# lru_cache

A least recently used cache implemented in Python with constant time lookups.

## Intro

This project was a technical question I received at one point during the job search and I wanted to turn it into an understandable Python library with CI.

## Installation

Install this library by checking it out directly and using PDM, or download the wheel artifact from the most recent build action.

## Release Process

1. Create the release branch
   - Checkout the commit you want to base your release off of
   - Create a branch of the format `release/vMAJ.MIN.PATCH`, updating the appropriate section
2. Change the version number
   - Update the version number in `pyproject.toml`
   - Update the version number in `CHANGELOG.md` and add a new `Unreleased` section
   - Commit the version number changes
3. Push the release branch and create a PR
   - Push the release branch to the remote
   - Create a PR from the release branch to `main`
   - Add the `release` label to the PR
4. After the PR is merged, finalize the drafted release
   - Open the drafted release and change the target to "main"
   - Publish the release
