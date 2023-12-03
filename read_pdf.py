"""Attempt to avoid copy/paste of zonation and succession text by reading the pdf directly

Documentation here: https://pypdf.readthedocs.io/en/stable/user/extract-text.html"""

# pylint: disable=line-too-long

# import pypdf
from pypdf import PdfReader

FILES_TO_PROCESS = (
    "w15",
    "w16",
)

TEXT_EXTRACTED = {}


def clean_text(text_to_clean) -> str:
    """factor out the cleaning up of the text"""
    cleaned_text = text_to_clean.replace("\n", " ").replace("- ", "-").replace(" ­ ", "").replace("Quer ­ cus", "Quercus").replace("­", "").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
    return cleaned_text


def write_text_to_file(text, text_filename, verbose=False):
    """factor out writing the text to the textfile"""

    with open(text_filename, 'w', encoding="utf-8") as f:
        chars_written = f.write(text)
        if verbose:
            print(text_filename, "written with", chars_written, "chars")

    return chars_written


def find_succession_text(text, verbose=False) -> str:
    """scan through the extracted text to find the section between
    'Zonation and succession ' and 'Distribution '
    """

    zs_str = "Zonation and succession "
    ds_str = "Distribution "

    result_subtext = ""

    if verbose:
        print("scanning", text)

    zs = text.find(zs_str)
    ds = text.find(ds_str)

    if verbose:
        print(zs_str, zs, ds_str, ds)

    if zs != -1 and zs < ds:
        first_partition = text.partition(zs_str)
        zs_subtext = first_partition[2]
        second_partition = zs_subtext.partition(ds_str)
        result_subtext = second_partition[0]

        if verbose:
            print(result_subtext)

    return result_subtext


def extract_text_from_pdf(pdf_filename, verbose=False):
    """extract text from file pdf_filename and write it to file text_filename"""
    if verbose:
        print("processing", pdf_filename)

    text: str = ""
    # cleaned_text: str = ""

    try:
        reader = PdfReader(pdf_filename)
        for page in reader.pages:
            text += page.extract_text()

    except Exception as exc:
        print("oops:", exc)

    return text


def process_batch_pdf_extractions(pdf_names, verbose=False):
    """iterate through tuple of pdf_filenames extracting text for each"""
    if verbose:
        print("processing batch", pdf_names)

    for p in pdf_names:
        if verbose:
            print(p)
        pdf_name = "pdfs/"+p+".pdf"
        txt_name = "txts/"+p+".txt"
        extracted_text = extract_text_from_pdf(pdf_name, verbose)
        cleaned_text = clean_text(extracted_text)
        found_text = find_succession_text(cleaned_text, verbose)
        write_text_to_file(found_text, txt_name, verbose)
        # if verbose:
        print("found", found_text)


process_batch_pdf_extractions(FILES_TO_PROCESS, False)
