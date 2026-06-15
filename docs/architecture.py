#!/usr/bin/env python3
"""Generate the Library Management System architecture diagram.

Dependencies:
    pip install diagrams

The diagrams package renders through Graphviz, so the Graphviz system package
must also be installed and its `dot` binary must be available on PATH.

Usage:
    python docs/architecture.py
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
import shutil
import sys


OUTPUT_PATH = Path(__file__).resolve().with_name("architecture")


def ensure_runtime_dependencies() -> None:
    """Fail early with actionable setup instructions."""
    if shutil.which("dot") is None:
        raise RuntimeError(
            "Graphviz executable `dot` was not found. Install Graphviz first "
            "(for example: `sudo apt-get install graphviz`)."
        )


try:
    from diagrams import Cluster, Diagram, Edge
    from diagrams.generic.blank import Blank
except ImportError as exc:
    raise SystemExit(
        "Missing Python dependency `diagrams`. Install it with: `pip install diagrams`"
    ) from exc


def icon(module_name: str, class_name: str):
    """Resolve an icon class while keeping the script tolerant of icon moves."""
    try:
        return getattr(import_module(module_name), class_name)
    except (ImportError, AttributeError):
        return Blank


Client = icon("diagrams.onprem.client", "Client")
Users = icon("diagrams.onprem.client", "Users")
Javascript = icon("diagrams.programming.language", "Javascript")
Nodejs = icon("diagrams.programming.language", "Nodejs")
Sqlite = icon("diagrams.onprem.database", "Sqlite")
Storage = icon("diagrams.generic.storage", "Storage")


def build_diagram() -> None:
    ensure_runtime_dependencies()

    graph_attr = {
        "bgcolor": "white",
        "pad": "0.35",
        "ranksep": "0.85",
        "nodesep": "0.55",
        "splines": "ortho",
    }

    with Diagram(
        "Library Management System Architecture",
        filename=str(OUTPUT_PATH),
        outformat="png",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        users = Users("Library staff\nand testers")

        with Cluster("Static Web Client"):
            browser = Client("Browser")
            spa = Javascript("Single-page UI\npublic/index.html\npublic/app.js")
            browser >> Edge(label="loads") >> spa

        with Cluster("Node.js / Express Application"):
            app = Nodejs("Express app\nsrc/app.js")
            swagger = Storage("Swagger UI + OpenAPI\n/api-docs\n/api-docs.json")

            with Cluster("REST Route Modules"):
                books = Nodejs("Books API\n/api/books")
                members = Nodejs("Members API\n/api/members")
                loans = Nodejs("Loans API\n/api/loans")
                reservations = Nodejs("Reservations API\n/api/reservations")
                search = Nodejs("Search API\n/api/search")
                reports = Nodejs("Reports API\n/api/reports")

            fees = Nodejs("Loan due dates\nand late fees\nsrc/fees.js")
            db_wrapper = Nodejs("Database wrapper\nsrc/db.js")

        with Cluster("SQLite Persistence"):
            sqljs = Sqlite("sql.js runtime\nin-process SQLite")
            db_file = Storage("library.db\nexported SQLite file")

            with Cluster("Tables"):
                books_table = Sqlite("books")
                members_table = Sqlite("members")
                loans_table = Sqlite("loans")
                reservations_table = Sqlite("reservations")

        users >> Edge(label="uses") >> browser
        spa >> Edge(label="HTTP + JSON") >> app

        app >> Edge(label="serves docs") >> swagger
        for route in [books, members, loans, reservations, search, reports]:
            app >> Edge(label="mounts") >> route
            route >> Edge(label="queries and writes") >> db_wrapper

        loans >> Edge(label="calculates") >> fees
        db_wrapper >> Edge(label="SQL") >> sqljs
        sqljs >> Edge(label="persists") >> db_file
        sqljs >> Edge(label="schema") >> [
            books_table,
            members_table,
            loans_table,
            reservations_table,
        ]


if __name__ == "__main__":
    try:
        build_diagram()
    except RuntimeError as exc:
        print(f"Unable to generate architecture diagram: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Generated {OUTPUT_PATH.with_suffix('.png')}")
