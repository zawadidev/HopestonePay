<!DOCTYPE html>
<html>
<head>
  <title>HopestonePay</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">

  <h2>HopestonePay 💰</h2>

  <!-- REGISTER -->
  <div style="border:1px solid #ccc; padding:20px; width:300px; margin:auto;">
    <h3>Register</h3>

    <input id="reg_phone" placeholder="Phone" /><br><br>
    <input id="reg_name" placeholder="Name" /><br><br>
    <input id="reg_email" placeholder="Email" /><br><br>
    <input id="reg_password" type="password" placeholder="Password" /><br><br>

    <button onclick="registerUser()">Register</button>
  </div>

  <br>

  <!-- LOGIN -->
  <div style="border:1px solid #ccc; padding:20px; width:300px; margin:auto;">
    <h3>Login</h3>

    <input id="log_phone" placeholder="Phone" /><br><br>
    <input id="log_password" type="password" placeholder="Password" /><br><br>

    <button onclick="loginUser()">Login</button>
  </div>

  <script>
    // 🔴 YOUR REAL BACKEND (already correct from your screenshot)
    const BASE_URL = "https://hopestonepay.onrender.com";

    function registerUser() {
      const phone = document.getElementById("reg_phone").value;
      const name = document.getElementById("reg_name").value;
      const email = document.getElementById("reg_email").value;
      const password = document.getElementById("reg_password").value;

      fetch(BASE_URL + "/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ phone, name, email, password })
      })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
      })
      .catch(err => {
        alert("Error connecting backend");
      });
    }

    function loginUser() {
      const phone = document.getElementById("log_phone").value;
      const password = document.getElementById("log_password").value;

      fetch(BASE_URL + "/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ phone, password })
      })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
      })
      .catch(err => {
        alert("Error connecting backend");
      });
    }
  </script>

</body>
</html>
