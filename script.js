console.log("Script loaded!");

// Définition d'une classe pour gérer toutes les cases à cocher et les champs masqués associés dans le formulaire.
function initCustomCheckbox(id, hiddenFieldsMapping) {
    // Récupération de la case à cocher et du groupe
    var checkbox = $('#' + id);
    var group = checkbox.data('group');
  
    // Fonction de mise à jour des champs masqués
    function updateHiddenFields() {
      for (var val in hiddenFieldsMapping) {
        var hiddenFieldName = hiddenFieldsMapping[val];
        var hiddenField = $('[name="' + hiddenFieldName + '"]');
        if (val === checkbox.val()) {
          hiddenField.show();
        } else {
          hiddenField.hide();
        }
      }
    }
  
    // Mise à jour des champs masqués au chargement de la page
    updateHiddenFields();
  
   // Ajout d'un écouteur d'événement pour mettre à jour les champs masqués lorsqu'on coche ou décoche la case
    checkbox.on('change', function() {
      updateHiddenFields();
    });
  
    // Ajout d'un écouteur d'événement pour mettre à jour les champs masqués lorsque le formulaire est soumis
    checkbox.closest('form').on('submit', function() {
      updateHiddenFields();
    });
  }

$(document).ready(function () {
    // Alerte investigation toggle
    $('#alerte-investigation-toggle').on('click', function () {
        $('#alerte-investigation-content').toggle();
    });

        
});
