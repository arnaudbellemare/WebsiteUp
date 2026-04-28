"""
GEO Optimizer CLI — Unified entry point.

Usage:
    geo audit --url https://example.com
    geo llms --base-url https://example.com
    geo schema --file index.html --analyze
"""

from __future__ import annotations

import logging
import warnings

import click


def _configure_runtime_noise_suppression() -> None:
    """Reduce third-party runtime noise for normal CLI usage."""
    # urllib3 on macOS/LibreSSL emits a persistent warning that does not affect
    # command behavior for this tool in normal environments.
    warnings.filterwarnings(
        "ignore",
        message=r"urllib3 v2 only supports OpenSSL 1\.1\.1\+.*",
        category=Warning,
    )

    # HuggingFace can emit noisy cache warnings/errors when cache dirs are
    # restricted by sandboxed environments. We handle embedding fallbacks
    # ourselves and keep CLI output focused.
    logging.getLogger("huggingface_hub.file_download").setLevel(logging.CRITICAL)
    logging.getLogger("sentence_transformers").setLevel(logging.ERROR)


# Apply suppression as early as possible (before subcommand imports)
_configure_runtime_noise_suppression()

from geo_optimizer import __version__


@click.group()
@click.version_option(version=__version__, prog_name="geo-optimizer")
@click.option(
    "--lang",
    default=None,
    envvar="GEO_LANG",
    type=click.Choice(["en", "fr", "it"], case_sensitive=False),
    help="Output language: en (default), fr, it",
)
def cli(lang):
    """AI Visibility Audit (GEO Optimizer) — scanner, scorer, fixer, and monitor."""
    _configure_runtime_noise_suppression()
    if lang:
        from geo_optimizer.i18n import set_lang

        set_lang(lang)


# Import and register subcommands
from geo_optimizer.cli.audit_cmd import audit  # noqa: E402
from geo_optimizer.cli.autopilot_cmd import autopilot  # noqa: E402
from geo_optimizer.cli.apply_cmd import apply_cmd  # noqa: E402
from geo_optimizer.cli.coherence_cmd import coherence  # noqa: E402
from geo_optimizer.cli.content_cmd import content_cmd  # noqa: E402
from geo_optimizer.cli.diff_cmd import diff  # noqa: E402
from geo_optimizer.cli.fix_cmd import fix  # noqa: E402
from geo_optimizer.cli.history_cmd import history  # noqa: E402
from geo_optimizer.cli.github_cmd import github_cmd  # noqa: E402
from geo_optimizer.cli.llms_cmd import llms  # noqa: E402
from geo_optimizer.cli.links_cmd import links_cmd  # noqa: E402
from geo_optimizer.cli.logs_cmd import logs  # noqa: E402
from geo_optimizer.cli.monitor_cmd import monitor  # noqa: E402
from geo_optimizer.cli.orchestrate_cmd import orchestrate_cmd  # noqa: E402
from geo_optimizer.cli.pipeline_cmd import pipeline_cmd  # noqa: E402
from geo_optimizer.cli.playbook_cmd import playbook_cmd  # noqa: E402
from geo_optimizer.cli.fullaudit_cmd import full  # noqa: E402
from geo_optimizer.cli.marketing_cmd import marketing  # noqa: E402
from geo_optimizer.cli.rivalry_cmd import rivalry  # noqa: E402
from geo_optimizer.cli.schema_cmd import schema  # noqa: E402
from geo_optimizer.cli.snapshots_cmd import snapshots  # noqa: E402
from geo_optimizer.cli.track_cmd import track  # noqa: E402

cli.add_command(audit)
cli.add_command(autopilot)
cli.add_command(apply_cmd)
cli.add_command(audit, name="visibility-audit")
cli.add_command(audit, name="scanner")
cli.add_command(audit, name="scorer")
cli.add_command(coherence)
cli.add_command(content_cmd)
cli.add_command(diff)
cli.add_command(fix)
cli.add_command(fix, name="citation-optimizer")
cli.add_command(fix, name="fixer")
cli.add_command(history)
cli.add_command(github_cmd)
cli.add_command(llms)
cli.add_command(links_cmd)
cli.add_command(logs)
cli.add_command(monitor)
cli.add_command(orchestrate_cmd)
cli.add_command(pipeline_cmd)
cli.add_command(playbook_cmd)
cli.add_command(full)
cli.add_command(marketing)
cli.add_command(rivalry)
cli.add_command(monitor, name="presence-monitor")
cli.add_command(schema)
cli.add_command(snapshots)
cli.add_command(track)
cli.add_command(track, name="readiness-monitor")


if __name__ == "__main__":
    cli()
