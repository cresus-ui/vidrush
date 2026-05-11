import json
import os

filepath = 'docs/MoneyPrinterTurbo.ipynb'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Update cells
    nb['cells'][0]['source'] = [
        "# Guide d'installation Vidrush (MoneyPrinterTurbo)\n",
        "\n",
        "Ce notebook vous guidera dans l'installation et le lancement de [Vidrush](https://github.com/cresus-ui/vidrush) sur Google Colab."
    ]

    nb['cells'][1]['source'] = [
        "## 1. Cloner le dépôt et installer les dépendances\n",
        "\n",
        "Nous allons cloner votre dépôt et installer les paquets nécessaires. \n",
        "*Note : Les messages d'erreur rouges concernant 'pip dependency resolver' sont normaux sur Colab et n'empêchent pas le fonctionnement de l'application.*"
    ]

    nb['cells'][2]['source'] = [
        "!git clone https://github.com/cresus-ui/vidrush.git\n",
        "%cd vidrush\n",
        "# Installation avec gestion des conflits Colab\n",
        "!pip install -r requirements.txt --quiet\n",
        "!pip install pyngrok --quiet"
    ]

    nb['cells'][3]['source'] = [
        "## 2. Configurer ngrok pour l'accès distant\n",
        "\n",
        "Nous utilisons ngrok pour créer un tunnel sécurisé afin d'accéder à l'interface Streamlit depuis votre navigateur.\n",
        "\n",
        "**Important** : Récupérez votre jeton (token) d'authentification sur le [tableau de bord ngrok](https://dashboard.ngrok.com/get-started/your-authtoken)."
    ]

    nb['cells'][4]['source'] = [
        "from pyngrok import ngrok\n",
        "import getpass\n",
        "\n",
        "# Demande le token de manière sécurisée\n",
        "print(\"Entrez votre token ngrok (collez-le ici) :\")\n",
        "authtoken = getpass.getpass()\n",
        "\n",
        "ngrok.kill()\n",
        "ngrok.set_auth_token(authtoken)"
    ]

    nb['cells'][5]['source'] = [
        "## 3. Lancer l'application et générer l'URL publique\n",
        "\n",
        "Démarrage du serveur et création du lien d'accès :"
    ]

    nb['cells'][6]['source'] = [
        "import subprocess\n",
        "import time\n",
        "\n",
        "print(\"🚀 Démarrage de Vidrush...\")\n",
        "streamlit_proc = subprocess.Popen([\n",
        "    \"streamlit\", \"run\", \"./webui/Main.py\", \"--server.port=8501\"\n",
        "])\n",
        "\n",
        "time.sleep(5)\n",
        "\n",
        "print(\"🌐 Création du tunnel ngrok...\")\n",
        "public_url = ngrok.connect(8501, bind_tls=True)\n",
        "\n",
        "print(\"\\n✅ Installation terminée !\")\n",
        "print(f\"Cliquez sur ce lien pour ouvrir l'interface : {public_url}\")"
    ]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)
    print("Notebook updated successfully")
else:
    print("Notebook not found")
