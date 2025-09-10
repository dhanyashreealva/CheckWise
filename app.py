import os
import tempfile
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfMerger
from PIL import Image