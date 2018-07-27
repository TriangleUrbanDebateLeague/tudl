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
    </head>
    <body>
        <div id="header">
           <?php include 'header.php';?>
        </div>

		<div id="huge-header" style="background-image: url(images/backgrounds/constitution.jpg)">
			<h1>Mission</h1>
		</div>

        <div id="content">

			       <p>Our vision is a world in which all students, regardless of income level, are able to benefit from the invaluable opportunities provided by competitive speech and debate. <br><br>Our mission is to create and sustain competitive speech and debate teams in public schools across the North Carolina Triangle region. Participating in speech and debate equips students with lifelong communication, professional, and research skills and fosters greater academic achievement. Yet, without initiatives like the Triangle Urban Debate League, this opportunity would be available only to the select few with the financial resources to obtain coaching or the fortune to attend a well-funded school with an established team. Our goal is to change that reality and provide speech and debate resources to students at every school in the region, at no cost to individual families. </p>
			       <h1>Whitepapers</h1>

			            <p>Coming Soon</p>


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
