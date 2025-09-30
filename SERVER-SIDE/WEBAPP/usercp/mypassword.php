<?php
session_start();
error_reporting(0);


if (!isset($_SESSION["UID"])) {
    echo '<script>alert("Please login")</script>';
    echo '<script>window.location.href = "/pages/login";</script>';
}

$UID = $_SESSION["UID"];

include "../files/inc/modules/header.php";

if ($Get_User) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Prepare the SQL statement
        $stmt = odbc_prepare($Get_User, 'UPDATE usertbl SET passwd = ? WHERE uid = ? AND passwd = ?');

        if ($stmt) {
            // Bind parameters
            $current_passwd = $_POST['current_passwd'];
            $new_passwd = $_POST['new_passwd'];
            $confirm_new_passwd = $_POST['confirm_new_passwd'];
            $confirm_current_passwd = $_POST['confirm_current_passwd'];
            $uid = $_SESSION['UID'];

            // Check if the new password matches the confirm password
            if ($new_passwd === $confirm_new_passwd) {
                // Check if the current password is correct
                $check_stmt = odbc_prepare($Get_User, 'SELECT * FROM usertbl WHERE uid = ? AND passwd = ?');
                odbc_execute($check_stmt, array($uid, $current_passwd));
                $existing_record = odbc_fetch_array($check_stmt);

                if ($existing_record) {
                    // Check if the new password is between 6 and 18 characters long
                    if (strlen($new_passwd) >= 6 && strlen($new_passwd) <= 18) {
                        // Check if the new password matches the current password
                        if ($current_passwd === $confirm_current_passwd) {
                            // Update the password
                            odbc_execute($stmt, array($new_passwd, $uid, $current_passwd));
                            echo "<script>alert('Password updated successfully!')</script>";
                        } else {
                            echo "<script>alert('Confirm current password does not match. Please try again.')</script>";
                        }
                    } else {
                        echo "<script>alert('The new password must be between 6 and 18 characters long. Please try again.')</script>";
                    }
                } else {
                    echo "<script>alert('Current password is incorrect. Please try again.')</script>";
                }
            } else {
                echo "<script>alert('New password and confirm new password do not match. Please try again.')</script>";
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
<body>
<div class="wrapper">
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
<?php include "../files/inc/modules/download.php"; ?>
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
<main class="main"><aside>

						<?php include "../files/inc/modules/default.php"; ?>		
						<?php include "../files/inc/modules/social.php"; ?>

</aside>
	
<div class="content">
<div class="h2-title h2-title-content flex-s-c">
<span>Account Setting</span>
</div>

<div class="acc">
<div class="acc-title">Change Account Password</div>
<div class="accBlock flex-s">
<div class="accBlock-content">
<div class="formGroup">
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

<span>Current Password</span><input type="password" type="password" name="current_passwd" placeholder="******" minlength="6" required>
<p style="margin: 10px; !important">Type your current password</p>
</div>
<div class="formGroup">
<span>New password</span><input type="password" type="password" name="new_passwd" placeholder="******" minlength="6" required>
<p style="margin: 10px; !important">Min 6 characters / Max 18 characters</p>
</div>
</div>
<div class="accBlock-content">
<div class="formGroup">
<span>Confirm current password</span><input type="password" type="password" name="confirm_current_passwd" placeholder="******" minlength="6" required>
<p style="margin: 10px; !important">Confirm your current password</p>
</div>
<div class="formGroup">
<span>Confirm new password</span><input type="password" type="password" name="confirm_new_passwd" placeholder="******" minlength="6" required>
<p style="margin: 10px; !important">Min 6 characters / Max 18 characters</p>
</div>
</div>
</div>
<div class="change-button">
<button class="big-button-blue" type="submit">Confirm Changes</button>
</div>
</form>

</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	