<?php
include "../files/inc/modules/header.php";

if ($Get_User) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Prepare the SQL statement
        $stmt = odbc_prepare($Get_User, 'INSERT INTO usertbl (account, passwd, email) VALUES (?, ?, ?)');

        if ($stmt) {
            // Bind parameters
            $account = $_POST['account'];
            $password = $_POST['password'];
            $confirm_password = $_POST['confirm_password'];
            $email = $_POST['email'];

            // Check if the email or account already exists
            $check_stmt = odbc_prepare($Get_User, 'SELECT * FROM usertbl WHERE account = ? OR email = ?');
            odbc_execute($check_stmt, array($account, $email));
            $existing_record = odbc_fetch_array($check_stmt);
            if ($existing_record) {
                echo "<script>alert('An account or email with the same value already exists. Please try again with a different value.')</script>";
            } else if (strlen($account) < 4 || strlen($account) > 10) {
                echo "<script>alert('The username must be between 4 and 10 characters long. Please try again.')</script>";
            } else if (strlen($password) < 4 || strlen($password) > 20) {
                echo "<script>alert('The password must be between 4 and 20 characters long. Please try again.')</script>";
            } else if ($password === $confirm_password) {
                odbc_execute($stmt, array($account, $password, $email));
                echo "<script>alert('Registration successful!')</script>";

                // Populate the session variables
                //$_SESSION['account'] = $account;
                //$_SESSION['email'] = $email;

                // Redirect the user to the home page
                //header('Location: ../usercp/account.php');
                //exit;

            } else {
                echo "Passwords do not match. Please try again.";
            }
        } else {
            echo "Error preparing SQL statement: " . odbc_errormsg($Get_User);
        }
    }

    // Close the connection
    odbc_close($Get_User);
} else {
    echo "Error connecting to SQL Server: " . odbc_errormsg();
}

?>
<div class="wrapper
register">
<header>
<div class="topPanel">
<div class="btn btn-drop" data-class="topPanel-left">
<span></span>
<span></span>
<span></span>
</div>
<div class="topPanel-wrapper flex-c">
<div class="topPanel-left flex-c">

<?php include "../files/inc/modules/navbar.php"; ?>



</div>
</div>
</div>
<!-- top-panel -->
<div class="hand-animation">
<div class="light-hand"></div>
<div class="rune-hand"></div>
</div>
<div class="sparks">
<div class="spark_1"></div>
<div class="spark_2"></div>
<div class="spark_3"></div>
<div class="spark_4 spark-big"></div>
</div>
<div class="logo">
<a href=""><img src="../files/images/row-new3.png" alt="" class="bright"></a>
</div>

</header><!-- .header-->
<style>
  .alert {
  padding: 20px;
  background-color: #f44336; /* Red */
  color: white;
  margin-bottom: 15px;
}

.alert-success {
  padding: 20px;
  background-color: #04AA6D; /* Red */
  color: white;
  margin-bottom: 15px;
}

.alert-warning {
  padding: 20px;
  background-color: #ff9800; /* Red */
  color: white;
  margin-bottom: 15px;
}

/* The close button */
.closebtn {
  margin-left: 15px;
  color: white;
  font-weight: bold;
  float: right;
  font-size: 22px;
  line-height: 20px;
  cursor: pointer;
  transition: 0.3s;
}

/* When moving the mouse over the close button */
.closebtn:hover {
  color: black;
}

/* Estilo específico para checkbox */
input[type="checkbox"] {
    width: auto; /* Resetamos a largura para permitir o tamanho padrão do checkbox */
    height: auto; /* Resetamos a altura para permitir o tamanho padrão do checkbox */
    background: transparent; /* Fundo transparente para checkbox */
    border: none; /* Sem bordas para o checkbox */
    padding: 0; /* Sem padding para o checkbox */
    margin-right: 10px; /* Espaçamento à direita para caso tenha um label ao lado */
    cursor: pointer; /* O cursor será uma mãozinha ao passar por cima do checkbox */
}

/* Estilo para o checkbox quando está marcado */
input[type="checkbox"]:checked::before {
    content: '✓'; /* Um símbolo de check */
    position: absolute;
    color: #fcedc0; /* Cor branca para o símbolo */
    font-size: 18px; /* Tamanho do símbolo */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); /* Centralizar o símbolo no meio do checkbox */
}

/* Se você quiser que o checkbox tenha uma aparência mais customizada (ex: um quadrado com bordas) */
input[type="checkbox"]::before {
    content: ''; /* Conteúdo vazio para criar o pseudo-elemento */
    position: absolute;
    top: 50%;
    left: 50%;
    width: 16px; /* Largura do pseudo-elemento */
    height: 16px; /* Altura do pseudo-elemento */
    background: #040609; /* Fundo preto, como os outros inputs */
    border: 1px solid #36383a; /* Bordas como os outros inputs */
    transform: translate(-50%, -50%); /* Centralizar no meio do input */
}
</style>	
<body>
<main class="main">
							
<div class="mainRegister">
<div class="regBlock" style="padding: 100px 120px !important;">
<span class="modalTitle">Create Your Account</span>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Username:</span></div>
<input type="text" placeholder="your username" id="account" name="account" required>
<p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important">4 to 10 aplha-numeric characters long</li>
<li style="margin: 5px; opacity: 0.5; !important">This is your game username. Use only letters and numbers</li>
</ul>
</p>


<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Password:</span></div>
<input type="password" placeholder="******" id="password" name="password" required>
<p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important">4 to 20 characters long</li>
<li style="margin: 5px; opacity: 0.5; !important">* Must have at least 8 characters.</li>
</ul>
</p>


<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Confirm Password:</span></div>
<input type="password" placeholder="******" id="confirm_password" name="confirm_password" required>
<p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important">Re-type your password</li>
<li style="margin: 5px; opacity: 0.5; !important">* Must have at least 8 characters.</li>
</ul>
</p>


<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Email Address:</span></div>
<input type="text" placeholder="your@best-email.com" id="email" name="email" required>
<p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important">Please use a valid email address</li>
</ul>
</p>


<p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important"><a href="/forgotpassword">Forgot your password?</a>
</li>
</ul>
</p>


<button type="submit"  value="Register" class="big-button-blue">Create Account</button>

</div>
</form>
</div>
</div>
</div>
</div>
</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	