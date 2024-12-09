from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

class DocumentProcessor:
    def __init__(self, upload_dir="uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
        
    async def save_file(self, file, incident_id: int):
        file_path = os.path.join(self.upload_dir, f"{incident_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return file_path
    
    def extract_text(self, file_path: str) -> str:
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext in ['jpg', 'jpeg', 'png']:
            return self._extract_from_image(file_path)
        elif file_ext == 'pdf':
            return self._extract_from_pdf(file_path)
        return ""
    
    def _extract_from_image(self, image_path: str) -> str:
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}")
            return ""
            
    def _extract_from_pdf(self, pdf_path: str) -> str:
        try:
            pages = convert_from_path(pdf_path)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page)
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return "" 