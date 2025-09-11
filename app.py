import os
import tempfile
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfMerger
from PIL import Image
import argparse


def pdf_to_searchable(input_pdf, output_pdf, dpi=300, lang='eng', poppler_path=None, tesseract_config='--oem 3 --psm 3'):
    pages = convert_from_path(input_pdf, dpi=dpi, poppler_path=poppler_path)
    merger = PdfMerger()
    for i, page in enumerate(pages, start=1):
        # page is a PIL.Image
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(page, lang=lang, config=tesseract_config, extension='pdf')
        temp_pdf = os.path.join(tempfile.gettempdir(), f"page_{i}.pdf")
        with open(temp_pdf, "wb") as f:
            f.write(pdf_bytes)
        merger.append(temp_pdf)
    merger.write(output_pdf)
    merger.close()
    print(f"[OK] Saved searchable PDF: {output_pdf}")

def extract_text_from_pdf_images(input_pdf, out_txt="extracted_text.txt", dpi=300, poppler_path=None, lang='eng', tesseract_config='--oem 3 --psm 3'):
    pages = convert_from_path(input_pdf, dpi=dpi, poppler_path=poppler_path)
    all_text = []
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang=lang, config=tesseract_config)
        all_text.append(f"--- Page {i} ---\n{text}\n")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.writelines(all_text)
    print(f"[OK] Saved extracted text: {out_txt}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input scanned PDF")
    parser.add_argument("output", help="Output searchable PDF")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--poppler-path", default=None, help="(Windows) full path to poppler 'bin' folder")
    parser.add_argument("--tess-config", default="--oem 3 --psm 3")
    args = parser.parse_args()

    pdf_to_searchable(args.input, args.output, dpi=args.dpi, lang=args.lang,
                      poppler_path=args.poppler_path, tesseract_config=args.tess_config)
    # also save extracted text beside the searchable PDF
    txt_out = os.path.splitext(args.output)[0] + "_extracted.txt"
    extract_text_from_pdf_images(args.input, out_txt=txt_out, dpi=args.dpi, poppler_path=args.poppler_path, lang=args.lang, tesseract_config=args.tess_config)