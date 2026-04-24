def chunk_text(text, max_words_per_chunk=100):
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

    chunks = []
    current_chunk = []
    current_length = 0
    
    for p in paragraphs:
        words = p.split()
        if current_length + len(words) > max_words_per_chunk and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = words
            current_length = len(words)
        else:
            current_chunk.extend(words)
            current_length += len(words)
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
