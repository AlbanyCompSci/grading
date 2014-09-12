// monitor for changes:
// http://dustinmartin.net/monitoring-a-form-for-changes-with-jquery/

var pageHasAce = typeof ace !== void 0;

var aceIdentifiersPopulated = function() {
  var deferred = $.Deferred();
  if (pageHasAce) {
    var check = setInterval(function() {
      var aceIdentifiers = $('.ace_identifier');
      if (aceIdentifiers.length > 0) {
        deferred.resolve();
        clearInterval(check);
      }
    }, 10);
  } else {
    deferred.resolve();
  }

  return deferred.promise();
}

var cleanSaveState = function() {
  $(':input').each(function(index, value) {
    var inputValue;
    if (pageHasAce) {
      inputValue = editors[index].getSession().getValue();
    } else {
      inputValue = $(this).val();
    }

    $(this).data('initialValue', inputValue);
  });
}

var allowSaveStateClear = aceIdentifiersPopulated();
allowSaveStateClear.then(cleanSaveState);

window.onbeforeunload = function() {
  var msg = 'You haven\'t saved your changes.';
  var isDirty = false;

  $(':input').each(function(index, value) {
    var inputValue;
    if (pageHasAce) {
      inputValue = editors[index].getSession().getValue();
    } else {
      inputValue = $(this).val();
    }

    if ($(this).data('initialValue') !== inputValue) {
      isDirty = true;
    }
  });

  if (isDirty === true) {
    return msg;
  }
};
