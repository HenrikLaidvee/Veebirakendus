function selectArvutused(shown, hidden) {
    const a = document.getElementById(shown);
    const b = document.getElementById(hidden);
    if (a && b) {
        a.style.display = 'block';
        toggleRequired(a, true);
        b.style.display = 'none';
        toggleRequired(b, false);
    }
}

function selectParameter(showId, hideId) {
    // need kaks muutuvad
    const show = document.getElementById(showId);
    const hide = document.getElementById(hideId);

    // kaugus jääb alati nähtavaks
    const distance = document.getElementById('tblKaugusArvuta');

    if (show && hide && distance) {
        show.style.display = 'flex';
        hide.style.display = 'none';
        toggleRequired(show, true);
        toggleRequired(hide, false);

        // tagab, et kaugus on nähtav
        distance.style.display = 'flex';
        toggleRequired(distance, true);
    }
}


function toggleRequired(element, isRequired) {
    const inputs = element.querySelectorAll('input');
    inputs.forEach(input => {
        if (isRequired) {
            input.setAttribute('required', 'required');
        } else {
            input.removeAttribute('required');
        }
    });
}