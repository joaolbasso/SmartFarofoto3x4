import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog

# --- Dimensões Padrão para Foto 3x4 ---
DPI = 300
PIXELS_PER_CM = DPI / 2.54  # Aproximadamente 118.11 pixels por cm a 300 DPI

FOTO_LARGURA_CM = 3.2
FOTO_ALTURA_CM = 4.2
LARGURA_PX = int(FOTO_LARGURA_CM * PIXELS_PER_CM)
ALTURA_PX = int(FOTO_ALTURA_CM * PIXELS_PER_CM)
AREA_FOTO_3X4_PX = LARGURA_PX * ALTURA_PX

# --- Tamanho da folha da reveladora (10x15cm, ou 15.2cm x 10.3cm) ---
FOLHA_LARGURA_CM = 15.2
FOLHA_ALTURA_CM = 10.3
FOLHA_LARGURA_PX = int(FOLHA_LARGURA_CM * PIXELS_PER_CM)
FOLHA_ALTURA_PX = int(FOLHA_ALTURA_CM * PIXELS_PER_CM)

# --- Constantes para detecção e recorte da face ---
PROPORCAO_AREA_FACE_NA_FOTO_FINAL = 0.28
# Após seu feedback, estamos usando -1.1cm. Isso efetivamente move o corte para baixo na foto.
VERTICAL_OFFSET_CM = -1.1
VERTICAL_OFFSET_PX = int(VERTICAL_OFFSET_CM * PIXELS_PER_CM)

# --- Espaçamento e Margem para o layout da folha de impressão ---
SPACING_CM = 0.2  # Espaçamento horizontal e vertical entre as fotos (em CM)
SPACING_PX = int(SPACING_CM * PIXELS_PER_CM)

# Margem mínima para as bordas externas (esquerda e direita principalmente)
GLOBAL_BORDER_MARGIN_CM = 0.5
GLOBAL_BORDER_MARGIN_PX = int(GLOBAL_BORDER_MARGIN_CM * PIXELS_PER_CM)

# Caminho para o classificador Haar Cascade para detecção facial
FACE_CASCADE_PATH = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')

def process_face_to_3x4(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    if face_cascade.empty():
        print(
            f"Erro: Não foi possível carregar o classificador de face. Verifique o caminho: {FACE_CASCADE_PATH}")
        print("Certifique-se de que 'haarcascade_frontalface_default.xml' está na mesma pasta ou o caminho está correto.")
        return None

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(
        min(img.shape[0], img.shape[1]) // 10, min(img.shape[0], img.shape[1]) // 10))

    if len(faces) == 0:
        print("Nenhuma face detectada na imagem.")
        cv2.imshow("Original (Nenhuma Face Detectada)",
                   cv2.resize(img, (800, 600)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return None
    elif len(faces) > 1:
        print(
            f"Múltiplas faces detectadas ({len(faces)}). Processando a maior face.")
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        x, y, w, h = faces[0]
    else:
        x, y, w, h = faces[0]

    if h == 0:
        print("Erro: Altura da face detectada é zero. Não é possível processar.")
        return None
    face_aspect_ratio = w / h

    nova_altura_face_final = int(np.sqrt(
        (AREA_FOTO_3X4_PX * PROPORCAO_AREA_FACE_NA_FOTO_FINAL) / face_aspect_ratio))
    nova_largura_face_final = int(nova_altura_face_final * face_aspect_ratio)

    if nova_largura_face_final == 0 or nova_altura_face_final == 0:
        print("Erro: Dimensões calculadas para a face final resultaram em zero. Ajuste as constantes ou a imagem.")
        return None

    if nova_largura_face_final > LARGURA_PX or nova_altura_face_final > ALTURA_PX:
        print("Aviso: A face redimensionada para a proporção desejada excede as dimensões da foto 3x4. Reduzindo proporção da face.")

        scale_factor_exceed = max(
            nova_largura_face_final / LARGURA_PX, nova_altura_face_final / ALTURA_PX)

        new_face_width_final = int(
            nova_largura_face_final / scale_factor_exceed)
        new_face_height_final = int(
            nova_altura_face_final / scale_factor_exceed)

        area_face_desejada_px = new_face_width_final * new_face_height_final

        nova_altura_face_final = new_face_height_final
        nova_largura_face_final = new_face_width_final
        print(
            f"Nova proporção de área da face na foto final ajustada para: {(area_face_desejada_px / AREA_FOTO_3X4_PX):.2f}")

    crop_width_original = int(w * (LARGURA_PX / nova_largura_face_final))
    crop_height_original = int(h * (ALTURA_PX / nova_altura_face_final))

    center_face_x = x + w // 2
    center_face_y = y + h // 2 - VERTICAL_OFFSET_PX

    crop_x1 = int(center_face_x - crop_width_original // 2)
    crop_y1 = int(center_face_y - crop_height_original // 2)
    crop_x2 = crop_x1 + crop_width_original
    crop_y2 = crop_y1 + crop_height_original

    img_height, img_width = img.shape[:2]

    if crop_x1 < 0:
        crop_x2 += abs(crop_x1)
        crop_x1 = 0
    if crop_x2 > img_width:
        crop_x1 -= (crop_x2 - img_width)
        crop_x2 = img_width

    if crop_y1 < 0:
        crop_y2 += abs(crop_y1)
        crop_y1 = 0
    if crop_y2 > img_height:
        crop_y1 -= (crop_y2 - img_height)
        crop_y2 = img_height

    photo_aspect = LARGURA_PX / ALTURA_PX

    if (crop_x2 - crop_x1) < crop_width_original:
        actual_crop_width = crop_x2 - crop_x1
        crop_height_original = int(actual_crop_width / photo_aspect)
        crop_y1 = int(center_face_y - crop_height_original // 2)
        crop_y2 = crop_y1 + crop_height_original
        if crop_y1 < 0:
            crop_y2 += abs(crop_y1)
            crop_y1 = 0
        if crop_y2 > img_height:
            crop_y1 -= (crop_y2 - img_height)
            crop_y2 = img_height

    if (crop_y2 - crop_y1) < crop_height_original:
        actual_crop_height = crop_y2 - crop_y1
        crop_width_original = int(actual_crop_height * photo_aspect)
        crop_x1 = int(center_face_x - crop_width_original // 2)
        crop_x2 = crop_x1 + crop_width_original
        if crop_x1 < 0:
            crop_x2 += abs(crop_x1)
            crop_x1 = 0
        if crop_x2 > img_width:
            crop_x1 -= (crop_x2 - img_width)
            crop_x2 = img_width

    crop_x1, crop_y1, crop_x2, crop_y2 = int(
        crop_x1), int(crop_y1), int(crop_x2), int(crop_y2)
    
    debug_display_img = img.copy()

    cv2.rectangle(debug_display_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.rectangle(debug_display_img, (crop_x1, crop_y1), (crop_x2, crop_y2), (0, 0, 255), 2)

    display_height, display_width = debug_display_img.shape[:2]
    max_display_dim = 900
    if display_width > max_display_dim or display_height > max_display_dim:
        scale_factor_display = max_display_dim / max(display_width, display_height)
        debug_display_img = cv2.resize(debug_display_img, (int(display_width * scale_factor_display), int(display_height * scale_factor_display)))

    cv2.imshow("Original com Recorte (Verde: Face, Vermelho: Recorte 3x4)", debug_display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if crop_x2 <= crop_x1 or crop_y2 <= crop_y1:
        print("Erro: Região de recorte inválida após ajustes de borda. Tente outra imagem ou ajuste proporção.")
        return None

    cropped_region = img[crop_y1:crop_y2, crop_x1:crop_x2]

    final_photo = cv2.resize(
        cropped_region, (LARGURA_PX, ALTURA_PX), interpolation=cv2.INTER_AREA)

    return final_photo

def confirm_and_get_copies(processed_photo):
    root = tk.Tk()
    root.withdraw()

    img_pil = Image.fromarray(cv2.cvtColor(processed_photo, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)

    top = tk.Toplevel(root)
    top.title("Confirmação de Recorte")
    panel = tk.Label(top, image=img_tk)
    panel.pack()

    confirm = messagebox.askyesno(
        "Confirmação de Recorte", "O recorte está adequado?")
    top.destroy()

    if not confirm:
        messagebox.showinfo("Cancelado", "Operação cancelada pelo usuário.")
        root.destroy()
        return None

    while True:
        num_copies_str = simpledialog.askstring(
            "Quantidade de Cópias", "Quantas cópias você deseja? (2, 4, 6)", parent=root)
        if num_copies_str is None:
            messagebox.showinfo(
                "Cancelado", "Operação cancelada pelo usuário.")
            root.destroy()
            return None
        try:
            num_copies = int(num_copies_str)
            if num_copies in [2, 4, 6, 8, 10]:
                break
            else:
                messagebox.showwarning(
                    "Entrada Inválida", "Por favor, digite 2, 4, 6.")
        except ValueError:
            messagebox.showwarning(
                "Entrada Inválida", "Por favor, digite um número válido (2, 4, 6).")

    root.destroy()
    return num_copies


def arrange_photos_on_sheet(photo_cv, num_copies):
    """
    Organiza as fotos 3x4 na folha de impressão (15.2cm x 10.3cm)
    posicionando-as no canto superior direito com espaçamento definido
    e ajustando as margens verticalmente para ficarem próximas das bordas superior e inferior.
    """
    photo_pil = Image.fromarray(cv2.cvtColor(photo_cv, cv2.COLOR_BGR2RGB))
    sheet_pil = Image.new(
        'RGB', (FOLHA_LARGURA_PX, FOLHA_ALTURA_PX), (255, 255, 255))

    photos_per_row = 2

    # Calcula o número de linhas necessárias. A função ceil() de matemática (ou a divisão com +1 e //)
    # garante que mesmo um número ímpar de fotos ocupe uma linha completa.
    num_rows = (num_copies + photos_per_row - 1) // photos_per_row

    total_height_of_photos_block = (
        num_rows * ALTURA_PX) + ((num_rows - 1) * SPACING_PX)

    # Calcula o espaço vertical total disponível para as margens superior e inferior
    remaining_vertical_space = FOLHA_ALTURA_PX - total_height_of_photos_block

    # Se houver espaço restante, distribua igualmente entre a margem superior e inferior.
    # Garantindo que a margem superior seja pelo menos GLOBAL_BORDER_MARGIN_PX
    if remaining_vertical_space > 0:
        # Tenta centralizar verticalmente o bloco de fotos, mas respeitando uma margem mínima
        # Isso fará com que o bloco todo se mova para cima ou para baixo conforme necessário
        # para que o topo e o fundo fiquem próximos das bordas.
        start_y = max(GLOBAL_BORDER_MARGIN_PX, remaining_vertical_space // 2)
        # Para forçar que o par superior fique BEM perto da borda superior (tipo 0.5cm),
        
        # Margem superior de 0.5cm (aprox. 59 pixels)
        start_y = int(0.5 * PIXELS_PER_CM)

    else:
        # Se não há espaço restante ou o bloco é maior que a folha, comece do topo
        start_y = 0
        print("Aviso: As fotos podem não caber perfeitamente na altura com o espaçamento e margens atuais.")

    positions_to_paste = []

    # Inicia a primeira foto na borda direita, com a margem lateral
    current_x = FOLHA_LARGURA_PX - LARGURA_PX - GLOBAL_BORDER_MARGIN_PX
    current_y = start_y  # Usa a margem vertical calculada

    for i in range(num_copies):
        # Verifica se a posição atual permite colar a foto na folha.
        # A condição `current_x >= -LARGURA_PX` é para permitir que o canto esquerdo da foto
        # possa começar fora da tela à esquerda, se for uma foto que será colada mais para a esquerda.
        if current_y + ALTURA_PX <= FOLHA_ALTURA_PX:  # Apenas verifica se há altura suficiente
            positions_to_paste.append((current_x, current_y))
        else:
            print(
                f"Aviso: Não há mais espaço na folha para a cópia {i+1}. Colocando {len(positions_to_paste)} fotos.")
            break

        # Move para a esquerda para a próxima foto na mesma linha
        current_x -= (LARGURA_PX + SPACING_PX)

        # Se atingiu o número de fotos por linha, reseta X e move Y para a próxima linha
        if (i + 1) % photos_per_row == 0:
            current_x = FOLHA_LARGURA_PX - LARGURA_PX - \
                GLOBAL_BORDER_MARGIN_PX  # Volta para a borda direita
            current_y += (ALTURA_PX + SPACING_PX)  # Desce para a próxima linha

    for pos in positions_to_paste:
        # Garante que a posição final está dentro dos limites visíveis para evitar erros de paste
        if pos[0] >= 0 and pos[1] >= 0 and \
           pos[0] + LARGURA_PX <= FOLHA_LARGURA_PX and \
           pos[1] + ALTURA_PX <= FOLHA_ALTURA_PX:
            sheet_pil.paste(photo_pil, pos)
        else:
            print(
                f"Aviso: Posição calculada ({pos}) está ligeiramente fora dos limites para colagem. Ignorando esta foto ou recortando-a.")
            # Opcional: Se quiser que ele tente colar mesmo que a borda seja cortada, remova essa condição.
            # sheet_pil.paste(photo_pil, pos)

    return sheet_pil


def main():
    if len(sys.argv) < 2:
        messagebox.showerror("Erro", "Nenhum arquivo de imagem foi fornecido.")
        return

    image_path = sys.argv[1]

    processed_photo = process_face_to_3x4(image_path)
    if processed_photo is None:
        original_img = cv2.imread(image_path)

    num_copies = confirm_and_get_copies(processed_photo)
    if num_copies is None:
        return

    final_sheet_pil = arrange_photos_on_sheet(processed_photo, num_copies)

    output_dir = os.path.join(os.path.dirname(image_path), "Farofoto_Output")
    os.makedirs(output_dir, exist_ok=True)
    original_filename = os.path.splitext(os.path.basename(image_path))[0]
    output_filename = f"{original_filename}_3x4_x{num_copies}.jpg"
    output_path = os.path.join(output_dir, output_filename)

    final_sheet_pil.save(output_path)
    messagebox.showinfo(
        "Sucesso!", f"As fotos foram geradas e salvas em:\n{output_path}")


if __name__ == "__main__":
    main()
