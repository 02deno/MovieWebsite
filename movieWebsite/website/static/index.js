
function deleteFilm(filmId) {
    fetch('/delete-film', {
        method: 'POST',
        body: JSON.stringify({filmId : filmId}),
    }).then((_res) => {
        window.location.href = "/"
    });
} 