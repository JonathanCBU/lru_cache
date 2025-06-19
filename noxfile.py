"""Nox CI sessions."""

from __future__ import annotations

import nox

from nox import Session

# Use PDM backend for consistent dependency management
nox.options.sessions = ["tests", "lint"]


@nox.session
def tests(session: Session) -> None:
    """Run tests with pytest."""
    # Use PDM to install dependencies in the session
    session.run("pdm", "install", "--no-self", external=True)
    session.run("pdm", "run", "pytest", external=True)


@nox.session
def lint(session: Session) -> None:
    """Run linting with ruff."""
    session.run("pdm", "install", "--no-self", external=True)
    session.run("pdm", "run", "ruff", "check", ".", external=True)


@nox.session
def style(session: Session) -> None:
    """Format code with ruff."""
    session.run("pdm", "install", "--no-self", external=True)
    session.run("pdm", "run", "ruff", "format", ".", external=True)
