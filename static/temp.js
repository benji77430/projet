function setup() {
    let canvas=createCanvas(900, 400);
    canvas.parent("gauge-temp");
    noStroke();
    clear();
}

function myTimer() {
  return;
} 
function draw() {
    clear();
    let temp;
    let temp_element = document.getElementById("temp");

    let xmlHttp_temp = new XMLHttpRequest();
    xmlHttp_temp.open( "GET", "/temp", false ); // false for synchronous request
    xmlHttp_temp.send( null );
    temp= xmlHttp_temp.responseText;
    console.log(temp);

    temp_element.innerText="Température : "+temp+"°C";

    fill(10,10,255);
    
    // Default fill mode.
    arc(450, 200, 200, 200, 0, map(temp,-10,140,0,2*PI));
    fill(255,255,255);
    arc(450, 200, 100, 100, 0, 2*PI);
    setTimeout(myTimer, 1000);

}   