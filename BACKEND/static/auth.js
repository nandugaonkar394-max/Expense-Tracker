const API = "";


// Show Login

function showLogin(){

    document.getElementById("registerBox").style.display="none";

    document.getElementById("loginBox").style.display="block";

}



// Show Register

function showRegister(){

    document.getElementById("loginBox").style.display="none";

    document.getElementById("registerBox").style.display="block";

}



// Register User

function register(){


fetch(API + "/register",{


method:"POST",

headers:{
"Content-Type":"application/json"
},


body:JSON.stringify({

name:
document.getElementById("name").value,


email:
document.getElementById("regEmail").value,


password:
document.getElementById("regPassword").value

})


})


.then(res=>res.json())


.then(data=>{


alert(data.message);


if(data.message=="Registration successful"){

    showLogin();

}


});


}





// Login User

function login(){

    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("loginPassword").value;


    fetch(API + "/login", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:email,
            password:password

        })

    })


    .then(response => response.json())


    .then(data => {


        console.log(data);


        alert(data.message);



        if(data.user_id){


            localStorage.setItem(
                "user_id",
                data.user_id
            );


            window.location.href = "/dashboard";


        }


    })


    .catch(error=>{

        console.log(error);

        alert("Backend connection failed");

    });


}