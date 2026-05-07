import base64
import fitz

def fitzDecode(value):
    try:
        pdf_data = base64.b64decode(value)
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return {"ok": True, "text": text}
    except Exception as e:
        return {"ok": False, "erro": str(e)}