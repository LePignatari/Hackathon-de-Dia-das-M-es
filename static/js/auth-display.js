const radios = document.querySelectorAll(
    'input[name="user_type"]'
)

const family_code_container = document.getElementById(
    'family-code-container'    
)

const familyInput = document.getElementById(
    'fam_code'
)

radios.forEach(radio => {
    radio.addEventListener(
        'change',
        function () {
            if (this.value === 'filho') {
                family_code_container.style.display = 'block'
                familyInput.setAttribute('required', 'required')
            }
            else {
                family_code_container.style.display = 'none'
                familyInput.removeAttribute('required')
            }
        }
    )
})