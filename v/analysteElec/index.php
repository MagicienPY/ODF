<?php
// Configuration de la base de données et démarrage de session
$servername = "localhost";
$username = "root";
$password = "geni";
$dbname = "odf_sec";

$conn = mysqli_connect($servername, $username, $password, $dbname);
if (!$conn) {
    die("La connexion à la base de données a échoué : " . mysqli_connect_error());
}

session_start();

function has_permission($module) {
    return isset($_SESSION['user_permissions']) && in_array($module, $_SESSION['user_permissions']);
}

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
                        <h2 class="title-1">ODF - Tableau de Bord Analyste Election</h2>
                    </div>
                </div>
            </div>

            <div class="row m-t-25">
                <!-- Module: Analyse Electoral -->
                <?php if (has_permission('analyse_electoral')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c1">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-trending-up"></i>
                                    </div>
                                    <div class="text">
                                        <h2>125</h2>
                                        <span>Analyses Electorales</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Faire Prédiction -->
                <?php if (has_permission('faire_prediction')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c2">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-chart"></i>
                                    </div>
                                    <div class="text">
                                        <h2>35</h2>
                                        <span>Prédictions Réalisées</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Module: Gérer Carte Electoral Social -->
                <?php if (has_permission('gerer_carte_electoral_social')): ?>
                    <div class="col-sm-6 col-lg-3">
                        <div class="overview-item overview-item--c3">
                            <div class="overview__inner">
                                <div class="overview-box clearfix">
                                    <div class="icon">
                                        <i class="zmdi zmdi-map"></i>
                                    </div>
                                    <div class="text">
                                        <h2>10</h2>
                                        <span>Cartes Electorales Sociales</span>
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
                        <p>&copy; 2024 . Tous droits réservés par <a href="#">C24</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once('footjs.php'); ?>
</body>
</html>
