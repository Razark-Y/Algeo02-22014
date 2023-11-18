import json
from fpdf import FPDF
image_width, image_height = 70, 70 
similarity_text_height = 10  
vertical_spacing = 10  
horizontal_spacing = 10  
max_images_per_row = 2  
max_rows_per_page = 3  
def add_pink_background(pdf):
    pdf.set_fill_color(255, 179, 193)
    pdf.rect(0, 0, 210, 297, 'F')  
def toPDF(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    pdf = FPDF()
    pdf.set_font("Courier", size=12)
    pdf.add_page()
    add_pink_background(pdf)
    pdf.set_xy(0, 10)
    pdf.set_font("Courier", 'B', 28)
    pdf.set_text_color(89, 13, 34)
    pdf.cell(210, 20, "Kosu Salted Caramel", 0, 1, 'C')
    pdf.set_font("Courier", 'B', 20)
    pdf.set_text_color(164, 19, 60)
    pdf.cell(190, 10    , "Similarity Results", 0, 1, 'C')
    pdf.set_font("Courier", 'B', 18)
    current_x, current_y = 10, 60  
    row_count, image_count = 0, 0
    first_page_rows = 2  
    if not data:
        pdf.set_font("Courier", 'B', 28)
        pdf.set_text_color(89, 13, 34)
        pdf.cell(0, 60, "", 0, 1, 'C')
        pdf.cell(0, 20, "Tidak ada Gambar yang cocok", 1, 1, 'C')
    else:
        for item in data:
            if (pdf.page_no() == 1 and row_count >= first_page_rows) or (pdf.page_no() > 1 and row_count >= max_rows_per_page):
                pdf.add_page()
                add_pink_background(pdf)
                current_x, current_y = 10, 10
                row_count, image_count = 0, 0
            pdf.image(item["image2"], x=current_x + 20, y=current_y, w=image_width, h=image_height)
            pdf.set_xy(current_x, current_y + image_height)
            pdf.cell(image_width + 40, similarity_text_height, f"Similarity: {item['similarity']}%", align='C')
            image_count += 1
            current_x += image_width + horizontal_spacing
            if image_count >= max_images_per_row:
                pdf.set_line_width(1.5)
                pdf.set_draw_color(89, 13, 34)
                line_y = current_y + image_height + similarity_text_height + (vertical_spacing / 2)
                pdf.line(10,line_y,200,line_y)
                current_y += image_height + similarity_text_height + vertical_spacing
                current_x = 10
                image_count = 0
                row_count += 1
    pdf.output("images_with_similarity_pink_background.pdf")

toPDF('similarity_results.json')