# Runbook — Administrative rights (Droits administratifs)

## Symptômes couverts
- Demande d'élévation de privilèges (administrateur local)
- Impossible d'installer un logiciel (droits insuffisants)
- Demande d'accès au Panneau de configuration ou au Registre
- Demande de modification de configuration système
- Logiciel bloqué par les stratégies de groupe (GPO)

## Procédure de dépannage

1. **Évaluer le besoin** : confirmer avec l'utilisateur pourquoi les droits administratifs sont nécessaires (installation d'un logiciel approuvé, configuration spécifique).
2. **Vérifier la politique de sécurité** : s'assurer que la demande respecte la politique de sécurité de l'entreprise (principe du moindre privilège).
3. **Installation temporaire** : pour un logiciel approuvé, l'équipe informatique peut effectuer l'installation avec un compte administrateur sans donner les droits permanents à l'utilisateur.
4. **Élévation temporaire** : si l'utilisateur doit vraiment avoir les droits, accorder des droits administratifs locaux pour une durée limitée (ex: 24h) avec journalisation.
5. **Modifier les stratégies de groupe** : si un logiciel est bloqué par une GPO, demander une exception au service sécurité après analyse des risques.
6. **Documenter** : enregistrer l'octroi des droits, la durée, le motif, et la personne qui a validé.

## Escalade
Toute demande de droits administratifs permanents doit être validée par le responsable de la sécurité des systèmes d'information et le manager de l'utilisateur (délai : 24-48h).

## Temps estimé
15 à 60 minutes selon la procédure de validation.

**Source :** Runbook Administrative rights — IT Helpdesk
