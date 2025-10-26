from transformers import pipeline

# Initializing only once  
# facebook/bart-large-cnn is strong for general summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def _chunks(words, chunk_size=700):
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

def summarize_text(text: str) -> str:
    words = text.split()
    # If it is short file we can pass it once and that is sufficient
    if len(words) <= 700:
        out = summarizer(text, max_length=220, min_length=80, do_sample=False)
        return out[0]["summary_text"]

    # If long, split into chunks , summarize and combine 
    partials = []
    for chunk in _chunks(words, chunk_size=700):
        res = summarizer(chunk, max_length=180, min_length=60, do_sample=False)
        partials.append(res[0]["summary_text"])

    mega = " ".join(partials)
    final = summarizer(mega, max_length=240, min_length=90, do_sample=False)
    return final[0]["summary_text"]
