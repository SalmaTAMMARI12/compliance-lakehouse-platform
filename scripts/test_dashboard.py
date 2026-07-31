import urllib.request, re

r = urllib.request.urlopen("http://127.0.0.1:5000/")
body = r.read().decode("utf-8")
print("Status: 200 OK")
print("Taille HTML:", len(body), "caracteres")

checks = ["Constat", "chapitre", "conformit", "IIV", "DGSSI", "N/A", "ecart", "POL-", "ACC-", "ORG-", "Organisationnel"]
for mot in checks:
    count = body.lower().count(mot.lower())
    tag = "OK" if count > 0 else "MANQUE"
    print(f"  [{tag}] '{mot}' x{count}")
