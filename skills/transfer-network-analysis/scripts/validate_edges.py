#!/usr/bin/env python3
"""Validate and normalize an evidence-typed transfer-network edge table."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

REQUIRED = [
    "edge_id",
    "source_id",
    "target_id",
    "source_type",
    "target_type",
    "edge_type",
    "direction_status",
    "weight",
    "weight_scale",
    "evidence_method",
    "evidence_unit",
    "sample_id",
    "direction_basis",
    "uncertainty",
    "thresholds",
    "provenance_id",
]

NODE_TYPES = {
    "arg",
    "gene",
    "feature",
    "mge",
    "plasmid",
    "virus",
    "integron",
    "transposon",
    "ice",
    "ime",
    "contig",
    "mag",
    "genome",
    "strain",
    "host",
    "taxon",
    "sample",
    "source",
    "sink",
    "person",
    "site",
    "unknown",
}

EDGE_DIRECTIONS = {
    "contains": {"directed"},
    "host_link": {"directed"},
    "hic_contact": {"undirected"},
    "sequence_similarity": {"undirected"},
    "gene_sharing": {"undirected"},
    "cooccurrence": {"undirected"},
    "strain_sharing": {"undirected"},
    "source_contribution": {"directed"},
    "hgt_candidate": {"directed", "ambiguous"},
    "transmission_posterior": {"directed"},
}

NON_NA = {
    "edge_id",
    "source_id",
    "target_id",
    "source_type",
    "target_type",
    "edge_type",
    "direction_status",
    "weight",
    "weight_scale",
    "evidence_method",
    "evidence_unit",
    "provenance_id",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an evidence-typed TSV edge table and write normalized output."
    )
    parser.add_argument("input_tsv", type=Path)
    parser.add_argument("output_tsv", type=Path)
    parser.add_argument("summary_json", type=Path)
    parser.add_argument(
        "--allow-self",
        action="store_true",
        help="Allow self-loops (rejected by default).",
    )
    return parser.parse_args()


def blank(value: str | None) -> bool:
    return value is None or not value.strip()


def missing(value: str | None) -> bool:
    return blank(value) or value.strip().upper() == "NA"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    if not args.input_tsv.is_file():
        raise SystemExit(f"input does not exist: {args.input_tsv}")
    resolved_paths = {
        args.input_tsv.resolve(),
        args.output_tsv.resolve(),
        args.summary_json.resolve(),
    }
    if len(resolved_paths) != 3:
        raise SystemExit("input, normalized output, and summary paths must be distinct")
    for path in (args.output_tsv, args.summary_json):
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing output: {path}")

    input_digest = sha256(args.input_tsv)
    errors: list[str] = []
    rows: list[dict[str, str]] = []
    edge_ids: set[str] = set()
    relation_keys: set[tuple[str, ...]] = set()
    node_types: dict[str, str] = {}

    with args.input_tsv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise SystemExit("input has no header")
        duplicate_headers = [
            name for name, count in Counter(reader.fieldnames).items() if count > 1
        ]
        if duplicate_headers:
            raise SystemExit("duplicate header(s): " + ", ".join(duplicate_headers))
        absent = [name for name in REQUIRED if name not in reader.fieldnames]
        extra = [name for name in reader.fieldnames if name not in REQUIRED]
        if absent:
            raise SystemExit("missing required column(s): " + ", ".join(absent))
        if extra:
            raise SystemExit("unexpected column(s): " + ", ".join(extra))

        for line_number, raw in enumerate(reader, start=2):
            row = {key: (raw.get(key) or "").strip() for key in REQUIRED}
            if raw.get(None):
                errors.append(f"line {line_number}: unexpected extra tab-delimited field(s)")
            for key in REQUIRED:
                if blank(row[key]):
                    errors.append(
                        f"line {line_number}: {key} is empty; use NA only when inapplicable"
                    )
            for key in NON_NA:
                if not blank(row[key]) and row[key].upper() == "NA":
                    errors.append(f"line {line_number}: {key} cannot be NA")

            source_type = row["source_type"].lower()
            target_type = row["target_type"].lower()
            edge_type = row["edge_type"].lower()
            direction = row["direction_status"].lower()
            scale = "_".join(row["weight_scale"].lower().replace("-", " ").split())
            row["source_type"] = source_type
            row["target_type"] = target_type
            row["edge_type"] = edge_type
            row["direction_status"] = direction
            row["weight_scale"] = scale

            if source_type not in NODE_TYPES:
                errors.append(f"line {line_number}: unsupported source_type {source_type!r}")
            if target_type not in NODE_TYPES:
                errors.append(f"line {line_number}: unsupported target_type {target_type!r}")
            for node_id, node_type in (
                (row["source_id"], source_type),
                (row["target_id"], target_type),
            ):
                previous_type = node_types.setdefault(node_id, node_type)
                if previous_type != node_type:
                    errors.append(
                        f"line {line_number}: node {node_id!r} has conflicting types "
                        f"{previous_type!r} and {node_type!r}"
                    )
            if edge_type not in EDGE_DIRECTIONS:
                errors.append(f"line {line_number}: unsupported edge_type {edge_type!r}")
            elif direction not in EDGE_DIRECTIONS[edge_type]:
                expected = "/".join(sorted(EDGE_DIRECTIONS[edge_type]))
                errors.append(
                    f"line {line_number}: {edge_type} requires direction_status {expected}"
                )
            if direction in {"directed", "ambiguous"} and missing(row["direction_basis"]):
                errors.append(
                    f"line {line_number}: {direction} edge requires a direction_basis"
                )

            if row["source_id"] == row["target_id"] and not args.allow_self:
                errors.append(f"line {line_number}: self-loop is not allowed")

            if not missing(row["weight"]):
                try:
                    weight = float(row["weight"])
                    if not math.isfinite(weight):
                        raise ValueError
                    if scale in {
                        "probability",
                        "posterior_probability",
                        "fraction",
                        "proportion",
                        "contribution",
                        "ani_fraction",
                        "acni_fraction",
                    } and not 0 <= weight <= 1:
                        errors.append(
                            f"line {line_number}: {scale} weight must be in [0, 1]"
                        )
                    if scale in {
                        "percent",
                        "identity_percent",
                        "coverage_percent",
                        "ani_percent",
                    } and not 0 <= weight <= 100:
                        errors.append(
                            f"line {line_number}: {scale} weight must be in [0, 100]"
                        )
                    if scale in {"correlation", "pearson_r", "spearman_r"} and not -1 <= weight <= 1:
                        errors.append(
                            f"line {line_number}: {scale} weight must be in [-1, 1]"
                        )
                    if scale == "binary" and weight not in {0, 1}:
                        errors.append(f"line {line_number}: binary weight must be 0 or 1")
                    if scale in {
                        "count",
                        "contacts",
                        "normalized_contacts",
                        "reads",
                        "event_count",
                        "snp_distance",
                    } and weight < 0:
                        errors.append(
                            f"line {line_number}: {scale} weight must be non-negative"
                        )
                except ValueError:
                    errors.append(f"line {line_number}: weight must be finite")

            edge_id = row["edge_id"]
            if edge_id in edge_ids:
                errors.append(f"line {line_number}: duplicate edge_id {edge_id!r}")
            edge_ids.add(edge_id)

            if direction == "undirected" and row["target_id"] < row["source_id"]:
                row["source_id"], row["target_id"] = row["target_id"], row["source_id"]
                row["source_type"], row["target_type"] = (
                    row["target_type"],
                    row["source_type"],
                )

            relation_key = (
                row["source_id"],
                row["target_id"],
                edge_type,
                direction,
                row["evidence_method"],
                row["sample_id"],
                row["provenance_id"],
            )
            if relation_key in relation_keys:
                errors.append(
                    f"line {line_number}: duplicate relation within method/sample/provenance"
                )
            relation_keys.add(relation_key)
            rows.append(row)

    if sha256(args.input_tsv) != input_digest:
        raise SystemExit("input changed during validation")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 2

    rows.sort(
        key=lambda row: (
            row["edge_type"],
            row["source_id"],
            row["target_id"],
            row["evidence_method"],
            row["edge_id"],
        )
    )
    args.output_tsv.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_tsv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "schema_version": "1.0",
        "input": str(args.input_tsv),
        "input_sha256": input_digest,
        "normalized_output": str(args.output_tsv),
        "normalized_output_sha256": sha256(args.output_tsv),
        "rows": len(rows),
        "unique_nodes": len(
            {row["source_id"] for row in rows} | {row["target_id"] for row in rows}
        ),
        "node_types": dict(sorted(Counter(node_types.values()).items())),
        "edge_types": dict(sorted(Counter(row["edge_type"] for row in rows).items())),
        "direction_status": dict(
            sorted(Counter(row["direction_status"] for row in rows).items())
        ),
        "evidence_methods": dict(
            sorted(Counter(row["evidence_method"] for row in rows).items())
        ),
        "weight_scales": dict(
            sorted(Counter(row["weight_scale"] for row in rows).items())
        ),
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        f"validated {summary['rows']} edges, {summary['unique_nodes']} nodes, "
        f"{len(summary['edge_types'])} edge types"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
