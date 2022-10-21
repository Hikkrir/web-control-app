window.addEventListener('keyup', (event) => {
    if (event.key === 's' 
        || event.key === 'w'
        || event.key === 'a'
        || event.key === 'd'){
        let key = event.key
        fetch(`/keyboard_control/${key}`)
    }
})