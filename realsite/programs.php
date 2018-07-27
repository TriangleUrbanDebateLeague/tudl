
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

		<div id="huge-header" style="background-image: url(images/backgrounds/convention.jpg)">

			<h1>Programs</h1>

		</div>

		<div id="content">

		<p>TUDL provides coaching and tournament opportunities in the Congressional Debate format.  Founded in 1938 by the National Speech and Debate Asosciation, Congressional Debate is the longest running form of Debate in the United States.  We believe that the opportunities that Congressional Debate offers with its focus on persuasive presentation, social collaboration, and a debating a wide variety of current events make it uniquely suited for building communication skills in students.</p>

			<h1>Coaching</h1>

			<p>In 2018-19, TUDL plans to coach 4 Durham County Public High Schools.  <br><br>TUDL provides Debate coaches to local high schools at no cost to schools or participants.  Each participant TUDL high school has between 1-3 coaches assigned to them for the semester.  Coaches may change between semesters, but TUDL strives to maintain continuity whenever possible.  TUDL coaches are often founding the first debate team a school has ever had, and responsible for building the team from the ground up.  TUDL works in partnership with local high schools to provide coaching sessions even when schools cannot provide for a staff member to attend meetings.<br><br>Coaches provide instruction and critiques to students at 90-minute weekly after school meetings.  Coaching sessions focus on preparing for upcoming tournaments and improving communication skills.  TUDL trains all coaches to ensure high standards of instruction and provides a standardized curriculum and guide to coaching.<br><br>Coaches are often university students with previous debate experience who commit to coaching for at least one semester.  In addition to becoming county approved volunteers, coaches also undergo TUDL’s extensive background check and vetting process to ensure the safety of all participants.<br><br>In addition to the formal TUDL coaches, TUDL also plans to provide informal supporting mentorship to students.  About once a month, students from developed debate teams in the area such as Cary and Durham Academy will visit TUDL high schools to work directly with their peers in collaborative research and mutual critiquing.  We believe this unique opportunity will foster a stronger sense of collective community in the Triangle region and level the playing field for all students.

			<h1>Tournaments</h1>

			<p>TUDL anticipates holding 4 tournaments in 2018-19.<br><br>TUDL is working to improve accessibility to debate by hosting tournaments specifically for participant TUDL high schools.  TUDL anticipates holding afterschool tournaments twice a semester at a nearby venue such as Durham or Cary Academy.  These tournaments will be completely free for all participants and TUDL will provide the transportation to the tournaments.<br><br>Tournaments will include two 1.5 hour sessions of Congressional Debate and an awards ceremony to honor top competitors.  Competitors will also receive written ballots with feedback from judges.<br><br>TUDL staff members along with volunteers from Cary and Durham Academy will run tournaments.  TUDL makes use of the software tabroom.com for tabulating results and tracking participants.</p>

		</div>

		<div id="footer">

			<?php include 'footer.php';?>

		</div>





		<script type="text/javascript">

			$(function() {

				if ($(document).width() <= 1200)

					$(".header-nav").toggle();

				$("#toggleButton").click(function() {

					$(".header-nav").slideToggle("slow");

				});

			});

			$(window).resize(function() {

				if (window.innerWidth > 1200)

					$(".header-nav").show();

				else

					$(".header-nav").hide();

			});

		</script>

	</body>

</html>
