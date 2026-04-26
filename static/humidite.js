// --- Temperature Gauge ---
const tempSketch = (p) => {
    let parentDiv;

    p.setup = () => {
        parentDiv = p.select('#gauge-temp');
        // Create canvas based on current parent width
        let canvasWidth = parentDiv.width; 
        let cnv = p.createCanvas(canvasWidth, canvasWidth); // Square canvas
        cnv.parent("gauge-temp");
        p.noStroke();
    };

    p.windowResized = () => {
        let canvasWidth = parentDiv.width;
        p.resizeCanvas(canvasWidth, canvasWidth);
    };

    p.draw = () => {
        fetch('/temp').then(r => r.text()).then(data => {
            let val = parseFloat(data) || 0;
            console.log("Température : "+val);

            document.getElementById("temp").innerText = "Température : " + val + "°C";
            
            p.clear();
            
            // Dynamics: use p.width and p.height instead of 300/150
            let cx = p.width / 2;
            let cy = p.height / 2;
            let outerDiam = p.width * 0.8; // Gauge takes 80% of width
            let innerDiam = p.width * 0.5; // Hole takes 50% of width

            p.fill(p.map(val, -10, 140, 0, 255), p.map(val, -10, 140, 255, 0), 0);
            p.arc(cx, cy, outerDiam, outerDiam, 0, p.map(val, -10, 140, 0, p.TWO_PI));
            
            p.fill(255); 
            p.ellipse(cx, cy, innerDiam, innerDiam);
        });
        p.frameRate(5);
    };
};
new p5(tempSketch);

// --- Temperature Gauge ---
const humdsketch = (p) => {
    let parentDiv;

    p.setup = () => {
        parentDiv = p.select('#gauge-humidite');
        // Create canvas based on current parent width
        let canvasWidth = parentDiv.width; 
        let cnv = p.createCanvas(canvasWidth, canvasWidth); // Square canvas
        cnv.parent("gauge-humidite");
        p.noStroke();
    };

    p.windowResized = () => {
        let canvasWidth = parentDiv.width;
        p.resizeCanvas(canvasWidth, canvasWidth);
    };

    p.draw = () => {
        fetch('/humidite').then(r => r.text()).then(data => {
            let val = parseFloat(data) || 0;
            console.log("Humidité : "+val);
            document.getElementById("humidite").innerText = "Humidité : " + val + "%";
            
            p.clear();
            
            // Dynamics: use p.width and p.height instead of 300/150
            let cx = p.width / 2;
            let cy = p.height / 2;
            let outerDiam = p.width * 0.8; // Gauge takes 80% of width
            let innerDiam = p.width * 0.5; // Hole takes 50% of width

            p.fill(p.map(val, -10, 140, 0, 255), p.map(val, -10, 140, 255, 0), 0);
            p.arc(cx, cy, outerDiam, outerDiam, 0, p.map(val, -10, 140, 0, p.TWO_PI));
            
            p.fill(255); 
            p.ellipse(cx, cy, innerDiam, innerDiam);
        });
        p.frameRate(5);
    };
};
new p5(humdsketch);

