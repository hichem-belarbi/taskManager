par hichem belarbi 

--introduction 
ceci est un projet que j'ai fait aucours de mon appritissage du developpement des application du bureau 
et pour cela il est pas structuré et optimisé comme il faut mais quand meme je voulais partager avec vous 
parcontre il est fonctionnel mais il faut pas le surcharger
je le trouve tres joli en considerant le fait qu'il est fait par un debutant 




--description 
ce projet est une application de desktop pour gerer ses tache (specialement les etudiant)
1)elle permet de creer des tache :
    -creation d'une tache (titre , date , importance , description ...)
    -la supprimmer 
    -la marquer faite 
    -rechercher une tache parmi les taches
    -visulaser l'historique des taches
    -...
2) elle permet de gerer ses depensations
    -enregister les depensation du jours 
    -claculer le total de depenstion entre deux date en depuis un nombre de jours 
    -visulation les depenstion 
    -faire des recherche dans l'historique 
    -...
3)elle permet de faire des calcule 
    -avec une calculatrice simple classique 
    -creer ses propre formule (moyenne , rang ,etc.. )
    -faire de calcule guidé par les formule créés 
    -eregistrer les resulta 
    -...


--des info technique 
**language de programmation :
    le language utilisé dans ce projet est python en combinason avec les bibliotheque PyQt5 (interfaces) et matplotlib (graphe)
**la bibliotheque myAnimation :
    est une bibliotheque que j'ai crée pour faire des animation que j'ai utiliser dans ce projet 
    vous pouvez les etulisez et y apporter librement des modifications 
**les interfaces graphique : (extension .ui)
    ce sont des interface graphique creer avec le logiciel Qtdesigner qui est un logiciel de creation de fentre graphique 
    avec Qt avec la technique DRAG&DROP .
**enregistrement des données :
    -les information sont enregistrer dans des fichier texte sous forme de ligne formaté (exmp: titre_date_desription)
    -pas la mailleur solution mais c'etait pas le but de ce projet '


---plus d'info :
    pour voir des captures des interface vous pouvez consulter le dossier "pics"



### les points fort :
    -mettre en evidance comment integrer des interface creer par qtdesigner dans un script python 
    -mettre en evidance la lecture et l'ecriture dans des fichiers texte 
    -mettre en evidance l'utilisation de la bibliotheque matplotlib 
    -mettre en evidance l'utilisation de la bibliothque PyQt5
    -ajouter des animations 
    -une interface relativement atrayyante 
    -interface intuitive

### les point faible :
    -non repartition du code en des fichiers (code dans un seul fichier)
    -base de donnée sous forme de fichier texte 
    -code non optimisé et relativement lourd (au dela de 1000 taches ca commance a devenir lourd)



/// ce code est ouvert à tout le monde à but d'apprendre  , utilisation ou modification 