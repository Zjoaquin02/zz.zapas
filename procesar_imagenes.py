import os
from PIL import Image, ImageDraw, ImageFont

def process_logo(logo_path, target_width=300, color='blanco'):
    """Convierte el logo de fondo blanco y letras negras a transparente con letras del color especificado."""
    logo = Image.open(logo_path).convert('L')
    logo_rgba = Image.new('RGBA', logo.size)
    logo_data = logo.getdata()
    new_data = []
    
    # Invertir: lo blanco se vuelve transparente, lo negro toma el color deseado.
    for p in logo_data:
        alpha = 255 - p  # Fondo blanco (255) -> Alpha 0. Texto negro (0) -> Alpha 255.
        if color == 'blanco':
            new_data.append((255, 255, 255, alpha))
        else:
            new_data.append((0, 0, 0, alpha))
        
    logo_rgba.putdata(new_data)
    
    aspect_ratio = logo_rgba.size[1] / logo_rgba.size[0]
    logo_rgba = logo_rgba.resize((target_width, int(target_width * aspect_ratio)), Image.Resampling.LANCZOS)
    return logo_rgba

def get_corner_coords(corner, block_w, block_h, img_w, img_h, margin_x=40, margin_y=50):
    if corner == '1': # Arriba Izquierda
        return margin_x, margin_y
    elif corner == '2': # Arriba Derecha
        return img_w - margin_x - block_w, margin_y
    elif corner == '3': # Abajo Derecha
        return img_w - margin_x - block_w, img_h - margin_y - block_h
    elif corner == '4': # Abajo Izquierda
        return margin_x, img_h - margin_y - block_h
    else:
        return margin_x, margin_y

def main():
    print("--- Creador de Imágenes ZZ ZAPAS ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "Img")
    dest_dir = os.path.join(base_dir, "Destino")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    imagenes = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not imagenes:
        print(f"No se encontraron imágenes en {img_dir}")
        return
        
    print("Imágenes disponibles:")
    for i, img_name in enumerate(imagenes):
        print(f"{i + 1}. {img_name}")
        
    sel = input("Elige el número de la imagen a convertir (o 'todas' para procesar todas): ")
    
    imgs_to_process = []
    if sel.lower() == 'todas':
        imgs_to_process = imagenes
    else:
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(imagenes):
                imgs_to_process.append(imagenes[idx])
            else:
                print("Selección inválida.")
                return
        except:
            print("Selección inválida.")
            return

    quieres_precio = input("¿Quieres poner precio? (s/n): ").strip().lower()
    precio = ""
    pos_precio = "1"
    if quieres_precio != 'n':
        precio = input("Ingresa el precio (ej. $55.000): ")
        pos_precio = input("¿Dónde quieres el precio? (1: Arriba Izq, 2: Arriba Der, 3: Abajo Der, 4: Abajo Izq): ").strip()
    
    preguntar_talle = input("¿Necesitas agregar los talles? (s/n): ")
    talles = ""
    pos_talle = "4"
    if preguntar_talle.lower() == 's':
        talles = input("Ingresa los talles (ej. 39 AL 43): ")
        pos_talle = input("¿Dónde quieres el talle? (1: Arriba Izq, 2: Arriba Der, 3: Abajo Der, 4: Abajo Izq): ").strip()

    pos_logo = input("¿Dónde quieres el logo? (1: Arriba Izq, 2: Arriba Der, 3: Abajo Der, 4: Abajo Izq): ").strip()

    color_texto = input("¿De qué color quieres las letras y el logo? (blanco/negro): ").strip().lower()
    if color_texto != 'negro':
        color_texto = 'blanco'
        fill_color = (255, 255, 255, 255)
    else:
        fill_color = (0, 0, 0, 255)

    # Intentar cargar fuentes elegantes (Calibri Light / Calibri)
    try:
        font_light = ImageFont.truetype("C:\\Windows\\Fonts\\calibril.ttf", 36)
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 90)
        font_medium = ImageFont.truetype("C:\\Windows\\Fonts\\calibril.ttf", 45)
    except IOError:
        font_light = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_medium = ImageFont.load_default()

    logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")
    logo = process_logo(logo_path, target_width=400, color=color_texto) if os.path.exists(logo_path) else None

    for img_name in imgs_to_process:
        print(f"Procesando {img_name}...")
        img_path = os.path.join(img_dir, img_name)
        img = Image.open(img_path).convert('RGBA')
        draw = ImageDraw.Draw(img)
        
        width, height = img.size
        
        # 2. Escribir el Precio
        if precio:
            bbox_title = draw.textbbox((0, 0), "PRECIO DE VENTA", font=font_medium)
            bbox_price = draw.textbbox((0, 0), precio, font=font_bold)
            w_title = bbox_title[2] - bbox_title[0]
            w_price = bbox_price[2] - bbox_price[0]
            block_w_precio = max(w_title, w_price)
            block_h_precio = bbox_title[3] + 30 + bbox_price[3]

            start_x_p, start_y_p = get_corner_coords(pos_precio, block_w_precio, block_h_precio, width, height, margin_x=40, margin_y=50)
            
            draw.text((start_x_p, start_y_p), "PRECIO DE VENTA", fill=fill_color, font=font_medium)
            text_bbox = draw.textbbox((start_x_p, start_y_p), "PRECIO DE VENTA", font=font_medium)
            draw.line([(start_x_p, text_bbox[3] + 10), (text_bbox[2], text_bbox[3] + 10)], fill=(255, 0, 0, 255), width=3)
            draw.text((start_x_p, text_bbox[3] + 30), precio, fill=fill_color, font=font_bold)
        
        # 3. Escribir los Talles
        if talles:
            talles_text = f"TALLES: {talles}"
            bbox_talles = draw.textbbox((0, 0), talles_text, font=font_medium)
            w_talles = bbox_talles[2] - bbox_talles[0]
            block_h_talles = bbox_talles[3] + 15
            
            start_x_t, start_y_t = get_corner_coords(pos_talle, w_talles, block_h_talles, width, height, margin_x=40, margin_y=50)
            
            draw.text((start_x_t, start_y_t), talles_text, fill=fill_color, font=font_medium)
            talles_bbox = draw.textbbox((start_x_t, start_y_t), talles_text, font=font_medium)
            draw.line([(start_x_t, talles_bbox[3] + 10), (start_x_t + 100, talles_bbox[3] + 10)], fill=(255, 0, 0, 255), width=3)

        # 4. Pegar el logo
        if logo:
            start_x_l, start_y_l = get_corner_coords(pos_logo, logo.width, logo.height, width, height, margin_x=10, margin_y=10)
            img.paste(logo, (start_x_l, start_y_l), logo)

        # Guardar resultado
        out_path = os.path.join(dest_dir, img_name)
        # Convertir de vuelta a RGB para guardar como JPEG
        img = img.convert('RGB')
        img.save(out_path, quality=95)
        print(f"Guardado exitosamente en: {out_path}")

if __name__ == '__main__':
    main()