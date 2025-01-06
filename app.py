import os
from tkinter import Tk, filedialog, Label, Button, Entry, Frame, StringVar
from html2image import Html2Image

# Définir le répertoire de sortie dynamiquement
user_documents = os.path.expanduser("~/Desktop")
output_path = os.path.join(user_documents, "cartes_professionnelles")
os.makedirs(output_path, exist_ok=True)  # Créer le répertoire s'il n'existe pas

# Autres variables globales
photo_path = ""
html_template_path = os.path.join(os.getcwd(), "badge1.html")
  # Utilisation d'un chemin relatif pour le template HTML
logo_path = os.path.join(os.getcwd(), "logo.png")  # Assurez-vous d'avoir un logo à cet endroit

# Fonction pour choisir une photo
def choisir_photo():
    global photo_path
    photo_path = filedialog.askopenfilename(
        title="Sélectionnez une photo",
        filetypes=[("Images", "*.png *.jpg *.jpeg")]
    )
    if photo_path:
        lbl_photo_path.config(text=f"Photo sélectionnée : {os.path.basename(photo_path)}", fg="green")
    else:
        lbl_photo_path.config(text="Aucune photo sélectionnée", fg="red")

# Fonction pour générer le badge
def generer_badge():
    if not all([nom_var.get(), prenom_var.get(), fonction_var.get(), matricule_var.get(), cni_var.get(), photo_path]):
        lbl_result.config(text="Tous les champs et la photo doivent être remplis.", fg="red")
        return

    # Charger le modèle HTML
    with open(html_template_path, "r", encoding="utf-8") as template_file:
        html_content = template_file.read()

    # Remplacer les informations dans le fichier HTML
    html_content = html_content.replace("{photo_path}", photo_path)
    html_content = html_content.replace("{nom}", nom_var.get())
    html_content = html_content.replace("{prenom}", prenom_var.get())
    html_content = html_content.replace("{fonction}", fonction_var.get())
    html_content = html_content.replace("{matricule}", matricule_var.get())
    html_content = html_content.replace("{cni}", cni_var.get())
    html_content = html_content.replace("{local_path}", logo_path)  # Remplacer le logo

    # Sauvegarder le fichier HTML temporaire
    input_file = os.path.join(output_path, "badge_temp.html")
    with open(input_file, "w", encoding="utf-8") as output_file:
        output_file.write(html_content)

    # Générer un nom de fichier dynamique pour l'image
    nom_fichier_image = f"carte_{nom_var.get().strip().replace(' ', '_')}_{prenom_var.get().strip().replace(' ', '_')}.png"
    nom_fichier_image = nom_fichier_image.replace("/", "_").replace("\\", "_")  # Nettoyage du nom
    output_image_path = os.path.join(output_path, nom_fichier_image)

    # Générer l'image avec html2image
    try:
        hti = Html2Image(output_path=output_path)
        hti.screenshot(html_file=input_file, save_as=nom_fichier_image, size=(400, 615))

        if os.path.exists(output_image_path):
            lbl_result.config(text=f"Badge généré avec succès : {output_image_path}", fg="green")
        else:
            lbl_result.config(text="Erreur : Le badge n'a pas pu être généré.", fg="red")
    except Exception as e:
        lbl_result.config(text=f"Erreur lors de la génération : {str(e)}", fg="red")

# Interface Tkinter
root = Tk()
root.title("Générateur de Carte Professionnelle")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

# Variables pour les champs de saisie
nom_var = StringVar()
prenom_var = StringVar()
fonction_var = StringVar()
matricule_var = StringVar()
cni_var = StringVar()

# Interface améliorée
Label(root, text="Générateur de Carte Professionnelle", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=10)

frame_inputs = Frame(root, bg="#f4f4f4")
frame_inputs.pack(pady=10)

Label(frame_inputs, text="Nom :", bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5, sticky="w")
Entry(frame_inputs, textvariable=nom_var, width=30).grid(row=0, column=1, pady=5)

Label(frame_inputs, text="Prénoms :", bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5, sticky="w")
Entry(frame_inputs, textvariable=prenom_var, width=30).grid(row=1, column=1, pady=5)

Label(frame_inputs, text="Fonction :", bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky="w")
Entry(frame_inputs, textvariable=fonction_var, width=30).grid(row=2, column=1, pady=5)

Label(frame_inputs, text="Matricule :", bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky="w")
Entry(frame_inputs, textvariable=matricule_var, width=30).grid(row=3, column=1, pady=5)

Label(frame_inputs, text="N°CNI :", bg="#f4f4f4").grid(row=4, column=0, padx=10, pady=5, sticky="w")
Entry(frame_inputs, textvariable=cni_var, width=30).grid(row=4, column=1, pady=5)

Button(root, text="Choisir une photo", command=choisir_photo, bg="#076633", fg="white").pack(pady=10)
lbl_photo_path = Label(root, text="Aucune photo sélectionnée", fg="red", bg="#f4f4f4")
lbl_photo_path.pack(pady=5)

Button(root, text="Générer le Badge", command=generer_badge, bg="#076633", fg="white").pack(pady=20)
lbl_result = Label(root, text="", fg="blue", bg="#f4f4f4")
lbl_result.pack(pady=10)

root.mainloop()
