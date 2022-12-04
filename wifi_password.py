#                               by Le_Marou

# subprocess permet d'utiliser les commandes du systeme
import subprocess
import io

# import re permet d'utiliser les expression reguliere
import re

liste_wifi = list()

cmd_sortie = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode("cp852")
nom_profiles = re.findall(": (.*)\r", cmd_sortie)
if len(nom_profiles) != 0:
    for nom in nom_profiles:
        wifi_profile = {}
        wifi_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", nom], capture_output=True).stdout.decode("cp852")
        if re.search("Clé de sécurité        : Absent", wifi_info):
            continue
        else:
            wifi_profile["ssid"] = nom
            wifi_info_bypass = subprocess.run(
                ["netsh", "wlan", "show", "profile", nom, "key=clear"], capture_output=True).stdout.decode("cp852")
            mode_passe = re.search(
                "Contenu de la clé            : (.*)\r", wifi_info_bypass)
            if mode_passe == None:
                wifi_profile["Mode Passe"] = None
            else:
                wifi_profile["Mode Passe"] = mode_passe[1]
            liste_wifi.append(wifi_profile)

for x in range(len(liste_wifi)):
    print(liste_wifi
          [x])
