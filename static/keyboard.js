let angle = 110
let speed = 0

window.addEventListener('keydown', (event) => {
    if (event.repeat === false){
        switch(event.key){
            case "a":
                angle = 75
                fetch(`/keyboard_control_angle/${angle}`)
                break;
            case "d":
                angle = 160
                fetch(`/keyboard_control_angle/${angle}`)
                break;
        }
    }
})
window.addEventListener('keydown', (event) => {
    if (event.repeat === false){
        switch(event.key){
            case "s":
                speed = -99
                fetch(`/keyboard_control_speed/${speed}`)
                break;
            case "w":
                speed = 99
                fetch(`/keyboard_control_speed/${speed}`)
                break;
        }
    }
})

window.addEventListener('keyup', (event) => {
    if (event.repeat === false){
        switch(event.key){
            case "s":
                speed = 0
                fetch(`/keyboard_control_speed/${speed}`)
                break;
            case "w":
                speed = 0
                fetch(`/keyboard_control_speed/${speed}`)
                break;
            }
    }
})
window.addEventListener('keyup', (event) => {
    if (event.repeat === false){
        switch(event.key){
            case "a":
                angle = 110
                fetch(`/keyboard_control_angle/${angle}`)
                break;
            case "d":
                angle = 110
                fetch(`/keyboard_control_angle/${angle}`)
                break;
            }
    }
})