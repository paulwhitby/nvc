"""Attempt to avoid copy/paste of zonation and succession text by reading the pdf directly

Documentation here: https://pypdf.readthedocs.io/en/stable/user/extract-text.html"""

# pylint: disable=line-too-long

# import pypdf
from pypdf import PdfReader

FILES_TO_PROCESS = (
"a1", "a10", "a11", "a12", "a13", "a14", "a15", "a16", "a17", "a18", "a19", "a2", "a20", "a21", "a22", 
"a23", "a24", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "cg1", "cg10", "cg11", "cg12", "cg13", "cg14", 
"cg2", "cg3", "cg4", "cg5", "cg6", "cg7", "cg8", "cg9", "h1", "h10", "h11", "h12", "h13", "h14", "h15", 
"h16", "h17", "h18", "h19", "h2", "h20", "h21", "h22", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "m1", 
"m10", "m11", "m12", "m13", "m14", "m15", "m16", "m17", "m18", "m19", "m2", "m20", "m21", "m22", "m23", 
"m24", "m25", "m26", "m27", "m28", "m29", "m3", "m30", "m31", "m32", "m33", "m34", "m35", "m36", "m37", 
"m38", "m4", "m5", "m6", "m7", "m8", "m9", "mc1", "mc10", "mc11", "mc12", "mc2", "mc3", "mc4", "mc5", 
"mc6", "mc7", "mc8", "mc9", "mg1", "mg10", "mg11", "mg12", "mg13", "mg2", "mg3", "mg4", "mg5", "mg6", 
"mg7", "mg8", "mg9", "ov1", "ov10", "ov11", "ov12", "ov13", "ov14", "ov15", "ov16", "ov17", "ov18", 
"ov19", "ov2", "ov20", "ov21", "ov22", "ov23", "ov24", "ov25", "ov26", "ov27", "ov28", "ov29", "ov3", 
"ov30", "ov31", "ov32", "ov33", "ov34", "ov35", "ov36", "ov37", "ov38", "ov39", "ov4", "ov40", "ov41", 
"ov42", "ov5", "ov6", "ov7", "ov8", "ov9", "s1", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17", 
"s18", "s19", "s2", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27", "s28", "s3", "s4", "s5", "s6", 
"s7", "s8", "s9", "sd1", "sd10", "sd11", "sd12", "sd13", "sd14", "sd15", "sd16", "sd17", "sd18", "sd19", 
"sd2", "sd3", "sd4", "sd5", "sd6", "sd7", "sd8", "sd9", "sm1", "sm10", "sm11", "sm12", "sm13", "sm14", 
"sm15", "sm16", "sm17", "sm18", "sm19", "sm2", "sm20", "sm21", "sm22", "sm23", "sm24", "sm25", "sm26", 
"sm27", "sm28", "sm3", "sm4", "sm5", "sm6", "sm7", "sm8", "sm9", "u1", "u10", "u11", "u12", "u13", "u14", 
"u15", "u16", "u17", "u18", "u19", "u2", "u20", "u21", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "w1", 
"w10", "w11", "w12", "w13", "w14", "w15", "w16", "w17", "w18", "w19", "w2", "w20", "w21", "w22", "w23", 
"w24", "w25", "w3", "w4", "w5", "w6", "w7", "w8", "w9"
)

MORE_FILES_TO_PROCESS = ( "u20", "sm7" )


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


def write_text_to_csv(key_text, text, csv_filename, verbose=False):
    """factor out writing the text to the textfile"""

    with open(csv_filename, 'w', encoding="utf-8") as f:
        new_text = '"'+key_text+'","'+text+'"'
        chars_written = f.write(new_text)
        if verbose:
            print(csv_filename, "written with", chars_written, "chars")

    return chars_written


def write_dict_to_csv(d, csv_filename, verbose=False):
    """factor out writing the compiled dict to a csv_file"""

    chars_written = 0

    with open(csv_filename, 'w', encoding="utf-8") as f:
        for k, v in d.items():
            csv_row = '"'+k+'","'+v+'"\n'
            chars_written += f.write(csv_row)

    if verbose:
        print(csv_filename, "written with", chars_written, "chars")

    return chars_written


def find_succession_text(text, verbose=False) -> str:
    """scan through the extracted text to find the section between
    'Zonation and succession ' and 'Distribution '
    """

    zs_str = "Zonation and succession " # "Zonation and succesion " # special processing for the TYPO IN U20
    ds_str = "Distribution "

    result_subtext = ""

    if verbose:
        print("scanning", text)

    zs = text.find(zs_str)
    ds = text.find(ds_str)

    if verbose:
        print(zs_str, zs, ds_str, ds)

    if zs != -1 and ds != 1:
        first_partition = text.partition(zs_str)
        zs_subtext = first_partition[1] + first_partition[2]
        second_partition = zs_subtext.partition(ds_str)
        result_subtext = second_partition[0] + second_partition[1]

        if verbose:
            print(result_subtext)
    else:
        print("***Distribution found before Zonation, or Zonation not found")

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

    extracted = {}

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
        extracted[p] = found_text
        write_text_to_csv(p, found_text, txt_name, verbose)
        # if verbose:
        print("found", found_text)

    return extracted


TEXT_EXTRACTED = process_batch_pdf_extractions(FILES_TO_PROCESS, False)
write_dict_to_csv(TEXT_EXTRACTED, "txts/all_processed_succession_text.csv", False)
