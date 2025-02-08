import os
import json
import glob

# Répertoire contenant les fichiers JSON et où seront générés les fichiers HTML
json_folder = "/home/batiste/Documents/Storm/final_tierlists"

# Récupérer tous les fichiers JSON dans le dossier
json_files = glob.glob(os.path.join(json_folder, "*.json"))

# Définition de l'ordre et des labels pour chaque tier
tier_order = [
    ("ssMonster", "SS Tier"),
    ("smonster", "S Tier"),
    ("amonster", "A Tier"),
    ("bmonster", "B Tier"),
    ("cmonster", "C Tier"),
    ("dmonster", "D Tier"),
]

# Liste qui contiendra le nom de chaque fichier HTML généré
generated_html_files = []

# Pour chaque fichier JSON, générer le fichier HTML correspondant
for json_filename in json_files:
    # Charger les données JSON
    with open(json_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extraire le "rank" depuis le nom du fichier (exemple : "G3_tier_list.json" → "G3")
    base_name = os.path.basename(json_filename)
    rank = base_name.split("_")[0]

    # Construire le contenu HTML en se basant sur le même style
    html_output = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Tier List des Monstres {rank}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #f9f9f9;
      padding: 20px;
    }}
    h1, h2 {{
      text-align: center;
    }}
    .tier {{
      margin-bottom: 30px;
      background: #fff;
      padding: 10px;
      border-radius: 8px;
      box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }}
    .tier-header {{
      font-size: 2em;
      margin-bottom: 10px;
      border-bottom: 2px solid #ccc;
      padding-bottom: 5px;
    }}
    .monster-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .monster-card {{
      background: #eaeaea;
      border-radius: 5px;
      padding: 8px;
      width: 120px;
      text-align: center;
    }}
    .monster-card img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
    }}
    .monster-name {{
      margin-top: 5px;
      font-weight: bold;
    }}
    .monster-score {{
      margin-top: 3px;
      font-size: 0.9em;
      color: #555;
    }}
  </style>
</head>
<body>
  <h1>Tier List des Monstres {rank}</h1>
  <h2>Donnée du 28 Octobre 2024 au 02 Février 2025</h2>
"""

    # Pour chaque tier défini, ajouter la section correspondante
    for tier_key, tier_label in tier_order:
        monsters = data.get(tier_key, [])
        html_output += f'  <div class="tier">\n'
        html_output += f'    <div class="tier-header">{tier_label}</div>\n'
        html_output += '    <div class="monster-container">\n'

        # Pour chaque monstre, créer une "carte"
        for monster in monsters:
            name    = monster["monsterName"]
            img_url = monster["monsterHeadImg"]
            score   = monster["aiScore"]
            html_output += f'''      <div class="monster-card">
        <img src="{img_url}" alt="{name}">
        <div class="monster-name">{name}</div>
        <div class="monster-score">Score: {score:.2f}</div>
      </div>
'''
        html_output += '    </div>\n'
        html_output += '  </div>\n'

    html_output += """
</body>
</html>
"""

    # Nom du fichier HTML de sortie (même nom que le JSON avec l'extension .html)
    output_filename = os.path.join(json_folder, os.path.splitext(base_name)[0] + ".html")
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(html_output)

    generated_html_files.append(os.path.basename(output_filename))
    print(f"Tier list générée dans le fichier '{output_filename}'.")

# --------------------------------------
# Création du fichier index.html
# --------------------------------------
index_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Index des Tier Lists</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            display: block;
            text-decoration: none;
            color: #333;
            background: #fff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        a:hover {
            background: #eaeaea;
        }
    </style>
</head>
<body>
    <h1>Index des Tier Lists</h1>
    <ul>
"""

# Ajouter un lien pour chaque fichier HTML généré
for html_file in generated_html_files:
    index_html += f'        <li><a href=final_tierlists/{html_file}>{html_file}</a></li>\n'

index_html += """    </ul>
</body>
</html>
"""

# Sauvegarder le fichier index.html dans le même dossier
index_filename = "index.html"
with open(index_filename, "w", encoding="utf-8") as file:
    file.write(index_html)

print(f"Fichier d'index généré dans '{index_filename}'.")
