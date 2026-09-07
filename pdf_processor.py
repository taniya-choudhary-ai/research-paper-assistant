import pymupdf


def extract_text(pdf_path):
    """
    Extract text from a PDF while keeping page numbers.
    """

    doc = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text().strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    doc.close()

    return pages


def create_chunks(pages, chunk_size=1000, overlap=200):
    """
    Split page text into smaller chunks.

    Each chunk keeps its page number.
    """

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = min(
                start + chunk_size,
                len(text)
            )

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page": page["page"]
            })

            # Stop when we reach the end of the text
            if end >= len(text):
                break

            start = end - overlap

    return chunks
