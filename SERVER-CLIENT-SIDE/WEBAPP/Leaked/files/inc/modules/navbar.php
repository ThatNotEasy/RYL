<?php
session_start();
if (isset($_SESSION['UID'])) {
    // Display navigation bar for logged-in users
    echo '
						<ul class="nav">
						<li><a href="/home">Homepage</a></li>
						<li><a href="/pages/downloads">Download Center</a></li>

						<li class="sub-menu"><a href="javascript:void(0)">Game Info</a>
						<ul>
						<li><a >Game Wiki</a></li>
						<li><a >Server Status</a></li>
						</ul>
						</li>

						<li class="sub-menu"><a href="javascript:void(0)">Rankings</a>
						<ul>
						<li><a href="/rankings/fame">Top Fame</a></li>
						<li><a href="/rankings/guilds">Top Guilds</a></li>
						</ul>
						</li>

						<li class="sub-menu"><a href="javascript:void(0)">Shop</a>
						<ul>
						<li><a href="/shops/premium">Premium</a></li>
						<li><a href="/shops/Potions">Events</a></li>
						</ul>
						</li>
						</ul>
						</div>
						<ul class="nav">
						<div class="topPanel-right">
						<li class="sub-menu"><a href="javascript:void(0)">My Account</a>
						<ul>
						<li><a href="/usercp/account">Information</a></li>
						<li><a href="/usercp/mypassword">Change Pass</a></li>
						<li><a href="/usercp/charge">Buy Points</a></li>
						<li><a href="/pages/logout">Log Out</a></li>
						</ul>
						</li>


';
} else {
    // Display navigation bar for guests
    echo '
						<ul class="nav">

						<li><a href="/home">Homepage</a></li>

						<li><a href="/pages/register">Create Account</a></li>

						<li><a href="/pages/downloads">Download Center</a></li>

						<li class="sub-menu"><a href="javascript:void(0)">Game Info</a>
						<ul>
						<li><a >Game Wiki</a></li>
						<li><a >Server Status</a></li>
						</ul>
						</li>

						<li class="sub-menu"><a href="javascript:void(0)">Rankings</a>
						<ul>
						<li><a href="/rankings/fame">Top Fame</a></li>
						<li><a href="/rankings/guilds">Top Guilds</a></li>
						</ul>
						</li>

						</ul>
						</div>
						<div class="topPanel-right">

						<!---<ul><a href="/pages/login" class="sign-in">Sign In</a></u>---!>

						<ul><a href="#register" class="sign-in open_modal">Sign In</a></ul>';
}
?>


<script type="text/javascript">
  var close = document.getElementsByClassName("closebtn");
  var i;

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function(){
      var div = this.parentElement;
      div.style.opacity = "0";
      div.style.display = "none";
      setTimeout(function(){ div.style.display = "none"; }, 600);
    }
  }
  </script>
		<div id="register" class="modal_div"> 
			<span class="modal_close"></span>
			<div class="modal-content">
				<span class="modalTitle">Sign In</span>
				<div class="fields">
				<div class="fieldGroup">
				<span>Username</span>
				<form action="/pages/login" method="post">
				<input class="input-re" type="text" name="account" placeholder="your username"></div>
				<div class="fieldGroup">
				<span>Password</span>
				<input class="input-re" type="password" name="password" placeholder="******"></div>
				<p></p>

				<div class="enter flex-s-c">
				<div class="enterLinks">
				<p><a href="/forgotpassword" class="forgot">Forgot Password?</a></p>
				<p><a href="/pages/register" class="sign">Sign Up</a></p>
				</div>
				<button class="button" name="submit" type="submit" value="submit">Sign In Now</button>
					</div>
				</form>
			</div> 
		</div>
	</div>
		<div id="overlay">
		</div>	