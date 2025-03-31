# tp_secure_chat
TP Unsecure Chat

1) Que pensez-vous de la confidentialité des données vis-à-vis du serveur ?
La confidentialité des données dépend de la manière dont elles sont stockées, puis transmises? Même si elles sont chiffrées le serveur a accès aux clef de déchiffrement. Le chiffrement est donc bien pour empecher le serveur d'acceder aux données, en clair.

2) Pouvez-vous expliquer en quoi la sérialisation pickle est certainement le plus mauvais choix ?

En faisant ça, c'est une porte ouverte aux attaque malveillante : un attaquant peut envoter un objet pickel conçu pour executer du code malveillant sur le serveur....

3)  Quels types de sérialisation pourrait-on utiliser pour éviter cela ? (hors CVE)
  
Selon une liste (trouver sur une site) 
 - JSON : Il ne permet pas l'execution  du dit code (question 2) )
 - MessagePack, similaire à JSON
 - Protocol Buffers developpé par google, c'est americain mais efficace

4) Pourquoi le chiffrement seul est-il insuffisant ?
   
Le chiffrement protege les data contre l'interception mais pas contre les attaques : si l'attaquant a la clé de chiffremenbt, il peut avoir nos données. Il faut donc en paralelle ajouter une intégrité des données via un MAC par exemple

5) Quelle fonction(s) en Python permet de générer un salt avec une qualité cryptographique ?
   
On peut utiliser os.urandom() ou secrets.token_bytes() pour générer un salt sécurisé :

import os  
salt = os.urandom(16)  # 16 octets = 128 bits

import secrets  
salt = secrets.token_bytes(16)

6) Faudra-t-il transmettre le salt comme champ en clair supplémentaire du paquet message ?

Oui, le salt doit être envoyé en clair car il n'a pas besoin d'être "secret". SOn role est d'empecher les attaque (comme des "rainbow tables"). <cependant, il doit rester unique. 

7)  Que peut faire le serveur s'il est malveillant sur les messages ?

Si le serveur est malveillant, on peut lire et modifier les messages s'ils ne sont pas signé/protéger ou encore stocker les données sensible afin de les utiliser plus tard à bon escient.

8) Que faudrait-il faire en théorie pour éviter l’action du rogue server ?
   Comme énoncé precedemment : on peut remplacer le pickle (pas safe) pâr un JSON ou MessagePack, ou alors ajouter une signature pour proteger les data (ou un HMAC pour garantir l'intégrité du message)

9) Pourquoi Fernet n’est pas adapté dans ce cadre ?

 Il n'est pas efficace car il ne protege pas contre un serveur malveilklant : il chiffre les donnée, mais le serveur peut toujours mofidier les message si il n'y a pas d'intégrité dessus (via HMAC par exemple)

Il y a certaines questions auquels je n'ai aps répondues : je n'ai pas trouvé de réponse intéressante ou je que je comprenais, je m'en excuse.
