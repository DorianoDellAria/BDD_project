Lancement du programme :
    placez la base de données dans le dossier "misc"
    placez-vous dans le dossier code et lancez : python3 Main.py <nom de la database>

commande :
    -help : affiche toutes les commandes disponibles

    -exit ou EOF : quitte le programme en fermant la database

    -addfd [nomDeLaTable lhs1 lhs2 lhs3 rhs] : si addfd est tapez sans arguments, vous rentrerez dans un menu de création de DF.
    vous pouvez également donner en argument le nom de la table suivi des noms de colonnes de la DF. Le dernier élément tapez sera ce qui est à
    droite de la flèche

    -tables : affiche les relations de la database

    -columm <table> : affiche les colonnes d'une table

    -fd [<table>] : affiche les DF, il est possible d'ajouter un filtre en spécifiant l'argument <table>

    -rmfd [<#DF>] : rmfd sans arguments vous proposera de tapez un entier correspondant à la DF que vous voulez supprimer
    il est possible de la supprimer directement en spéifiant l'argument <#DF> qui correspond au numéro de la DF

    -check : affiche toutes les DF suivi de True ou False si la DF est respectée ou non

    -closure <atr1> [<atr2> ...] : affiche la fermeture transitive d'un ou plusieurs attirbuts

    -cons <table> : affiche les dépendances fonctionelles d'une table qui sont une conséquence d'autres DF

    -key <table> : affiche les clé d'une table

    -bcnf <table> : vérifie qu'une table soit en bcnf

    -3nf <table> : vérifie qu'une table soit en 3nf

    -decompose <table> [<database_name>] : exporte une décomposition si la table n'est pas en 3nf. Par défaut la database s'appelle "décomposition.db",
    mais vous êtes libre de changer le nom en spécifiant le paramètre database_name. Attention si la database donnée en argument existe déjà, elle est écrasée. 