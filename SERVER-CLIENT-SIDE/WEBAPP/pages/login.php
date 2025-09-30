<?php
include "../files/inc/modules/header.php";
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
</style>	
<body>
<main class="main">							
<div class="mainRegister">
<div class="regBlock" style="padding: 100px 120px !important;">
<span class="modalTitle">Login</span>
                        <?php
	        include "../include/database.config.php";
                        if (isset($_POST['account'])) {
                            $account = $_POST['account'];
                            $password = $_POST['password'];
                            $stmt = odbc_prepare($Get_User, 'SELECT * FROM usertbl WHERE account = ? AND passwd = ?');
                            $result = odbc_execute($stmt, array($account, $password));
                            $status = odbc_num_rows($stmt);
                            $data = odbc_fetch_array($stmt);
                            if ($data["account"] ==  $account) {
                                $_SESSION["UID"] =  $data['uid'];
                                echo '<script>window.location.replace("/usercp/account");</script>';
                            } else {
                                echo '<div class="alert-warning"><span class="closebtn">&times;</span><strong>Failed!</strong> Invalid username or password !!
			</div>';
                            }
                        }
                        ?>

                    <form method="POST">
                        <div class="form-group">

<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Username:</span></div><div style="width: 346px;">
<input type="text" placeholder="your username" class="form-control" id="account" name="account" required><p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important"></li>
</ul>
</p>
<div class="fieldGroup" style="margin: 0 0 10px 0 !important"><span>Password:</span></div><div style="width: 346px;">
<input type="password" placeholder="******" class="form-control" id="password" name="password" required><p class="text-muted">
<ul>
<li style="margin: 5px; opacity: 0.5; !important"></li>
</ul>
</p>
<p class="text-muted"><ul><li style="margin: 5px; opacity: 0.5; !important"><a href="/forgotpassword">Forgot your password?</a></li></ul></p>
<button type="submit"  class="big-button-blue">Sign In</button>


                    </form>
                    <div class="message mt-4">

                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	