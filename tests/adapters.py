from __future__ import annotations
from cs336_data.extract_text import extract_text 
from cs336_data.language_identification import identify_language
from cs336_data.mask_emails import mask_emails, mask_phone_numbers, mask_ip_addresses
from cs336_data.harmful_content import identify_hatespeech, identify_nsfw
from cs336_data.gopher_filters import gopher_quality_filter
import os
from typing import Any



def run_extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    return extract_text(html_bytes)


def run_identify_language(text: str) -> tuple[Any, float]:
    return identify_language(text)


def run_mask_emails(text: str) -> tuple[str, int]:
    return mask_emails(text)


def run_mask_phone_numbers(text: str) -> tuple[str, int]:
    return mask_phone_numbers(text)


def run_mask_ips(text: str) -> tuple[str, int]:
    return mask_ip_addresses(text)


def run_classify_nsfw(text: str) -> tuple[Any, float]:
    return identify_nsfw(text)


def run_classify_toxic_speech(text: str) -> tuple[Any, float]:
    return identify_hatespeech(text)


def run_classify_quality(text: str) -> tuple[Any, float]:
    raise NotImplementedError


def run_gopher_quality_filter(text: str) -> bool:
    return gopher_quality_filter(text)


def run_exact_line_deduplication(
    input_files: list[os.PathLike], output_directory: os.PathLike
):
    raise NotImplementedError


def run_minhash_deduplication(
    input_files: list[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngrams: int,
    jaccard_threshold: float,
    output_directory: os.PathLike,
):
    raise NotImplementedError
