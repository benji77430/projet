// --- Temperature Gauge ---
const tempSketch = (p) => {
    p.setup = () => {
        // Create a canvas that fits your white box
        let cnv = p.createCanvas(300, 300); 
        cnv.parent("gauge-temp");
        p.noStroke();
    };

    p.draw = () => {
        fetch('/temp').then(r => r.text()).then(data => {
            let val = parseFloat(data) || 0;
            document.getElementById("temp").innerText = "Température : " + val + "°C";
            p.clear();
            p.fill(p.map(val,-10,140,0,255), p.map(val,-10,140,255,0), 0); // Red
            // Center is 150, 150 (half of 300)
            p.arc(150, 150, 200, 200, 0, p.map(val, -10, 140, 0, p.TWO_PI));
            p.fill(255); // Inner "donut" hole
            p.ellipse(150, 150, 120, 120);
        });
        p.frameRate(0.5); // Only update twice a second to save battery/CPU
    };
};
new p5(tempSketch);

// --- Humidity Gauge ---
const humidSketch = (p) => {
    p.setup = () => {
        let cnv = p.createCanvas(300, 300);
        cnv.parent("gauge-humidite");
        p.noStroke();
    };

    p.draw = () => {
        fetch('/humidite').then(r => r.text()).then(data => {
            let val = parseFloat(data) || 0;
            document.getElementById("humidite").innerText = "Humidité : " + val + "%";
            p.clear();
            p.fill(50, 50, 255); // Blue
            p.arc(150, 150, 200, 200, 0, p.map(val, 0, 100, 0, p.TWO_PI));
            p.fill(255);
            p.ellipse(150, 150, 120, 120);
        });
        p.frameRate(0.5);
    };
};
new p5(humidSketch);
