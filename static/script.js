const headline = document.getElementById("headline");
const btn = document.getElementById("btn");
function sayHello(){
    if(headline.textContent === "Hello from Flask!")
        headline.textContent = "Hello from javascript!";
    else
        headline.textContent = "Hello from Flask!";
}
btn.addEventListener("click", sayHello);

export {sayHello};