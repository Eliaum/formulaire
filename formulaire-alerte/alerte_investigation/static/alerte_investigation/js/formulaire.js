// Affiche le champ « précision sur la source » uniquement lorsque la source « Autre » est cochée.
(function () {
    "use strict";

    const formulaire = document.getElementById("formulaire-alerte");
    const bloc = document.getElementById("bloc-precision-source");
    if (!formulaire || !bloc) {
        return;
    }

    const champ = bloc.querySelector("input, textarea");
    const choix = formulaire.querySelectorAll('input[name="source_alerte"]');

    function mettreAJour() {
        const autre = formulaire.querySelector('input[name="source_alerte"][value="autre"]');
        const visible = Boolean(autre && autre.checked);
        bloc.hidden = !visible;
        if (champ) {
            champ.required = visible;
        }
    }

    choix.forEach(function (bouton) {
        bouton.addEventListener("change", mettreAJour);
    });
    mettreAJour();
})();
