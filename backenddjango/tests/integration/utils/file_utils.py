"""
File utilities for integration tests.
"""

import os
import io
import tempfile
from typing import Tuple, Optional, BinaryIO
from django.core.files.uploadedfile import SimpleUploadedFile


def create_text_file(
    content: str = "Test file content",
    filename: str = "test.txt",
    content_type: str = "text/plain"
) -> SimpleUploadedFile:
    """
    Create a text file for testing file uploads.
    
    Args:
        content: Content of the file
        filename: Name of the file
        content_type: MIME type of the file
        
    Returns:
        SimpleUploadedFile: The created file
    """
    return SimpleUploadedFile(
        name=filename,
        content=content.encode('utf-8'),
        content_type=content_type
    )


def create_binary_file(
    content: bytes = b"Binary test content",
    filename: str = "test.bin",
    content_type: str = "application/octet-stream"
) -> SimpleUploadedFile:
    """
    Create a binary file for testing file uploads.
    
    Args:
        content: Content of the file
        filename: Name of the file
        content_type: MIME type of the file
        
    Returns:
        SimpleUploadedFile: The created file
    """
    return SimpleUploadedFile(
        name=filename,
        content=content,
        content_type=content_type
    )


def create_image_file(
    filename: str = "test.jpg",
    size: Tuple[int, int] = (100, 100),
    color: str = "red",
    format: str = "JPEG"
) -> SimpleUploadedFile:
    """
    Create an image file for testing image uploads.
    
    Args:
        filename: Name of the file
        size: Size of the image (width, height)
        color: Color of the image
        format: Format of the image (JPEG, PNG, etc.)
        
    Returns:
        SimpleUploadedFile: The created image file
    """
    from PIL import Image
    
    image = Image.new('RGB', size, color=color)
    image_io = io.BytesIO()
    image.save(image_io, format=format)
    image_io.seek(0)
    
    content_type = f"image/{format.lower()}"
    
    return SimpleUploadedFile(
        name=filename,
        content=image_io.getvalue(),
        content_type=content_type
    )


def create_pdf_file(
    content: str = "Test PDF content",
    filename: str = "test.pdf"
) -> SimpleUploadedFile:
    """
    Create a PDF file for testing PDF uploads.
    
    Args:
        content: Content of the PDF
        filename: Name of the file
        
    Returns:
        SimpleUploadedFile: The created PDF file
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, content)
        c.save()
        
        pdf_content = buffer.getvalue()
        
        return SimpleUploadedFile(
            name=filename,
            content=pdf_content,
            content_type="application/pdf"
        )
    except ImportError:
        # Fallback if reportlab is not installed
        return create_binary_file(
            content=f"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Resources<<>>/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 22>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n({content}) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000102 00000 n \n0000000182 00000 n \ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n254\n%%EOF".encode('utf-8'),
            filename=filename,
            content_type="application/pdf"
        )


def create_excel_file(
    filename: str = "test.xlsx",
    data: Optional[list] = None
) -> SimpleUploadedFile:
    """
    Create an Excel file for testing Excel uploads.
    
    Args:
        filename: Name of the file
        data: Data to include in the Excel file (list of lists)
        
    Returns:
        SimpleUploadedFile: The created Excel file
    """
    try:
        import xlsxwriter
        
        if data is None:
            data = [
                ["Name", "Age", "City"],
                ["John Doe", 30, "New York"],
                ["Jane Smith", 25, "Los Angeles"],
                ["Bob Johnson", 40, "Chicago"]
            ]
        
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                worksheet.write(row_idx, col_idx, value)
        
        workbook.close()
        buffer.seek(0)
        
        return SimpleUploadedFile(
            name=filename,
            content=buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        # Fallback if xlsxwriter is not installed
        return create_binary_file(
            content=b"PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00_rels/.rels",
            filename=filename,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def create_temp_directory() -> str:
    """
    Create a temporary directory for file operations.
    
    Returns:
        str: Path to the temporary directory
    """
    return tempfile.mkdtemp()


def create_temp_file(content: str = "Test content") -> Tuple[str, BinaryIO]:
    """
    Create a temporary file with the given content.
    
    Args:
        content: Content of the file
        
    Returns:
        Tuple[str, BinaryIO]: Path to the temporary file and the file object
    """
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    
    return path, open(path, 'rb')
