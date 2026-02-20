"""
Ingestion script: chunk textbook Markdown files, embed, and upsert into Qdrant.

Usage:
    python -m scripts.ingest --docs-dir ../textbook/docs
"""
import argparse
import asyncio
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tiktoken
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.config import settings
from app.services.embedder import embed_text

ENCODER = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = 500
OVERLAP_TOKENS = 50


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by ---."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip()
    return text


def split_into_sentences(text: str) -> list[str]:
    """Naively split text on sentence-ending punctuation."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chapter_slug: str) -> list[dict]:
    """Chunk text into ≤MAX_TOKENS token segments with OVERLAP_TOKENS overlap."""
    text = strip_frontmatter(text)
    sentences = split_into_sentences(text)
    chunks: list[dict] = []
    current_tokens: list[int] = []
    current_sentences: list[str] = []
    chunk_index = 0

    for sentence in sentences:
        sentence_tokens = ENCODER.encode(sentence)
        if len(current_tokens) + len(sentence_tokens) > MAX_TOKENS and current_sentences:
            # Save current chunk
            chunk_text_str = " ".join(current_sentences)
            chunks.append({
                "chunk_id": f"{chapter_slug}_{chunk_index}",
                "chapter_slug": chapter_slug,
                "content": chunk_text_str,
                "token_count": len(current_tokens),
            })
            chunk_index += 1
            # Overlap: keep last OVERLAP_TOKENS worth of sentences
            overlap_sentences: list[str] = []
            overlap_tokens: list[int] = []
            for s in reversed(current_sentences):
                s_toks = ENCODER.encode(s)
                if len(overlap_tokens) + len(s_toks) <= OVERLAP_TOKENS:
                    overlap_sentences.insert(0, s)
                    overlap_tokens = s_toks + overlap_tokens
                else:
                    break
            current_sentences = overlap_sentences + [sentence]
            current_tokens = overlap_tokens + sentence_tokens
        else:
            current_sentences.append(sentence)
            current_tokens.extend(sentence_tokens)

    # Save final chunk
    if current_sentences:
        chunk_text_str = " ".join(current_sentences)
        chunks.append({
            "chunk_id": f"{chapter_slug}_{chunk_index}",
            "chapter_slug": chapter_slug,
            "content": chunk_text_str,
            "token_count": len(current_tokens),
        })

    return chunks


def derive_ids(filepath: str, docs_dir: str) -> tuple[str, str]:
    """Derive module_id and chapter_slug from the file path."""
    rel = os.path.relpath(filepath, docs_dir)
    parts = rel.replace("\\", "/").split("/")
    module_id = parts[0] if len(parts) >= 2 else "general"
    filename = os.path.splitext(parts[-1])[0]
    # Remove numeric prefix like "01-"
    chapter_slug = re.sub(r"^\d+-", "", filename)
    return module_id, f"{module_id}-{chapter_slug}"


async def ensure_collection(client: AsyncQdrantClient) -> None:
    """Create Qdrant collection if it does not exist."""
    collections = await client.get_collections()
    names = [c.name for c in collections.collections]
    if settings.qdrant_collection not in names:
        await client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print(f"✅ Created Qdrant collection: {settings.qdrant_collection}")
    else:
        print(f"ℹ  Qdrant collection already exists: {settings.qdrant_collection}")


async def ingest(docs_dir: str) -> None:
    client = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    await ensure_collection(client)

    total_chunks = 0
    md_files = []
    for root, _, files in os.walk(docs_dir):
        for f in sorted(files):
            if f.endswith(".md") and not f.startswith("_"):
                md_files.append(os.path.join(root, f))

    for filepath in md_files:
        module_id, chapter_slug = derive_ids(filepath, docs_dir)
        with open(filepath, encoding="utf-8") as fh:
            text = fh.read()

        chunks = chunk_text(text, chapter_slug)
        if not chunks:
            print(f"  ⚠  No chunks for {filepath}")
            continue

        points: list[PointStruct] = []
        for chunk in chunks:
            embedding = await embed_text(chunk["content"])
            payload = {
                "chunk_id": chunk["chunk_id"],
                "chapter_slug": chunk["chapter_slug"],
                "module_id": module_id,
                "content": chunk["content"],
                "token_count": chunk["token_count"],
            }
            points.append(
                PointStruct(
                    id=abs(hash(chunk["chunk_id"])) % (2**63),
                    vector=embedding,
                    payload=payload,
                )
            )

        await client.upsert(
            collection_name=settings.qdrant_collection,
            points=points,
        )
        print(f"  ✅ {chapter_slug}: {len(chunks)} chunks upserted")
        total_chunks += len(chunks)

    print(f"\n✅ Ingestion complete. Total chunks: {total_chunks}")
    await client.close()


def main():
    parser = argparse.ArgumentParser(description="Ingest textbook content into Qdrant")
    parser.add_argument(
        "--docs-dir",
        default="../textbook/docs",
        help="Path to the Docusaurus docs/ directory",
    )
    args = parser.parse_args()
    docs_dir = os.path.abspath(args.docs_dir)
    if not os.path.isdir(docs_dir):
        print(f"ERROR: docs-dir not found: {docs_dir}")
        sys.exit(1)
    asyncio.run(ingest(docs_dir))


if __name__ == "__main__":
    main()
