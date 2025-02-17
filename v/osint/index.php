<?php
// Configuration de la base de données et démarrage de session
$servername = "localhost";
$username = "root";
$password = "geni";
$dbname = "odf_sec";

// Connexion à la base de données
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Vérification de la connexion
if (!$conn) {
    die("La connexion à la base de données a échoué : " . mysqli_connect_error());
}

session_start();

// Fonction pour vérifier les permissions utilisateur
function has_permission($module) {
    // Vérifiez la session utilisateur pour le rôle ou les permissions
    return isset($_SESSION['user_permissions']) && in_array($module, $_SESSION['user_permissions']);
}

// Redirection si l'utilisateur n'est pas connecté
if (!isset($_SESSION['user_id'])) {
    header("Location: ../../");
    exit();
}
?>

<?php include_once('tete.php'); ?>

<!-- CONTENU PRINCIPAL -->
<div class="main-content">
    <div class="section__content section__content--p30">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="overview-wrap">
                        <h2 class="title-1">ODF-OSINT Dashboard</h2>
                        
                    </div>
                </div>
            </div>

            <div class="row m-t-25">
                <!-- Module: Terrorist Database -->
                <?php if (has_permission('terrorist_database')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c1">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-account-o"></i>
                                    </div>
                                    <div class="text">
                                        <h2>2</h2>
                                        <span>Terrorist Database</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Transport Analysis -->
                <?php if (has_permission('transport_analysis')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c2">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-car"></i>
                                    </div>
                                    <div class="text">
                                        <h2>388,688</h2>
                                        <span>Transport Analysis</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: SOCMINT (Social Media Intelligence) -->
                <?php if (has_permission('socmint')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c3">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-comments"></i>
                                    </div>
                                    <div class="text">
                                        <h2>1,086</h2>
                                        <span>SOCMINT</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Cyber Threat Intelligence -->
                <?php if (has_permission('cyber_threats')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c4">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-shield-security"></i>
                                    </div>
                                    <div class="text">
                                        <h2>452</h2>
                                        <span>Cyber Threat Intelligence</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Financial Intelligence -->
                <?php if (has_permission('financial_intelligence')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c5">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-money"></i>
                                    </div>
                                    <div class="text">
                                        <h2>$1,060,386</h2>
                                        <span>Financial Intelligence</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: News Monitoring -->
                <?php if (has_permission('news_monitoring')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c6">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-collection-text"></i>
                                    </div>
                                    <div class="text">
                                        <h2>200+</h2>
                                        <span>News Monitoring</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Location Analysis -->
                <?php if (has_permission('location_analysis')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c7">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-pin"></i>
                                    </div>
                                    <div class="text">
                                        <h2>85</h2>
                                        <span>Location Analysis</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="copyright">
                        <p>Copyright © 2024 . All rights reserved. by <a href="#">C24</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once('footjs.php'); ?>
</body>
</html>
