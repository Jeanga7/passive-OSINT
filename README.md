# 🔍 Passive Reconnaissance Tool

## 📌 Introduction
L'information est la clé de toute attaque ou défense en cybersécurité. L'un des premiers pas d'un pentest consiste à recueillir un maximum de renseignements sur une cible. Ce processus est connu sous le nom de **reconnaissance passive**.

Le but de cet outil est de vous aider à effectuer une collecte d'informations en utilisant des techniques OSINT (*Open Source Intelligence*). Il vous permettra d'effectuer des recherches sur :

- 📌 **Nom complet** : Recherche de l'adresse et du numéro de téléphone dans les annuaires publics.
- 🌍 **Adresse IP** : Identification de l'ISP et de la localisation approximative.
- 🕵️‍♂️ **Nom d'utilisateur** : Vérification de la présence d'un compte sur plusieurs réseaux sociaux.

⚠️ **Cet outil est à des fins éducatives uniquement. Toute utilisation abusive est sous votre propre responsabilité.**

---

## 🚀 Installation et utilisation

### 📥 Prérequis
- Python 3.x
- Bibliothèques requises : `requests`, `fake_useragent`

Installez les dépendances avec :
```bash
pip install -r requirements.txt
```

### 🎯 Commandes disponibles
Affichez l'aide avec :
```bash
passive --help
```

| Option | Description |
|--------|-------------|
| `-fn`  | Recherche par **nom complet** |
| `-ip`  | Recherche par **adresse IP** |
| `-u`   | Recherche par **nom d'utilisateur** |

### 📌 Exemples d'utilisation

#### 🔎 Recherche d'un nom complet
```bash
passive -fn "Jean Dupont"
```
📌 Résultat :
```
First name: Jean
Last name: Dupont
Address: 7 rue du Progrès
75016 Paris
Number: +33601010101
Saved in result.txt
```

#### 🌍 Recherche d'une adresse IP
```bash
passive -ip 127.0.0.1
```
📌 Résultat :
```
ISP: FSociety, S.A.
City Lat/Lon: (13.731) / (-1.1373)
Saved in result2.txt
```

#### 🕵️‍♂️ Recherche d'un nom d'utilisateur
```bash
passive -u "@user01"
```
📌 Résultat :
```
Facebook : yes
Twitter : yes
Linkedin : yes
Instagram : no
Skype : yes
Saved in result3.txt
```

---

## 🛠️ Fonctionnalités et principes clés

### 🔍 **Reconnaissance passive vs active**
- **Passive Reconnaissance** : Aucune interaction directe avec la cible. L'outil utilise uniquement des sources publiques.
- **Active Reconnaissance** : Interaction avec la cible (ex : scan de ports, requêtes directes).

### 📡 **OSINT (Open Source Intelligence)**
L'OSINT regroupe l'ensemble des techniques permettant de collecter des informations accessibles publiquement, comme :
- Annuaires en ligne 📚
- Réseaux sociaux 📲
- Bases de données publiques 🗃️
- Whois & DNS 📌

### 🔐 **Éthique et responsabilité**
Cet outil est destiné **uniquement** à des fins éducatives et légales. L'utilisation de ces techniques sans autorisation peut enfreindre la loi.

---

## 🏆 Bonus & Améliorations
🔹 Ajout de **nouvelles API** pour plus de données 📊  
🔹 Interface web pour une utilisation simplifiée 🎨  
🔹 Système de **proxy** pour éviter d'être détecté 🛡️  

---

## 📜 Licence
Ce projet est sous licence [**AGPL**](/LICENSE). Utilisation libre mais **responsable**.

### WARNING 

⚠️ Ces méthodes et outils sont uniquement destinés à des fins éducatives, afin que vous puissiez mieux comprendre comment vous protéger contre des vulnérabilités similaires. Vous devez vous assurer que vous ne tentez aucune activité de type exploit sans l'autorisation explicite du propriétaire de la machine, du système ou de l'application. Si vous n'obtenez pas cette autorisation, vous risquez d'enfreindre la loi.
---

## 💡 Ressources utiles
- 🔗 [Liste d'outils OSINT](https://en.kali.tools/all/?category=recon)
- 📖 [OSINT sur Wikipedia](https://en.wikipedia.org/wiki/Open-source_intelligence)
- 📚 [Apprendre l'OSINT](https://github.com/topics/osint-tools)

---

🚀 **Happy Hacking & Stay Ethical!** 👨‍💻🔥

