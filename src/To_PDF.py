from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os
import json
#Ini untuk read from json 
def ReadJSON(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    image_paths = []
    similarities = []
    for entry in data:
        image_path = entry['image2'] 
        similarity = f"Similarity: {entry['similarity']:.2f}%"  
        if entry['similarity']>=60:
            image_paths.append(image_path)
            similarities.append(similarity)
    
    return image_paths, similarities
#Ini hanya sebagai pembuat rapi gambar
def resize_image(image, max_width, max_height):
    """Resize the image to fit within the max dimensions, preserving aspect ratio."""
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if img_width > max_width or img_height > max_height:
        if (max_width / aspect_ratio) <= max_height:
            return image.resize((int(max_width), int(max_width / aspect_ratio)), Image.Resampling.LANCZOS)
        else:
            return image.resize((int(max_height * aspect_ratio), int(max_height)), Image.Resampling.LANCZOS)
    return image
#Nah ini fungsi utama, buat jadi pdf
def Create_PDF(image_folder, pdf_path, texts):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    page_width, page_height = letter

    margin = 10  # Margin on each side
    bottom_margin = 50  # Increased bottom margin
    max_img_width = (page_width - 3 * margin) / 2  # Two images per row, three margins in total
    max_img_height = (page_height - 4 * margin - 20 * 2 - bottom_margin) / 2  # Adjust for new bottom margin
    num_images = len(image_paths)
    images_per_page = 4
    for page in range((num_images - 1) // images_per_page + 1):
        for i in range(images_per_page):
            idx = page * images_per_page + i
            if idx >= num_images:
                break

            try:
                image_path = image_paths[idx]
                with Image.open(image_path) as img:
                    img = resize_image(img, max_img_width, max_img_height)

                img_width, img_height = img.size
                col = i % 2
                row = i // 2
                image_x = margin + col * (max_img_width + margin)
                image_y = page_height - bottom_margin - (row + 1) * (max_img_height + margin + 20)

                # Draw text above the image
                text = texts[idx] if idx < len(texts) else ""
                text_y = image_y + max_img_height - 10  # Reduce the vertical space between text and image more
                c.drawString(image_x, text_y, text)

                # Draw image
                c.drawImage(image_path, image_x, image_y - margin, width=img_width, height=img_height)
            except Exception as e:
                print(f"Error processing {images[idx]}: {e}")

        c.showPage()  # End the current page and start a new page

    c.save()
#Kr kr begini cara runnya
json_file_path = 'similarity_results.json'
image_paths, texts = ReadJSON(json_file_path)
pdf_path = 'SimilarityResults1.pdf'
Create_PDF(image_paths, pdf_path, texts)
