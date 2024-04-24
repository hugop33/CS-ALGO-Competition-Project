
# Instructions

## AVANT DE COMMENCER

Suivez les instructions suivantes :

1. Créez un compte sur Codalab. Ce compte doit être créer en utilisant **IMPERATIVEMENT** votre adresse mail de l’école. Les soumissions effectuées avec une adresse mail différente de votre adresse mail d’élève de CentraleSupélec **SERONT INVALIDÉES** !!!
2. Connectez-vous sur la page de la compétition et allez dans l’onglet Participate pour valider les conditions d’utilisations.
3. Téléchargez le fichier zip Starter Kit sur la page de participation. C’est une soumission vierge. Une fois décompressé, le zip donne un répertoire avec le squelette de code et un fichier README avec des instructions complémentaires. Le fichier README est un fichier texte que vous pouvez ouvrir avec votre IDE préférée pour coder en python.
4. Téléchargez le fichier zip Public Data sur la page de participation. Une fois décompressé, ce zip donne un répertoire qui contient des instances de test pour travailler.
5. Complétez le squelette de code, testez votre programme. Une commande pour le test est indiqué dans le fichier README. Une fois satisfait, zipper le répertoire de soumission.
6. Uploader sur la page de participation votre fichier zip de soumission.
7. Attendez quelque peu que votre code soit exécuté et intégré aux résultats.
8. Sur la page de participation, vous pourrez télécharger le résultat de l’exécution de votre programme ainsi que le score associé.

Le tournois est organisé en deux rounds :

### ROUND 1 - le problème du dominant

L’objectif est résoudre, aussi bien que possible, des instances du problème, en un temps limité. Dans cette variante du dominant, il ne s'agit pas de trouver un unique dominant mais deux dominants D1 et D2, le plus petits possibles et partageant le moins de sommets.

Pour le premier concours, nous travaillons sur 13 instances de taille 50, 250, 500 et 1000 noeuds. Le temps maximum d’exécution est 20 secondes au total.

Chaque instance vous rapporte un certain nombre de points suivant les dominants que vos algorithmes trouverons. Le poids d'une solution est données par la formule suivante où V est l'ensemble des sommets : (|D1|+|D2|+|D1 inter D2|)/|V|.
Le score de votre soumission est la somme des scores de chaque instance.
Le classement est établi à partir de ce score. La durée d'exécution est utilisé pour départager les égalités.

[Lien vers le premier concours : codalab](url_du_concours)

**Remarques :**

Dans un premier temps, vous pourrez télécharger sur Codalab.org, un squelette de code et un jeu d’instances. Vous pourrez ainsi travailler localement sur un algorithme et le tester.

Une fois satisfait, vous pourrez soumettre sur codalab votre programme. Il sera exécuté par le site qui analysera vos résultats et, si vous produisez une solution valide en un temps raisonnable, votre résultat sera intégré dans le classement général. Vous pouvez faire jusqu’à 100 soumissions.

Le 24 octobre 2023 à 10:57 a.m UTC, le concours passera dans la phase finale. Les résultats des instances de test seront écartées. Un nouveau jeu d’instances, qui resteront secrètes jusqu’à la fin, sera utilisé pour les résultats finaux. Ces instances sont générées de manière identique aux premières instances (même taille, même paramètrage).

Dans codalab, les warnings sont ignorés. Si vous en observez dans les logs, ce n'est pas grave. Évidement, les erreurs restent problématiques...

Nous utilisons networkx pour la représentation des graphes. Cela permet en particulier, d'obtenir facilement des itérables sur les noeuds (g.nodes) ou sur les poids des noeuds ( nx.get_node_attributes(g, 'weight') ). Également accessible, le voisinage d'un noeud ( g.neighbors(v) ).

### ROUND 2 - Slow-Fast Scheduling

L’énoncé du deuxième round est dans le pdf énoncé n°2.

Le classement sera établi en fonction du coût moyen calculé sur les instances d’un jeu de données.

La manière de procéder est la même que dans le cas du concours du premier bloc : le moule en python et un jeu d’instances d’entraînement sont fournis sur codalab, le lien pour cette épreuve est [ici](url_vers_le_concours).

La phase finale se joue la veille de la session de retour d’expérience planifié le mardi 7 novembre 2023 à 13h30 – le classement sera réalisé selon les résultats de vos algorithmes sur des instances dévoilées « à la dernière minute ».
