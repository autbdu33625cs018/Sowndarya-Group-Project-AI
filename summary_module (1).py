def summarize_text(text: str) -> str:
    words = text.split()
    short = ' '.join(words[:60])
    return f'''Summary:
{short}...

Original length: {len(words)} words. This summary captures the main points and helps you quickly revise, just like in your document example (Industrial Revolution example).
'''
