<?php
echo <div id="footer">
			<div class="footer-text">
                <div class="pure-g">
                    <div class="pure-u-1">
                        <div class="center">
                            <img alt="TUDL Logo" src="images/Logos/logo_reduced.png" class="small-logo">
                        </div>
                    </div>
                    
                    <div class="pure-u-xl-1-4 pure-u-1-2 footer-button">
                        <a href="TODO"></i>&nbsp;&nbsp;Follow on Google+</a>
                    </div>
                    <div class="pure-u-xl-1-4 pure-u-1-2 footer-button">
                        <a href="TODO"></i>&nbsp;&nbsp;(855) 939 2013</a>
                    </div>
                    <div class="pure-u-xl-1-4 pure-u-1-2 footer-button">
                        <a href="TODO"></i>&nbsp;&nbsp;Follow on Facebook</a>
                    </div>
                    <div class="pure-u-xl-1-4 pure-u-1-2 footer-button text-normal">
                        <a href="TODO"></i>&nbsp;&nbsp;info@<wbr>tudl<wbr>.org</a>
                    </div>
                    
                    <div class="pure-u-lg-1-4 pure-u-1"></div>
                    <div class="pure-u-lg-1-2 pure-u-1">
                        <div class="footer-disclaimer text-normal">
                            Developed by The Triangle Urban Debate League Team.
                        </div>
                    </div>
                    <div class="pure-u-lg-1-1 pure-u-1"></div>
                    
                    <div class="pure-u-1-1 footer-links">
                        <a href="mission.php">Mission</a> 
                        <a href="privacy.php">Privacy&nbsp;Policy</a>
                        <a href="schedule.php">Tournament Schedule</a> 
                    </div>
                </div>
            </div>
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
        </script>;
?>
