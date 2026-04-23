document.addEventListener("DOMContentLoaded", function() {
    const today= new Date().toISOString().split('T');
    document.getElementById("date1").value = today[0];
    document.getElementById("date2").value = today[0];

    document.getElementById("submit").addEventListener("click", function(event) {
        event.preventDefault();

        var date1 = document.getElementById("date1").value; 
        var date2 = document.getElementById("date2").value; 

        const [year1, month1, day1] = date1.split('-');
        const formattedDate1 = `${day1}-${month1}-${year1}`;

        console.log(formattedDate1);
        const [year2, month2, day2] = date2.split('-');
        const formattedDate2 = `${day2}-${month2}-${year2}`;

        console.log(formattedDate2);
        window.location.href = window.location.origin +`/logs?date1=${formattedDate1}&date2=${formattedDate2}`;
    });

});
