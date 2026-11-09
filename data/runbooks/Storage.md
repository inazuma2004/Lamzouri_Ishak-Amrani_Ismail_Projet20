# Runbook — Storage (Stockage)

## Symptômes couverts
- Disque dur plein (espace disque insuffisant)
- Quota de stockage dépassé (boîte mail, OneDrive, partage réseau)
- Sauvegarde échouée
- Disque réseau inaccessible ou lent
- Fichier ou dossier introuvable sur le partage

## Procédure de dépannage

1. **Identifier les fichiers volumineux** : utiliser l'Explorateur de fichiers ou un outil d'analyse d'espace disque pour localiser les dossiers occupant le plus d'espace (téléchargements, fichiers temporaires, vidéos).
2. **Vider les fichiers temporaires** : lancer Nettoyage de disque (Windows) ou vider le cache navigateur et les dossiers temp.
3. **Vider la corbeille** : s'assurer que la corbeille est vidée pour libérer l'espace.
4. **Déplacer les données personnelles** : inviter l'utilisateur à déplacer ses fichiers personnels vers un stockage cloud ou un disque externe.
5. **Vérifier le quota** : consulter le quota attribué sur le partage réseau ou le service cloud. Si dépassé, demander une augmentation ou archiver les anciennes données.
6. **Vérifier la sauvegarde** : confirmer que la dernière sauvegarde a réussi. Si échouée, relancer manuellement et vérifier l'espace de destination.
7. **Tester l'accès au disque réseau** : vérifier la connexion VPN/réseau, les mappages de lecteurs, et les autorisations NTFS.

## Escalade
Si le disque physique est défectueux ou si l'espace ne peut être libéré, ouvrir un ticket d'infrastructure pour ajout de stockage (délai : 2-5 jours ouvrés).

## Temps estimé
15 à 45 minutes.

**Source :** Runbook Storage — IT Helpdesk
