function formAnimation(){
    const arrows = document.querySelectorAll(".fa-arrow-right")
    
    arrows.forEach(arrow => {
        arrow.addEventListener('click',()=>{
            const input = arrow.previousElementSibling;
            const parent = arrow.parentElement;
            const nextForm = parent.nextElementSibling;

            // Validation
            if(input.type === "text" && validateUser(input)){
                nextSlide(parent,nextForm)
            }
            else if(input.type === "email" && validateEmail(input)){
                nextSlide(parent,nextForm)
            }
            else if(input.type === "password" && validateUser(input)){
                // nextSlide(parent,nextForm)
                document.getElementById("form_reg").submit()
            }
            else{
                parent.style.animation = "rotate 0.4s ease"
            }
            parent.addEventListener('animationend',()=>{
                parent.style.animation = ""
            })
        })
    });
}

function validateUser(user){
    if(user.value.length < 6){
        console.log("short length")
        error("rgb(189,87,87)");
    }
    else{
        error("rgb(96,170,96)");
        return true;
    }
}

function validateEmail(email){
    const validFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
    if(validFormat.test(email.value)){
        error("rgb(96,170,96)")
        return true;
    }
    else{
        error("rgb(189,87,87)")
    }
}

function nextSlide(parent,nextForm){
    parent.classList.add('innactive');
    parent.classList.remove('active');
    nextForm.classList.add('active');
}

function error(color){
    document.body.style.backgroundColor = color;
}

formAnimation()