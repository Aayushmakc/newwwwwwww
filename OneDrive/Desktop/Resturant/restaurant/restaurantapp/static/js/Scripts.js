const input = document.querySelector("#phone");
const world = window.intlTelInput(input, {
  initialCountry: "us",
  strictMode: true,
  loadUtils: () => import("https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/25.2.1/build/js/utils.js") // for formatting/placeholders etc
});


document.getElementById('contactForm').addEventListener('submit',function(e)
{
  if(world.isValidNumber()){
       input.value = world.getNumber(); //fully country code data
       
  }
  else{
    e.preventDefault();
    alert("Invalid phone number. Please enter a valid number.");
  }
})