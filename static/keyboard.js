window.addEventListener('keyup', (event) => {
    if (event.key === 's' 
        || event.key === 'w'
        || event.key === 'a'
        || event.key === 'd'){
        let key = event.key
        fetch(`/keyboard_control/${key}`)
            .then(function (response) {
                return response.text();
            }).then(function (text) {
                console.log('GET response text:');
                console.log(text); 
            });
    }
})