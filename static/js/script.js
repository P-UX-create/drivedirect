const vehicleChart = document.getElementById("vehicleChart");

if(vehicleChart){

new Chart(vehicleChart,{

type:"pie",

data:{

labels:[
"Available",
"Rented",
"Maintenance"
],

datasets:[{

data:[

window.availableCars,

window.rentedCars,

window.maintenanceCars

]

}]

}

});

}

const revenueChart=document.getElementById("revenueChart");

if(revenueChart){

new Chart(revenueChart,{

type:"bar",

data:{

labels:["Revenue","Maintenance"],

datasets:[{

label:"Amount",

data:[

window.revenue,

window.maintenanceCost

]

}]

}

});

}