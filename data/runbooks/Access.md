# Runbook — Access (Accès & Authentification)

## Symptômes couverts
- Impossible de se connecter au VPN
- Mot de passe expiré ou oublié
- Compte verrouillé après plusieurs tentatives échouées
- Impossible d'accéder à une application ou un partage réseau
- Erreur d'authentification SSO / Active Directory

## Procédure de dépannage

1. **Vérifier le verrouillage du compte** : dans Active Directory, vérifier si le compte utilisateur est verrouillé. Si oui, déverrouiller et réinitialiser le mot de passe.
2. **Réinitialiser le mot de passe** : envoyer un lien de réinitialisation ou définir un mot de passe temporaire conformément à la politique de sécurité.
3. **Vérifier la connexion VPN** : s'assurer que le client VPN est installé et à jour. Vérifier les certificats et la configuration du serveur.
4. **Tester depuis un autre réseau** : essayer la connexion depuis un réseau différent pour exclure un blocage réseau local.
5. **Vérifier les autorisations** : confirmer que l'utilisateur dispose des droits d'accès sur la ressource demandée (partage réseau, application).
6. **Vider le cache d'authentification** : déconnecter/reconnecter l'utilisateur, vider les identifiants mis en cache (Gestionnaire d'identifiants Windows).

## Escalade
Si le compte reste verrouillé ou si l'accès VPN ne peut être rétabli, transférer à l'équipe sécurité/identité (délai : 4h ouvrées).

## Temps estimé
10 à 30 minutes.

**Source :** Runbook Access — IT Helpdesk
