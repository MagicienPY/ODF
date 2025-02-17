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
                        <h2 class="title-1">ODF-OSINT Dashboard/Mots</h2>
                        
                    </div>
                </div>
            </div>

            <div class="row m-t-25">
            <form class="form-header" action="" method="POST">
                                <input class="au-input au-input--xl" type="text" name="search" placeholder="écrivez ce que vous cherchez ici..." />
                                <button class="au-btn--submit" type="submit">
                                    <i class="zmdi zmdi-search"></i>
                                </button>
                            </form>
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
