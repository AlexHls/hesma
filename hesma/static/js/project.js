/* Project specific Javascript goes here. */
function validateHydroForm(model_names) {
  let sim_name = document.forms['hydroDetails']['sim_name'].value;
  if (sim_name == '') {
    alert('Name must be filled out');
    return false;
  } else if (model_names.includes(sim_name.normalize())) {
    alert('Model name already exists');
    return false;
  }

  let url = document.forms['hydroDetails']['reference'].value;
  if (url == '') {
    return true;
  } else if (!isValidUrl(url)) {
    alert('Please enter a valid URL');
    return false;
  }
}

function isValidUrl(url) {
  try {
    new URL(url);
  } catch (_) {
    return false;
  }
  return true;
}
