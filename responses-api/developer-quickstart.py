from openai import OpenAI  # Importiert den offiziellen OpenAI-Python-Client
from dotenv import load_dotenv  # Importiert die Funktion zum Laden von Umgebungsvariablen aus einer .env-Datei

load_dotenv()  # Lädt die Umgebungsvariablen aus der .env-Datei

# Erstellt einen Client, der automatisch API-Key und Einstellungen aus der Umgebung liest
client = OpenAI()

# Stellt dem Modell "gpt-5" eine Frage und erzeugt eine neue Antwort
response = client.responses.create(
    model="gpt-5-nano",
    input="Was ist ein KI-Agent."
)

# Gibt nur den Textanteil der Modellantwort auf der Konsole aus
print(response.output_text)
