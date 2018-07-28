<!DOCTYPE html>
<html>
    <head>
        <title>Triangle Urban Debate League</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="css/pure.min.css" rel='stylesheet' type='text/css' />
        <link href="css/grids-responsive.min.css" rel='stylesheet' type='text/css' />
        <link href="css/base.css" rel='stylesheet' type='text/css' />
        <link href="https://fonts.googleapis.com/css?family=Lora:400,700" rel='stylesheet' type='text/css' />
        <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel='stylesheet' type='text/css' />
        <link href="/static/favicon.ico" rel='shortcut icon' />
		
		<link href="css/about.css" rel="stylesheet" type="text/css">
		<script src="script/about.js" defer></script>
    </head>
    <body>
        <div id="header">
           <?php include 'header.php';?>
        </div>
        
		<div id="huge-header" style="background-image: url(images/backgrounds/memorial.jpg)">
			<h1>About Us</h1>
		</div>
		
        <div id="content">
			<p>The purpose of the Triangle Urban Debate League (TUDL) is to create and sustain competitive speech and debate programs for public schools across the North Carolina Triangle region.  TUDL strives to provide free coaching, tournaments and other forensics opportunities to historically disadvantaged schools.</p>
			
			<p>TUDL was founded in the summer of 2018 as a joint initiative between Cary and Durham Academy.  TUDL is incorporated in North Carolina and registered with the IRS as a 501(c)(3) non-profit organization.</p>
			
			<div class="pure-g" id="select-tab">
				<div class="pure-u-1-2">
					<h1 id="officers-select">Officers</h1>
				</div>
				<div class="pure-u-1-2">
					<h1 id="board-select">Board</h1>
				</div>
			</div>
			
			<div class="content-tab" id="officers-tab">
				<div>
					<h2>President</h2>
				</div>
				<div>
					<h2>Vice President</h2>
				</div>
				<div>
					<h2>Vice President</h2>
				</div>
				<div>
					<h2>Treasurer</h2>
				</div>
				<div>
					<h2>Secretary</h2>
				</div>
			</div>
			
			<div class="content-tab" id="board-tab">
				<div>
					<h2>Board member</h2>
				</div>
				<div>
					<h2>Board member</h2>
				</div>
				<div>
					<h2>Board member</h2>
				</div>
				<div>
					<h2>Board member</h2>
				</div>
				<div>
					<h2>Board member</h2>
				</div>
				<div>
					<h2>Board member</h2>
				</div>
			</div>

        <div id="footer">
            <?php include 'footer.php';?>
        </div>
        
        <script type="text/javascript">
            $(function() {
                if ($(document).width() <=  1200)
                    $(".header-nav").toggle();
                $("#toggleButton").click(function() {
                    $(".header-nav").slideToggle("slow");
                });
            });
            $(window).resize(function() {
                if (window.innerWidth >  1200)
                    $(".header-nav").show();
                else
                    $(".header-nav").hide();
            });
        </script>
    </body>
</html>
