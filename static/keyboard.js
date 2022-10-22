let angle = 110
let speed = 0

window.addEventListener('keydown', (event) => {
    if (event.repeat !== true){
        switch(event.key){
            case "a":
                angle = 75
                break;
            case "d":
                angle = 160
                break;
        }
        fetch(`/keyboard_control_angle/${angle}`)
    }
})
window.addEventListener('keydown', (event) => {
    if (event.repeat !== true){
        switch(event.key){
            case "s":
                speed = -99
                break;
            case "w":
                speed = 99
                break;
        }
        fetch(`/keyboard_control_speed/${speed}`)
    }
})

window.addEventListener('keyup', (event) => {
    if (event.repeat !== true){
        switch(event.key){
            case "s":
                speed = 0
                break;
            case "w":
                speed = 0
                break;
            }
            fetch(`/keyboard_control_speed/${speed}`)
    }
})
window.addEventListener('keyup', (event) => {
    if (event.repeat !== true){
        switch(event.key){
            case "a":
                angle = 110
                break;
            case "d":
                angle = 110
                break;
            }
            fetch(`/keyboard_control_angle/${angle}`)
    }
})