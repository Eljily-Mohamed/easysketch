# Documentation sur notre application

Dans cette section, nous allons expliquer les éléments de l'interface graphique (IHM) qui peuvent ne pas être immédiatement évidents ou intuitifs pour les utilisateurs, afin de rendre l'expérience plus fluide.

### 1. **Tracé de polygone**

Le tracé de polygones peut être un peu complexe pour un utilisateur novice. Voici une explication détaillée :

- **Placement des points** : Pour dessiner un polygone, l'utilisateur doit cliquer à plusieurs endroits sur la zone de dessin pour placer les points du polygone.
- **Fermeture du polygone** : Une fois tous les points placés, l'utilisateur doit **double-cliquer** sur le dernier point ou sur le premier point qu'il a tracé pour fermer le polygone et afficher l'objet graphique complet.

### 2. **Sélection d'une couleur avec le dialogue de sélection de couleur**

Lors de la sélection d'une couleur (que ce soit pour le stylo ou le pinceau), un dialogue de couleur s'ouvre. Si un utilisateur n'a jamais utilisé ce type de dialogue auparavant, voici comment l'utiliser :

- **Choix de la couleur** : L'utilisateur peut choisir une couleur parmi les couleurs standards ou entrer une couleur personnalisée en utilisant le format HEX ou RGB.
- **Utilisation du bouton OK** : Après avoir sélectionné la couleur souhaitée, l'utilisateur doit appuyer sur le bouton OK pour appliquer la couleur à l'élément graphique en cours de modification.

### 3. **Utilisation de la fonctionnalité de "Undo/Redo" (Annuler/Rétablir)**

La fonctionnalité d'annulation et de rétablissement des actions est très utile mais peut être confuse si l'utilisateur ne comprend pas comment elle fonctionne :

- **Annuler une action** : En appuyant sur `Ctrl+Z`, l'utilisateur peut annuler la dernière action effectuée (par exemple, supprimer un élément ou modifier sa couleur).
- **Rétablir une action** : En appuyant sur `Ctrl+Y`, l'utilisateur peut rétablir une action précédemment annulée.

## Problèmes éventuels rencontrés lors du développement

Cette section décrit certains des défis techniques et des problèmes rencontrés pendant le développement, ainsi que des solutions apportées.

### 1. **Problèmes avec l'historique d'actions (Undo/Redo)**

L'une des principales difficultés a été la gestion de l'historique des actions de dessin pour permettre une fonctionnalité d'Undo/Redo fluide. En effet, lorsque plusieurs objets sont dessinés en même temps, ou qu'un utilisateur effectue plusieurs actions de suite, il devient difficile de garder une trace de toutes les actions effectuées et d'assurer une synchronisation correcte entre les objets graphiques.

**Solution** :

- Nous avons utilisé une structure de données basée sur une **pile** pour enregistrer les actions de l'utilisateur et permettre une gestion efficace de l'annulation et du rétablissement des actions.
- Chaque action (comme le tracé d'une ligne, d'un rectangle, etc.) est enregistrée dans la pile, et lorsque l'utilisateur annule une action, l'état précédent de l'objet est restauré.

### 2. **Problèmes avec le texte (édition et déplacement)**

Lors de l'implémentation de la gestion du texte, plusieurs défis ont été rencontrés, notamment en ce qui concerne l'édition et le déplacement du texte. Par exemple, certains textes étaient difficiles à sélectionner, et leur déplacement entraînait souvent des comportements inattendus, tels qu'une perte d'alignement ou des modifications accidentelles de leur contenu.

**Solution** :

- Nous avons introduit une zone de texte dédiée qui permet une sélection claire et une modification facile des contenus textuels, même lorsqu'ils sont superposés à d'autres éléments graphiques.
- Pour le déplacement, une logique spécifique a été ajoutée pour verrouiller la position initiale du texte pendant le déplacement afin d'éviter des décalages accidentels. Cette logique repose sur un système de coordonnées fixes qui maintient la relation entre le texte et les autres éléments graphiques adjacents.

### 3. **Manque de retour visuel pendant le dessin**

Lors du dessin d'une forme ou de la sélection d'une zone, les utilisateurs ne pouvaient pas visualiser en temps réel ce qu'ils étaient en train de créer. Cela pouvait entraîner des erreurs ou des ajustements imprécis une fois la souris relâchée.

**Solution** :

- Nous avons ajouté une **bande élastique (rubber band)**, représentée par un rectangle temporaire en pointillé. Cette bande suit les mouvements de la souris pendant le dessin ou la sélection, permettant à l'utilisateur de visualiser dynamiquement la forme ou la zone avant de finaliser l'action. Une fois le clic relâché, la bande devient invisible pour ne pas encombrer l'interface.

## Ce README apparaîtra également dans le menu d'aide de l'application (About the Application)

Lorsque l'utilisateur sélectionne "À propos de l'application" dans le menu d'aide, ce fichier README sera affiché, donnant à l'utilisateur des informations détaillées sur le fonctionnement de l'application, les fonctionnalités disponibles, ainsi que des conseils utiles pour résoudre certains problèmes fréquents.

L'idée est de fournir une aide complète et détaillée, accessible directement depuis l'application, afin que l'utilisateur n'ait pas besoin de rechercher des informations ailleurs. Cela améliore l'expérience utilisateur et permet de résoudre rapidement les questions qui pourraient se poser au cours de l'utilisation de l'application.

---

## Conclusion

Ce fichier README vise à offrir une aide complète à l'utilisateur de l'application, qu'il soit débutant ou plus expérimenté. En expliquant les fonctionnalités, les problèmes rencontrés et les solutions mises en place, nous espérons rendre l'application plus accessible et éviter des frustrations inutiles. Si vous rencontrez des problèmes ou avez des suggestions pour améliorer l'application, n'hésitez pas à nous contacter via la page de support.
