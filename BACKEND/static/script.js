const API_URL = "/api/expenses";

const user_id = localStorage.getItem("user_id");

let editingId = null;


document.getElementById("date").value =
    new Date().toISOString().split("T")[0];



function addExpense() {

    let title = document.getElementById("title").value.trim();
    let amount = document.getElementById("amount").value;
    let date = document.getElementById("date").value;
    let category = document.getElementById("category").value;


    if (title === "" || amount === "" || date === "" || category === "") {

        alert("Please fill all fields.");
        return;

    }


    let expense = {

        user_id: user_id,
        title: title,
        amount: amount,
        date: date,
        category: category

    };


    let url = API_URL;
    let method = "POST";


    if (editingId !== null) {

        url = API_URL + "/" + editingId;
        method = "PUT";

    }



    fetch(url, {

        method: method,

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(expense)

    })


    .then(response => response.json())


    .then(data => {


        alert(data.message);


        editingId = null;


        const addButton = document.querySelector(".add-btn");


        if(addButton){

            addButton.innerText = "Add Expense";

        }


        clearForm();

        loadExpenses();


    })


    .catch(error => {

        console.log(error);

        alert("Backend connection failed");

    });


}

function loadExpenses(){


    fetch(API_URL + "/" + user_id)


    .then(response => response.json())


    .then(data => {


        let list = document.getElementById("expenseList");


        list.innerHTML = "";


        let total = 0;



        data.forEach(expense => {


            total += Number(expense.amount);



            let item = document.createElement("li");



            item.innerHTML = `


            <b>${expense.title}</b><br>


            Amount: ₹${Number(expense.amount).toLocaleString("en-IN")}<br>


            Date: ${expense.date}<br>


            Category: ${expense.category}


            <br><br>


            <div class="actions">


                <button class="edit-btn" onclick="editExpense(${expense.id})">

                    Edit

                </button>



                <button class="remove-btn" onclick="deleteExpense(${expense.id})">

                    Delete

                </button>


            </div>


            `;



            list.appendChild(item);



        });



        document.getElementById("totalExpense").innerHTML =
        "₹" + total.toLocaleString("en-IN");



    })


    .catch(error => {

        console.log(error);

    });


}


function editExpense(id){


    fetch(API_URL + "/" + user_id)


    .then(response => response.json())


    .then(data => {



        let expense = data.find(e => e.id === id);



        if(!expense)

            return;



        document.getElementById("title").value = expense.title;


        document.getElementById("amount").value = expense.amount;


        document.getElementById("date").value = expense.date;


        document.getElementById("category").value = expense.category;



        editingId = id;



        const addButton = document.querySelector(".add-btn");



        if(addButton){

            addButton.innerText = "Update Expense";

        }



    });


}


function deleteExpense(id){


    if(!confirm("Are you sure you want to delete this expense?"))

        return;



    fetch(API_URL + "/" + id, {


        method:"DELETE"


    })



    .then(response => response.json())


    .then(data => {



        alert(data.message);


        loadExpenses();



    })



    .catch(error => {


        console.log(error);


    });


}

function deleteAllExpenses(){


    if(!confirm("Are you sure you want to delete all expenses?"))

        return;



    fetch(API_URL, {


        method:"DELETE"


    })



    .then(response=>response.json())


    .then(data=>{


        alert(data.message);


        loadExpenses();



    })



    .catch(error=>{


        console.log(error);


    });


}

function clearForm(){


    document.getElementById("title").value = "";

    document.getElementById("amount").value = "";

    document.getElementById("category").value = "";


    document.getElementById("date").value =

    new Date().toISOString().split("T")[0];


}

function logout(){


    localStorage.removeItem("user_id");


    window.location = "/";


}

loadExpenses();